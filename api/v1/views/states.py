#!/usr/bin/python3
""" this for View for State objects that handles default API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ This for
    Retrieves the list of all State objects
    """
    retStates = storage.all(State).values()
    listSatae = [state.to_dict() for state in retStates]
    return jsonify(listSatae)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def stateIdRerive(state_id):
    """ This for Retrieves a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletState(state_id):
    """ This for Deletes State object
    """
    delState = storage.get(State, state_id)
    if delState:
        storage.delete(delState)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


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
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putState(state_id):
    """ This for Updates a State object
    """

    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(404, 'Not a JSON')
        data = request.get_json()
        anoKey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in anoKey:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
