#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
app.py file
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

"""Create a Flask app"""
app = Flask(__name__)

"""Register the blueprint app_views to the Flask instance app"""
app.register_blueprint(app_views)

"""Method to handle teardown after each request"""
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == "__main__":
    """Get the host and port from environment variables or use default values"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    """Run the Flask app"""
    app.run(host=host, port=port, threaded=True)
