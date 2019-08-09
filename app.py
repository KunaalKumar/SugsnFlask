from flask import Flask
import pymongo
from populateDatabase import MovieItem

client = pymongo.MongoClient("localhost", 27017)
db = client.sugsn

testItem = MovieItem("Name", "2100", "R", "140 min",
                     "Drama", "7.8", "80", "Testing db")

testItem2 = MovieItem("The Terminator", "1991", "R", "140 min",
                      "Drama", "7.8", "80", "The Terminator 2")

db.movies.update_one({"name": "Name"}, {"$set": testItem.__dict__}, True)
db.movies.update_one({"name": testItem2.name}, {
                     "$set": testItem2.__dict__}, True)


# Flask API
# app = Flask(__name__)

# @app.route('/topRatedMovies', methods=['GET'])
# def getTopRatedMovies():
#     return ""
