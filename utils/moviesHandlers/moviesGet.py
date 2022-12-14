from flask import jsonify
import json
from jsonschema import validate, exceptions


# Get All Movies
def get_movies(db_connection, json_request):
    # Get movie id json
    page_json = json_request

    # Create schema for JSON data validation
    json_data_schema = {
        "type": "object",
        "properties": {
            "page": {
                "type": "integer"
            }
        },
        "required": ["page"]
    }

    # If some of these inputs are not valid, return 'error'
    try:
        validate(instance=page_json, schema=json_data_schema)
    except exceptions.ValidationError as e:
        return jsonify(error=e.message), 400

    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
        page = page_json["page"] - 1

        # Get All Movies
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'id', id, "
                       "'name', name, "
                       "'synopsis', synopsis, "
                       "'releaseDate', releaseDate, "
                       "'imdbRating', imdbRating, "
                       "'runTime', runTime, "
                       "'cover', cover, "
                       "'ageRatingId', ageRatingId, "
                       "'imdbUrl', imdbUrl "
                       ")) AS Movies "
                       "FROM Movies "
                       f"LIMIT 5 OFFSET {page * 5}")

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
                       "'id', id, "
                       "'name', name, "
                       "'synopsis', synopsis, "
                       "'releaseDate', releaseDate, "
                       "'imdbRating', imdbRating, "
                       "'runTime', runTime, "
                       "'cover', cover, "
                       "'ageRatingId', ageRatingId, "
                       "'imdbUrl', imdbUrl "
                       ")) AS Movies "
                       "FROM Movies "
                       f"WHERE Id = {movie_id}")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        movie_json = json.loads(str_values)

        cursor.close()

        return movie_json, 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400
