import json
import random
import time


class CapsulePresenceSensorDescriptor:

    def __init__(self):
        self.timestamp = 0
        self.value = False

    def check_capsule_presence(self):
        self.value = bool(random.getrandbits(1))
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
