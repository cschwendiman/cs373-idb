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

# db.session.query(Tweet).delete()
# db.session.query(Hashtag).delete()
# db.session.query(Location).delete()

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

hashed = {}
cities = {}
tweet_ids = {}

json_list = []
for stuff in os.listdir("../cs373-tweetCity/"):
    if stuff.endswith(".json") and stuff.startswith("new"):
        json_list.append("../cs373-tweetCity/"+stuff)

for path in json_list:
    tweets = json.load(open(path))

    for tweet_id, info in tweets.items():
        if tweet_id not in tweet_ids:
            tweet_ids[tweet_id] = tweet_id
            
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

            if city not in cities:
                cities[city] = Location(city, state, country)
                db.session.add(cities[city])

            data = Tweet(tweet_id, info["text"], info["name"], "https://twitter.com/statuses/"+tweet_id,\
            datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
            info["geo"]["coordinates"][1], info["geo"]["coordinates"][0], info["location_id"])

            cities[city].tweets.append(data)
            db.session.add(data)
            cur_tweet = data    

            for hashy in info["hashtags"]:
                if hashy not in hashed:
                    data = Hashtag(hashy, "https://twitter.com/hashtag/"+hashy)
                    hashed[hashy] = data
                    db.session.add(data)
                if hashed[hashy] not in cities[city].hashtags:
                    cities[city].hashtags.append(hashed[hashy])
                hashed[hashy].tweets.append(cur_tweet)
db.session.commit()