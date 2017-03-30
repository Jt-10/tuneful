from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from . import app

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# The Song SQLalchemy Model
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    files = relationship("File", uselist=False, back_populates="songs")

    # Add code to create the database and interact with it

    def as_dictionary(self):
        song = {
            "id": self.id,
            "file": {
                "id": self.File.id,
                "name": self.File.name
            }
        }
        # Add code to query the table and retrieve the data

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

Base.metadata.create_all(engine)
