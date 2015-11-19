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

# cities = [Location("Austin", "Texas", "United States"), Location("San Francisco", "California", "United States"), Location("New York City", "New York", "United States"), Location("Tokyo", "Kanto", "Japan")]
# for index in range(len(cities)):
#     if Location.query.filter_by(city=cities[index].city).first() is None:
#         db.session.add(cities[index])

hashed = {}
cities = {}

json_list = []
for stuff in os.listdir("../cs373-tweetCity/"):
    if stuff.endswith(".json"):
        json_list.append("../cs373-tweetCity/"+stuff)

for index, path in enumerate(json_list):
    tweets = json.load(open(path))
    for tweet_id, info in tweets.items():
        if Tweet.query.filter_by(twitter_tweet_id=tweet_id).first() is None and info["geo"] is not None:
            data = Tweet(tweet_id, info["text"], info["name"], "https://twitter.com/statuses/"+tweet_id,\
            datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
            info["geo"]["coordinates"][1], info["geo"]["coordinates"][0], index+1)
            city, state = info["place"].split(",")
            pattern = re.compile('[\W_]+')
            city = pattern.sub(city, string.ascii_letters)
            state = pattern.sub(state, string.ascii_letters)

            cities[city] = Location(city, state, "United States")
            if Location.query.filter_by(city=city).first() is None:
                db.session.add(cities[city])
            data.location = cities[city]
            db.session.add(data)
            cur_tweet = data    

            for hashy in info["hashtags"]:
                if hashy not in hashed:
                    data = Hashtag(hashy, "https://twitter.com/hashtag/"+hashy)
                    hashed[hashy] = data
                    cities[city].hashtags.append(data)
                    db.session.add(data)
                else:
                    data = hashed[hashy]
                    if data not in cities[city].hashtags:
                        cities[city].hashtags.append(data)
                data.tweets.append(cur_tweet)
                
db.session.commit()