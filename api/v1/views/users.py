#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def ret_users():
    """ Retrieves the list of all Users """
    list_users = []
    # Remember is an objects dictionary
    users = storage.all("User").values()
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def ret_users_id(user_id):
    """ Retrieves an object depends on its ID """
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user_id(user_id):
    """ Delete a User object depends on its ID"""
    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', methods=['POST'])
def post_users():
    """ POST a new user, by typing the name"""
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
    """ Update a user object """
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
