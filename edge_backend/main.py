from flask import Flask, request, jsonify
from mqtt_handler import mqtt_client
from prophet_analysis import check_anomaly
from openai_recommender import generate_recommendation

app = Flask(__name__)

sensor_data_store = {}

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    sensor_type = data.get('sensor_type')
    value = data.get('value')
    timestamp = data.get('timestamp')

    if not sensor_type or value is None:
        return jsonify({"error": "Invalid data"}), 400

    if sensor_type not in sensor_data_store:
        sensor_data_store[sensor_type] = []

    sensor_data_store[sensor_type].append({'timestamp': timestamp, 'value': value})

    # Run analysis if we have enough data
    if len(sensor_data_store[sensor_type]) > 10:
        anomalies = check_anomaly(sensor_data_store[sensor_type])
        if anomalies:
            rec = generate_recommendation(sensor_type, anomalies[-1]['value'])
            return jsonify({"anomaly": True, "recommendation": rec})

    return jsonify({"status": "data received"})

if __name__ == '__main__':
    mqtt_client.loop_start()
    app.run(host='0.0.0.0', port=5000)
    
