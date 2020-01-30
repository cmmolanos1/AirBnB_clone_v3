#!/usr/bin/python3
""" API file """

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask_cors import CORS
import os
from flasgger import Swagger


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'HBNB API',
    'description': 'Documentation explaining the diferents method to work\
    with our API',
    'uiversion': 2
}
swagger = Swagger(app)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Export json 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
