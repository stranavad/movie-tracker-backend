from flask_restful import Resource, reqparse
from flask_cors import cross_origin
from src import get_connection
import mysql.connector  # just for errors
import json

user_get = reqparse.RequestParser()
user_get.add_argument("id", help="user id", required="true", type=str)

user_post = reqparse.RequestParser()
user_post.add_argument("id", help="user id", required="true", type=str)
user_post.add_argument("movie_id", help="movie id", required="true", type=int)
user_post.add_argument("title", help="movie title", required="true", type=str)
user_post.add_argument("photo", help="movie photo url", required="true", type=str)
user_post.add_argument("year", help="movie year", required="false", type=int)
# user_post.add_argument("category", help="movie category", required="true", type=str)
user_post.add_argument("rating", help="user rating", required="true", type=int)
# user_post.add_argument("notes", help="user notes", required="false", type=str)

class Movies(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        # Get token from frontend and based on that return list off all Movies
        # Table name is the id
        # Error check
        user_id = user_get.parse_args()["id"]
        try:
            mydb, mycursor = get_connection()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 1, "errno": e.errno})

        try:
            mycursor.execute("SHOW TABLES")
        except mysql.connector.Error as e:
            print(e.errno)
            mydb.close()
            return json.dumps({"code": 101, "errno": e.errno})

        tables_db = mycursor.fetchall()
        tables = []
        for table in tables_db:
            tables.append(table[0])

        if f"{user_id}_movies" in tables:
            try:
                mycursor.execute(f"SELECT * FROM {user_id}_movies")
                result = mycursor.fetchall()
            except mysql.connector.Error as e:
                mydb.close()
                print(e.errno)
                return json.dumps({"code": 102, "errno": e.errno})

            if not result:
                return json.dumps({"code": 103})  # no movies inside user table

            return_dict = {"movies": {}, "code": 104}
            for res in result:
                return_dict["movies"][res[1]] = {
                "title": res[2],
                "photo": res[3],
                "year": res[4],
                "rating": res[5],
                }

            return json.dumps(return_dict)
        else:
            # creating table for the first time
            sql = f"CREATE TABLE {user_id}_movies (id INT AUTO_INCREMENT PRIMARY KEY, movie_id INT, title VARCHAR(255), photo VARCHAR(255), year INT, rating INT)"

            try:
                mycursor.execute(sql)
                mydb.commit()
                mydb.close()
            except mysql.connector.Error as e:
                print(e.errno)
                return json.dumps({"code": 105, "errno": e.errno})

            return json.dumps({"code": 106})


    @cross_origin(supports_credentials=True)
    def post(self):
        args = user_post.parse_args()

        try:
            mydb, mycursor = get_connection()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 1, "errno": e.errno})

        sql = f"INSERT INTO {args['id']}_movies (movie_id, title, photo, year, rating) VALUES (%s, %s, %s, %s, %s)"
        values = (args["movie_id"], args["title"], args["photo"], args["year"], args["rating"])

        try:
            mycursor.execute(sql, values)
            mydb.commit()
        except mysql.connector.Error as e:
            print(e.errno)
            mydb.close()
            return json.dumps({"code": 111, "errno": e.errno})

        return json.dumps({"code": 112})


get_movie_id = reqparse.RequestParser()
get_movie_id.add_argument("id", help="user id", type=str, required=True)

class MovieIds(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        # get movies from database
        user_id = get_movie_id.parse_args()["id"]

        try:
            mydb, mycursor = get_connection()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 1, "errno": e.errno})

        try:
            mycursor.execute(f"SELECT * FROM {user_id}_movies")
            result = mycursor.fetchall()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 102})

        for res in result:
            to_return.append(res[1])
        return json.dumps({"code": "104", "movies": to_return})
