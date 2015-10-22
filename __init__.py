from flask import Flask, render_template
import json

app = Flask(__name__, static_url_path='/static')

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
