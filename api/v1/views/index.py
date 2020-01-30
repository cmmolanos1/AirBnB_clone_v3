#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Shows the status of the API.
    ---
    tags:
      - "INDEX"
    produces:
      - "application/xml"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def cls_count():
    """Shows the number of objects of each type.
    ---
    tags:
      - "INDEX"
    produces:
      - "application/xml"
    responses:
        200:
          description: "successful operation"
        404:
          description: "not found"
    """
    count = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}

    return jsonify(count)
