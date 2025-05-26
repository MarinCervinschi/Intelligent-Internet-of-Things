from typing import ClassVar

class MqttConfigurationParameters(object):
    BROKER_ADDRESS: ClassVar[str] = "127.0.0.1"
    BROKER_PORT: ClassVar[int] = 7883
    BASIC_TOPIC: ClassVar[str] = "fleet/vehicle"
    TELEMETRY_TOPIC: ClassVar[str] = "telemetry"
    EVENT_TOPIC: ClassVar[str] = "event"
    CONTROL_TOPIC: ClassVar[str] = "control"
    COMMAND_TOPIC: ClassVar[str] = "command"