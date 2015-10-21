from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLAlchemy(app)

"""
Tweets:
    Text
    Username
    City ID
    URL
    Longitude
    Latitude

Hashtags:
    Hashtag
    URL

Location:
    City
    State
    Country
"""

class Tweet(db.Model):
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True)
    # Check length of this field
    text = db.Column(db.String(140))
    username = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(80), unique=True)
    # Check if float is ok
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    #city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    #city = db.relationship('City', backref=db.backref('tweets', lazy='dynamic'))
    city = db.relationship("City", uselist=False, backref="tweet") # one-to-one with city
    city_id = Column(Integer, ForeignKey('city.id'))

    hashtag = db.relationship("Hashtag") # one to many with Hashtag
    hashtag_id = Column(Integer, ForeignKey('hashtag.id'))


    def __init__(self, text, username, url, longitude, latitude, city, hashtag):
        self.text = text
        self.username = username
        self.url = url
        self.longitude = longitude
        self.latitude = latitude
        self.city = city
        self.hashtag = hashtag

    def __repr__(self):
        return '<Tweet %d>' % self.id

class Hashtag(db.Model):
    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(140), unique=True)
    url = db.Column(db.String(80), unique=True)

    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = db.relationship("Tweet") # one to many with tweet

    city_id = Column(Integer, ForeignKey('city.id'))
    city = db.relationship("City")

    def __init__(self, hashtag, url, tweet, city):
        self.hashtag = hashtag
        self.url = url
        self.tweet = tweet
        self.city = city

    def __repr__(self):
        return '<Hashtag %d>' % self.id


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))

    tweet_id = db.Column(Integer, ForeignKey('tweet.id'))
    tweet = db.relationship("Tweet") # one to many with Tweet

    hashtag_id = Column(Integer, ForeignKey('hashtag.id'))
    hashtag = db.relationship("Hashtag") # one to many with Hashtag

    def __init__(self, city, state, country, tweet, hashtag):
        self.city = city
        self.state = state
        self.country = country
        self.tweet = tweet
        self.hashtag = hashtag

    def __repr__(self):
        return '<City %d>' % self.id




