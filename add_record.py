from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Tweet
import time
from time import mktime
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idb.db'
db = SQLAlchemy(app)

data = Tweet("9527", "some text", "random guy", "www.tweetcity.abc", datetime.fromtimestamp(mktime(time.strptime("Mon Nov 02 15:01:54 2015", "%a %b %d %H:%M:%S %Y"))) ,30.30, -127.27, 5)
db.session.add(data)
db.session.commit()
print(db.session.query(Tweet).first().id)

db.session.query(Tweet).delete()
db.session.commit()