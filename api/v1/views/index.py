#!/usr/bin/python3
""" This for Index """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This for Returns JSON """
    response = {'status': 'ok'}
    return jsonify(response)
