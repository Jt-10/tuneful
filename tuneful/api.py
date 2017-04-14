import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from . import app
from .database import session
from .utils import upload_path

# JSON Schema describing the structure of a post
post_schema = {
    'properties': {
        'file': {
            'properties': {
                'id': {'type': 'integer'}
            }, 'required': ['id']
    }
}}

@app.route('/api/songs', methods=['GET'])
@decorators.accept('application/json')
def get_songs():
    """ Get all the song from songs database and return as JSON """
    # Query the songs database
    songs = session.query(models.Song).all()

    # Convert the songs to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_song():
    """ Post a song to the database that is formatted as JSON in the request """
    # Collect JSON supplied in request
    data = request.json

    # Check that the JSON supplied is valid
    # If not return a 422 Un-processable Entry
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype='application/json')

    # Check whether file exists in the 'files' table
    file = session.query(models.File).get(data['file']['id'])
    if not file:
        data = {'message': 'Could not find file with id {}'.format(id)}
        return Response(json.dumps(data), 404, mimetype='application/json')

    # Add a corresponding song to the 'songs' table
    new_song = models.Song(files=file)
    session.add(new_song)
    session.commit()

    data = new_song.as_dictionary()
    return Response(json.dumps(data), 201, mimetype='application/json')






