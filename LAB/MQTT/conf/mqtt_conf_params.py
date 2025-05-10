class MqttConfigurationParameters(object):
    BROKER_ADDRESS = "127.0.0.1"
    BROKER_PORT = 7883
    MQTT_USERNAME = "marin"
    MQTT_PASSWORD = "UniMoRe"
    MQTT_BASIC_TOPIC = "/iot/user/{0}".format(MQTT_USERNAME)
    VEHICLE_TOPIC = "vehicle"
    VEHICLE_TELEMETRY_TOPIC = "telemetry"
    VEHICLE_INFO_TOPIC = "info"
