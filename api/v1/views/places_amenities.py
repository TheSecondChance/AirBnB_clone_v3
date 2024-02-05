#!/usr/bin/python3
"""This for View for the link between Place and Amenity Review"""
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from os import getenv
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def placesAmenities(place_id):
    """ This for Retrieves the list of
    Amenities objects in Place"""
    rtrivePlace = storage.get("Place", place_id)
    if not rtrivePlace:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        datas = [amenity.to_dict() for amenity in rtrivePlace.amenities]
    else:
        datas = [storage.get(
            "Amenity", id).to_dict() for id in rtrivePlace.amenity_ids]
    return jsonify(datas)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def amenityPlace(place_id, amenity_id):
    """
    This for Links an Amenity and a Place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delPlaces_amenities(place_id, amenity_id):
    """ This for Deletes Amenity object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)
