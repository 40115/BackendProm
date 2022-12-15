from flask import jsonify
from jsonschema import validate, exceptions
from datetime import date

def insert_or_update_backlog_entry(db_connection, json_request):
    # Get movie id json
    backlog_json = json_request

    # Create schema for JSON data validation
    json_data_schema = {
        "type": "object",
        "properties": {
            "userId": {
                "type": "integer"
            },
            "movieId": {
                "type": "integer"
            },
            "statusId": {
                "type": "integer"
            },
            "watchedDate": {
                "type": "string",
                "pattern": "^(\d{4}-(02-(0[1-9]|[12][0-9])|(0[469]|11)-(0[1-9]|[12][0-9]|30)|(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))([T0-9:.Z])*)$"
            },
            "rating": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
            }
        },
        "required": ["userId", "movieId"]
    }

    try:
        validate(instance=backlog_json, schema=json_data_schema)
    except exceptions.ValidationError as e:
        return jsonify(error=e.message), 400

    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
        user_id = backlog_json["userId"]
        movie_id = backlog_json["movieId"]

        status_id = backlog_json["statusId"] if 'statusId' in backlog_json else 2               # Plan To Watch
        watched_date = backlog_json["watchedDate"] if 'watchedDate' in backlog_json else None
        rating = backlog_json["rating"] if 'rating' in backlog_json else None

        # See if entry exists
        cursor.execute("SELECT Id, UserId, MovieId, WatchedDate, StatusId, Rating "
                       "FROM Backlogs "
                       f"WHERE UserId = {user_id} "
                       f"AND MovieId = {movie_id}")

        # Insert if it doesn't exist
        if cursor.rowcount == 0:
            insert_columns = "UserId, MovieId"
            insert_values = f"{user_id}, {movie_id}"

            if status_id is not None:
                insert_columns += ", StatusId"
                insert_values += f", {status_id}"

            if watched_date is not None:
                insert_columns += ", WatchedDate"
                insert_values += f", '{watched_date}'"

            if rating is not None:
                insert_columns += ", Rating"
                insert_values += f", {rating}"

            insert_query = f"INSERT INTO Backlogs ({insert_columns}) VALUES ({insert_values})"
            cursor.execute(insert_query)

        else:
            backlogged_movie = cursor.fetchone()
            set_query = "SET "

            if status_id != backlogged_movie.StatusId:
                set_query += f"StatusId = {status_id}, "
            if watched_date != backlogged_movie.WatchedDate:
                set_query += f"WatchedDate = '{watched_date}', "
            if rating != backlogged_movie.Rating:
                set_query += f"Rating = {rating}, "

            if set_query != "SET ":
                cursor.execute(f"UPDATE Backlogs {set_query[:-2]}")

        cursor.commit()
        cursor.close()
        return jsonify(success="success"), 200

    except Exception:
        cursor.rollback()
        cursor.close()
        return jsonify(error='error'), 400
