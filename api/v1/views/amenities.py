#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def ret_amenities():
    """ Retrieves the list of all Amenity objects """
    list_amenities = []
    amenities = storage.all("Amenity")
    # Remember we are calling an object's dictionary
    for val in amenities.values():
        list_amenities.append(val.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def ret_amenities_id(amenity_id):
    """Retrieves an Amenity object when it's typed the AMENITY ID.
    ---
    tags:
      - "AMENITIES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "amenity_id"
        in: "path"
        description: "ID of amenity to return"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    try:
        key = "Amenity." + amenity_id
        return storage.all("Amenity")[key].to_dict()
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenities_id(amenity_id):
    """Deletes a AMENITY object by its ID.
    ---
    tags:
      - "AMENITIES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "amenity_id"
        in: "path"
        description: "ID of amenity to delete"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenities():
    """POST a new amenity, by typing the name.
    ---
    tags:
        - "AMENITIES"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "Amenity Name"
          in: "body"
          description: "Name of the new amenity to be created"
          required: true
          schema:
              id: postName
              type: "object"
              properties:
                name:
                  type: string
          example:
              "name": "Playground"
    responses:
        201:
            description: "successful operation"
        404:
            description: "not found"
        400:
            description: "Not a JSON, or, Missing name"
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    # Imitating create in console
    amenity = Amenity(**content)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenities(amenity_id):
    """UPDATE the name of amenity object.
    ---
    tags:
        - "AMENITIES"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "Amenity ID"
          in: "path"
          description: "ID of the amenity to be updated"
          required: true
        - name: "Amenity Name"
          in: "body"
          description: "Name of the new amenity to be created"
          required: true
          schema:
              id: postName
              type: "object"
              properties:
                name:
                  type: string
          example:
              "name": "POOL"
    responses:
        201:
            description: "successful operation"
        404:
            description: "not found"
        400:
            description: "Not a JSON"
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
