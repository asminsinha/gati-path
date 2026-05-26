# real_hardware_listener.py
import json
import httpx
import paho.mqtt.client as mqtt


MQTT_BROKER = "broker.hivemq.com"  
MQTT_TOPIC = "vitarai/fleet/telemetry/#"
ROUTER_URL = "http://127.0.0.1:8000/gati-path/iot-ping"

# 2. This event triggers ONLY when an actual truck transmits a wireless packet
def on_message(client, userdata, msg):
    try:
        raw_payload = msg.payload.decode("utf-8")
        hardware_sensor_data = json.loads(raw_payload)
        
        tracking_id = hardware_sensor_data["tracking_id"]
        print(f"📡 [WIRELESS CELL FRAME RECEIVED] From Truck: {tracking_id}")
        
        compiled_packet = {
            "tracking_id":              tracking_id,
            "lat":                      float(hardware_sensor_data["lat"]),
            "lng":                      float(hardware_sensor_data["lng"]),
            "current_fuel_liters":       float(hardware_sensor_data["fuel"]),
            "cargo_load_kg":            float(hardware_sensor_data["load"]),
            "hours_driven_without_rest": float(hardware_sensor_data["hours"])
        }
        
        response = httpx.post(ROUTER_URL, json=compiled_packet)
        print(f" [Router Updated] Server Cache Status: {response.status_code}")
        
    except Exception as e:
        print(f" Error parsing hardware packet: {e}")

# 3. Initialize the background listener engine
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

print(" Connecting Python backend to Cellular Ingestion Network...")
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_forever()