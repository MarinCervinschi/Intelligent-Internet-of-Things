import aiocoap.resource as resource
import aiocoap
from model.temperature_sensor import TemperatureSensorDescriptor


class TemperatureSensorResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.temperature_sensor = TemperatureSensorDescriptor()

    async def render_get(self, request):
        print("TemperatureSensorResource -> GET Request Received ...")
        print("TemperatureSensorResource -> Reading updated temperature value ...")
        self.temperature_sensor.measure_temperature()
        print(
            "TemperatureSensorResource -> Updated Temperature Value : %f"
            % self.temperature_sensor.value
        )

        payload_string = self.temperature_sensor.to_json()

        return aiocoap.Message(content_format=50, payload=payload_string.encode('utf8'))
