#!/usr/bin/python3
""" PACKAGE """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def ret_places_in_city(city_id):
    """ Retrieves the list of all Place objects of a City """
    list_places = []
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)
    # Remember is an objects dictionary
    places = storage.all("Place").values()
    for place in places:
        if place.city_id == str(city_id):
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def ret_places_id(place_id):
    """ Retrieves an object depends on its ID """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_places_id(place_id):
    """ Delete a Place object depends on its ID"""
    place = storage.get("Place", str(place_id))
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.place_id == place_id:
            review.delete()
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_places(city_id):
    """ POST a new places, by typing the name and the id """
    city = storage.get("City", str(city_id))
    if city is None:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    content = request.get_json()
    if "User." + content["user_id"] not in storage.all("User"):
        abort(404)
    # Adding state_id as attribute
    content['city_id'] = str(city_id)
    # Imitating create in console
    place = Place(**content)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_places(place_id):
    """ Update a place object """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key is not 'id' and \
           key is not 'city_id' and \
           key is not 'user_id' and \
           key is not 'created_at' and \
           key is not 'updated_at':
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def put_places_search():
    """ print a place object by city,state or amenitie """
    search = request.get_json()
    all_places = storage.all("Place")
    result = []
    no_amenity = True

    # rule empty body
    try:
        if len(search) == 0 and type(search) == dict:
            result = [value.to_dict() for value in all_places.values()]
            return jsonify(result)
    except:
        # rule not json
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400

    # rule empty values
    is_empty = [len(value) == 0 for value in search.values()]
    if False not in is_empty:
        result = [value.to_dict() for value in all_places.values()]
        return jsonify(result)
    # rule if amenities in json
    if "states" in search and len(search["states"]) != 0:
        for state_id in search["states"]:
            state = storage.get("State", str(state_id))
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place.to_dict() not in result:
                            result.append(place.to_dict())
            else:
                pass
        no_amenity = False
    # rule if cities in json
    if "cities" in search and len(search["cities"]) != 0:
        for city_id in search["cities"]:
            city = storage.get("City", city_id)
            if city:
                for place in city.places:
                    if place.to_dict() not in result:
                        result.append(place.to_dict())
        no_amenity = False
    # rule if amenities in json
    if len(search.get("amenities", [])):
        amenities = [storage.get("Amenity", id) for id in search["amenities"]]
        places = [place for place in places
                  if all([a in place.amenities for a in amenities])]
        result = [place.to_dict() for place in places]

    if "amenities" in search and len(search["amenities"]) != 0:
        if no_amenity is False:
            all_places = []
            for place in result:
                all_places.append(storage.get("Place", str(place["id"])))
        else:
            all_places = storage.all("Place").values()
        for place in all_places:
            flag = 0
            am_list = [amenity.id for amenity in place.amenities]
            for amenity_id in search["amenities"]:
                if amenity_id not in am_list:
                    flag = 1
            if flag == 0 and len(am_list) > 0:
                place = place.to_dict()
                if "amenities" in place:
                    del place["amenities"]
                ids_in_result = [resul['id'] for resul in result]
                print(ids_in_result)
                if place['id'] not in ids_in_result:
                    result.append(place)
    return jsonify(result)
