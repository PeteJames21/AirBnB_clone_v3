#!/usr/bin/python3
"""
Defines the /states endpoint
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def all_states(state_id=""):
    """Defines endpoints for dealing with state objects."""
    if state_id:
        # If provided, state_id must point to an existing state
        state = storage.get(State, state_id)
        if not state:
            abort(404)

    if request.method == "GET":
        # Return all states
        if not state_id:
            all_states = []
            for state in storage.all("State").values():
                all_states.append(state.to_dict())
            return jsonify(all_states)
        return jsonify(state.to_dict())

    if request.method == "PUT":
        # Update an existing state.
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({})

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, 'Missing name')
        new_state = State(**request.get_json())
        new_state.save()
        return jsonify(new_state.to_dict()), 201
