from flask import jsonify
import json
from jsonschema import validate, exceptions


# Get user's backlog
def get_backlog_by_user(db_connection, json_request):
    # Get movie id json
    user_id_json = json_request

    # Create schema for JSON data validation
    json_data_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "userId": {
                    "type": "integer"
                }
            },
            "required": ["userId"]
        }
    }

    # If some of these inputs are not valid, return 'error'
    try:
        validate(instance=user_id_json, schema=json_data_schema)
    except exceptions.ValidationError as e:
        return jsonify(error=e.message), 400

    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
        user_id = user_id_json[0]["userId"]

        # Get backlog
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'movieId', m.Id, "
                       "'movieName', m.Name, "
                       "'releaseDate', m.ReleaseDate, "
                       "'imdbRating', m.ImdbRating, "
                       "'runTime', m.RunTime, "
                       "'ageRating', ar.Description, "
                       "'watchedDate', b.WatchedDate, "
                       "'statusId', s.Id, "
                       "'status', s.Description, "
                       "'userRating', b.Rating "
                       ")) AS Backlog "
                       "FROM Backlogs b "
                       "LEFT JOIN Movies m ON m.Id = b.MovieId "
                       "LEFT JOIN Statuses s ON s.Id = b.StatusId "
                       "LEFT JOIN AgeRatings ar ON ar.Id = m.AgeRatingId "
                       "LEFT JOIN Users u ON u.Id = b.UserId "
                       f"WHERE u.Id = {user_id}")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        backlog_json = json.loads(str_values)

        cursor.close()
        return backlog_json, 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400
