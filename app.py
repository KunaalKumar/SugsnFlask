from flask import Flask, jsonify
import pymongo
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
    topRatedMovies = db.topRatedMovies
    offset = 500
    limit = 10
    moviesList = topRatedMovies.find({"listNum": {"$gte": 300}}).sort(
        'listNum', pymongo.ASCENDING).limit(limit)
    output = []
    for movie in moviesList:
        output.append(convertMovieToJson(movie))
    return jsonify({"result": output, "prev_page": "", "next_page": ""})


if __name__ == "__main__":
    app.run(debug=True)
