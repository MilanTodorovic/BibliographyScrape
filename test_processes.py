from multiprocessing import Process, Queue, Semaphore
import multiprocessing
import bs4, requests
import os, sys, time


class Spider:

    def __init__(self, url):
        self._base_url = url
        self._iframe = "glavni_niz.html"
        self._url = Queue()
        self._url.put(self._base_url)  # starting URL, appends others on the way

        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}

        self.languages = ["nor", "dan", "swe", "esk", "fin", "ice", "sme", "smi", "smn", "lap"]
        self._count = 4  # max processes count
        self._sema = Semaphore(value=self._count)

    def run(self):
        print("Entering run")
        self.extract_urls_from_main_page(self._url.get())
        for url in iter(self._url.get, None):
            print(url)
            self.p = Process(target=self.extract_books_and_links, args=(url, self.languages))
            self.p.start()
        print("Done.")

    def extract_urls_from_main_page(self, url):
        print("Entering extract_urls_from_main_page")
        resp = self.visit_url(url)
        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        links = soup.body.center.find_all("a")  # returns a result set (basically a list) of bs4 elements
        print("Links:", links)
        for link in links:
            self._url.put(self._base_url+link["href"][:-10]+self._iframe)
        print("Exiting extract_urls_from_main_page")
        print("URLs", self._url)

    def visit_url(self, url):
        return requests.get(url, headers=self._headers)

    def extract_books_and_links(self, url, langs):
        with self._sema:
            print("Entering extract_books_and_links")
            resp = self.visit_url(url)
            soup = bs4.BeautifulSoup(resp.content, "html.parser")
            divs = soup.body.find_all("div", {"id":"znak"})
            for div in divs:
                r = s = res = link = None
                a = div.find("a", {"href": True})  # div.a == div.find("a",{"href":True})
                link = a["href"]  # link to visit a seperate site with more info on the book
                print(link)
                while not r:
                    r = self.visit_url(link)
                    print(r.status_code)
                    s = bs4.BeautifulSoup(r.content, "html.parser")
                    if "overloaded" in s:
                        r = None
                res = self.check_if_foreign_book(s, link, langs)
                if res:
                    a_tag = div.find_previous("a")
                    self.extract_book_info(a_tag, res)
                    del res, r, link
                else:
                    del res, r, link
                    continue
            self.save()
            print("Exiting extract_books_and_links")

    def check_if_foreign_book(self, soup, link, langs):
        print("Entering check_if_foreign_book")
        table = soup.find("td", {"class": "text1"})
        try:
            r = s = None
            link = table.find("a").find_next_sibling("a")
            while not r:
                time.sleep(20)
                r = self.visit_url(link["href"])
                s = bs4.BeautifulSoup(r.content, "html.parser")
                if "overloaded" in s:
                    r = None
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
