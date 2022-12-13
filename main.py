import json

from flask import Flask, jsonify, request, abort
from dynaconf import FlaskDynaconf
from flask_cors import CORS
from flask_mysqldb import MySQL
import pyodbc as pyodbc

from utils.helper.connection import connectionSet

app = Flask(__name__)

FlaskDynaconf(app, settings_files=["config/settings.yaml", "config/.secrets.yaml", "config/.env"])

# CORS
cors = CORS(app)


@app.route('/', methods=['GET'])
async def index():
    connection = await connectionSet(app.config)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies')
    columns = [column[0] for column in cursor.description]
    strValues = cursor.fetchall()
    data = []
    for row in strValues:
        data.append(dict(zip(columns, row)))
    #a=jsonify(data)
    data = json.dumps(data)
    return data, 200

@app.route('/login', methods=['POST'])
async def loginHandler():
    connection = await connectionSet(app.config)
    # response = login(
    #     request.json['email'].lower().strip(),
    #     request.json['pass'],
    #     connection
    # )
    # connection.close()
    # return response


if __name__ == "__main__":
    dlist = pyodbc.drivers()
    for d in dlist:
        print(d)
    app.run(host=app.config['app_config'].host, port=app.config['app_config'].port,
            debug=app.config['app_config'].debug)
