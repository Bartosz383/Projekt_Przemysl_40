from flask import Flask, render_template, jsonify
import threading
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Dane globalne
sensor_data = []

# Obsługa MQTT
def on_message(client, userdata, message):
    global sensor_data
    data = json.loads(message.payload.decode())
    sensor_data.append(data)
    if len(sensor_data) > 100:  # Przechowuj maksymalnie 100 rekordów
        sensor_data.pop(0)

def mqtt_client():
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("iot/sensors")
    client.on_message = on_message
    client.loop_forever()

# API do pobierania danych
@app.route('/api/data')
def get_data():
    return jsonify(sensor_data)

# Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Start MQTT w wątku
thread = threading.Thread(target=mqtt_client)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(debug=True)
