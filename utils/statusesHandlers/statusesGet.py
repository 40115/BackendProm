from flask import jsonify
import json


# Get All Statuses
def get_statuses(db_connection):
    # Establish connection with DB
    cursor = db_connection.cursor()

    try:
         # Get All Statuses
        cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT("
                       "'id', id, "
                       "'statusName', description "
                       ")) AS Statuses "
                       "FROM Statuses s")

        values = cursor.fetchall()
        if len(values) == 0:
            return "[]", 200

        str_values = ''.join(str(value[0]) for value in values)
        statuses_json = json.loads(str_values)

        cursor.close()
        return jsonify(statuses_json), 200

    except Exception:
        cursor.close()
        return jsonify(error='error'), 400
