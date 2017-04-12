import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import database
from . import decorators
from . import app
from .database import session
from .utils import upload_path

# JSON Schema describing the structure of a post
post_schema = {'properties': {
    'file': {'id': 'integer'}
    },
    'required': 'id'
}

@app.route("/api/songs", methods=["GET"])
def get_songs():
    """ Get all the song from songs database and return as JSON """
    # Query the songs database
    songs = session.query(database.Song)

    # Convert the songs to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
def post_song():
    """ Post a song to the database that is formatted as JSON in the request """
    data = request.json

    # Check that the JSON supplied is valid
    # If not you return a 422 Un-processable Entry
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    Response(data, 201, mimetype="application/json")

    # Add the song to the database
    data = database.Song()
    session.add(data)
    session.commit()






