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

@app.route('/collision-detection', methods=['GET'])
def get_collision_detection_data():
    return jsonify(collision_detection_data), 200

@app.route('/passenger-management', methods=['GET'])
def get_passenger_management_data():
    return jsonify(passenger_management_data), 200

@app.route('/road-condition', methods=['GET'])
def get_road_condition_mapping_data():
    return jsonify(road_condition_mapping_data), 200

if __name__ == '__main__':
    app.run(debug=True)
