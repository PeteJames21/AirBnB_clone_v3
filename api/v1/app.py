#!/usr/bin/python3
'''Creates a blueprint and runs the Flask app'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """Closes storage session after every request has been fulfilled."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error and give json formatted respons"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Setting host and port based
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Running the Flask app
    app.run(host=host, port=port, threaded=True)
