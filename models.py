from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

"""
-------
Classes
-------

Tweet:
    twitter_tweet_id
    text
    user
    url
    date_time
    longitude
    latitude

Hashtag:
    text
    url

Location:
    city
    state
    country
	
---------------
Relationships
between classes
---------------

Tweet - Hashtag : many-to-many
Location - Hashtag : many-to-many
Location - Tweet : one-to-many (one location to many tweets)
	
--------------------------
Association tables for
many-to-many relationships
--------------------------

hashtag_tweet_table
hashtag_location_table

"""

# Association table for many-to-many relationship between Hashtag and Tweet
hashtag_tweet_table = Table('hashtag_tweet', Base.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id')),
    Column('tweet_id', Integer, ForeignKey('tweet.d'))
)

# Association table for many-to-many relationship between Hashtag and Location
hashtag_location_table = Table('hashtag_location', Base.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)

class Tweet(Base):
    """
    Tweet class.
    Attributes: id, twitter_tweet_id, text, user, url, date_time, latitude, longitude, location_id.
	
    twitter_tweet_id is the id given by Twitter for a tweet. id is the id for the tweet in our database.
    location_id is the id (foreign key) of the Location where the tweet was tweeted. 
	
    Tweet has a many-to-many relationship with Hashtag.
    Also has a one-to-many relationship with Location (one Location to many Tweets).
	
    The relationship with Location includes a backref so that Locations have access to tweets
    associated with them.
    """
	
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    # Check length of this field
    twitter_tweet_id = Column(String(50))
    text = Column(String(140))
    user = Column(String(80))
    url = Column(String(80), unique=True)
    date_time = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)
	
    # foreign key for one-to-many relationship with Location.
    # backref so locations can access tweets associated with them.
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", backref=backref("tweets", lazy='dynamic'))

    def __repr__(self):
        return '<Tweet %d>' % self.id

class Hashtag(Base):
    """
    Hashtag class.
    Attributes: id, text, url.
	
    Hashtag has a many-to-many relationship with both Tweet and Location.
    """
	
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    text = Column(String(140), unique=True)
    url = Column(String(80), unique=True)

    tweets = relationship("Tweet", secondary=hashtag_tweet_table, backref="hashtag")

    def __repr__(self):
        return '<Hashtag %d>' % self.id


class Location(Base):
    """
    Location class.
    Attributes: id, city, state, country.
	
    Location has a many-to-many relationship with Hashtag.
    Also has a one-to-many relationship with Tweet (one Location to many Tweets).
    """
	
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String(80))
    state = Column(String(80))
    country = Column(String(80))

    hashtags = relationship("Hashtag", secondary=hashtag_location_table, backref="city")

    def __repr__(self):
        return '<City %d>' % self.id
