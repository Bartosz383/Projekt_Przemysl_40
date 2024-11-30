import time
import random
import json
import paho.mqtt.client as mqtt
import numpy as np
from send_email import send_email  # Importujemy funkcję wysyłania e-maili

# Ustawienia MQTT
broker = "localhost"
port = 1883
topic = "iot/sensors"

# Parametry
t = 0  # Zmienna czasu (w sekundach)


# Funkcje generujące dane na podstawie wzorców matematycznych
def generate_data(t):
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())

    # Temperatura między 20 a 22 stopni
    temperature = round(20.0 + (2.0 * np.sin(t / 10.0)), 2)

    # Położenie, prędkość, przyspieszenie - wzory wahadła matematycznego
    position = round(1000 * np.sin(t / 5.0), 2)  # Przykładowe położenie
    speed = round(100 * np.cos(t / 5.0), 2)  # Prędkość
    acceleration = round(-100 * np.sin(t / 5.0), 2)  # Przyspieszenie (pochodna prędkości)

    # Sprawność - funkcja logarytmiczna
    efficiency = round(10 * np.log1p(t / 10.0), 2)  # Logarytm naturalny

    # Napięcie - funkcja sinusoidalna
    voltage = round(5.0 * np.sin(t / 5.0), 2)  # Sinusoidalny przebieg napięcia

    # Prędkość wiatru - losowa z przedziału 0 do 5 m/s
    windspeed = round(random.uniform(0.0, 5.0), 2)

    # Wilgotność - funkcja logarytmiczna
    humidity = round(50 + (50 * np.log1p(t / 5.0)), 2)  # Wilgotność rosnąca logarytmicznie

    data = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "position": position,
        "speed": speed,
        "acceleration": acceleration,
        "efficiency": efficiency,
        "voltage": voltage,
        "windspeed": windspeed,  # Dodanie prędkości wiatru
    }
    return data


# Wysyłanie danych MQTT
client = mqtt.Client()
client.connect(broker, port)

try:
    while True:
        data = generate_data(t)
        payload = json.dumps(data)
        client.publish(topic, payload)
        print(f"Published: {payload}")

        # Sprawdzenie, czy temperatura przekracza 21,5 stopnia
        if data["temperature"] > 31.5:
            send_email()  # Jeśli temperatura przekroczy 21,5 stopnia, wyślij e-mail

        t += 1  # Zwiększenie zmiennej czasu
        time.sleep(1)
except KeyboardInterrupt:
    print("Przerwano wysyłanie danych.")
    client.disconnect()
