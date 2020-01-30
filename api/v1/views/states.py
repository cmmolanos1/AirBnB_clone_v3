#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def ret_states():
    """ Retrieves the list of all State objects
    ---
    tags:
      - "STATES"
    """
    list_states = []
    states = storage.all("State")
    # Remember we are calling an object's dictionary
    for val in states.values():
        list_states.append(val.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def ret_states_id(state_id):
    """Retrieves a State object when it's typed the STATE ID.
    ---
    tags:
      - "STATES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "state_id"
        in: "path"
        description: "ID of state to return"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
          schema:
          id: Palette
          type: object
        404:
          description: "not found"
    """
    try:
        key = "State." + state_id
        return storage.all("State")[key].to_dict()
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_states_id(state_id):
    """Deletes a STATE object by its ID.
    ---
    tags:
      - "STATES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "state_id"
        in: "path"
        description: "ID of state to delete"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/', methods=['POST'])
def post_states():
    """Creates a new state, posting its name.
    ---
    tags:
        - "STATES"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "State Name"
          in: "body"
          description: "Name of the new state to be created"
          required: true
          schema:
              id: postName
              type: "object"
              "properties":
                "name":
                  "type": string
          examples:
              name: California
    responses:
        201:
            description: "successful operation"
        404:
            description: "not found"
    """
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
    """UPDATE the state name.
    ---
    tags:
        - "STATES"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "State ID"
          in: "path"
          description: "ID of state to update"
          required: true
        - name: "State Name"
          in: "body"
          description: "Name of the new state to be updated"
          required: true
          schema:
              id: postName
              type: "object"
              "properties":
                "name":
                  "type": string
          examples:
              name: Nebraska
    responses:
        200:
            description: "successful operation"
        404:
            description: "not found"
    """
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
