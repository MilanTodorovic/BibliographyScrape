import requests, bs4


r = requests.get("http://bibliografija.nsk.hr/a/A2009_11_v1/glavni_niz.html")
soup = bs4.BeautifulSoup(r.content, "html.parser")
div = soup.body.find("div", {"id":"znak"})
link = div.find("a",{"href":True})  # div.a == div.find("a",{"href":True})
print(link)
links = link["href"].split("=")[2]
print(links)
a = div.find_previous("a")
print(a)

