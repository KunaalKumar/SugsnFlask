from bs4 import BeautifulSoup
import requests
import pymongo
from dto import MovieItem
import logging


class PopulateDatabase:

    baseUrl = "https://www.imdb.com"
    headers = {"Accept-Language": "en-US"}
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logHandler = logging.FileHandler("Logs/populate_database.log")
    logHandler.setFormatter(logging.Formatter(
        "%(asctime)s (%(filename)s)/(%(funcName)s): %(message)s"))
    logger.addHandler(logHandler)

    logger.info("-----------NEW SESSION-----------")

    pymongo.has_c() == True

    def __init__(self, client):
        self.db = client.sugsn

    def parseToMovieItem(self, object):
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
                         secondaryInfo.findNext(
                             "span", class_="certificate").text,
                         secondaryInfo.findNext("span", class_="runtime").text,
                         secondaryInfo.findNext("span", class_="genre").text,
                         ratingsInfo.findNext("strong").text,
                         ratingsInfo.findNext(
                             "div", class_="inline-block ratings-metascore").findNext("span").text,
                         ratingsInfo.findNext("p", class_="text-muted").text,
                         posterData["loadlate"]
                         )

    # Imdb Parser

    def getTopRatedMovies(self):
        html = requests.get(
            self.baseUrl + "/search/title/?sort=user_rating&title_type=feature&num_votes=250000,", headers=self.headers)
        soup = BeautifulSoup(html.content, "lxml")
        nextTag = soup.findAll("a", class_="lister-page-next next-page")

        # Traverse pages
        while(len(nextTag) != 0):
            # Populate database
            resultList = soup.find_all(
                "div", class_="lister-item mode-advanced")

            for item in resultList:
                movie = self.parseToMovieItem(item)
                self.logger.info("Adding " + str(movie.listNum) +
                                 " - %s" % movie.name)
                self.db.topRatedMovies.update_one({"listNum": movie.listNum}, {
                    "$set": movie.__dict__}, True)

            # Load next page
            html = requests.get(
                self.baseUrl + nextTag[0]["href"], headers=self.headers)
            soup = BeautifulSoup(html.content, "lxml")
            nextTag = soup.findAll("a", class_="lister-page-next next-page")
