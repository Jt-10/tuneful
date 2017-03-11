import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine

# The Song SQLalchemy Model
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    files = relationship("File", uselist=False, back_populates="songs")

    def as_dictionary(self):
        song = {
            "id": self.id,
            "file": {
                "id": self.File.id,
                "name": self.File.name
            }
        }
        return song



# The File SQLalchemy Model
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    songs_id = Column(Integer, ForeignKey("songs.id"))
    songs = relationship("Song", back_populates="files")

    def as_dictionary(self):
        file = {
            "id": self.id,
            "name": self.name
        }
        return file


