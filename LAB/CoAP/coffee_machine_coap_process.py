import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
from resources.temperature_sensor_resource import TemperatureSensorResource
from resources.coffee_actuator_resource import CoffeeActuatorResource
from resources.capsule_presence_sensor_resource import CapsulePresenceSensorResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.INFO)
# logging.getLogger("coap-server").setLevel(logging.DEBUG)


async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(["temperature"], TemperatureSensorResource())
    root.add_resource(["capsule"], CapsulePresenceSensorResource())
    root.add_resource(["coffee"], CoffeeActuatorResource())
    await aiocoap.Context.create_server_context(root, bind=("127.0.0.1", 5683))
    await asyncio.get_event_loop().create_future()  # Keeps the loop running


if __name__ == "__main__":
    asyncio.run(main())
