from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
import json
from resources.resource_data_listener import ResourceDataListener

T = TypeVar("T")


@dataclass
class SmartObjectResource(ABC, Generic[T]):
    """
    Abstract base class for observable resources using dataclass.
    Maintains the listener pattern while gaining dataclass benefits.
    """

    id: str = None
    type: str = None
    resource_listener_list: List[ResourceDataListener] = field(
        default_factory=list, init=False, repr=False
    )

    @abstractmethod
    def load_updated_value(self) -> T:
        """Abstract method to load the updated resource value"""
        pass

    def add_data_listener(self, resource_data_listener: ResourceDataListener) -> None:
        """Add a new listener to be notified of changes"""
        if resource_data_listener not in self.resource_listener_list:
            self.resource_listener_list.append(resource_data_listener)

    def remove_data_listener(
        self, resource_data_listener: ResourceDataListener
    ) -> None:
        """Remove an existing listener"""
        if resource_data_listener in self.resource_listener_list:
            self.resource_listener_list.remove(resource_data_listener)

    def notify_update(self, updated_value: T) -> None:
        """Notify all registered listeners of a value change"""
        if not self.resource_listener_list:
            print("No active listeners - nothing to notify")
            return

        for listener in self.resource_listener_list:
            if listener is not None:
                listener.on_data_changed(self, updated_value)

    def to_json(self) -> str:
        """Serialize the resource to JSON, excluding non-serializable fields"""
        data = {
            "id": self.id,
            "type": self.type,
        }
        return json.dumps(data)
