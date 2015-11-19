from flask import Flask
import json
import os
from models import Tweet, Hashtag, Location, db
from flask import jsonify
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'idb.db') +
                               '?check_same_thread=False')
    app.debug = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)
db.app = app

# API Requests
@app.route("/api/tweets/")
@app.route("/api/tweets/pages/<int:page>/")
def tweets(page=1):
    raw_data = Tweet.query.paginate(page, 50, False).items
    json_data = raw_to_json(raw_data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweets/<int:id>/")
def tweet(id):
    data = db.session.query(Tweet).get(id)
    data = data.__dict__
    del data['_sa_instance_state']
    data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweets/<int:id>/<string:resource>/")
def tweet_subresources(id, resource):
    tweet = db.session.query(Tweet).get(id)
    raw_data = getattr(tweet, resource)
    json_data = raw_to_json(raw_data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/tweets/search/<string:search_query>/")
def search_tweets(search_query):
    result = {}
    json_data = raw_to_json(Tweet.search(search_query.replace("&", " ").split())[0])
    result[search_query] = json_data
    json_data = raw_to_json(Tweet.search(search_query.replace("&", " ").split())[1])
    result[search_query+"_or"] = json_data
    return jsonify(result)

@app.route("/api/anime/search/<string:search_query>/")
def search_anime_tweet(search_query):
    import requests
    anime_json = requests.get("http://animedb.me/search/"+search_query).json()["searchResults"]
    result = {}
    for anime in anime_json:
        print(search_query.replace("&", " ").split(), anime["title"], [x in anime["title"] for x in search_query.replace("&", " ").split()])
        if all([x in anime["title"] for x in search_query.replace("&", " ").split()]):
            json_data = raw_to_json(Tweet.search(search_query.replace("&", " ").split())[0])
            result[anime["title"]] = json_data
            json_data = raw_to_json(Tweet.search(search_query.replace("&", " ").split())[1])
            result[anime["title"]+"_or"] = json_data

    return jsonify(result)

@app.route("/api/hashtags/")
@app.route("/api/hashtags/pages/<int:page>/")
def hashtags(page=1):
    raw_data = Hashtag.query.paginate(page, 50, False).items
    json_data = raw_to_json(raw_data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtags/<int:id>/")
def hashtag(id):
    data = db.session.query(Hashtag).get(id)
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtags/<int:id>/<string:resource>/")
def hashtag_subresources(id, resource):
    hashtag = db.session.query(Hashtag).get(id)
    raw_data = getattr(hashtag, resource)
    json_data = raw_to_json(raw_data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/hashtags/search/<string:search_query>/")
def search_hashtags(search_query):
    result = {}
    json_data = raw_to_json(Hashtag.search(search_query.replace("&", " ").split())[0])
    result[search_query] = json_data
    json_data = raw_to_json(Hashtag.search(search_query.replace("&", " ").split())[1])
    result[search_query+"_or"] = json_data
    return jsonify(result)

@app.route("/api/locations/")
@app.route("/api/locations/pages/<int:page>/")
def locations(page=1):
    raw_data = Location.query.paginate(page, 50, False).items
    json_data = []
    for data in raw_data:
        data = data.__dict__
        del data['_sa_instance_state']
        json_data.append(data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/locations/<int:id>/")
def location(id):
    data = db.session.query(Location).get(id)
    data = data.__dict__
    del data['_sa_instance_state']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))


@app.route("/api/locations/<int:id>/<string:resource>/")
def location_subresources(id, resource):
    location = db.session.query(Location).get(id)
    raw_data = getattr(location, resource)
    json_data = raw_to_json(raw_data)
    return json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/api/search/<string:search_query>/")
def search(search_query):
    search_query_strings = search_query.replace("&", " ").split()
    json_data = {
        "tweets" : raw_to_json(Tweet.search(search_query_strings)[0]),
        "tweets_or": raw_to_json(Tweet.search(search_query_strings)[1]),
        "hashtags" : raw_to_json(Hashtag.search(search_query_strings)[0]),
        "hashtags_or": raw_to_json(Hashtag.search(search_query_strings)[1])
    }
    return jsonify(json_data)

@app.route('/unit-tests/')
def run_unit_tests():
    from datetime import datetime
    import subprocess
    bashCommand = "coverage3 run --branch " + os.path.join(basedir, 'tests.py')
    s = subprocess.Popen(bashCommand.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    out = ""
    for line in s.stdout:
        out += line.decode("utf-8")

    bashCommand = "coverage3 report -m"
    s = subprocess.Popen(bashCommand.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    for line in s.stdout:
        out += line.decode("utf-8")

    return ("You ran the tests on: " + datetime.now().strftime("%I:%M%p on %B %d, %Y") + " GMT\n" + out)

# Funnel all other requests to angular
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

def raw_to_json(*raw_query):
    json_data = []
    for raw_data in raw_query:
        for data in raw_data:
            data = data.__dict__
            del data['_sa_instance_state']
            if ('date_time' in data):
                data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
            json_data.append(data)
    return json_data

if __name__ == "__main__":
    app.run(host='0.0.0.0')
