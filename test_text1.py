import requests, bs4

r = requests.get("http://katalog.nsk.hr/F/?func=direct&doc_number=000698896")
soup = bs4.BeautifulSoup(r.content, "html.parser")
table = soup.find("td", {"class":"text1"})
#print(table)
link = table.find("a").find_next_sibling("a")
#print("LINK       ", link)
r = requests.get(link["href"])
print(r.status_code)
soup = bs4.BeautifulSoup(r.content, "html.parser")
row = soup.find("td", text="0411")
print(row)
n = row.find_next_sibling("td")
print(n)
if "ger" in n.text:
    print("True")
