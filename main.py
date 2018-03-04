import bs4, requests, docx
import os, sys, threading, queue, time


class Spider:

    def __init__(self, url):
        self._base_url = url
        self._iframe = "glavni_niz.html"
        self._url = queue.Queue()
        self._url.put(self._base_url)  # starting URL, appends others on the way

        self._jobs = queue.Queue()  # queue for jobs

        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}

        self.languages = ["nor", "dan", "swe", "esk", "fin", "ice", "sme", "smi", "smn", "lap"]
        self._count = 3  # max thread count
        self._sema = threading.Semaphore(value=self._count)

    def run(self):
        print("Entering run")
        self.extract_urls_from_main_page(self._url.get())
        for url in iter(self._url.get, None):
            print(url)
            doc = docx.Document()
            doc.add_paragraph(url)
            paragraphs = {}
            for language in self.languages:
                paragraphs[language] = doc.add_paragraph(language + "\n")
            resp = self.visit_url(url)
            print(resp.status_code)
            print(resp)
            self.t = threading.Thread(target=self.extract_books_and_links, args=(resp.content, doc, paragraphs))
            self.t.start()
            # self.t.join()
        # self.save()
        print("Done.")

    def extract_urls_from_main_page(self, url):
        print("Entering extract_urls_from_main_page")
        resp = self.visit_url(url)
        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        links = soup.body.center.find_all("a")  # returns a result set (basically a list) of bs4 elements
        print("Links:", links)
        for link in links:
            self._url.put(self._base_url+link["href"][:-10]+self._iframe)
            # break
        print("Exiting extract_urls_from_main_page")
        print("URLs", self._url)

    def visit_url(self, url):
        return requests.get(url, headers=self._headers)

    def extract_books_and_links(self, content, doc, paragraph):
        self._sema.acquire()
        print("Entering extract_books_and_links")
        soup = bs4.BeautifulSoup(content, "html.parser")
        time.sleep(50)
        divs = soup.body.find_all("div", {"id":"znak"})
        for div in divs:
            a = div.find("a", {"href": True})  # div.a == div.find("a",{"href":True})
            link = a["href"]  # link to visit a seperate site with more info on the book
            # book_id = link.split("=")[2]  # book id; used to find the right a tag later on
            print(link)
            resp = self.visit_url(link)
            print(resp.status_code)
            res = self.check_if_foreign_book(resp.content, paragraph, link)
            if res:

                a_tag = div.find_previous("a")
                self.extract_book_info(a_tag, res, paragraph)
                del res, resp, link
                # self.save(doc)
                # break
            else:
                # a_tag = div.find_previous("a")
                # self.extract_book_info(a_tag, "nor")
                # self.save()
                # break
                continue
        print("Exiting extract_books_and_links")
        self.save(doc)
        self._sema.release()

    def check_if_foreign_book(self, content, paragraph, link):
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
                for lang in paragraph.keys():
                    if lang in languages:
                        print("Found one!!")
                        return lang
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

    def extract_book_info(self, soup, language, paragraph):
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
        paragraph[language].add_run(text+"\n")
        print("Exiting extract_book_info")

    def save(self, doc):
        print("Saving file")
        doc.save("./knjige/{}.docx".format(time.clock()))


if __name__ == "__main__":

    staring_url = "http://bibliografija.nsk.hr/a/"

    spider = Spider(staring_url)
    spider.run()
