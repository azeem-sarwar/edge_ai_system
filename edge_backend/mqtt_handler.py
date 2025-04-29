# Content of mqtt_handler.py
import paho.mqtt.client as mqtt
import requests
import json

BROKER = 'mqtt.eclipseprojects.io'
PORT = 1883
TOPICS = ['sensor/temperature', 'sensor/motorload']

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code ", rc)
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received message from {msg.topic}: {msg.payload.decode()}")
    sensor_type = msg.topic.split('/')[-1]
    payload = json.loads(msg.payload.decode())
    payload['sensor_type'] = sensor_type
    requests.post('http://localhost:5000/api/sensor-data', json=payload)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT, 60)
