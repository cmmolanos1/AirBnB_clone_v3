#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def ret_rev_in_place(place_id):
    """ Retrieves the list of all Reviews objects of a place
    ---
    tags:
      - "PLACES REVIEWS"
    parameters:
      - name: "place_id"
        in: "path"
        description: "ID of the place where we want to read the reviews"
        required: true
        type: "string"
    """
    list_reviews = []
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    # Remember is an objects dictionary
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.place_id == str(place_id):
            list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def ret_reviews_id(review_id):
    """Retrieves a Review object when it's typed the REVIEW ID.
    ---
    tags:
      - "PLACES REVIEWS"
    produces:
      - "application/json"
    parameters:
      - name: "review_id"
        in: "path"
        description: "ID of the review to return"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_reviews_id(review_id):
    """ Delete a Review object depends on its ID
    ---
    tags:
      - "PLACES REVIEWS"
    produces:
      - "application/json"
    parameters:
      - name: "review_id"
        in: "path"
        description: "ID of review to delete"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def post_reviews(place_id):
    """ POST a new review, by typing the user id and a description
    ---
    tags:
        - "PLACES REVIEWS"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "Place ID"
          in: "path"
          description: "The ID of place we want to add reviews."
          required: true
        - name: "User and Description"
          in: "body"
          description: "Field to add the User ID and the description."
          required: true
          schema:
              id: postReview
              type: "object"
              "properties":
                "user_id":
                  "type": string
                "text":
                  "type": string
          examples:
              user_id: "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd"
              text: "Good place"
    responses:
        201:
            description: "successful operation"
        400:
            description: "Not a JSON - Missing user_id - Missing text"
        404:
            description: "not found"
    """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    content = request.get_json()
    user_id = content['user_id']
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if 'text' not in content.keys():
        return jsonify({"error": "Missing text"}), 400
    # Adding place_id
    content['place_id'] = str(place_id)
    # Imitating create in console
    review = Review(**content)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_reviews(review_id):
    """ Update a review object
    ---
    tags:
        - "PLACES REVIEWS"
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
        - name: "review_id"
          in: "path"
          description: "ID of review to update"
          required: true
          type: "string"
        - name: "User and Description"
          in: "body"
          description: "Field to add the User ID and the description."
          required: true
          schema:
              id: postReview
              type: "object"
              "properties":
                "user_id":
                  "type": string
                "text":
                  "type": string
          examples:
              user_id: "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd"
              text: "Good place"
    responses:
        200:
            description: "successful operation"
        404:
            description: "not found"
    """
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'user_id' and \
           key is not 'place_id' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
