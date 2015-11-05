from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'idb.db') +
                               '?check_same_thread=False')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# API Requests
@app.route("/api/tweets/")
def tweets():
    return app.send_static_file('json/tweets.json')

@app.route("/api/tweet/<int:id>/")
def tweet(id):
    tweets = json.load(open("json/tweets.json"))
    tweet = tweets[str(id)]
    return json.dumps(tweet, ensure_ascii=False)

@app.route("/api/hashtags/")
def hashtags():
    return app.send_static_file('json/hashtags.json')

@app.route("/api/hashtag/<int:id>/")
def hashtag(id):
    tweets = json.load(open("json/hashtag.json"))
    tweet = tweets[str(id)]
    return json.dumps(tweet, ensure_ascii=False)

@app.route("/api/locations/")
def locations():
    return app.send_static_file('json/locations.json')

@app.route("/api/location/<int:id>/")
def location(id):
    tweets = json.load(open("json/location.json"))
    tweet = tweets[str(id)]
    return json.dumps(tweet, ensure_ascii=False)


# Funnel all other requests to angular
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
