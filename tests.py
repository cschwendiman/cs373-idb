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

import requests

from models import *


# from __init__ import unittests
# unittests()

class testModels(TestCase):
    # setup the database
    def setUp(self):
        app = Flask("tests", static_url_path='/static')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_idb.db'
        db.init_app(app)
        db.app = app
        db.configure_mappers()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # -------------
    # Tweets_model
    # -------------

    def test_tweets_writability(self):
        tweets = Tweet.query.all()
        startSize = len(tweets)

        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                             datetime.fromtimestamp(
                                 mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                             -127.27, 5))
        db.session.commit()
        tweets = Tweet.query.all()

        endSize = len(tweets)

        self.assertEqual(startSize + 1, endSize)

    def test_tweets_readability(self):
        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                             datetime.fromtimestamp(
                                 mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                             -127.27, 5))
        db.session.commit()

        query = Tweet.query.all()
        found = False

        for x in query:
            if (x.text == "test"):
                found = True

        assert (found)

    def test_tweets_attribute_readability(self):
        db.session.add(Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                             datetime.fromtimestamp(
                                 mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                             -127.27, 5))
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
        assert (query.city_id == 5)

    def test_tweets_delete_ability(self):
        db.session.add(Tweet("123", "test", "deleteMe", "https://twitter.com/testUser/status/661196539696513024",
                             datetime.fromtimestamp(
                                 mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                             -127.27, 5))
        db.session.commit()

        query = db.session.query(Tweet).filter(Tweet.user == "deleteMe").first()

        assert (query != None)

        db.session.delete(query)
        db.session.commit()

        toRemove = db.session.query(Tweet).filter(Tweet.user == "deleteMe").first()
        assert (toRemove == None)

    # ---------------
    # Hashtags_model
    # ---------------

    def test_hashtags_writability(self):
        hashtags = Hashtag.query.all()
        startSize = len(hashtags)

        db.session.add(Hashtag(text="test", url="www.foo.com"))
        db.session.commit()
        hashtags = Hashtag.query.all()

        endSize = len(hashtags)

        self.assertEqual(startSize + 1, endSize)

    def test_hashtags_readability(self):
        db.session.add(Hashtag(text="test", url="www.foo.com"))
        db.session.commit()

        hashtags = Hashtag.query.all()
        found = False

        for x in hashtags:
            if (x.text == "test"):
                found = True

        assert (found)

    def test_hashtags_attribute_readability(self):
        db.session.add(Hashtag(text="test123", url="www.foo.com"))
        db.session.commit()

        query = db.session.query(Hashtag).filter(Hashtag.text == "test123").first()

        assert (query is not None)
        assert (query.url == "www.foo.com")

    def test_hashtags_delete_ability(self):
        db.session.add(Hashtag(text="test123", url="www.deleteme.com"))
        db.session.commit()

        query = db.session.query(Hashtag).filter(Hashtag.url == "www.deleteme.com").first()

        assert (query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(Hashtag).filter(Hashtag.url == "www.deleteme.com").first()
        assert (toRemove == None)

    # ----------------
    # Locations_model
    # ----------------

    def test_locations_writability(self):
        locations = Location.query.all()
        startSize = len(locations)

        db.session.add(Location(city="Austin", state="TX", country="USA"))
        db.session.commit()
        locations = Location.query.all()

        endSize = len(locations)

        self.assertEqual(startSize + 1, endSize)

    def test_locations_readability(self):
        db.session.add(Location(city="Austin", state="TX", country="USA"))
        db.session.commit()

        locations = Location.query.all()
        found = False

        for x in locations:
            if (x.city == "Austin"):
                found = True

        assert (found)

    def test_locations_attribute_readability(self):
        db.session.add(Location(city="Austin", state="TX", country="USA"))
        db.session.commit()

        query = db.session.query(Location).filter(Location.city == "Austin").first()

        assert (query is not None)
        assert (query.state == "TX")
        assert (query.country == "USA")

    def test_locations_delete_ability(self):
        db.session.add(Location(city="Austin", state="TX", country="USA"))
        db.session.commit()

        query = db.session.query(Location).filter(Location.city == "Austin").first()

        assert (query != None)

        db.session.delete(query)
        db.session.commit()

        toRemove = db.session.query(Location).filter(Location.city == "Austin").first()
        assert (toRemove == None)

    # --------------------
    # hashtag_tweet_table
    # --------------------

    def test_hashtag_tweet_writability(self):
        tweets = Tweet.query.all()
        hashtags = Hashtag.query.all()

        numTweets = len(tweets)
        numHashtags = len(hashtags)

        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, 5)
        new_hashtag = Hashtag(text="test", url="www.foo.com")

        new_hashtag.tweets.append(new_tweet)

        db.session.add(new_hashtag)
        db.session.commit()

        assert (db.session.query(Tweet).filter_by(
            url="https://twitter.com/testUser/status/661196539696513024").first().hashtags[0] == new_hashtag)
        assert (len(db.session.query(Tweet).filter_by(
            url="https://twitter.com/testUser/status/661196539696513024").first().hashtags) == numHashtags + 1)
        assert (db.session.query(Hashtag).filter_by(url="www.foo.com").first().tweets[0] == new_tweet)
        assert (len(db.session.query(Hashtag).filter_by(url="www.foo.com").first().tweets) == numTweets + 1)

        tweets = Tweet.query.all()
        hashtags = Hashtag.query.all()

        assert (len(tweets) == numTweets + 1)
        assert (len(hashtags) == numHashtags + 1)

    def test_hashtag_tweet_readability(self):
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, 5)
        new_hashtag = Hashtag(text="test", url="www.foo.com")
        new_hashtag.tweets.append(new_tweet)

        db.session.add(new_hashtag)
        db.session.commit()

        found = False

        hashtag_tweets = db.session.query(Hashtag).filter_by(url="www.foo.com").first().tweets

        for x in hashtag_tweets:
            if (x.id == new_tweet.id):
                found = True

        assert (found)

        found = False

        tweet_hashtags = db.session.query(Tweet).filter_by(
            url="https://twitter.com/testUser/status/661196539696513024").first().hashtags

        hashtags = Hashtag.query.all()
        tweets = Tweet.query.all()

        for x in tweet_hashtags:
            if (x.id == new_hashtag.id):
                found = True
                assert (hashtags[0].text == "test")
                assert (hashtags[0].url == "www.foo.com")
                assert (tweets[0].text == "test")
                assert (tweets[0].user == "testUser")
                assert (tweets[0].url == "https://twitter.com/testUser/status/661196539696513024")
                assert (tweets[0].longitude == 30.30)
                assert (tweets[0].latitude == -127.27)

        assert (found)

    def test_hashtag_tweet_delete_ability(self):
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, 5)
        new_hashtag = Hashtag(text="test", url="www.foo.com")
        new_hashtag.tweets.append(new_tweet)

        db.session.add(new_hashtag)
        db.session.commit()

        hashtags = Hashtag.query.all()
        tweets = Tweet.query.all()

        assert (len(tweets) == 1)
        assert (len(hashtags) == 1)

        db.session.delete(tweets[0])
        db.session.commit()

        hashtags = Hashtag.query.all()
        tweets = Location.query.all()
        assert (len(tweets) == 0)
        assert (len(hashtags) == 1)

        db.session.delete(hashtags[0])
        db.session.commit()

        hashtags = Hashtag.query.all()
        assert (len(hashtags) == 0)

        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, 5)
        new_hashtag = Hashtag(text="test", url="www.foo.com")
        new_hashtag.tweets.append(new_tweet)

        db.session.add(new_hashtag)
        db.session.commit()

        hashtags = Hashtag.query.all()

        db.session.delete(hashtags[0])
        db.session.commit()

        hashtags = Hashtag.query.all()
        tweets = Tweet.query.all()

        assert (len(tweets) == 1)
        assert (len(hashtags) == 0)

    # ----------------------
    # hashtag_location_table
    # ----------------------

    def test_hashtag_location_writability(self):
        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        numHashtags = len(hashtags)
        numLocations = len(locations)
        new_hashtag = Hashtag(text="thisisatest", url="www.foo.com")
        new_location = Location(city="Austin", state="TX", country="USA")

        assert (len(new_location.hashtags) == 0)

        new_location.hashtags.append(new_hashtag)

        assert (len(new_location.hashtags) == 1)

        db.session.add(new_location)

        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        assert (len(hashtags) == numHashtags + 1)
        assert (len(locations) == numLocations + 1)
        assert (hashtags[0] == new_hashtag)
        assert (locations[0] == new_location)
        assert (hashtags[0].cities[0] == new_location)
        assert (locations[0].hashtags[0] == new_hashtag)

    def test_hashtag_location_readability(self):
        new_hashtag = Hashtag(text="thisisatest", url="www.foo.com")
        new_location = Location(city="Austin", state="TX", country="USA")
        new_location.hashtags.append(new_hashtag)
        db.session.add(new_location)

        hashtags = Hashtag.query.all()
        locations = Location.query.all()

        assert (hashtags[0].text == "thisisatest")
        assert (hashtags[0].url == "www.foo.com")
        assert (locations[0].city == "Austin")
        assert (locations[0].state == "TX")
        assert (locations[0].country == "USA")

    def test_hashtag_location_delete_ability(self):
        new_hashtag = Hashtag(text="thisisatest", url="www.foo.com")
        new_location = Location(city="Austin", state="TX", country="USA")
        new_location.hashtags.append(new_hashtag)
        db.session.add(new_location)

        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        assert (len(locations) == 1)
        assert (len(hashtags) == 1)

        db.session.delete(locations[0])

        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        assert (len(locations) == 0)
        assert (len(hashtags) == 1)

        db.session.delete(hashtags[0])

        hashtags = Hashtag.query.all()
        assert (len(hashtags) == 0)

        new_hashtag = Hashtag(text="thisisatest", url="www.foo.com")
        new_location = Location(city="Austin", state="TX", country="USA")
        new_location.hashtags.append(new_hashtag)
        db.session.add(new_location)

        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        db.session.delete(hashtags[0])

        hashtags = Hashtag.query.all()
        locations = Location.query.all()
        assert (len(locations) == 1)
        assert (len(hashtags) == 0)

    # ----------------------------
    # tweet_location (one-to-many)
    # ----------------------------

    def test_tweet_location_writability(self):
        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        numTweets = len(tweets)
        numLocations = len(locations)

        new_location = Location(city="Austin", state="TX", country="USA")
        db.session.add(new_location)
        new_location = list(db.session.query(Location))[0]
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, new_location.id)

        assert (new_tweet.city == None)
        assert (len(list(new_location.tweets)) == 0)

        new_location.tweets.append(new_tweet)

        assert (new_tweet.city == new_location)
        assert (len(list(new_location.tweets)) == 1)

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        assert (len(tweets) == numTweets + 1)
        assert (len(locations) == numLocations + 1)
        assert (tweets[0] == new_tweet)
        assert (locations[0] == new_location)
        assert (tweets[0].city == new_location)
        assert (locations[0].tweets[0] == new_tweet)

    def test_tweet_location_readability(self):
        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        numTweets = len(tweets)
        numLocations = len(locations)

        new_location = Location(city="Austin", state="TX", country="USA")
        db.session.add(new_location)
        new_location = list(db.session.query(Location))[0]
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, new_location.id)

        new_location.tweets.append(new_tweet)

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))

        assert (tweets[0].twitter_tweet_id == "123")
        assert (tweets[0].text == "test")
        assert (tweets[0].user == "testUser")
        assert (tweets[0].url == "https://twitter.com/testUser/status/661196539696513024")
        assert (tweets[0].longitude == 30.30)
        assert (tweets[0].latitude == -127.27)
        assert (tweets[0].city_id == new_location.id)
        assert (locations[0].city == "Austin")
        assert (locations[0].state == "TX")
        assert (locations[0].country == "USA")

    def test_tweet_location_delete_ability(self):
        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        numTweets = len(tweets)
        numLocations = len(locations)

        new_location = Location(city="Austin", state="TX", country="USA")
        db.session.add(new_location)
        new_location = list(db.session.query(Location))[0]
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, new_location.id)

        new_location.tweets.append(new_tweet)

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))

        assert (len(tweets) == 1)
        assert (len(locations) == 1)

        db.session.delete(locations[0])

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        assert (len(locations) == 0)
        assert (len(tweets) == 1)

        db.session.delete(tweets[0])

        tweets = list(db.session.query(Tweet))
        assert (len(tweets) == 0)

        new_location = Location(city="Austin", state="TX", country="USA")
        db.session.add(new_location)
        new_location = list(db.session.query(Location))[0]
        new_tweet = Tweet("123", "test", "testUser", "https://twitter.com/testUser/status/661196539696513024",
                          datetime.fromtimestamp(
                              mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))), 30.30,
                          -127.27, new_location.id)

        new_location.tweets.append(new_tweet)

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))

        assert (len(tweets) == 1)
        assert (len(locations) == 1)

        db.session.delete(tweets[0])

        tweets = list(db.session.query(Tweet))
        locations = list(db.session.query(Location))
        assert (len(locations) == 1)
        assert (len(tweets) == 0)

        db.session.delete(locations[0])

        locations = list(db.session.query(Location))
        assert (len(locations) == 0)


    # ---------
    # API Tests
    # ---------

    def test_tweet_api_1(self):
        data = requests.get("http://tweetcity.me/api/tweets")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) > 0)
        assert(data[0]["city_id"] == 1)
        assert(data[0]["date_time"] == "2015-11-02 18:59:53")
        assert(data[0]["id"] == 1)
        assert(data[0]["text"] == "Want to work in #Austin, TX? View our latest opening: https://t.co/sibbQPMdP8 #Banking #Job #Jobs #Hiring")

        assert(data[4]["city_id"] == 1)
        assert(data[4]["date_time"] == "2015-11-02 21:58:54")
        assert(data[4]["id"] == 5)
        assert(data[4]["text"] == "See our latest #CedarPark, TX #job and click to apply: Branch Service Leader (Cedar Park) - https://t.co/aOzw2o6kSK #regions #regionsbank")

    def test_tweet_api_2(self):
        data = requests.get("http://tweetcity.me/api/tweets/5")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) == 9)
        assert(data["city_id"] == 1)
        assert(data["date_time"] == "2015-11-02 21:58:54")
        assert(data["id"] == 5)
        assert(data["text"] == "See our latest #CedarPark, TX #job and click to apply: Branch Service Leader (Cedar Park) - https://t.co/aOzw2o6kSK #regions #regionsbank")

    def test_hashtags_api_1(self):
        data = requests.get("http://tweetcity.me/api/hashtags")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) > 0)
        assert(data[0]["id"] == 1)
        assert(data[0]["text"] == "Austin")
        assert(data[0]["url"] == "https://twitter.com/hashtag/Austin")

        assert(data[4]["id"] == 5)
        assert(data[4]["text"] == "Hiring")
        assert(data[4]["url"] == "https://twitter.com/hashtag/Hiring")

    def test_hashtags_api_2(self):
        data = requests.get("http://tweetcity.me/api/hashtags/5")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) == 3)
        assert(data["id"] == 5)
        assert(data["text"] == "Hiring")
        assert(data["url"] == "https://twitter.com/hashtag/Hiring")

    def test_locations_api_1(self):
        data = requests.get("http://tweetcity.me/api/locations")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) == 3)
        assert(data[0]["id"] == 1)
        assert(data[0]["city"] == "Austin")
        assert(data[0]["state"] == "Texas")
        assert(data[0]["country"] == "United States")

        assert(data[1]["id"] == 2)
        assert(data[1]["city"] == "San Francisco")
        assert(data[1]["state"] == "California")
        assert(data[1]["country"] == "United States")

        assert(data[2]["id"] == 3)
        assert(data[2]["city"] == "New York City")
        assert(data[2]["state"] == "New York")
        assert(data[2]["country"] == "United States")

    def test_locations_api_2(self):
        data = requests.get("http://tweetcity.me/api/locations/2")
        assert(data.status_code == 200)
        data = data.json()
        assert(len(data) == 4)
        assert(data["id"] == 2)
        assert(data["city"] == "San Francisco")
        assert(data["state"] == "California")
        assert(data["country"] == "United States")

if __name__ == "__main__":
    main()
