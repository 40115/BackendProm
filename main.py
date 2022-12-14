from flask import Flask, request
from dynaconf import FlaskDynaconf
from flask_cors import CORS

from utils.helper.connection import connectionSet
from utils.moviesHandlers.moviesGet import get_movies, get_movie_by_id
from utils.accountHandlers.login import login
from utils.accountHandlers.register import register

app = Flask(__name__)

FlaskDynaconf(app, settings_files=["config/settings.yaml", "config/.secrets.yaml", "config/.env"])

# CORS
cors = CORS(app)


@app.route('/movies/getmovies', methods=['POST'])
async def get_movies_handler():
    connection = await connectionSet(app.config)
    response = get_movies(
        connection,
        request.json
    )
    connection.close()
    return response


@app.route('/movies/getmoviebyid', methods=['POST'])
async def get_movie_by_id_handler():
    connection = await connectionSet(app.config)
    response = get_movie_by_id(
        connection,
        request.json
    )
    connection.close()
    return response


@app.route('/login', methods=['POST'])
async def login_handler():
    connection = await connectionSet(app.config)
    response = login(
        request.json['email'].lower().strip(),
        request.json['password'],
        connection
    )
    connection.close()
    return response


@app.route('/register', methods=['POST'])
async def register_handler():
    connection = await connectionSet(app.config)
    response = register(
        request.json['email'].lower().strip(),
        request.json['username'],
        request.json['password'],
        connection
    )
    connection.close()
    return response


if __name__ == "__main__":
    app.run(host=app.config['app_config'].host, port=app.config['app_config'].port,
            debug=app.config['app_config'].debug)
