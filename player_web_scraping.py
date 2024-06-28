from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(1991, 2025))
player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

service = Service(executable_path="/Users/eshaangovil/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)

for year in years:
    url = player_stats_url.format(year)
    
    driver.get(url)
    driver.execute_script("window.scrollTo(1,10000)")
    time.sleep(2)
    
    with open("player/{}.html".format(year), "w+") as f:
        f.write(driver.page_source)

dfs = []
for year in years:
    with open("player/{}.html".format(year)) as f:
        page = f.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    player_table = soup.find_all(id="per_game_stats")[0]
    player_df = pd.read_html(str(player_table))[0]
    player_df["Year"] = year
    dfs.append(player_df)

players = pd.concat(dfs)
players.to_csv("players.csv")