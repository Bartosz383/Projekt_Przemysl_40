import time
import random
import json
import paho.mqtt.client as mqtt
import numpy as np

# Ustawienia MQTT
broker = "localhost"
port = 1883
topic = "iot/sensors"

# Symulacja danych
def generate_data():
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    temperature = round(random.uniform(20.0, 30.0), 2)  # Temperatura
    humidity = round(random.uniform(30.0, 70.0), 2)  # Wilgotność
    position = [round(np.sin(time.time()), 2), round(np.cos(time.time()), 2), 0.0]
    speed = round(abs(np.sin(time.time())), 2)
    voltage = round(random.uniform(1.0, 5.0), 2)  # Napięcie
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "position": position,
        "speed": speed,
        "voltage": voltage,
    }

# Wysyłanie danych MQTT
client = mqtt.Client()
client.connect(broker, port)

while True:
    data = generate_data()
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"Published: {payload}")
    time.sleep(1)
