import requests
from requests_oauthlib import OAuth1
import json

# Token are hidden due to security concern

result={}

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def generate_json(data):
    count = 0
    global result
    for tweet in data["statuses"]:
        if tweet["place"] is not None and len(tweet["entities"]["hashtags"]) > 0:
            twit = {}
            twit["text"] = tweet["text"]
            twit["name"] = tweet["user"]["screen_name"]
            twit["location_id"] = tweet["place"]["id"]
            twit["hashtags"] = list([text["text"] for text in tweet["entities"]["hashtags"]])
            twit["place"] = tweet["place"]["full_name"]
            twit["geo"] = tweet["geo"]
            result[tweet["id"]] = twit

    return sorted(result.keys())[0]

def main():
    oauth = get_oauth()
    r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?geocode=37.78%2C-122.4167%2C25mi&result_type=recent&count=100", auth=oauth)
    max_id = int(generate_json(r.json()))-1
    for x in range(70):
        r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?geocode=37.78%2C-122.4167%2C25mi&result_type=recent&count=100&max_id="+str(max_id), auth=oauth)
        max_id = int(generate_json(r.json()))-1

    global result
    print(json.dumps(result, indent=4))

def check():
    oauth = get_oauth()
    r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json", auth=oauth)
    print(json.dumps(r.json()["resources"]["search"], indent=4))

if __name__ == "__main__":
    # check()
    main()