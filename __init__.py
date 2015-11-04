from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'idb.db') +
                               '?check_same_thread=False')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

"""
@app.route("/api/")
def api():
    return "API"
"""

# Funnel all requests to angular
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
