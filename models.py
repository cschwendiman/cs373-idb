from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLAlchemy(app)

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
hashtag_tweet_table = db.Table('hashtag_tweet',
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.d'))
)

# Association table for many-to-many relationship between Hashtag and Location
hashtag_location_table = db.Table('hashtag_location',
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
)

class Tweet(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    # Check length of this field
    twitter_tweet_id = db.Column(db.String(50))
    text = db.Column(db.String(140))
    user = db.Column(db.String(80))
    url = db.Column(db.String(80), unique=True)
    date_time = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
	
    # foreign key for one-to-many relationship with Location.
    # backref so locations can access tweets associated with them.
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = relationship("Location", backref=backref("tweets", lazy='dynamic'))

    def __init__(self, twitter_tweet_id, text, user, url, date_time, longitude, latitude):
        self.twitter_tweet_id = twitter_tweet_id
        self.text = text
        self.user = user
        self.url = url
        self.date_time = date_time
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Tweet %d>' % self.id

class Hashtag(db.Model):
    """
    Hashtag class.
    Attributes: id, text, url.
	
    Hashtag has a many-to-many relationship with both Tweet and Location.
    """
	
    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), unique=True)
    url = db.Column(db.String(80), unique=True)

    tweets = relationship("Tweet", secondary=hashtag_tweet_table, backref="hashtag")

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __repr__(self):
        return '<Hashtag %d>' % self.id


class Location(db.Model):
    """
    Location class.
    Attributes: id, city, state, country.
	
    Location has a many-to-many relationship with Hashtag.
    Also has a one-to-many relationship with Tweet (one Location to many Tweets).
    """
	
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))

    hashtags = relationship("Hashtag", secondary=hashtag_location_table, backref="city")

    def __init__(self, city, state, country, tweet, hashtag):
        self.city = city
        self.state = state
        self.country = country

    def __repr__(self):
        return '<City %d>' % self.id




