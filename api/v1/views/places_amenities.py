#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def ret_amenities_in_place(place_id):
    """Retrieves a list of all Amenities linked to a Place.
    ---
    tags:
      - "PLACES AMENITIES"
    produces:
      - "application/json"
    parameters:
      - name: "place_id"
        in: "path"
        description: "ID of place"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    list_amenities = []
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    # List of amenities objects linked to this place
    amenities = place.amenities
    for amen in amenities:
        list_amenities.append(amen.to_dict())
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def del_amenitie_in_place(place_id, amenity_id):
    """Deletes an Amenity object from a Place.
    ---
    tags:
      - "PLACES AMENITIES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "place_id"
        in: "path"
        description: "ID of place where the amenity is deleted"
        required: true
        type: "string"
      - name: "amenity_id"
        in: "path"
        description: "ID of amenity"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)

    # List of amenities objects linked to this place
    amenities = place.amenity

    # Search if amenity_id is linked to the object
    listOfAmenitiesID = [amen.id for amen in amenities]
    if amenity_id not in listOfAmenitiesID:
        abort(404)

    for amen in amenities:
        if amen.id == amenity_id:
            amen.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def post_amenities_in_place(place_id, amenity_id):
    """ POST a new amenity in a specific place.
    ---
    tags:
      - "PLACES AMENITIES"
    produces:
      - "application/xml"
      - "application/json"
    parameters:
      - name: "place_id"
        in: "path"
        description: "ID of place"
        required: true
        type: "string"
      - name: "amenity_id"
        in: "path"
        description: "ID of amenity to be linked"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # Search if the amenity is already linked
    for amen in place.amenities:
        if amen.id == str(amenity_id):
            return jsonify(amen.to_dict()), 200

    # Link the amenity with the place
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
