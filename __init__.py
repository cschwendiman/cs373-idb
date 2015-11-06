from flask import Flask
import json
import os
from models import Tweet, Hashtag, Location, db
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idb.db'

db.init_app(app)
db.app = app

# API Requests
@app.route("/api/tweets/")
def tweets():
    raw_data = db.session.query(Tweet).all()
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweet/<int:id>/")
def tweet(id):
    data = db.session.query(Tweet).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtagsByTweet/<int:id>/")
def hashtagsByTweet(id):
    raw_data = db.session.query(Tweet).filter_by(id=id).first().hashtags
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtags/")
def hashtags():
    raw_data = db.session.query(Hashtag).all()
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtag/<int:id>/")
def hashtag(id):
    data = db.session.query(Hashtag).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/locationsByHashtag/<int:id>/")
def locationsByHashtag(id):
    raw_data = db.session.query(Hashtag).filter_by(id=id).first().cities
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweetsByHashtag/<int:id>/")
def tweetsByHashtag(id):
    raw_data = db.session.query(Hashtag).filter_by(id=id).first().tweets
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweetsByCity/<int:id>/")
def tweetsByCity(id):
    raw_data = db.session.query(Location).filter_by(id=id).first().tweets
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtagsByCity/<int:id>/")
def hashtagsByCity(id):
    raw_data = db.session.query(Location).filter_by(id=id).first().hashtags
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/locations/")
def locations():
    raw_data = db.session.query(Location).all()
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


@app.route("/api/location/<int:id>/")
def location(id):
    data = db.session.query(Location).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

# Funnel all other requests to angular
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
