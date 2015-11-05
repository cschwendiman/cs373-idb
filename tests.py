from unittest import main, TestCase
import time
from time import mktime
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, LargeBinary, Boolean

import threading
from flask import Flask, render_template, url_for, g, request, session, redirect, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy

from models import *
#from __init__ import unittests
#unittests()

class testModels(TestCase):

    #setup the database
    def setUp(self):
        db.configure_mappers()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #-------------
    # Tweets_model
    #-------------

    def test_tweets_writability(self):
        tweets = Tweet.query.all()
        startSize = len(tweets)

        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5))
        db.session.commit()
        tweets = Tweet.query.all()

        endSize = len(tweets)

        self.assertEqual(startSize + 1, endSize)

    def test_tweets_readability(self):
        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5))
        db.session.commit()

        query = Tweet.query.all()
        found = False

        for x in query:
            if(x.text == "test"):
                found = True

        assert(found)

    def test_tweets_attribute_readability(self):
        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5))
        db.session.commit()

        query = db.session.query(Tweet).first()

        assert (query is not None)
        assert (query.twitter_tweet_id == "123")
        assert (query.text == "test")
        assert (query.user == "testUser")
        assert (query.url == "https://twitter.com/testUser/status/661196539696513024")
        assert (query.date_time == datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015"))))
        assert (query.longitude == 30.30)
        assert (query.latitude == -127.27)
        assert (query.location_id == 5)

    def test_tweets_delete_ability(self):
        db.session.add(Tweet("123", "test", "deleteMe", "https://twitter.com/testUser/status/661196539696513024", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5))
        db.session.commit()

        query = db.session.query(Tweet).filter(Tweet.user == "deleteMe").first()

        assert(query != None)

        db.session.delete(query)
        db.session.commit()

        toRemove = db.session.query(Tweet).filter(Tweet.user == "deleteMe").first()
        assert(toRemove == None)


    #---------------
    # Hashtags_model
    #---------------

    def test_hashtags_writability(self):
        hashtags = Hashtag.query.all()
        startSize = len(hashtags)

        db.session.add(Hashtag(text = "test", url = "www.foo.com"))
        db.session.commit()
        hashtags = Hashtag.query.all()

        endSize = len(hashtags)

        self.assertEqual(startSize + 1, endSize)

    def test_hashtags_readability(self):
        db.session.add(Hashtag(text = "test", url = "www.foo.com"))
        db.session.commit()

        hashtags = Hashtag.query.all()
        found = False

        for x in hashtags:
            if(x.text == "test"):
                found = True

        assert(found)

    def test_hashtags_attribute_readability(self):
        db.session.add(Hashtag(text = "test123", url = "www.foo.com"))
        db.session.commit()

        query = db.session.query(Hashtag).filter(Hashtag.text == "test123").first()

        assert (query is not None)
        assert (query.url == "www.foo.com")


    def test_hashtags_delete_ability(self):
        db.session.add(Hashtag(text = "test123", url = "www.deleteme.com"))
        db.session.commit()

        query = db.session.query(Hashtag).filter(Hashtag.url == "www.deleteme.com").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(Hashtag).filter(Hashtag.url == "www.deleteme.com").first()
        assert(toRemove == None)

    #----------------
    # Locations_model
    #----------------
    
    def test_locations_writability(self):
        locations = Location.query.all()
        startSize = len(locations)

        db.session.add(Location(city = "Austin", state = "TX", country = "USA" ))
        db.session.commit()
        locations = Location.query.all()

        endSize = len(locations)

        self.assertEqual(startSize + 1, endSize)

    def test_locations_readability(self):
        db.session.add(Location(city = "Austin", state = "TX", country = "USA"))
        db.session.commit()

        locations = Location.query.all()
        found = False

        for x in locations:
            if(x.city == "Austin"):
                found = True

        assert(found)

    def test_locations_attribute_readability(self):
        db.session.add(Location(city = "Austin", state = "TX", country = "USA"))
        db.session.commit()

        query = db.session.query(Location).filter(Location.city == "Austin").first()

        assert (query is not None)
        assert (query.state == "TX")
        assert (query.country == "USA")

    def test_locations_delete_ability(self):
        db.session.add(Location(city = "Austin", state = "TX", country = "USA"))
        db.session.commit()

        query = db.session.query(Location).filter(Location.city == "Austin").first()

        assert(query != None)

        db.session.delete(query)
        db.session.commit()

        toRemove = db.session.query(Location).filter(Location.city == "Austin").first()
        assert(toRemove == None)

if __name__ == "__main__":
    main()