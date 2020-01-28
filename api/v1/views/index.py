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
    count = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}

    return jsonify(count)
