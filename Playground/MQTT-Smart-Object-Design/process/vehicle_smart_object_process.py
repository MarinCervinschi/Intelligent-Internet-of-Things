import uuid
import paho.mqtt.client as mqtt
from device.VehicleMqttSmartObject import VehicleMqttSmartObject
from resources.gps_gpx_sensor_resource import GpsGpxSensorResource
from resources.battery_sensor_resource import BatterySensorResource
from conf.mqtt_conf_params import MqttConfigurationParameters


def run():
    try:
        vehicle_id = f"python-vehicle-id-{str(uuid.uuid4())}"
        mqtt_client = mqtt.Client(vehicle_id)
        mqtt_client.connect(
            MqttConfigurationParameters.BROKER_ADDRESS,
            MqttConfigurationParameters.BROKER_PORT,
        )

        resource_map = {
            "gps": GpsGpxSensorResource(),
            "battery": BatterySensorResource(),
        }

        vehicle_mqtt_smart_object = VehicleMqttSmartObject(
            vehicle_id, mqtt_client, resource_map
        )

        vehicle_mqtt_smart_object.start()
        mqtt_client.loop_start()

    except Exception as e:
        print(f"An error occurred while running the vehicle smart object process: {e}")


if __name__ == "__main__":
    run()
