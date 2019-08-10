from bs4 import BeautifulSoup
import requests
import re
import json

rottenBaseUrl = "https://www.rottentomatoes.com"

html = requests.get(rottenBaseUrl + "/search/?search=avengers")
soup = BeautifulSoup(html.content, "lxml")
script = soup.find("div", id="main_container").find(
    "div", class_="col col-left-center col-full-xs").findNext("script").text.strip()
if(script[0:7] != "require"):
    print("exiting")
    exit()
matches = re.findall(r"{.*", script)
results = json.loads(matches[1][:-2])
print(results)
