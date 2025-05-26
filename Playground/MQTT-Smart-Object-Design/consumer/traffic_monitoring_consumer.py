import json
import threading
import uuid
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import paho.mqtt.client as mqtt

from resources.gps_gpx_sensor_resource import GpsGpxSensorResource
from model.traffic_event_descriptor import TrafficEventDescriptor
from messagge.telemetry_message import TelemetryMessage
from messagge.control_message import ControlMessage
from conf.mqtt_conf_params import MqttConfigurationParameters


ALARM_BATTERY_LEVEL = 2.0
TARGET_TOPIC = "fleet/vehicle/+/telemetry/gps"
ALARM_MESSAGE_CONTROL_TYPE = "traffic_alarm_message"
TRAFFIC_EVENT_DISTANCE_ALERT_THRESHOLD = 2  # km


@dataclass
class TrafficMonitoringConsumer:

    mqtt_client: mqtt.Client = None

    client_id: str = None
    is_alarm_notified: bool = field(default=False, init=False, repr=False)
    traffic_event_list: List[TrafficEventDescriptor] = None

    def __post_init__(self):
        self.traffic_event_list = self.init_demo_traffic_event()

    def init_demo_traffic_event(self) -> List[TrafficEventDescriptor]:
        return [
            TrafficEventDescriptor(
                type="jam_traffic_event",
                latitude=44.79503800000001,
                longitude=10.32686911666667,
                timestamp=int(time.time() * 1000),
            )
        ]

    def run(self):
        print("MQTT Consumer Started...")

        self.client_id = f"traffic-monitor-{uuid.uuid4()}"
        self.mqtt_client = mqtt.Client(client_id=self.client_id)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        try:
            self.mqtt_client.connect(
                MqttConfigurationParameters.BROKER_ADDRESS,
                MqttConfigurationParameters.BROKER_PORT,
            )
            self.mqtt_client.loop_forever()
        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            self.mqtt_client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected ! 🐶🚦 Client Id: {self.client_id}")
            client.subscribe(TARGET_TOPIC)
        else:
            print(f"❌ Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            telemetry_msg = self.parse_telemetry_message(payload)

            if (
                telemetry_msg
                and telemetry_msg.type == GpsGpxSensorResource.RESOURCE_TYPE
            ):

                gps_data = telemetry_msg.data_value
                print(
                    f"📍 New GPS Telemetry Data Received! Latitude: {gps_data.get('latitude')}, Longitude: {gps_data.get('longitude')}"
                )

                relevant_events = self.get_available_traffic_events(
                    gps_data["latitude"], gps_data["longitude"]
                )

                if relevant_events and not self.is_alarm_notified:
                    target_topic = msg.topic.replace(
                        "/telemetry/gps",
                        f"/{MqttConfigurationParameters.CONTROL_TOPIC}",
                    )
                    print(50 * "-")
                    print(
                        f"🚥 Relevant Traffic Event Detected! Sending Control to: {target_topic}"
                    )

                    control_msg = ControlMessage(
                        type=ALARM_MESSAGE_CONTROL_TYPE,
                        timestamp=int(time.time() * 1000),
                        metadata={"event_list": [e.__dict__ for e in relevant_events]},
                    )

                    self.publish_control_message(target_topic, control_msg)
                    self.is_alarm_notified = True

        except Exception as e:
            print(f"❌ Error processing message: {e}")

    def get_available_traffic_events(
        self, latitude: float, longitude: float
    ) -> List[TrafficEventDescriptor]:
        return [
            event
            for event in self.traffic_event_list
            if self.calculate_distance(
                latitude, longitude, event.latitude, event.longitude
            )
            <= TRAFFIC_EVENT_DISTANCE_ALERT_THRESHOLD
        ]

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Simplified distance calculation - replace with proper implementation
        return (
            (lat1 - lat2) ** 2 + (lon1 - lon2) ** 2
        ) ** 0.5 * 111  # Approximate km conversion

    @staticmethod
    def parse_telemetry_message(payload: str) -> Optional[TelemetryMessage]:
        try:
            payload_json = json.loads(payload)
            return TelemetryMessage(
                payload_json["type"],
                payload_json["data_value"],
                timestamp=payload_json["timestamp"],
            )
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse message: {e}")
            return None

    def publish_control_message(self, topic: str, message: ControlMessage):
        def publish():
            try:
                payload = message.to_json()
                result = self.mqtt_client.publish(topic, payload, qos=0, retain=False)

                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"✅ Control message published to {topic}")
                else:
                    print(f"❌ Failed to publish message: {result}")

            except Exception as e:
                print(f"❌ Error publishing message: {e}")

            print(50 * "-")

        threading.Thread(target=publish).start()


if __name__ == "__main__":
    import time

    consumer = TrafficMonitoringConsumer()
    consumer.run()
