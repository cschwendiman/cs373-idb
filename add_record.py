from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Tweet, Hashtag, Location

import time
from time import mktime
from datetime import datetime
import json

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idb.db'
db = SQLAlchemy(app)

db.drop_all()
db.configure_mappers()
db.create_all()

# db.session.query(Tweet).delete()
# db.session.commit()

# for many to many adding
# Senpai notice me!
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship

tweets = json.load(open("/home/ka/Desktop/cs373-tweetCity/new_AUX.json"))
for tweet_id, info in tweets.items():
    data = Tweet(tweet_id, info["text"], info["name"], "http://twitter.com/statuses/"+tweet_id,\
    datetime.fromtimestamp(mktime(time.strptime(info["datetime"].replace("+0000", ""), "%a %b %d %H:%M:%S %Y"))), \
    info["geo"]["coordinates"][0], info["geo"]["coordinates"][1], info["location_id"])
    db.session.add(data)

#     db.session.add
#     # for hashy in info["hashtags"]:
#     #     if 
#     #     data = Hashtag(hashy, "http://twitter.com/statuses/"+tweet)
#     #     db.session.add(data)

# db.session.commit()
# print(db.session.query(Tweet).all())

# data = Tweet("9527", "some text", "random guy", "www.tweetcity.abc", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5)
# db.session.add(data)
# db.session.commit()
# print(db.session.query(Tweet).first().id)

# db.session.query(Tweet).delete()
# db.session.commit()