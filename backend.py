from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory data storage (could be replaced with a database)
fleet_data = {}
driver_monitoring_data = {}
collision_detection_data = {}
passenger_management_data = {}
road_condition_mapping_data = {}
adaptive_cruise_data = {}

@app.route('/track', methods=['POST'])
def track_vehicle():
    data = request.get_json()
    vehicle_id = data['vehicle_id']
    fleet_data[vehicle_id] = {"latitude": data["latitude"], "longitude": data["longitude"]}
    return jsonify({"status": "success"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/fleet', methods=['GET'])
def get_fleet_data():
    return jsonify(fleet_data), 200

@app.route('/driver-monitoring', methods=['GET'])
def get_driver_monitoring_data():
    return jsonify(driver_monitoring_data), 200

@app.route('/driver-monitoring', methods=['POST'])
def post_driver_monitoring_data():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id', 'UNKNOWN')
    driver_monitoring_data[vehicle_id] = {
        "drowsy": data.get("drowsy", False),
        "timestamp": data.get("timestamp")
    }
    return jsonify({"status": "accepted"}), 200

@app.route('/collision-detection', methods=['GET'])
def get_collision_detection_data():
    return jsonify(collision_detection_data), 200

@app.route('/collision-detection', methods=['POST'])
def post_collision_detection_data():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id', 'UNKNOWN')
    collision_detection_data[vehicle_id] = {
        "distance_cm": data.get("distance_cm"),
        "warning": data.get("warning", False),
        "timestamp": data.get("timestamp")
    }
    return jsonify({"status": "accepted"}), 200

@app.route('/passenger-management', methods=['GET'])
def get_passenger_management_data():
    return jsonify(passenger_management_data), 200

@app.route('/passenger-management', methods=['POST'])
def post_passenger_management_data():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id', 'UNKNOWN')
    passenger_management_data[vehicle_id] = {
        "count": data.get("count", 0),
        "overcrowded": data.get("overcrowded", False),
        "timestamp": data.get("timestamp")
    }
    return jsonify({"status": "accepted"}), 200

@app.route('/road-condition', methods=['GET'])
def get_road_condition_mapping_data():
    return jsonify(road_condition_mapping_data), 200

@app.route('/adaptive-cruise', methods=['GET'])
def get_adaptive_cruise_data():
    return jsonify(adaptive_cruise_data), 200

@app.route('/adaptive-cruise', methods=['POST'])
def post_adaptive_cruise_data():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id', 'UNKNOWN')
    adaptive_cruise_data[vehicle_id] = {
        "speed_kmh": data.get("speed_kmh", 0),
        "distance_m": data.get("distance_m"),
        "timestamp": data.get("timestamp")
    }
    return jsonify({"status": "accepted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
