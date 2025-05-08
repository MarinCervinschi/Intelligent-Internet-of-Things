from flask import Flask
from flask_restful import Resource, Api, reqparse
from resources.devices_resource import DevicesResource
from model.device_model import DeviceModel
from persistence.data_manager import DataManager

app = Flask(__name__)
api = Api(app)

ENDPOINT_PREFIX = "/api/iot/inventory"

print("Starting HTTP RESTful API Server ...")

dataManager = DataManager()

demoDevice = DeviceModel(
    " device00001 ", " iot : demosensor ", "v0 .0.0.1 ", "Acme - Inc "
)

dataManager.add_device(demoDevice)

api.add_resource(
    DevicesResource,
    ENDPOINT_PREFIX + "/device",
    resource_class_kwargs={"data_manager": dataManager},
    endpoint="devices",
    methods=["GET", "POST"],
)

if __name__ == "__main__":
    app.run()
