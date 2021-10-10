from flask import Flask
from flask_restful import Api
import mysql.connector
from flask_cors import CORS
from src.config import config

mydb = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    passwd=config["passwd"],
    database="movie_tracker",
    pool_name="movie_tracker",
    pool_size=5,
)

def get_connection():
    db = mysql.connector.connect(pool_name="movie_tracker")
    return db, db.cursor()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = "randomsecretkey-movietracker"
    return app

def create_api(app):
    api = Api(app)

    from src.movies.routes import Movies
    api.add_resource(Movies, "/user")

    from src.movies.routes import MovieIds
    api.add_resource(MovieIds, "/user/moviesids")

    return api
