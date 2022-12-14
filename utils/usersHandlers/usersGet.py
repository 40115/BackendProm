from flask import jsonify
import json
from jsonschema import validate, exceptions

# Get Movie
def get_user_by_id(db_connection, json_request):
    # Get movie id json
    user_id_json = json_request

    # Create schema for JSON data validation
    json_data_schema = {
        "type": "object",
        "properties": {
            "userId": {
                "type": "integer"
            }
        },
        "required": ["userId"]
    }

    # If some of these inputs are not valid, return 'error'
    try:
        validate(instance=user_id_json, schema=json_data_schema)
    except exceptions.ValidationError as e:
        return jsonify(error=e.message), 400

    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
        user_id = user_id_json["userId"]

        # Get User data
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'email', u.email, "
                       "'username', u.username "
                       ")) AS User "
                       "FROM Users u "
                       f"WHERE u.Id = {user_id}")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        user_json = json.loads(str_values)

        cursor.close()

        return jsonify(user_json), 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400
