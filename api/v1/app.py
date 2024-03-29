#!/usr/bin/python3
"""This for app.py to connect to API
create a flask app and register the blueprint app_views with
the flask instance
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """This for teardown_appcontext
    remove the current sqlachemy Session object
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This for not found for the json response
    this for error massage"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
