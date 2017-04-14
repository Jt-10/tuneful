import unittest
import os
import shutil
import json

try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def test_get_empty_songs(self):
        """ Test GET songs from empty database """
        # Ensure endpoint exists and is returning JSON
        response = self.client.get("/api/songs", headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        # Ensure songs database is empty
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data, [])

    def test_get_songs(self):
        """ Test GET songs from populated database """
        # Add test files and songs to database
        fileA = models.File(filename='love_song.mp3')
        fileB = models.File(filename='another_song.mp3')
        session.add_all([fileA, fileB])

        songA = models.Song(files=fileA)
        songB = models.Song(files=fileB)
        session.add_all([songA, songB])
        session.commit()

        # Ensure endpoint exists and is returning JSON
        response = self.client.get("api/songs", headers=[("Accept", "application/json")])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        # Ensure 'songs' table contains two entries related to those in the 'files' table
        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['file']['id'], fileA.id)
        self.assertEqual(data[1]['file']['id'], fileB.id)


    def test_post_song(self):
        """ Test POSTing a song to the database"""
        # Add test files to 'files' table
        fileA = models.File(filename='love_song.mp3')
        fileB = models.File(filename='another_song.mp3')
        session.add_all([fileA, fileB])
        session.commit()

        # Post a song to the database
        data = {'file': {'id': fileA.id}}

        response = self.client.post('api/songs',
                    data = json.dumps(data),
                    content_type='application/json',
                    headers=[('Accept', 'application/json')]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')


        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['file']['name'], 'love_song.mp3')
        self.assertEqual(data['file']['id'], fileA.id)

    def test_put_song(self):
        """Test PUTting a song to the database"""
        # Add test files to 'files' table
        fileA = models.File(filename='love_song.mp3')
        fileB = models.File(filename='another_song.mp3')
        session.add_all([fileA, fileB])
        session.commit()

        # Put a song to the database
        data = {'file': {'id': fileA.id}}

        response = self.client.put('api/songs',
                    data = json.dumps(data),
                    content_type='application/json',
                    headers=[('Accept', 'application/json')]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data.decode('ascii'))
        self.assertEqual(data['file']['name'], 'love_song.mp3')
        self.assertEqual(data['file']['id'], fileA.id)
