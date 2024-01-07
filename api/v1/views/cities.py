#!/usr/bin/python3
"""
Defines all endpoints related to operations on City objects.
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"])
def cities(state_id):
    """Retrieve a list of cities in a state or add a city."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        # Get all cities in the specified state
        state = storage.get(State, state_id)
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == "POST":
        if not request.json:
            abort(400, "Not a JSON")
        json_dict = request.get_json()
        if "name" not in json_dict.keys():
            abort(400, "Missing name")
        new_city = City(**json_dict)
        new_city.state_id = state.id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["GET", "PUT", "DELETE"])
def cities2(city_id):
    """Retrieve, update, or delete a specific city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        # Update a city
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
