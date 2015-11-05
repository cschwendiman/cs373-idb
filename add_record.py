from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

import time
from time import mktime
from datetime import datetime
import json

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://../idb.db'
db = SQLAlchemy(app)

db.session.query(Tweet).delete()
db.session.commit()

tweets = json.load(open("/home/ka/Desktop/cs373-idb/data_scraper/new_AUX.json"))
for tweet, info in tweets.items():
    data = Tweet(tweet, info["text"], info["name"], "http://twitter.com/statuses/"+tweet,\
    datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
    info["geo"]["coordinates"][0], info["geo"]["coordinates"][1], info["location_id"])
    db.session.add(data)

    for hashy in info["hashtags"]:
        data = Hashtag(hashy, "http://twitter.com/statuses/"+tweet)
        db.session.add(data)

db.session.commit()
print(db.session.query(Tweet).all())

# data = Tweet("9527", "some text", "random guy", "www.tweetcity.abc", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5)
# db.session.add(data)
# db.session.commit()
# print(db.session.query(Tweet).first().id)

# db.session.query(Tweet).delete()
# db.session.commit()