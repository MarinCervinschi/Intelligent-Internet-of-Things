import logging
import asyncio
import link_header
from aiocoap import *
import json
from request.make_coffee_request import MakeCoffeeRequestDescriptor

logging.basicConfig(level=logging.INFO)

RT_TEMPERATURE_SENSOR = "it.unimore.device.sensor.temperature"
RT_CAPSULE_SENSOR = "it.unimore.device.sensor.capsule_presence"
RT_COFFEE_ACTUATOR = "it.unimore.device.actuator.coffee"
TARGET_ENDPOINT = "coap://127.0.0.1:5683"
WELL_KNOWN_CORE_URI = "/.well-known/core"

target_temperature_sensor_uri = None
target_capsule_presence_sensor_uri = None
target_coffee_actuator_uri = None

COFFEE_TYPE = {
    "short": MakeCoffeeRequestDescriptor.COFFEE_TYPE_SHORT,
    "medium": MakeCoffeeRequestDescriptor.COFFEE_TYPE_MEDIUM,
    "long": MakeCoffeeRequestDescriptor.COFFEE_TYPE_LONG,
}


def is_device_valid(core_link_format_response):
    global target_capsule_presence_sensor_uri, target_temperature_sensor_uri, target_coffee_actuator_uri
    links_headers = link_header.parse(core_link_format_response)
    for link in links_headers.links:
        if link.href != WELL_KNOWN_CORE_URI:
            for pair in link.attr_pairs:
                key = pair[0]
                value = pair[1]
                if key == "rt" and value == RT_TEMPERATURE_SENSOR:
                    target_temperature_sensor_uri = link.href
                elif key == "rt" and value == RT_CAPSULE_SENSOR:
                    target_capsule_presence_sensor_uri = link.href
                elif key == "rt" and value == RT_COFFEE_ACTUATOR:
                    target_coffee_actuator_uri = link.href

    if (
        target_capsule_presence_sensor_uri is not None
        and target_capsule_presence_sensor_uri is not None
        and target_coffee_actuator_uri is not None
    ):
        print("Temperature Sensor Uri: " + target_temperature_sensor_uri)
        print("Capsule Presence Sensor Uri: " + target_capsule_presence_sensor_uri)
        print("Coffee Actuator Sensor Uri: " + target_coffee_actuator_uri)
        return True
    else:
        return False


async def is_coffee_capsule_available(coap_client):
    request = Message(
        code=Code.GET, uri=TARGET_ENDPOINT + target_capsule_presence_sensor_uri
    )
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        return False
    else:
        response_string = response.payload.decode("utf-8")
        json_senml = json.loads(response_string)
        if json_senml[0]["vb"] == True:
            return True
        else:
            return False


async def trigger_coffee(coap_client, coffee_type="short"):
    request = Message(code=Code.PUT, uri=TARGET_ENDPOINT + target_coffee_actuator_uri)
    coffee_request = MakeCoffeeRequestDescriptor(COFFEE_TYPE[coffee_type])

    payload_json_string = coffee_request.to_json()
    request.payload = payload_json_string.encode("utf-8")
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        print("Failed to fetch resources:")
        print(e)
    else:
        if response.code.is_successful():
            return True
        else:
            return False


def ask_coffee_type():
    print("\nChoose coffee type:")
    print("1. Short (default)")
    print("2. Medium")
    print("3. Long")
    choice = input("Select coffee type [1/2/3]: ").strip()
    if choice == "2":
        return "medium"
    elif choice == "3":
        return "long"
    return "short"


async def main():

    coap_client = await Context.create_client_context()

    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + WELL_KNOWN_CORE_URI)

    try:
        response = await coap_client.request(request).response
    except Exception as e:
        print("Failed to fetch resource:")
        print(e)
    else:
        response_string = response.payload.decode("utf-8")
        print(response_string)
        if is_device_valid(response_string):
            print("Valid Target Device Detected !")
            if await is_coffee_capsule_available(coap_client):
                print("Capsule Available !")
                coffee_type = ask_coffee_type()
                coffee_result = await trigger_coffee(coap_client, coffee_type)
                if coffee_result == True:
                    print(f"Drink your {coffee_type} Coffee ☕️! ✅")
                else:
                    print("Error making Coffee ! Please try later ...")
            else:
                print("Capsule Not Available 😭! Stopping ...❌")
        else:
            print("Error: Invalid Device Detected !")


if __name__ == "__main__":
    asyncio.run(main())
