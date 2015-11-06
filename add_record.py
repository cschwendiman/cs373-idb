from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Tweet, Hashtag, Location, db

import time
from time import mktime
from datetime import datetime
import json
from sqlalchemy import exists

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

cities = [Location("Austin", "Texas", "United States"), Location("San Francisco", "California", "United States"), Location("New York City", "New York", "United States")]
for index in range(len(cities)):
    db.session.add(cities[index])

hashed = []

for index, path in enumerate(["../cs373-tweetCity/new_AUX.json", "../cs373-tweetCity/new_SF.json", "../cs373-tweetCity/new_NYC.json"]):
    tweets = json.load(open(path))
    for tweet_id, info in tweets.items():
        data = Tweet(tweet_id, info["text"], info["name"], "https://twitter.com/statuses/"+tweet_id,\
        datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
        info["geo"]["coordinates"][0], info["geo"]["coordinates"][1], index+1)
        data.location = cities[index]
        db.session.add(data)
        cur_tweet = data    

        for hashy in info["hashtags"]:
            if hashy not in hashed:
                hashed.append(hashy)
                data = Hashtag(hashy, "https://twitter.com/hashtag/"+hashy)
                data.tweets.append(cur_tweet)
                db.session.add(data)
                cities[index].hashtags.append(data)

db.session.commit()