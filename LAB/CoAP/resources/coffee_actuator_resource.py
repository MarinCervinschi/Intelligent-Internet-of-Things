import aiocoap.resource as resource
import aiocoap
from aiocoap.numbers.codes import Code
from model.coffee_history import CoffeeHistoryDescriptor
from request.make_coffee_request import MakeCoffeeRequestDescriptor
import json


class CoffeeActuatorResource(resource.ObservableResource):

    def __init__(self):
        super().__init__()
        self.coffee_history = CoffeeHistoryDescriptor()

    async def render_get(self, request):
        print("CoffeeActuatorResource -> GET Request Received ... ")
        payload_string = self.coffee_history.to_json()
        return aiocoap.Message(content_format=50, payload=payload_string.encode("utf8"))

    async def render_post(self, request):
        print("CoffeeActuatorResource -> POST Request Received ...")
        self.coffee_history.increase_short_coffee()
        self.updated_state()
        return aiocoap.Message(code=aiocoap.CHANGED)

    async def render_put(self, request):
        print("CoffeeActuatorResource -> PUT Byte payload : %s" % request.payload)
        json_payload_string = request.payload.decode("UTF-8")
        print("CoffeeActuatorResource -> PUT String Payload : %s" % json_payload_string)
        make_coffee_request = MakeCoffeeRequestDescriptor(
            **json.loads(json_payload_string)
        )
        print("Coffee Type Request Received : %s" % make_coffee_request.type)
        if make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_SHORT:
            self.coffee_history.increase_short_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_MEDIUM:
            self.coffee_history.increase_medium_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_LONG:
            self.coffee_history.increase_long_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        else:
            return aiocoap.Message(code=Code.BAD_REQUEST)
