#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ Get the status in json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def cls_count():
    """ Export as json th number of objects of cls"""
    count = {"amenities": "Amenity",
             "cities": "City",
             "places": "Place",
             "reviews": "Review",
             "states": "State",
             "users": "User"}

    for key, value in count.items():
        count[key] = storage.count(value)

    return jsonify(count)
