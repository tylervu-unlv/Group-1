"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return counter_response(name, status.HTTP_201_CREATED)

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve an existing counter"""
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    return counter_response(name, status.HTTP_200_OK)

def counter_response(name, http_status):
    """Build the standard JSON response for a counter"""
    return jsonify({name: COUNTERS[name]}), http_status
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters', methods=['GET'])
def list_counters():
    """List all counters"""
    return jsonify(COUNTERS), status.HTTP_200_OK
@app.route('/counters/<name>', methods =["PUT"])
def increment_counter(name):
    """increment a counter"""
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK
  
@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete a counter"""
    if not counter_exists(name):
        return '', status.HTTP_404_NOT_FOUND
    del COUNTERS[name]
    return '', status.HTTP_204_NO_CONTENT
