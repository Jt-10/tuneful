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

@app.route("/api/songs", methods=["GET"])
def get_songs():
    """ Get all the song from songs database and return as JSON """
    # Query the songs database
    songs = session.query(database.Song)

    # Convert the songs to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")




