from abc import ABC, abstractmethod
import uuid

class Sensor(ABC):
    def __init__(self):
        self.sensor_id = uuid.uuid4()
        self.state = "Created"

    @abstractmethod
    def start_sensing(self):
        """Abstract method to start sensing."""
        pass

    @abstractmethod
    def stop_sensing(self):
        """Abstract method to stop sensing."""
        pass
    
    def enable_sensor(self):
        """Enables the sensor."""
        pass

    def disable_sensor(self):
        """Disables the sensor."""
        pass

    def start_data_streaming(self):
        """Start straming the sensor data"""
        pass

    def stop_data_streaming(self):
        """Stop straming the sensor data"""
        pass