from bs4 import BeautifulSoup
import requests
import re
import pymongo

# Imdb Parser
html = requests.get(
    "https://www.imdb.com/search/title/?sort=user_rating&title_type=feature&num_votes=250000,")
soup = BeautifulSoup(html.content, "lxml")
resultList = soup.find_all("div", class_="lister-item mode-advanced")


class MovieItem:
    def __init__(self, imdbId, name, year, filmRating, runTime, genre, imdbRating, metaScore, description, posterUrl):
        self.imdbId = imdbId
        self.name = name
        self.year = re.search("[0-9]{4}", year).group(0)
        self.filmRating = filmRating
        self.runTime = runTime
        self.genre = genre.strip()
        self.imdbRating = imdbRating
        self.metaScore = metaScore.strip()
        self.description = description.strip()
        self.posterUrl = posterUrl.replace(".jpg", "#\$1.jpg") # Replace to increase poster resolution

    def __str__(self):
        return self.imdbId


def parseToMovieItem(object):
    primaryInfo = object.findNext("h3", class_="lister-item-header")
    secondaryInfo = object.findNext("p", class_="text-muted")
    ratingsInfo = object.findNext("div", class_="ratings-bar")
    posterData = object.findNext(
        "div", class_="lister-item-image float-left").findNext("a").findNext("img")

    return MovieItem(posterData["data-tconst"],
                     primaryInfo.findNext("a").text,
                     primaryInfo.findNext(
                         "span", class_="lister-item-year text-muted unbold").text,
                     secondaryInfo.findNext("span", class_="certificate").text,
                     secondaryInfo.findNext("span", class_="runtime").text,
                     secondaryInfo.findNext("span", class_="genre").text,
                     ratingsInfo.findNext("strong").text,
                     ratingsInfo.findNext(
                         "div", class_="inline-block ratings-metascore").findNext("span").text,
                     ratingsInfo.findNext("p", class_="text-muted").text,
                     posterData["loadlate"]
                     )


for item in resultList:
    print(parseToMovieItem(item))
