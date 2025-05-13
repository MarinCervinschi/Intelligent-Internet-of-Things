import aiocoap.resource as resource
import aiocoap
from model.capsule_presence_sensor import CapsulePresenceSensorDescriptor


class CapsulePresenceSensorResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.sensor = CapsulePresenceSensorDescriptor()

    async def render_get(self, request):
        print("CapsulePresenceResource -> GET Request Received ...")
        print("CapsulePresenceResource -> Check Capsule Presence ...")
        self.sensor.check_capsule_presence()
        print(
            "CapsulePresenceResource -> Updated Capsule Presence Sensor Value : %f"
            % self.sensor.value
        )
        payload_string = self.sensor.to_json()
        return aiocoap.Message(content_format=50, payload=payload_string.encode("utf8"))
