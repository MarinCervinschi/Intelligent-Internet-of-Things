from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

ENDPOINT_PREFIX = "/api/iot/inventory"

print("Starting HTTP RESTful API Server ...")

@app.route('/')
def index():
    return "Welcome to the IoT Inventory API!"


if __name__ == '__main__':
    app.run()