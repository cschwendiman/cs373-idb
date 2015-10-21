from flask import Flask
import json
app = Flask(__name__)

@app.route("/")
def index():
    data = json.load(open("parsed_aux.json"))
    tweets = list(data.items())[0:10]
    return render_template('index.html',
                           place="Austin",
                           posts=tweets)

@app.route("/cities/")
def cities():
    return "All Cities"

@app.route("/tweets/")
def tweets():
    return "All Tweets"

@app.route("/hashtags/")
def hastags():
    return "All Hashtags"

@app.route("/city/<city_name>")
def city(city_name):
    return "City %s" % city_name

@app.route("/hashtag/<hashtag>")
def hashtag(hashtag):
    return "Hashtag %s" % hashtag

@app.route("/tweet/<int:tweet_id>")
def tweet(tweet_id):
    return "Tweet with id %d" % tweet_id

if __name__ == "__main__":
    app.run(host='0.0.0.0')
