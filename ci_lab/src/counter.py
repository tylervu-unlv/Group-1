"""
Counter API Implementation
"""
from flask import Flask, jsonify
from src import status
import re

app = Flask(__name__)

# Dictionary to store counters
COUNTERS = {}

def is_valid_counter_name(name):
    """Validate counter name to ensure it contains only alphanumeric characters"""
    return re.match(r"^[a-zA-Z0-9_]+$", name) is not None

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a new counter"""
    if not is_valid_counter_name(name):
        return jsonify({"error": "Invalid counter name. Only alphanumeric and underscores allowed."}), status.HTTP_400_BAD_REQUEST
    if name in COUNTERS:
        return jsonify({"error": f"Counter '{name}' already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Increment an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    del COUNTERS[name]
    return jsonify({"message": f"Counter '{name}' deleted"}), status.HTTP_204_NO_CONTENT

@app.route('/counters', methods=['GET'])
def list_counters():
    """List all counters"""
    return jsonify(COUNTERS), status.HTTP_200_OK

@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters"""
    COUNTERS.clear()
    return jsonify({"message": "All counters have been reset"}), status.HTTP_200_OK

@app.route('/counters/total', methods=['GET'])
def get_total_counters():
    """Retrieve the sum of all counter values"""
    total = sum(COUNTERS.values())
    return jsonify({"total": total}), status.HTTP_200_OK

@app.route('/counters/top/<int:n>', methods=['GET'])
def get_top_n_counters(n):
    """Retrieve the top N highest counters"""
    if not COUNTERS:
        return jsonify({"error": "No counters available"}), status.HTTP_404_NOT_FOUND

    # Sort by value in descending order
    sorted_items = sorted(COUNTERS.items(), key=lambda item: item[1], reverse=True)

    # Get top N items
    top_n = dict(sorted_items[:n])

    return jsonify(top_n), status.HTTP_200_OK

@app.route('/counters/bottom/<int:n>', methods=['GET'])
def get_bottom_n_counters(n):
    """Retrieve the bottom N lowest counters"""
    if not COUNTERS:
        return jsonify({"error": "No counters available"}), status.HTTP_404_NOT_FOUND
    # Sort by value in ascending order (to get the lowest)
    sorted_items = sorted(COUNTERS.items(), key=lambda item: item[1])
    # Get bottom N items
    bottom_n = dict(sorted_items[:n])
    return jsonify(bottom_n), status.HTTP_200_OK

@app.route('/counters/<name>/set/<value>', methods=['PUT'])
def set_counter_value(name, value):
    """Set a counter to a specific value"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    try:
        value = int(value)  # Convert value to an integer
    except ValueError:
        return jsonify({"error": "Invalid counter value"}), status.HTTP_400_BAD_REQUEST
    if value < 0:
        return jsonify({"error": "Counter value cannot be negative"}), status.HTTP_400_BAD_REQUEST
    COUNTERS[name] = value
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>/reset', methods=['POST'])
def reset_single_counter(name):
    """Reset a single counter to zero"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/count', methods=['GET'])
def get_total_number_of_counters():
    """Get the total number of counters"""
    total_count = len(COUNTERS)  # Only count actual active counters
    return jsonify({"count": total_count}), status.HTTP_200_OK

@app.route('/counters/greater/<int:threshold>', methods=['GET'])
def get_counters_greater_than(threshold):
    """Retrieve counters greater than a given threshold"""
    filtered_counters = {key: val for key, val in COUNTERS.items() if val > threshold}
    return jsonify(filtered_counters), status.HTTP_200_OK

@app.route('/counters/less/<int:threshold>', methods=['GET'])
def get_counters_less_than_threshold(threshold):
    """Get all counters with values less than the given threshold"""
    filtered_counters = {k: v for k, v in COUNTERS.items() if v < threshold}  # Only keep valid ones
    return jsonify(filtered_counters), status.HTTP_200_OK
def describe_status(code):
    mapping = {
        200: "OK",
        404: "Not Found",
    }
    return mapping.get(code, "Unknown")

