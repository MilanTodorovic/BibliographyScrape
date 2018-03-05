from multiprocessing import Process, Queue, Semaphore
import bs4, requests
import os, sys, time

# napraviti listu umesto self._url, izbrisati klasu
# with Pool(10) as p:
#   p.map(extract_books_and_links, args=(lst,))
#   p.start()
# iz extract pozvati sve ostale funkcije
# len(self._url) i prema tome otvoriti po jedan proces/thread za svaki link, eventualno grupisati u listama od po 4-5

class Spider:

    def __init__(self, url):
        self._base_url = url
        self._iframe = "glavni_niz.html"
        self._url = Queue()
        self._url.put(self._base_url)  # starting URL, appends others on the way

        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}

        self.languages = ["nor", "dan", "swe", "esk", "fin", "ice", "sme", "smi", "smn", "lap"]
        self._count = 10  # max processes count
        self._sema = Semaphore(value=self._count)

    def run(self):
        print("Entering run")
        self.extract_urls_from_main_page(self._url.get())
        for url in iter(self._url.get, None):
            print(url)
            resp = self.visit_url(url)
            print(resp.status_code)
            print(resp)
            self.p = Process(target=self.extract_books_and_links, args=(resp.content, self.languages))
            self.p.start()
            #self.p.terminate()
            #self.p.join()
        # self.save()
        #self._url.join()
        print("Done.")

    def extract_urls_from_main_page(self, url):
        print("Entering extract_urls_from_main_page")
        resp = self.visit_url(url)
        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        links = soup.body.center.find_all("a")  # returns a result set (basically a list) of bs4 elements
        print("Links:", links)
        for link in links:
            if "skupni" in link:
                pass
            else:
                self._url.put(self._base_url+link["href"][:-10]+self._iframe)
                break
        print("Exiting extract_urls_from_main_page")
        print("URLs", self._url)

    def visit_url(self, url):
        return requests.get(url, headers=self._headers)

    def extract_books_and_links(self, content, langs):
        self._sema.acquire()
        print("Entering extract_books_and_links")
        soup = bs4.BeautifulSoup(content, "html.parser")
        # time.sleep(50)
        divs = soup.body.find_all("div", {"id":"znak"})
        for div in divs:
            a = div.find("a", {"href": True})  # div.a == div.find("a",{"href":True})
            link = a["href"]  # link to visit a seperate site with more info on the book
            print(link)
            resp = self.visit_url(link)
            print(resp.status_code)
            res = self.check_if_foreign_book(resp.content, link, langs)
            if res:
                a_tag = div.find_previous("a")
                self.extract_book_info(a_tag, res)
                del res, resp, link
                # break
            else:
                continue
        self.save()
        self._sema.release()
        print("Exiting extract_books_and_links")

    def check_if_foreign_book(self, content, link, langs):
        print("Entering check_if_foreign_book")
        soup = bs4.BeautifulSoup(content, "html.parser")
        table = soup.find("td", {"class": "text1"})
        if not table:
            table = soup.find("td", {"class": "text1"})
        else:
            pass
        try:
            link = table.find("a").find_next_sibling("a")
            r = self.visit_url(link["href"])
            s = bs4.BeautifulSoup(r.content, "html.parser")
            row = s.find("td", text="0411")  # contains information about the srource language
            if row:
                n = row.find_next_sibling("td")
                print(n)
                languages = n.text
                for lang in langs:
                    if lang in languages:
                        print("Found one!!")
                        return lang
                    else:
                        continue
                else:
                    return False
            else:
                return False
        except:
            print("Exception found!")
            with open("./greske/greska{}.txt".format(time.clock()), "w") as f:
                f.write(link)
                f.flush()
                f.write(soup.text)
                f.flush()
        print("Exiting check_if_foreign_book")

    def extract_book_info(self, soup, language):
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
        self.save(text)
        print("Exiting extract_book_info")

    def save(self, text):
        print("Saving file")
        with open("./knjige/{}.txt".format(time.clock()), "w") as f:
                f.write(text)
                f.flush()
        return 0

if __name__ == "__main__":

    staring_url = "http://bibliografija.nsk.hr/a/"

    spider = Spider(staring_url)
    spider.run()
