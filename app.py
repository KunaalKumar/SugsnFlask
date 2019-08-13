from flask import Flask, jsonify, request
from threading import Thread
import pymongo
import math
import os
import populate_database
from dto import MovieItem

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


client = pymongo.MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
# client = pymongo.MongoClient("localhost", 27017)
db = client.sugsn

app = Flask(__name__)


@app.route('/popDB', methods=['GET'])
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
    return jsonify({"current_page": page, "total_pages": math.floor(topRatedMovies.count() / limit), "result": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
