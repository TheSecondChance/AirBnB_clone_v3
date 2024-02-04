#!/usr/bin/python3
"""
This for view for User objects
that handles default API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ This for Retrieves the list of all User objects"""
    allUser = storage.all(User)
    return jsonify([obj.to_dict() for obj in allUser.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getUserId(user_id):
    """
    Retrieves user using by id
    """
    userById = storage.get("User", user_id)
    if not userById:
        abort(404)
    return jsonify(userById.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletUser(user_id):
    """
    This for Deletes a User object """
    delUser = storage.get("User", user_id)
    if not delUser:
        abort(404)
    delUser.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def postUser():
    """
    This for reates a User object
    """
    newUser = request.get_json()
    if not newUser:
        abort(400, "Not a JSON")
    if "email" not in newUser:
        abort(400, "Missing email")
    if "password" not in newUser:
        abort(400, "Missing password")
    addUser = User(**newUser)
    storage.new(addUser)
    storage.save()
    return make_response(jsonify(addUser.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """ This for Updates a User object """
    putUser = storage.get("User", user_id)
    if not putUser:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    for key, v in body_request.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(putUser, key, v)
    storage.save()
    return make_response(jsonify(putUser.to_dict()), 200)
