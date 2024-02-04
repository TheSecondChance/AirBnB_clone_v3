#!/usr/bin/python3
"""This for amenty crud
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenities():
    """This for
    amenity information for all amenities
    """
    allAmenities = []
    for amenity in storage.all(Amenity).values():
        allAmenities.append(amenity.to_dict())
    return jsonify(allAmenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    """This for
    amenity info for specified amenity"""
    singleAmenity = storage.get(Amenity, amenity_id)
    if singleAmenity is None:
        abort(404)
    return jsonify(singleAmenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """This for
    deletes amenity based on its id
    """
    deletAmenity = storage.get(Amenity, amenity_id)
    if deletAmenity is None:
        abort(404)
    deletAmenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """This for create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    createdAmenity = Amenity(**request.get_json())
    saveNewCreated = createdAmenity.save()
    return make_response(jsonify(saveNewCreated.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """
    This for update amenity
    """
    updatedAmenity = storage.get(Amenity, amenity_id)
    if updatedAmenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(updatedAmenity, attr, val)
    updatedAmenity.save()
    return jsonify(updatedAmenity.to_dict())
