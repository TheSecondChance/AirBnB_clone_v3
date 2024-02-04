#!/usr/bin/python3
"""This for api crud"""

from models.place import Place
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def Places(city_id):
    """This for
    place info all places in a specified city
    """
    cityId = storage.get(City, city_id)
    if cityId is None:
        abort(404)
    places = []
    for place in cityId.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def Place(place_id):
    """This for
    place info for specified place
    """
    onePlace = storage.get(Place, place_id)
    if onePlace is None:
        abort(404)
    return jsonify(onePlace.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """This for deletes a place based on its id"""
    deletPlace = storage.get(Place, place_id)
    if deletPlace is None:
        abort(404)
    deletPlace.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    """This for create new place"""
    city = storage.get(City, city_id)
    newCity = city
    if newCity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def putPlace(place_id):
    """ This for Updates a Place object """
    updatePlace = storage.get(Place, place_id)
    if not updatePlace:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    for key, v in body_request.items():
        if key not in ['id', 'user_id', 'city_at',
                'created_at', 'updated_at']:
            setattr(updatePlace, key, v)
    storage.save()
    return make_response(jsonify(updatePlace.to_dict()), 200)
