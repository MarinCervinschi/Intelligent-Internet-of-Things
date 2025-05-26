import uuid
import paho.mqtt.client as mqtt
from typing import Any, ClassVar, Dict
from dataclasses import dataclass, field
from resources.smart_object_resource import SmartObjectResource
from messagge.telemetry_message import TelemetryMessage
from resources.gps_gpx_sensor_resource import GpsGpxSensorResource
from resources.resource_data_listener import ResourceDataListener
from model.gps_location_descriptor import GpsLocationDescriptor
from resources.battery_sensor_resource import BatterySensorResource
from conf.mqtt_conf_params import MqttConfigurationParameters


@dataclass
class VehicleMqttSmartObject:

    vehicle_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mqtt_client: mqtt.Client = None
    resource_map: Dict[str, SmartObjectResource] = None

    def __post_init__(self):
        """Init the vehicle smart object with its ID, the MQTT Client and the Map of managed resources"""
        print(
            "Vehicle Smart Object correctly created! Resource Number: %d"
            % (len(self.resource_map) if self.resource_map else 0)
        )

    def start(self) -> None:
        """Start vehicle behaviour"""
        try:
            if self.mqtt_client is not None and self.resource_map is not None:
                print("Starting Vehicle Emulator ....")

                self._register_to_control_channel()
                self.register_to_available_resources()
        except Exception as e:
            print(f"❌ - Error Starting the Vehicle Emulator ! Msg: {e}")

    def _register_to_control_channel(self):
        try:
            device_control_topic = "{0}/{1}/{2}".format(
                MqttConfigurationParameters.BASIC_TOPIC,
                self.vehicle_id,
                MqttConfigurationParameters.CONTROL_TOPIC,
            )

            print(f"Registering to Control Topic ({device_control_topic}) ... ")

            def on_message(client, userdata, msg):
                if msg is not None:
                    print(50 * "#")
                    print(
                        f"🖲️ [CONTROL CHANNEL] -> Control Message Received 📥 -> {msg.payload.decode()}"
                    )
                    print(50 * "#")
                else:
                    print("🖲️ [CONTROL CHANNEL] -> Null control message received 📥 !")

            self.mqtt_client.subscribe(device_control_topic)
            self.mqtt_client.message_callback_add(device_control_topic, on_message)

        except Exception as e:
            print(f"❌ - ERROR Registering to Control Channel ! Msg: {e}")

    def register_to_available_resources(self):
        try:
            for resource_key, resource_value in self.resource_map.items():
                if not resource_key or not resource_value:
                    continue

                smart_object_resource: SmartObjectResource = resource_value

                print(
                    "Registering to Resource %s (id: %s) notifications ..."
                    % (smart_object_resource.type, smart_object_resource.id)
                )
                # Register to GpsGpxSensorResource Notification

                if smart_object_resource.type == GpsGpxSensorResource.RESOURCE_TYPE:
                    gps_gpx_sensor_resource: GpsGpxSensorResource = (
                        smart_object_resource
                    )

                    listner = self._get_listener(
                        type=GpsLocationDescriptor,
                        resource_key=resource_key,
                        smart_object_resource=smart_object_resource,
                    )
                    gps_gpx_sensor_resource.add_data_listener(listner)

                # Register to BatterySensorResource Notification
                if smart_object_resource.type == BatterySensorResource.RESOURCE_TYPE:
                    battery_sensor_resource: BatterySensorResource = (
                        smart_object_resource
                    )
                    listner = self._get_listener(
                        type=float,
                        resource_key=resource_key,
                        smart_object_resource=smart_object_resource,
                    )
                    battery_sensor_resource.add_data_listener(listner)

        except Exception as e:
            print(f"❌ - Error Registering to Resource ! Msg: {e}")

    def stop(self):
        """Stop the emulated vehicle"""
        print("Stopping Vehicle Emulator ...")
        if self.resource_map:
            for resource in self.resource_map.values():
                for attr_name in dir(resource):
                    if attr_name.startswith("stop_periodic_"):
                        stop_method = getattr(resource, attr_name)
                        if callable(stop_method):
                            stop_method()

        if self.mqtt_client is not None:
            try:
                self.mqtt_client.disconnect()
                print("MQTT client disconnected.")
            except Exception as e:
                print(f"Error disconnecting MQTT client: {e}")

    def _get_listener(
        self, type: Any, resource_key: str, smart_object_resource: SmartObjectResource
    ):
        vehicle_id = self.vehicle_id
        publish_telemetry_data = self._publish_telemetry_data

        class Listener(ResourceDataListener[type]):
            def on_data_changed(self, resource, updated_value):
                try:
                    topic = "{0}/{1}/{2}/{3}".format(
                        MqttConfigurationParameters.BASIC_TOPIC,
                        vehicle_id,
                        MqttConfigurationParameters.TELEMETRY_TOPIC,
                        resource_key,
                    )
                    telemetry_message = TelemetryMessage(
                        smart_object_resource.type, updated_value
                    )

                    publish_telemetry_data(topic, telemetry_message)
                except Exception as e:
                    print(f"Error publishing telemetry data: {e}")

        return Listener()

    def _publish_telemetry_data(
        self, topic: str, telemetry_message: TelemetryMessage[Any]
    ):
        try:
            if topic is None or telemetry_message is None:
                print("❌ - Error: Topic or Msg = Null!")
                return

            print(f"📤 - Sending to topic: {topic} -> Data: {telemetry_message}")

            if self.mqtt_client is not None and self.mqtt_client.is_connected():
                message_payload = telemetry_message.to_json()
                self.mqtt_client.publish(
                    topic=topic, payload=message_payload, qos=0, retain=False
                )

                print(f"✅ - Data Correctly Published to topic: {topic}")
            else:
                print("❌ - Error: MQTT Client is not Connected !")
        except Exception as e:
            print(f"❌ - Exception in _publish_telemetry_data: {e}")
            raise
