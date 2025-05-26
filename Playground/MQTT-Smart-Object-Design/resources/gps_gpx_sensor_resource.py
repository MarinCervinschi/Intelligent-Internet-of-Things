from dataclasses import dataclass, field
from typing import List, Optional, ClassVar
import uuid
import gpxpy
import threading
from resources.smart_object_resource import SmartObjectResource
from resources.resource_data_listener import ResourceDataListener
from model.gps_location_descriptor import GpsLocationDescriptor


@dataclass
class GPXTrackPoint:
    """Represents a single GPS track point from GPX file"""

    latitude: float
    longitude: float
    elevation: Optional[float] = None
    time: Optional[str] = None


@dataclass
class GpsGpxSensorResource(SmartObjectResource[GpsLocationDescriptor]):
    """
    A GPS sensor resource that reads waypoints from a GPX file and
    simulates movement by iterating through them.
    """

    # Class constants
    RESOURCE_TYPE: ClassVar[str] = "📍iot:sensor:gps"
    GPX_FILE_NAME: ClassVar[str] = "tracks/demo.gpx"
    UPDATE_PERIOD: ClassVar[int] = 1  # seconds
    TASK_DELAY_TIME: ClassVar[int] = 5  # seconds

    # Instance variables
    way_point_list: List[GPXTrackPoint] = field(default_factory=list, init=False)
    updated_location: Optional[GpsLocationDescriptor] = field(default=None, init=False)
    _way_point_index: int = field(default=0, init=False, repr=False)
    _reverse: bool = field(default=False, init=False, repr=False)
    _update_timer: Optional[threading.Timer] = field(
        default=None, init=False, repr=False
    )

    def __post_init__(self):
        """Initialize after dataclass construction"""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.type is None:
            self.type = self.RESOURCE_TYPE

        try:
            self.way_point_list = self._load_gpx_waypoints()
            print(f"GPX File loaded with {len(self.way_point_list)} waypoints")
            self._start_periodic_update_task()
        except Exception as e:
            print(f"Error initializing GPS resource: {e}")
            raise

    def _load_gpx_waypoints(self) -> List[GPXTrackPoint]:
        """Load waypoints from GPX file"""
        with open(self.GPX_FILE_NAME, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            return [
                GPXTrackPoint(
                    latitude=point.latitude,
                    longitude=point.longitude,
                    elevation=point.elevation,
                    time=point.time.isoformat() if point.time else None,
                )
                for track in gpx.tracks
                for segment in track.segments
                for point in segment.points
            ]

    def _start_periodic_update_task(self) -> None:
        """Start the periodic location update task"""

        print(f"📍 - Starting periodic Update Task with Period: {self.UPDATE_PERIOD} ms")

        def update_task():
            try:
                if not self.way_point_list:
                    return

                # Get current waypoint
                current_point = self.way_point_list[self._way_point_index]

                # Update location descriptor
                self.updated_location = GpsLocationDescriptor(
                    latitude=current_point.latitude,
                    longitude=current_point.longitude,
                    elevation=current_point.elevation or 0.0,
                    provider=GpsLocationDescriptor.FILE_LOCATION_PROVIDER,
                )

                # Notify listeners
                self.notify_update(self.updated_location)

                # Update index and handle direction changes
                self._way_point_index += 1 if not self._reverse else -1

                if self._way_point_index >= len(self.way_point_list):
                    self._handle_direction_change(reverse=True)
                elif self._way_point_index < 0:
                    self._handle_direction_change(reverse=False)

                # Schedule next update
                self._update_timer = threading.Timer(self.UPDATE_PERIOD, update_task)
                self._update_timer.start()

            except Exception as e:
                print(f"Error in GPS update task: {e}")

        self._update_timer = threading.Timer(self.TASK_DELAY_TIME, update_task)
        self._update_timer.start()

    def _handle_direction_change(self, reverse: bool) -> None:
        """Handle reversing direction when reaching end of waypoints"""
        self.way_point_list.reverse()
        self._way_point_index = 0
        self._reverse = not self._reverse
        direction = "backward" if reverse else "forward"
        print(f"Reversing direction, now iterating {direction}")

    def load_updated_value(self) -> Optional[GpsLocationDescriptor]:
        """Return the current GPS location"""
        return self.updated_location

    def stop_periodic_update_task(self) -> None:
        """Stop the periodic updates"""
        if self._update_timer:
            self._update_timer.cancel()
            self._update_timer = None

    def __del__(self):
        """Ensure timer is stopped when instance is deleted"""
        self.stop_updates()


if __name__ == "__main__":
    try:
        gps_gpx_sensor_resource = GpsGpxSensorResource()

        print(
            "New %s Resource Created with Id: %s ! Updated Value: %s"
            % (
                gps_gpx_sensor_resource.type,
                gps_gpx_sensor_resource.id,
                gps_gpx_sensor_resource.load_updated_value(),
            )
        )

        class Listener(ResourceDataListener[GpsLocationDescriptor]):
            def on_data_changed(self, resource, updated_value):
                if resource is not None and updated_value is not None:
                    print(
                        f"Device: {resource.id} -> New Value Received: {updated_value}"
                    )
                else:
                    print("onDataChanged Callback -> Null Resource or Updated Value !")

        gps_gpx_sensor_resource.add_data_listener(Listener())

    except KeyboardInterrupt:
        print("Exiting...")
