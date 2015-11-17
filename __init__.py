from flask import Flask
import json
import os
from models import Tweet, Hashtag, Location, db
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'idb.db') +
                               '?check_same_thread=False')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

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

@app.route("/api/tweets/<int:id>/")
def tweet(id):
    data = db.session.query(Tweet).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweets/<int:id>/<string:resource>/")
def tweet_subresources(id, resource):
    tweet = db.session.query(Tweet).filter_by(id=id).first()
    raw_data = getattr(tweet, resource)
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

@app.route("/api/hashtags/<int:id>/")
def hashtag(id):
    data = db.session.query(Hashtag).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtags/<int:id>/<string:resource>/")
def hashtag_subresources(id, resource):
    hashtag = db.session.query(Hashtag).filter_by(id=id).first()
    raw_data = getattr(hashtag, resource)
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        if ('date_time' in data):
            data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
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

@app.route("/api/locations/<int:id>/")
def location(id):
    data = db.session.query(Location).filter_by(id=id).first()
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


@app.route("/api/locations/<int:id>/<string:resource>/")
def location_subresources(id, resource):
    location = db.session.query(Location).filter_by(id=id).first()
    raw_data = getattr(location, resource)
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        if ('date_time' in data):
            data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

# Funnel all other requests to angular
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
