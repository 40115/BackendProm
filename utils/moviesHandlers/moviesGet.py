from flask import jsonify
import json
from jsonschema import validate, exceptions


# Get All Movies
def get_movies(db_connection):
    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
         # Get All Movies
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'id', m.id, "
                       "'name', m.name, "
                       "'releaseDate', m.releaseDate, "
                       "'imdbRating', m.imdbRating, "
                       "'runTime', m.runTime, "
                       "'ageRating', ar.description, "
                       ")) AS Movies "
                       "FROM Movies m "
                       "LEFT JOIN AgeRatings ar ON ar.id = m.ageRatingId")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        movies_json = json.loads(str_values)

        cursor.close()
        return movies_json, 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400


# Get Movie
def get_movie_by_id(db_connection, json_request):
    # Get movie id json
    movie_id_json = json_request

    # Create schema for JSON data validation
    json_data_schema = {
        "type": "object",
        "properties": {
            "movieId": {
                "type": "integer"
            }
        },
        "required": ["movieId"]
    }

    # If some of these inputs are not valid, return 'error'
    try:
        validate(instance=movie_id_json, schema=json_data_schema)
    except exceptions.ValidationError as e:
        return jsonify(error=e.message), 400

    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
        movie_id = movie_id_json["movieId"]

        # Get Movie
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'id', m.id, "
                       "'name', m.name, "
                       "'synopsis', m.synopsis, "
                       "'releaseDate', m.releaseDate, "
                       "'imdbRating', m.imdbRating, "
                       "'runTime', m.runTime, "
                       "'cover', m.cover, "
                       "'ageRating', ar.description, "
                       "'imdbUrl', m.imdbUrl "
                       ")) AS Movies "
                       "FROM Movies m "
                       "LEFT JOIN AgeRatings ar ON ar.id = m.ageRatingId "
                       f"WHERE m.Id = {movie_id}")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        movie_json = json.loads(str_values)

        # Get Movie's genres
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'id', g.id, "
                       "'genreName', g.description "
                       ")) AS Genres "
                       "FROM Genres g "
                       "LEFT JOIN MovieGenres mg ON g.Id = mg.GenreId "
                       f"WHERE mg.MovieId = 2")

        values = cursor.fetchall()

        str_values = ''.join(str(value[0]) for value in values)
        genres_json = json.loads(str_values) if str_values != 'None' else '[]'

        info = {
            "movie": movie_json,
            "genres": genres_json
        }

        cursor.close()

        return jsonify(info), 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400
