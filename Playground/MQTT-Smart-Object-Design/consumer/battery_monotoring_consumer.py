import uuid
import paho.mqtt.client as mqtt
from resources.battery_sensor_resource import BatterySensorResource
from messagge.telemetry_message import TelemetryMessage
from messagge.control_message import ControlMessage
import json
from typing import Dict, Any, Optional, ClassVar
from dataclasses import dataclass, field
import threading
from conf.mqtt_conf_params import MqttConfigurationParameters


@dataclass
class BatteryMonitoringConsumer:

    ALARM_BATTERY_LEVEL: ClassVar[float] = 2
    TARGET_TOPIC: ClassVar[str] = "fleet/vehicle/+/telemetry/battery"
    ALARM_MESSAGE_CONTROL_TYPE: ClassVar[str] = "battery_alarm_message"

    mqtt_client: mqtt.Client = None
    client_id: str = None
    is_alarm_notified: bool = field(default=False, init=False, repr=False)
    battery_history_map: Dict[str, float] = field(
        default_factory=dict, init=False, repr=False
    )

    def run(self):
        try:
            print("MQTT Consumer Tester Started ...")

            self.client_id = f"battery-monitor-{str(uuid.uuid4())}"
            self.mqtt_client = mqtt.Client(self.client_id)
            self.mqtt_client.connect(
                MqttConfigurationParameters.BROKER_ADDRESS,
                MqttConfigurationParameters.BROKER_PORT,
            )

            try:
                self.mqtt_client.on_connect = self.on_connect
                self.mqtt_client.on_message = self.on_message
                self.mqtt_client.loop_forever()
            except Exception as e:
                print(f"Connection failed: {e}")
            finally:
                self.mqtt_client.disconnect()

        except Exception as e:
            print(
                f"An error occurred while running the vehicle smart object process: {e}"
            )

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected ! 🐶🔋 Client Id: {self.client_id}")
            client.subscribe(self.TARGET_TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            telemetry_message = self._parse_telemetry_message_payload(msg)
            if (
                telemetry_message is not None
                and telemetry_message.type == BatterySensorResource.RESOURCE_TYPE
            ):
                new_battery_level = telemetry_message.data_value
                print(
                    f"New Battery Telemetry Data Received ! Battery Level: {new_battery_level} 🪫"
                )

                # if is the first value
                if (
                    msg.topic not in self.battery_history_map
                    or new_battery_level > self.battery_history_map[msg.topic]
                ):
                    print(f"💾 New Battery Level Saved for: {msg.topic}")
                    self.battery_history_map[msg.topic] = new_battery_level
                    self.is_alarm_notified = False
                else:
                    if (
                        self._is_battery_level_alarm(
                            self.battery_history_map[msg.topic], new_battery_level
                        )
                        and not self.is_alarm_notified
                    ):
                        print(30 * "-")
                        print(
                            "🚨 BATTERY LEVEL ALARM DETECTED ! Sending Control Notification ..."
                        )
                        self.is_alarm_notified = True
                        control_topic: str = "{0}/{1}".format(
                            msg.topic.replace("/telemetry/battery", ""),
                            self.CONTROL_TOPIC,
                        )
                        metadata = {
                            "charging_station_id": "cs00001",
                            "charging_station_lat": 44.79503800000001,
                            "charging_station_lng": 10.32686911666667,
                        }
                        control_message = ControlMessage(
                            self.ALARM_MESSAGE_CONTROL_TYPE, metadata
                        )
                        self.publish_control_message(control_topic, control_message)

        except Exception as e:
            print(f"❌ Failed to parse message: {e}")
            print(f"Raw Payload: {msg.payload}")

    def _is_battery_level_alarm(self, origin_value: float, new_value: float):
        return origin_value - new_value >= self.ALARM_BATTERY_LEVEL

    def _parse_telemetry_message_payload(self, msg) -> Optional[TelemetryMessage[Any]]:
        try:
            if msg is None or not hasattr(msg, "payload"):
                return None
            payload_str = msg.payload.decode()
            payload_json = json.loads(payload_str)
            return TelemetryMessage(
                payload_json["type"],
                payload_json["data_value"],
                timestamp=payload_json["timestamp"],
            )
        except Exception:
            return None

    def publish_control_message(
        self, topic: str, control_message: ControlMessage
    ) -> None:
        def publish():
            try:
                print(
                    f"📤 Publishing Control Message:\n  Topic: {topic}\n  Type: {control_message.type}"
                )
                print(f"  Metadata:")
                for k, v in control_message.metadata.items():
                    print(f"\t{k}: {v}")
                print(f"  Timestamp: {getattr(control_message, 'timestamp', 'N/A')}")

                if (
                    self.mqtt_client is not None
                    and self.mqtt_client.is_connected()
                    and control_message is not None
                    and topic is not None
                ):
                    message_payload = control_message.to_json()

                    self.mqtt_client.publish(
                        topic, payload=message_payload, qos=0, retain=False
                    )

                    print(f"✅ Data Correctly Published to topic: {topic}")
                else:
                    print(
                        "❌ Error: Topic or Msg = Null or MQTT Client is not Connected!"
                    )
                print(30 * "-")
            except Exception as e:
                print(f"Exception while publishing control message: {e}")

        threading.Thread(target=publish).start()


if __name__ == "__main__":
    app = BatteryMonitoringConsumer()
    app.run()
