import logging
import asyncio
import aiocoap
from aiocoap import *
import json

logging.basicConfig(level=logging.INFO)


def print_payload(r, message, pretty=False):
    if pretty:
        try:
            payload = r.payload.decode("utf-8")
            data = json.loads(payload)
            print(message)
            for item in data:
                print(f"  {item['n']}: {item['v']}")
        except Exception as e:
            print("Failed to parse first response payload:", e)
            print("Raw payload:", r.payload)
    else:
        print("%s %s\n%r" % (message, r, r.payload))


PRETTY = False


async def main():
    protocol = await Context.create_client_context()

    request = Message(code=aiocoap.GET, uri="coap://127.0.0.1:5683/coffee", observe=0)

    protocol_request = protocol.request(request)

    r = await protocol_request.response
    print_payload(r, "First response:", pretty=PRETTY)

    received_observation = 0

    async for r in protocol_request.observation:
        print_payload(r, "Next result:", pretty=PRETTY)

        received_observation += 1
        if received_observation == 10:
            print("Canceling Observation ...")
            protocol_request.observation.cancel()
            break

    await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
