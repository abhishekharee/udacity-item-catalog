import os
import sys

# Import relevant SQLAlchemy packages
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Declare Base
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    user_email = Column(String(50), nullable=False)


class Podcast(Base):
    __tablename__ = 'podcast'

    podcast_id = Column(Integer, primary_key=True)
    podcast_name = Column(String(250), nullable=False)
    podcast_description = Column(String(1000), nullable=False)
    podcast_user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'podcast_id': self.podcast_id,
            'podcast_name': self.podcast_name,
            'podcast_description': self.podcast_description
        }


class Episode(Base):

    __tablename__ = 'episode'

    episode_id = Column(Integer, primary_key=True)
    episode_name = Column(String(100), nullable=False)
    episode_description = Column(String(1000), nullable=False)
    episode_date = Column(String(10), nullable=False)
    episode_listened = Column(String(8), nullable=True)
    podcast_id = Column(Integer, ForeignKey('podcast.podcast_id'))
    podcast = relationship(Podcast)
    episode_user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'episode_id': self.episode_id,
            'episode_name': self.episode_name,
            'episode_description': self.episode_description,
            'episode_date': self.episode_date,
            'episode_listened': self.episode_listened,
            'podcast_id': self.podcast_id

        }


engine = create_engine('sqlite:///podcastepisodes.db')
# Create database by running engine
Base.metadata.create_all(engine)
