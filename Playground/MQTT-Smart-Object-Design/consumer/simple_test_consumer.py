import uuid
import json
import paho.mqtt.client as mqtt
from conf.mqtt_conf_params import MqttConfigurationParameters

TARGET_TOPIC: str = "#"


def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        payload_json = json.loads(payload_str)
        print(f"\n--- MQTT Message Received ---")
        print(f"Topic      : {msg.topic}")
        print(f"Type       : {payload_json.get('type', 'N/A')}")
        print(f"Timestamp  : {payload_json.get('timestamp', 'N/A')}")
        data_value = payload_json.get("data_value", {})
        if isinstance(data_value, dict):
            print("Data Value :")
            for k, v in data_value.items():
                print(f"  {k}: {v}")
        else:
            print(f"Data Value : {data_value}")
        print("-----------------------------\n")
    except Exception as e:
        print(f"Failed to parse message: {e}")
        print(f"Raw Payload: {msg.payload}")


def run():
    try:
        print("MQTT Consumer Tester Started ...")

        client_id = f"client-id-{str(uuid.uuid4())}"
        mqtt_client = mqtt.Client(client_id)
        mqtt_client.connect(
            MqttConfigurationParameters.BROKER_ADDRESS,
            MqttConfigurationParameters.BROKER_PORT,
        )

        print(f"Connected ! 🐶 Client Id: {client_id}")

        mqtt_client.subscribe(TARGET_TOPIC)
        try:
            mqtt_client.on_message = on_message
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            mqtt_client.disconnect()

    except Exception as e:
        print(f"An error occurred while running the vehicle smart object process: {e}")


if __name__ == "__main__":
    run()
