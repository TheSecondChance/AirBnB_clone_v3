#!/usr/bin/python3
""" This for Index """


from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This for Returns JSON """
    response = {'status': 'ok'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    allStats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(allStats)


if __name__ == "__main__":
    pass
