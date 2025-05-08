from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse
from model.device_model import DeviceModel

class DevicesResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    def get(self):
        device_list = [device.__dict__ for device in self.dataManager.devices_dictionary.values()]
        return device_list, 200
