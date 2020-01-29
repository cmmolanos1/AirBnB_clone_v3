#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def ret_rev_in_place(place_id):
    """ Retrieves the list of all Reviews objects of a place """
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
    """ Retrieves an object depends on its ID """
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_reviews_id(review_id):
    """ Delete a Review object depends on its ID"""
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def post_reviews(place_id):
    """ POST a new review, by typing the name and the id """
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
    """ Update a city object """
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
