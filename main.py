from multiprocessing import Process, Queue, Semaphore, Lock
import bs4, requests
import os, sys, time


class Spider:

    def __init__(self, url):
        self._base_url = url
        self._iframe = "glavni_niz.html"  # loads iframe directly without otherparts of the site
        self._marc_view = "&format=001"  # used for comining book link for direct MARC view of the book
        self._url = Queue()
        self._url.put(self._base_url)  # starting URL, appends others on the way

        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}

        self.languages = ["nor", "dan", "swe", "esk", "fin", "ice", "sme", "smi", "smn", "lap"]
        self._count = 8  # max processes count
        self._sema = Semaphore(value=self._count)
        self._lock = Lock()

    def run(self):
        print("Entering run")
        self.extract_urls_from_main_page(self._url.get())
        for url in iter(self._url.get, None):
            print(url)
            self.p = Process(target=self.extract_books_and_links, args=(url, self.languages, self._lock))
            self.p.start()
        print("Done.")

    def extract_urls_from_main_page(self, url):
        print("Entering extract_urls_from_main_page")
        resp = self.visit_url(url)
        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        links = soup.body.center.find_all("a")  # returns a result set (basically a list) of bs4 elements
        # print("Links:", links)
        for link in links:
            self._url.put(self._base_url+link["href"][:-10]+self._iframe)
        print("Exiting extract_urls_from_main_page")
        # print("URLs", self._url)

    def visit_url(self, url):
        return requests.get(url, headers=self._headers)

    def extract_books_and_links(self, url, langs, lock):
        with self._sema:
            print("Entering extract_books_and_links")
            resp = self.visit_url(url)
            soup = bs4.BeautifulSoup(resp.content, "html.parser")
            divs = soup.body.find_all("div", {"id": "znak"})
            for div in divs:
                r = s = res = link = None
                a = div.find("a", {"href": True})  # div.a == div.find("a",{"href":True})
                link = a["href"]+self._marc_view  # link to visit a separate site with more info on the book
                print(link)
                while not r:
                    time.sleep(0.3)
                    r = self.visit_url(link)
                    print(r.status_code)
                    s = bs4.BeautifulSoup(r.content, "html.parser")
                    if "System is overloaded" in s.text:
                        r = s = None
                    else:
                        break
                res = self.check_if_foreign_book(s, link, langs, lock, r)
                if res:
                    a_tag = div.find_previous("a")
                    if a_tag.p:
                        if "margin-left" in a_tag.p["style"]:
                            real_a_tag = a_tag.find_previuso("a")
                            # mode so that we don't separate book volumes
                            _ = real_a_tag.a.extract()  # delete nested tag
                            del _
                            self.extract_book_info(real_a_tag, res, lock, 0)
                            self.extract_book_info(a_tag, res, lock, 1)
                    else:
                        self.extract_book_info(a_tag, res, lock, 0)
                    del res, r, link
                else:
                    del res, r, link
            print("Exiting extract_books_and_links")

    def check_if_foreign_book(self, soup, link, langs, lock, response):
        print("Entering check_if_foreign_book")
        try:
            row = soup.find("td", text="0411")  # contains information about the srource language
            if row:
                n = row.find_next_sibling("td")
                print(n)
                languages = n.text
                for lang in langs:
                    if lang in languages:
                        # print("Found one!!")
                        return lang
                    else:
                        continue
                else:
                    return False
            else:
                return False
        except:
            print("Exception found!")
            lock.acquire()
            with open("./greske/greska.txt".format(time.clock()), "a") as f:
                f.write("-----------------------------\n{}".format(time.strftime("%H:%M:%S")))
                f.flush()
                f.write("{}\n{}".format(link, response.status_code))
                f.flush()
                f.write(soup.text)
                f.flush()
            lock.release()
        print("Exiting check_if_foreign_book")

    def extract_book_info(self, soup, language,lock,mode=0):
        print("Entering extract_book_info")
        spans = soup.find_all()
        text = ""
        if spans[0].has_attr("style"):
            for span in spans[:1]:
                text += span.text
            for span in spans[3:]:
                if span.name == "br":
                    text += "\n"
                else:
                    text += span.text
        else:
            for span in spans:
                if span.name == "br":
                    text += "\n"
                else:
                    text += span.text
        if mode == 0:
            self.save(text, language, lock)
        else:
            self.save(text, "", lock)
        print("Exiting extract_book_info")

    def save(self, text, language, lock):
        print("Saving file")
        lock.acquire()
        with open("./knjige/knjige_.txt", "a", encoding='utf-16') as f:
            f.write("{0}\n{1}\n".format(language,text))
            f.flush()
        lock.release()


if __name__ == "__main__":

    staring_url = "http://bibliografija.nsk.hr/a/"
    
    spider = Spider(staring_url)
    spider.run()
