from flask import Flask, jsonify, request
from threading import Thread
import pymongo
import math
import os
import populate_database
from dto import MovieItem
from apscheduler.schedulers.background import BackgroundScheduler


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


#client = pymongo.MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
client = pymongo.MongoClient("mongo_sugsn", 27017)
db = client.sugsn

app = Flask(__name__)


def populateDB():
    thread = Thread(target=populate_database.getTopRatedMovies)
    thread.start()
    return "Populating db..."


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
    return jsonify({"current_page": page, "total_pages": math.floor(topRatedMovies.count_documents / limit), "result": output})


def initApp():
    if(db.topRatedMovies.count_documents == 0):
        print("Populating new database\n")
        populateDB()
    scheduler = BackgroundScheduler()
    scheduler.add_job(populateDB, 'interval', hours=1)
    scheduler.start()


if __name__ == "__main__":
    initApp()
    app.run(host="flask_sugsn", debug=False)
