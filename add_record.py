from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Tweet

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idb.db'
db = SQLAlchemy(app)

# data = Tweet(2, "9527", "some text", "random guy", "www.tweetcity.me2", 30.30, -127.27, 5)
# db.session.add(data)
# db.session.commit()


db.session.query(Tweet).delete()
db.session.commit()