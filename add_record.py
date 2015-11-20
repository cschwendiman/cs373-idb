from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Tweet, Hashtag, Location, db

import time
from time import mktime
from datetime import datetime
import json
from sqlalchemy import exists

import os
import re, string

# setting up tables and models
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idb.db'
db.init_app(app)
db.app = app
db.configure_mappers()
db.create_all()

# for many to many adding
# Senpai notice me!
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship

# cache the processed data to avoid collision
hashed = {}
cities = {}
tweet_ids = {}

# scan throught our private repo searching for data
json_list = []
for stuff in os.listdir("../cs373-tweetCity/"):
    if stuff.endswith(".json") and stuff.startswith("new"):
        json_list.append("../cs373-tweetCity/"+stuff)

for path in json_list:
    tweets = json.load(open(path))

# grab one tweet at a time
    for tweet_id, info in tweets.items():
        if tweet_id not in tweet_ids:
            tweet_ids[tweet_id] = tweet_id
            
            # first process the place info, sanitize weird user input and null input
            info["place"] = re.sub('[\s+]', '', info["place"])
            locale = info["place"].split(",")
            city, state, country = "Not applicable", "Not applicable", "United States"
            if len(locale) < 2:
                city = locale[0]
                if "TKY" in path:
                    country = "Japan"
            else:
                if "TKY" in path:
                    city = locale[1]
                    country = "Japan"
                elif locale[1] == "USA":
                    state = locale[0]
                else:
                    city, state = locale[0], locale[1]

            # first, put in location object in db
            if city not in cities:
                cities[city] = Location(city, state, country)
                db.session.add(cities[city])

            # second, put tweet object in db
            data = Tweet(tweet_id, info["text"], info["name"], "https://twitter.com/statuses/"+tweet_id,\
            datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
            info["geo"]["coordinates"][1], info["geo"]["coordinates"][0], info["location_id"])

            # third, link location with tweet
            cities[city].tweets.append(data)
            db.session.add(data)
            cur_tweet = data    

            # forth, put hashtag object in db
            # link location with hastag
            # link hastag with tweet
            for hashy in info["hashtags"]:
                if hashy not in hashed:
                    data = Hashtag(hashy, "https://twitter.com/hashtag/"+hashy)
                    hashed[hashy] = data
                    db.session.add(data)
                if hashed[hashy] not in cities[city].hashtags:
                    cities[city].hashtags.append(hashed[hashy])
                hashed[hashy].tweets.append(cur_tweet)
db.session.commit()