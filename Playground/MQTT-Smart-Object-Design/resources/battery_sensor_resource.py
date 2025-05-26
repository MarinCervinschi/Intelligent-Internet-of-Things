import uuid
import random
import threading
from dataclasses import dataclass, field
from resources.smart_object_resource import SmartObjectResource
from resources.resource_data_listener import ResourceDataListener
from typing import Optional, ClassVar


@dataclass
class BatterySensorResource(SmartObjectResource[float]):
    """
    A battery sensor resource that periodically updates its battery level
    and notifies listeners of changes.
    """

    RESOURCE_TYPE: ClassVar[str] = "🔋iot:sensor:battery"
    MIN_BATTERY_LEVEL: ClassVar[float] = 50.0
    MAX_BATTERY_LEVEL: ClassVar[float] = 70.0
    MIN_BATTERY_LEVEL_CONSUMPTION: ClassVar[float] = 0.1
    MAX_BATTERY_LEVEL_CONSUMPTION: ClassVar[float] = 1.0
    UPDATE_PERIOD: ClassVar[int] = 5  # seconds
    TASK_DELAY_TIME: ClassVar[int] = 5  # seconds

    updated_battery_level: float = field(init=False)
    _timer: Optional[threading.Timer] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Initialize after dataclass construction"""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.type is None:
            self.type = self.RESOURCE_TYPE

        self.updated_battery_level = self.MIN_BATTERY_LEVEL + random.random() * (
            self.MAX_BATTERY_LEVEL - self.MIN_BATTERY_LEVEL
        )
        self.start_periodic_event_value_update_task()

    def load_updated_value(self) -> float:
        """Return the current battery level"""
        return self.updated_battery_level

    def start_periodic_event_value_update_task(self) -> None:
        """Start the periodic battery level update task"""

        print(
            f"🔋 - Starting periodic Update Task with Period: {self.UPDATE_PERIOD} ms"
        )

        def update_task():
            try:
                consumption = random.uniform(
                    self.MIN_BATTERY_LEVEL_CONSUMPTION,
                    self.MAX_BATTERY_LEVEL_CONSUMPTION,
                )
                self.updated_battery_level = max(
                    0.0, self.updated_battery_level - consumption
                )

                if self.updated_battery_level <= 0.0:
                    print("Battery depleted!")
                    self.stop_periodic_event_value_update_task()
                    return

                self.notify_update(self.updated_battery_level)

                self._timer = threading.Timer(self.UPDATE_PERIOD, update_task)
                self._timer.start()
            except Exception as e:
                print(f"Error updating battery level: {e}")

        self._timer = threading.Timer(self.TASK_DELAY_TIME, update_task)
        self._timer.start()

    def stop_periodic_event_value_update_task(self) -> None:
        """Stop the periodic update task"""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def __del__(self):
        """Ensure timer is stopped when instance is deleted"""
        self.stop_periodic_event_value_update_task()


if __name__ == "__main__":

    battery_sensor = BatterySensorResource()
    print(
        "New %s Resource Created with Id: %s ! Battery Level: %.2f"
        % (battery_sensor.type, battery_sensor.id, battery_sensor.load_updated_value())
    )

    class Listner(ResourceDataListener[float]):
        def on_data_changed(self, resource, updated_value):
            if resource is not None and updated_value is not None:
                print(
                    "Device: %s -> New Battery Level Received: %.2f"
                    % (resource.id, updated_value)
                )
            else:
                print("on_data_changed Callback -> Null Resource or Updated Value !")

    battery_sensor.add_data_listener(Listner())
