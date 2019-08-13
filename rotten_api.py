from bs4 import BeautifulSoup
import requests
import re
import json

rottenBaseUrl = "https://www.rottentomatoes.com"
headers = {"Accept-Language": "en-US"}


def isValidMovie(searchYear, movieYear):
    test = abs(searchYear - movieYear)
    if(test == 1 or test == 0):
        return True
    return False


def getRottenMovieRating(movieName, movieYear):
    html = requests.get(rottenBaseUrl + "/search/?search=" +
                        movieName, headers=headers)
    soup = BeautifulSoup(html.content, "lxml")
    script = soup.find("div", id="main_container").find(
        "div", class_="col col-left-center col-full-xs").findNext("script").text.strip()

    # If script doesn't start with "require", no results found
    if(script[0:7] != "require"):
        return ""

    matches = re.findall(r"{.*", script)

    # Remove last two elemnts that belong to script and convert to json
    results = json.loads(matches[1][:-2])

    for movie in results["movies"]:
        if(movie["year"] is not None
           and isValidMovie(int(movie["year"]), movieYear)
           and "meterScore" in movie):
            return movie["meterScore"]
        else:
            print("Failed rotten match for " +
                  movieName + " against %s" % movie["name"])
