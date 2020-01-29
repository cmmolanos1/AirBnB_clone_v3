#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def ret_states():
    """ Retrieves the list of all State objects """
    list_states = []
    states = storage.all("State")
    # Remember we are calling an object's dictionary
    for val in states.values():
        list_states.append(val.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def ret_states_id(state_id):
    """ Retrieves an object depends on its ID """
    try:
        key = "State." + state_id
        return storage.all("State")[key].to_dict()
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_states_id(state_id):
    """ Delete a State object depends on its ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/', methods=['POST'])
def post_states():
    """ POST a new state, by typing the name """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    # Imitating create in console
    state = State(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states(state_id):
    """ Update a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
