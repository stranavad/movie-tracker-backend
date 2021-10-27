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
user_post.add_argument("overview", help="movie description", type=str)
user_post.add_argument("genres", help="array of genre names", type=list)

delete_movie = reqparse.RequestParser()
delete_movie.add_argument("id", help="user id", required="true", type=str)
delete_movie.add_argument("movie_id", type=int, help="Movie id from table", required="true") # binary search


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
                mydb.close()
            except mysql.connector.Error as e:
                mydb.close()
                print(e.errno)
                return json.dumps({"code": 102, "errno": e.errno})

            if not result:
                return json.dumps({"code": 103})  # no movies inside user table

            return_dict = {"movies": {}, "code": 104}
            for res in result:
                data_object = json.loads(res[1])
                return_dict["movies"][data_object["movie_id"]] = {
                    "movie_table_id": res[0],
                    "title": data_object["title"],
                    "photo": data_object["photo"],
                    "year": data_object["year"],
                    "rating": data_object["rating"],
                }

            return json.dumps(return_dict)
        else:
            # creating table for the first time
            # sql = f"CREATE TABLE {user_id}_movies (id INT AUTO_INCREMENT PRIMARY KEY, movie_id INT, title VARCHAR(255), photo VARCHAR(255), year INT, rating INT)"
            sql = f"CREATE TABLE {user_id}_movies (id INT AUTO_INCREMENT PRIMARY KEY, movie JSON)"

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

        movie_object = {
            "movie_id": args["movie_id"],
            "title": args["title"],
            "photo": args["photo"],
            "year": args["year"],
            "rating": args["rating"],
            "overview": args["overview"],
            "genres": args["genres"]
        }
        sql = f"INSERT INTO {args['id']}_movies (movie) VALUES (%s)"
        values = (json.dumps(movie_object),)

        try:
            mycursor.execute(sql, values)
            mydb.commit()
            mydb.close()
        except mysql.connector.Error as e:
            print(e.errno)
            mydb.close()
            return json.dumps({"code": 111, "errno": e.errno})

        return json.dumps({"code": 112})

    @cross_origin(supports_credentials=True)
    def delete(self):
        args = delete_movie.parse_args()
        try:
            mydb, mycursor = get_connection()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 1, "errno": e.errno})

        try :
            print(args["id"])
            print(args["movie_id"])
            mycursor.execute(f"DELETE FROM {args['id']}_movies WHERE id={args['movie_id']}")
            mydb.commit()
            mydb.close()
        except mysql.connector.Error as e:
            print(e.errno)
            return json.dumps({"code": 121, "errno": e.errno})

        return json.dumps({"code": 122})



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
            mydb.close()
        except mysql.connector.Error as e:
            mydb.close()
            print(e.errno)
            return json.dumps({"code": 102})

        to_return = []
        for res in result:
            movie_id = json.loads(res[1])["movie_id"]
            to_return.append(movie_id)
        return json.dumps({"code": 104, "movies": to_return})
