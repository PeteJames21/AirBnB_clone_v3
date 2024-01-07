#!/usr/bin/python3
"""Set routes for the flask app"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    """Route to status page"""
    d = {'status': 'OK'}
    return jsonify(d)


@app_views.route('/stats', methods=['GET'])
def count():
    """Retrieve the number of each objects by type"""
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return make_response(count_dict)
