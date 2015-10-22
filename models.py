from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLAlchemy(app)

"""
Tweet:
    text
    user
    URL
    longitude
    latitude

Hashtag:
    text
    URL

Location:
    city
    state
    country
"""

hashtag_tweet_table = db.Table('hashtag_tweet',
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.d'))
)

hashtag_location_table = db.Table('hashtag_location',
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
)

class Tweet(db.Model):
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True)
    # Check length of this field
    text = db.Column(db.String(140))
    user = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(80), unique=True)
	date_time = db.Column(db.DateTime)
    # Check if float is ok
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
	
	location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
	location = relationship("Location", backref="tweets")

    def __init__(self, text, user, url, date_time, longitude, latitude):
        self.text = text
        self.user = user
        self.url = url
        self.date_time = date_time
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Tweet %d>' % self.id

class Hashtag(db.Model):
    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(140), unique=True)
    url = db.Column(db.String(80), unique=True)

    tweets = relationship("Tweet", secondary=hashtag_tweet_table)

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __repr__(self):
        return '<Hashtag %d>' % self.id


class Location(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))

    hashtags = relationship("Hashtag", secondary=hashtag_location_table)

    def __init__(self, city, state, country, tweet, hashtag):
        self.city = city
        self.state = state
        self.country = country

    def __repr__(self):
        return '<City %d>' % self.id




