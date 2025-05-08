from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse
from model.device_model import DeviceModel


class DeviceResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs["data_manager"]

    def get(self, device_id):
        if device_id in self.dataManager.device_dictionary:
            return self.dataManager.device_dictionary[device_id].__dict__, 200
        else:
            return {"error ": " Device Not Found !"}, 404

    def put(self, device_id):
        try:
            if device_id not in self.dataManager.device_dictionary:
                return {"error": "Device UUID does't exists"}, 404
            else:
                json_data = request.get_json(force=True)
                updatedDevice = DeviceModel(**json_data)

                self.dataManager.update_device(updatedDevice)
                return Response(
                    status=204,
                    headers={"Location": request.url + "/" + device_id},
                )
        except JSONDecodeError:
            return {"error": "Invalid JSON ! Check the request"}, 400

        except Exception as e:
            return {"error": "Generic Internal Server Error ! Reason : " + str(e)}, 500

    def delete(self, device_id):
        try:
            if device_id not in self.dataManager.device_dictionary:
                return {"error": "Device UUID does't exists"}, 404

            self.dataManager.remove_device(device_id)
            return Response(status=204)
        except Exception as e:
            return {"error": "Generic Internal Server Error ! Reason : " + str(e)}, 500
