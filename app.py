from flask import Flask, jsonify, request
import pymongo
import math
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


client = pymongo.MongoClient("localhost", 27017)
db = client.sugsn

app = Flask(__name__)


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
    app.run(debug=True)
