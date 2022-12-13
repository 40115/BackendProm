import json

from flask import Flask, jsonify, request, abort
from dynaconf import FlaskDynaconf
from flask_cors import CORS
import pyodbc as pyodbc

from utils.helper.connection import connectionSet
from utils.moviesHandlers.moviesGet import get_movies, get_movie_by_id

app = Flask(__name__)

FlaskDynaconf(app, settings_files=["config/settings.yaml", "config/.secrets.yaml", "config/.env"])

# CORS
cors = CORS(app)


@app.route('/movies/getmovies', methods=['GET'])
async def getMoviesHandler():
    connection = await connectionSet(app.config)
    response = get_movies(
        connection
    )
    connection.close()
    return response


@app.route('/movies/getmoviebyid', methods=['POST'])
async def getMovieByIdHandler():
    connection = await connectionSet(app.config)
    response = get_movie_by_id(
        connection,
        request.json
    )
    connection.close()
    return response


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
