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
    moviesList = topRatedMovies.find().sort('listNum', pymongo.ASCENDING)
    output = []
    for movie in moviesList:
        output.append(convertMovieToJson(movie))
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
