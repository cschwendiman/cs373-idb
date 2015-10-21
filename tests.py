from unittest import main, TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_searchable import search

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, LargeBinary, Boolean

import threading
from flask import Flask, render_template, url_for, g, request, session, redirect, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy

from models import *
from __init__ import unittests
unittests()

class testModels(TestCase):

    #setup the database
    def setUp(self):
        db.configure_mappers()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #-------------
    # Tweets_model
    #-------------

    def test_tweets_writability(self):
        query = rep.query.all()
        startSize = len(query)

        db.session.add(Tweet(text = "This is a test tweet"))
        db.session.commit()
        query = rep.query.all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)

    # def test_tweets2(self):

    # def test_tweets3(self):


    # #---------------
    # # Hashtags_model
    # #---------------

    # def test_hashtags1(self):

    # def test_hashtags2(self):

    # def test_hashtags3(self):

    # #----------------
    # # Locations_model
    # #----------------
    
    # def test_locations1(self):

    # def test_locations2(self):

    # def test_locations3(self):

if __name__ == "__main__":
    main()