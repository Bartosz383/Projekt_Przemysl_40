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
    data = {
        "timestamp": timestamp,
        "temperature": round(random.uniform(20.0, 22.0), 2),  # Temperatura
        "humidity": round(random.uniform(30.0, 35.0), 2),  # Wilgotność
        "position": round(random.uniform(-950.0, 1050.0), 2),  # Położenie
        "speed": round(random.uniform(100.0, 1000.0), 2),  # Prędkość
        "acceleration": round(random.uniform(10.0, 100.0), 2),  # Przyspieszenie
        "efficiency": round(random.uniform(0.0, 10.0), 2),  # Sprawność
        "voltage": round(random.uniform(0.0, 5.0), 2),  # Napięcie
        #"windspeed": round(random.uniform(0.0, 5.0), 2),  # Prędkość wiatru
    }
    return data

# Wysyłanie danych MQTT
client = mqtt.Client()
client.connect(broker, port)

try:
    while True:
        data = generate_data()
        payload = json.dumps(data)
        client.publish(topic, payload)
        print(f"Published: {payload}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Przerwano wysyłanie danych.")
    client.disconnect()
