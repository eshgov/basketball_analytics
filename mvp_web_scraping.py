import requests
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(1991, 2025))
url_template = "https://www.basketball-reference.com/awards/awards_{}.html"

for year in years:
    url = url_template.format(year)
    data = requests.get(url)
    with open("/mvp/{}.html".format(year), "w+") as f:
        f.write(data.text)

dfs = []
for year in years:
    with open("mvp/{}.html".format(year)) as f:
        page = f.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="over_header").decompose()
    mvp_table = soup.find_all(id="mvp")[0]
    mvp_df = pd.read_html(str(mvp_table))[0]
    mvp_df["Year"] = year
    dfs.append(mvp_df)

mvps = pd.concat(dfs)
mvps.to_csv("mvps.csv")