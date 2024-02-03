#!/usr/bin/python3
""" State objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ This for Retrieves the list of all City objects
    """
    checkState = storage.get("State", state_id)
    if not checkState:
        abort(404)
    return jsonify([city.to_dict() for city in checkState.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id_retirve(city_id):
    """ This for Retrieves City object
    """
    CeckCity = storage.get("City", city_id)
    if not CeckCity:
        abort(404)
    return jsonify(CeckCity.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cityDelet(city_id):
    """ This for Deletes a City object
    """
    deletCity = storage.get("City", city_id)
    if not deletCity:
        abort(404)
    deletCity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity(state_id):
    """ This for Creates City object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    adisKetem = request.get_json()
    if not adisKetem:
        abort(400, "Not a JSON")
    if "name" not in adisKetem:
        abort(400, "Missing name")
    kete = City(**adisKetem)
    setattr(kete, 'state_id', state_id)
    storage.new(kete)
    storage.save()
    return make_response(jsonify(kete.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def putCity(city_id):
    """ This for Updates a City object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    requestBody = request.get_json()
    if not requestBody:
        abort(400, "Not a JSON")

    for k, v in requestBody.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
