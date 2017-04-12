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
from tuneful import database
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
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])

    def test_get_all_songs(self):
        """ Test GET songs from populated database """
        # Add test songs to database
        songA = database.Song()
        songB = database.Song()
        songA.name = "Example Song A"
        songB.name = "Example Song B"

        session.add_all([songA, songB])
        session.commit()

        # Ensure endpoint exists and is returning JSON
        response = self.client.get("api/songs", headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        # Ensure songs database contains two entries
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'file': {'id': 1, 'name': 'Example Song A'}, 'id': 1})
        self.assertEqual(data[1], {'file': {'id': 2, 'name': 'Example Song B'}, 'id': 2})


    def test_post_song(self):
        """ Test POST song to the database"""
        # Post a song to the database
        data = {
            "file": {
            "id": 1
            }
        }

        response = self.client.post("api/songs",
                    data = json.dumps(data),
                    content_type="application/json",
                    headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "applicationl/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path, "api/songs")

        data = json.loads(response.decode("ascii"))
        self.assertEqual(data["file"], "Sample File")
        self.assertEqual(data["id"], 7)
