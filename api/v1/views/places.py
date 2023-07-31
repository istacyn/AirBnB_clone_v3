#!/usr/bin/python3
"""
places api
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Create a new view for City objects that handles all default
    RestFul API actions.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in city.places])

    if request.method == 'POST':
        post = get_json(request)
        if not post:
            return make_respone('Not a JSON\n', 400)
        if 'name' not in post.keys():
            return make_response('Missing name\n', 400)
        if 'user_id' not in post.keys():
            return make_response('Missing user_id\n', 400)
        if storage.get(User, post.get('user_id')) is None:
            abort(404)
        post.update({'city_id': city_id})
        new_place = Place(**post)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place_id(place_id):
    """Retrieves a city object with a specific id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        put = get_json(request)
        if not put:
            return make_response('Not a JSON\n', 400)
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id']:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for Place objects based on the
    provided JSON in the request body.
    """
    request_data = get_json(request)
    if request_data is None:
        return make_response('Not a JSON\n', 400)

    places = []
    if "states" in request_data.keys():
        states = [storage.get(State, state_id)
                  for state_id in request_data.get('states')]
        for state in states:
            for city in state.cities:
                filter_places_by_amenities(places, city,
                                           request_data.get('amenities'))
    if "cities" in request_data.keys():
        cities = [storage.get(City, city_id)
                  for city_id in request_data.get('cities')]
        for city in cities:
            filter_places_by_amenities(places, city,
                                       request_data.get('amenities'))
    if len(request_data) == 0 or all([len(request_data) == 1,
                                     request_data.get('amenities')
                                     is not None]):
        states = storage.all(State).values()
        for state in states:
            for city in state.cities:
                filter_places_by_amenities(places, city,
                                           request_data.get('amenities'))

    return make_response(jsonify(places))


def filter_places_by_amenities(place_list, city, amenities=None):
    """Filter places based on specified amenities
    """
    if amenities is not None:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in amenities]
        for place in city.places:
            place_dict = place.to_dict()

            # For database storage, add a 'amenities' attribute
            # with a list of unserializable amenity objects to
            # the place, removing the key-value pair to avoid JSON
            # serialization errors and maintain object string
            # representation consistency.
            if place_dict.get("amenities"):
                place_dict.pop("amenities")
            if all([amenity in place.amenities for amenity in amenities]):
                if place_dict not in place_list:
                    place_list.append(place_dict)

    else:
        for place in city.places:
            place_dict = place.to_dict()
            if place_dict.get("amenities"):
                place_dict.pop("amenities")
            if place.to_dict() not in place_list:
                place_list.append(place_dict)


def get_json(request):
    """
    Extract JSON data from the request body and handle error responses.
    """
    try:
        data = request.get_json()
    except Exception:
        data = None
    return data
