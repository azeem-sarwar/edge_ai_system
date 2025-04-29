# == sensor_simulator/sensor.py ==
import time
import requests
import random
from datetime import datetime

URL = "http://edge_backend:8000/ingest"

while True:
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(30 + random.uniform(-5, 5), 2),
        "load": round(60 + random.uniform(-10, 10), 2)
    }
    try:
        res = requests.post(URL, json=payload)
        print("Posted:", payload, res.status_code)
    except Exception as e:
        print("Error:", e)
    time.sleep(5)