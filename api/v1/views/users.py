#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def ret_users():
    """ Retrieves the list of all Users
    ---
    tags:
        - "USERS"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    list_users = []
    # Remember is an objects dictionary
    users = storage.all("User").values()
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def ret_users_id(user_id):
    """Retrieves an USER object depends on its ID
    ---
    tags:
      - "USERS"
    produces:
      - "application/json"
    parameters:
      - name: "user_id"
        in: "path"
        description: "ID of user to return"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user_id(user_id):
    """Delete an User object depends on its ID
    ---
    tags:
      - "USERS"
    produces:
      - "application/json"
    parameters:
      - name: "user_id"
        in: "path"
        description: "ID of user to delete"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', methods=['POST'])
def post_users():
    """POST a new user, by typing the email and password
    ---
    tags:
        - "USERS"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "email and password"
          in: "body"
          description: "Email and password of the new user"
          required: true
          schema:
              id: postPlace
              type: "object"
              "properties":
                "email":
                  "type": string
                "password":
                  "type": string
    responses:
        201:
            description: "successful operation"
        400:
            description: "Not a JSON - Missing name - Missing user_id"
        404:
            description: "not found"
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400

    content = request.get_json()
    # Imitating create in console
    user = User(**content)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_users(user_id):
    """ Update a user object
    ---
    tags:
        - "USERS"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "user_id"
          in: "path"
          description: "ID of the user we want to update"
          required: true
        - name: "email and password"
          in: "body"
          description: "Email and password to update user"
          required: true
          schema:
              id: postPlace
              type: "object"
              "properties":
                "email":
                  "type": string
                "password":
                  "type": string
    responses:
        201:
            description: "successful operation"
        400:
            description: "Not a JSON - Missing name - Missing user_id"
        404:
            description: "not found"
"""
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'email' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
