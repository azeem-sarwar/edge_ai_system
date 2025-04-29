# == sensor_simulator/Dockerfile ==
FROM python:3.10-slim
WORKDIR /simulator
COPY . .
RUN pip install requests
CMD ["python", "sensor.py"]


