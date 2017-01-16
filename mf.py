import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

gold_mf = "http://www.morningstar.in/gold-rated-mutual-fund.aspx"
final_mf = {}
final_poftifolio = {}

gold_mf_page = requests.get(gold_mf)
gold_soup = bs(gold_mf_page.text,"lxml")
mf = gold_soup.find("div",{"class":"fundsArchive"})
mf_list = mf.find("table").findAll("tr")
for m in mf_list:
    for td in m.findAll("td"):
        if td is not None:
            for a in td.findAll("a"):
                final_mf[a['title']] = "http://www.morningstar.in"+a['href'][:-21]+ "detailed-portfolio.aspx"

for fund in final_mf:
    stocks = []
    pfolio = requests.get(final_mf[fund])
    if pfolio.status_code == 200:
        pfolio_soup = bs(pfolio.text,"lxml")
        k = pfolio_soup.findAll("a", id = re.compile("^ctl00_ContentPlaceHolder1_lstvStock_ctrl[1-9]\d*"))
        l = pfolio_soup.findAll("span", id = re.compile("^ctl00_ContentPlaceHolder1_lstvStock_ctrl[1-9]\d*"))
        for s in k:
            stocks.append(s["title"])
        for s in l:
            if s.text != "Total Stock":
                stocks.append(s.text)
        # table = pfolio_soup.find("table",{"class":"pf_detailed"})
        # for row in table.findAll("tr"):
        #     a = row.find("a")
        #     # print(a)
        #     if a is not None:
        #         stocks.append(a["title"])
        final_poftifolio[fund] = stocks


total_stocks = []

for fund in final_poftifolio:
