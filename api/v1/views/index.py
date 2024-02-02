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


if __name__ == "__main__":
    pass
