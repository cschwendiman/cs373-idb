from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey, String, or_
from sqlalchemy.orm import relationship, backref

"""
-------
Classes
-------

Tweet:
    twitter_tweet_id
    text
    user
    url
    date_time
    longitude
    latitude

Hashtag:
    text
    url

Location:
    city
    state
    country
    
---------------
Relationships
between classes
---------------

Tweet - Hashtag : many-to-many
Location - Hashtag : many-to-many
Location - Tweet : one-to-many (one location to many tweets)
    
--------------------------
Association tables for
many-to-many relationships
--------------------------

hashtag_tweet_table
hashtag_location_table

"""

db = SQLAlchemy()

# Association table for many-to-many relationship between Hashtag and Tweet
hashtag_tweet_table = Table('hashtag_tweet', db.Model.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id')),
    Column('tweet_id', Integer, ForeignKey('tweet.id'))
)

# Association table for many-to-many relationship between Hashtag and Location
hashtag_location_table = Table('hashtag_location', db.Model.metadata,
    Column('hashtag_id', Integer, ForeignKey('hashtag.id')),
    Column('location_id', Integer, ForeignKey('city.id'))
)

class Tweet(db.Model):
    """
    Tweet class.
    Attributes: id, twitter_tweet_id, text, user, url, date_time, latitude, longitude, location_id.
    
    twitter_tweet_id is the id given by Twitter for a tweet. id is the id for the tweet in our datadb.Model.
    location_id is the id (foreign key) of the Location where the tweet was tweeted. 
    
    Tweet has a many-to-many relationship with Hashtag.
    Also has a one-to-many relationship with Location (one Location to many Tweets).
    
    The relationship with Location includes a backref so that Locations have access to tweets
    associated with them.
    """
    
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    # Check length of this field
    twitter_tweet_id = Column(String(50))
    text = Column(String(140))
    user = Column(String(80))
    url = Column(String(80), unique=True)
    date_time = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)
    
    # foreign key for one-to-many relationship with Location.
    # backref so locations can access tweets associated with them.
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("Location", backref=backref("tweets", lazy='dynamic'))

    def __init__(self, twitter_tweet_id, text, user, url, date_time, longitude, latitude, city_id):
        self.twitter_tweet_id = twitter_tweet_id
        self.text = text
        self.user = user
        self.url = url
        self.date_time = date_time
        self.longitude = longitude
        self.latitude = latitude
        self.city_id = city_id

    def __repr__(self):
        return '<Tweet %d>' % self.id

    @staticmethod
    def search(query_strings):
        and_queries = (Tweet.text.like("%{:s}%".format(query)) for query in query_strings)
        or_queries = (Tweet.text.like("%{:s}%".format(query)) for query in query_strings)
        return Tweet.query.filter(*and_queries).union(Tweet.query.filter(or_(*or_queries)))

class Hashtag(db.Model):
    """
    Hashtag class.
    Attributes: id, text, url.
    
    Hashtag has a many-to-many relationship with both Tweet and Location.
    """
    
    __tablename__ = 'hashtag'

    id = Column(Integer, primary_key=True)
    text = Column(String(140), unique=True)
    url = Column(String(80), unique=True)

    tweets = relationship("Tweet", secondary=hashtag_tweet_table, backref="hashtags")

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __repr__(self):
        return '<Hashtag %d>' % self.id

    @staticmethod
    def search(query_strings):
        and_queries = (Hashtag.text.like("%{:s}%".format(query)) for query in query_strings)
        or_queries = (Hashtag.text.like("%{:s}%".format(query)) for query in query_strings)
        return Hashtag.query.filter(*and_queries).union(Hashtag.query.filter(or_(*or_queries)))


class Location(db.Model):
    """
    Location class.
    Attributes: id, city, state, country.
    
    Location has a many-to-many relationship with Hashtag.
    Also has a one-to-many relationship with Tweet (one Location to many Tweets).
    """
    
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String(80))
    state = Column(String(80))
    country = Column(String(80))

    hashtags = relationship("Hashtag", secondary=hashtag_location_table, backref="cities")

    def __init__(self, city, state, country):
        self.city = city
        self.state = state
        self.country = country


    def __repr__(self):
        return '<City %d>' % self.id


def raw_data_to_json(*raw_data_sets):
    json_data = []
    for raw_data in raw_data_sets:
        for data in raw_data:
            data = data.__dict__
            del data['_sa_instance_state']
            if ('date_time' in data):
                data["date_time"] = data["date_time"].strftime("%Y-%m-%d %H:%M:%S")
            json_data.append(data)
    return json_data