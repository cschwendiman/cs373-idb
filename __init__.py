from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://idb:idb@localhost/idb'
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
