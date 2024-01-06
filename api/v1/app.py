#!/usr/bin/python3
'''Creates a blueprint and runs the Flask app'''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """ Closes storage session """
    storage.close()


if __name__ == "__main__":
    # Setting host and port based
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Running the Flask app
    app.run(host=host, port=port, threaded=True)
