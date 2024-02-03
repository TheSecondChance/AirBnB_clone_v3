#!/usr/bin/python3
""" this for View for State objects that handles default API actions
"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ This for
    Retrieves the list of all State objects
    """
    retStates = storage.all(State)
    return jsonify([obj.to_dict() for obj in retStates.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def stateIdRerive(state_id):
    """ This for Retrieves a State object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletState(state_id):
    """ This for Deletes State object
    """
    delState = storage.get("State", state_id)
    if not delState:
        abort(404)
    delState.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def postState():
    """ This for Creates a State object
    """
    createState = request.get_json()
    if not createState:
        abort(400, "Not a JSON")
    if "name" not in createState:
        abort(400, "Missing name")
    state = State(**createState)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putState(state_id):
    """ This for Updates a State object
    """
    updateState = storage.get("State", state_id)
    if not updateState:
        abort(404)

    requestBody = request.get_json()
    if not requestBody:
        abort(400, "Not a JSON")

    for key, value in requestBody.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(updateState, key, value)

    storage.save()
    return make_response(jsonify(updateState.to_dict()), 200)
