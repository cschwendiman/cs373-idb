from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

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

class Tweet(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # Check length of this field
    text = db.Column(db.String(140))
    username = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(80), unique=True)
    # Check if float is ok
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City', backref=db.backref('tweets', lazy='dynamic'))

    def __init__(self, text, username, url, longitude, latitude, city):
        self.text = text
        self.username = username
        self.url = urk
        self.longitude = longitude
        self.latitude = latitude
        self.city = city

    def __repr__(self):
        return '<Tweet %d>' % self.id

class Hashtag(db.model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(140), unique=True)
    url = db.Column(db.String(80), unique=True)

class City(db.model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.column(db.String(80))
    state = db.column(db.String(80))
    country = db.column(db.String(80)


