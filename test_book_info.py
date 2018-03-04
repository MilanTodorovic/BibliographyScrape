import requests, bs4

r = requests.get("http://bibliografija.nsk.hr/a/A2017_10_v3/glavni_niz.html")
soup = bs4.BeautifulSoup(r.content, "html.parser")
div = soup.body.find_all("div", {"id":"znak"})
link = div[1].find("a",{"href":True})  # div.a == div.find("a",{"href":True})
# print(link)
links = link["href"].split("=")[2]
# print(links)
a = div[1].find_previous("a")
# print(a)

spans = a.find_all()
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

print(text)
