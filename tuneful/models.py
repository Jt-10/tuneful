import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine


# The Song SQLalchemy Model
class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    files = relationship('File', uselist=False, back_populates='songs')

    def as_dictionary(self):
        return {"id": self.id, "file": self.files.as_dictionary()}

# The File SQLalchemy Model
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    songs_id = Column(Integer, ForeignKey('songs.id'))
    filename = Column(String(1024))
    songs = relationship('Song', back_populates='files')

    def as_dictionary(self):
        return {
            'id': self.id,
            'name': self.filename,
        }

Base.metadata.create_all(engine)