from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Splash Page"

@app.route("/locations/")
def locations():
    return "All Locations"

@app.route("/tweets/")
def tweets():
    return "All Tweets"

@app.route("/hashtags/")
def hashtags():
    return "All Hashtags"

@app.route("/location/<city_name>")
def location(city):
    return "Location %s" % city

@app.route("/hashtag/<hashtag_name>")
def hashtag(text):
    return "Hashtag %s" % text

@app.route("/tweet/<int:tweet_id>")
def tweet(tweet_id):
    return "Tweet with id %d" % tweet_id

if __name__ == "__main__":
    app.run(host='0.0.0.0')