#!/usr/bin/python3
"""
Defines endpoints for handling all operations related to
User objects.
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def users(user_id=""):
    """Defines endpoints for dealing with User objects."""
    if user_id:
        # If provided, user_id must point to an existing user
        user = storage.get(User, user_id)
        if not user:
            abort(404)

    if request.method == "GET":
        # Return all users
        if not user_id:
            all_users = []
            for user in storage.all("User").values():
                all_users.append(user.to_dict())
            return jsonify(all_users)
        return jsonify(user.to_dict())

    if request.method == "PUT":
        # Update an existing user.
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at", "email"]:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({})

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, 'Missing name')
        new_user = User(**request.get_json())
        new_user.save()
        return jsonify(new_user.to_dict()), 201
