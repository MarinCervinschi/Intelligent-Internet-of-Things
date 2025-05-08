from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse


class DeviceResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs["data_manager"]

    def get(self, device_id):
        if device_id in self.dataManager.device_dictionary:
            return self.dataManager.device_dictionary[device_id].__dict__, 200
        else:
            return {"error ": " Device Not Found !"}, 404
