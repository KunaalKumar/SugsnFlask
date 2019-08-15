from flask import Flask, jsonify, request
import pymongo
from threading import Thread
import math
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import app_init
import populate_database
from dto import MovieItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.FileHandler("Logs/app.log")
logHandler.setFormatter(logging.Formatter(
    "%(asctime)s (%(filename)s)/(%(funcName)s): %(message)s"))
logger.addHandler(logHandler)
logger.info("-----------NEW SESSION-----------")

# Convert MovieItem object to dictionary


def convertMovieToJson(movie):
    return {"name": movie["name"],
            "year": movie["year"],
            "runTime": movie["runTime"],
            "imdbRating": movie["imdbRating"],
            "rottenRating": movie["rottenRating"],
            "metaScore": movie["metaScore"],
            "description": movie["description"],
            "filmRating": movie["filmRating"],
            "genre": movie["genre"],
            "imdbId": movie["imdbId"],
            "posterUrl": movie["posterUrl"]}


client = pymongo.MongoClient("mongo_sugsn", 27017)
# client = pymongo.MongoClient("localhost", 27017)

db = client.sugsn

app = Flask(__name__)

populateObj = populate_database.PopulateDatabase(client)


def populateDB():
    thread = Thread(target=populateObj.getTopRatedMovies)
    thread.start()
    logger.info("Started populating database on a new thread")

# @app.route('/forceUpdate', methods=['GET'])
# def forceUpdateDb():
    # populateDB()


@app.route('/topRatedMovies', methods=['GET'])
def getTopRatedMovies():
    page = 1
    limit = 20

    topRatedMovies = db.topRatedMovies

    # Set query values if they exist
    if request.args.get("page") is not None:
        page = int(request.args.get("page"))
    if request.args.get("limit") is not None:
        limit = int(request.args["limit"])

    moviesList = topRatedMovies.find({"listNum": {"$gte":  (limit * (page - 1)) + 1}}).sort(
        'listNum', pymongo.ASCENDING).limit(limit)
    output = []
    for movie in moviesList:
        output.append(convertMovieToJson(movie))
    return jsonify({"current_page": page, "total_pages": math.floor(topRatedMovies.estimated_document_count() / limit), "result": output})


def initApp():
    if(db.topRatedMovies.estimated_document_count() == 0):
        logger.info("Populating new database\n")
        populateDB()
    logger.info("Setting scheduler to run every 1 hour")
    scheduler = BackgroundScheduler()
    scheduler.add_job(populateDB, 'interval', hours=1)
    scheduler.start()


if __name__ == "__main__":
    initApp()
    app.run(host="flask_sugsn", debug=False)
    # app.run(host="0.0.0.0", debug=False)
