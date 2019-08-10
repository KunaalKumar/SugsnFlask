from bs4 import BeautifulSoup
import requests
import re
import pymongo
from DTO import MovieItem

client = pymongo.MongoClient("localhost", 27017)
db = client.sugsn
baseUrl = "https://www.imdb.com"

# Imdb Parser
html = requests.get(
    baseUrl + "/search/title/?sort=user_rating&title_type=feature&num_votes=250000,")
soup = BeautifulSoup(html.content, "lxml")
nextTag = soup.findAll("a", class_="lister-page-next next-page")


def parseToMovieItem(object):
    primaryInfo = object.findNext("h3", class_="lister-item-header")
    secondaryInfo = object.findNext("p", class_="text-muted")
    ratingsInfo = object.findNext("div", class_="ratings-bar")
    posterData = object.findNext(
        "div", class_="lister-item-image float-left").findNext("a").findNext("img")

    return MovieItem(primaryInfo.findNext("span", class_="lister-item-index unbold text-primary").text,
                     posterData["data-tconst"],
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


# Traverse pages
while(len(nextTag) != 0):
    # Populate database
    resultList = soup.find_all("div", class_="lister-item mode-advanced")

    for item in resultList:
        movie = parseToMovieItem(item)
        print("Adding " + str(movie.listNum) + " - " + movie.name)
        db.topRatedMovies.update_one({"listNum": movie.listNum}, {
            "$set": movie.__dict__}, True)

    # Load next page
    html = requests.get(baseUrl + nextTag[0]["href"])
    soup = BeautifulSoup(html.content, "lxml")
    nextTag = soup.findAll("a", class_="lister-page-next next-page")
