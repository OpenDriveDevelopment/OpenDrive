from typing import List
from enum import Enum

class SensorPosition(Enum):
    FRONTAL = "Frontal"
    REAR = "Rear"
    SIDE = "Side"
    CUSTOM = "Custom"

class SensorType(Enum):
    CAMERA = "Camera"
    LIDAR = "Lidar"
    CUSTOM = "Custom"


class SensorToModelPipeline:
    
    SENSOR_TYPES = [e.value for e in SensorType]
    SENSOR_POSITIONS = [e.value for e in SensorPosition]
    
    def __init__(self, input_sensor: str, sensor_type: str, sensor_position: str, output_decision: str , perceptions: List[str] = None):
        """
        Parameters:
            input_sensor (str): The name of the input sensor.
            sensor_type (str): The type of sensor. Must be one of ['Camera', 'Lidar', 'Custom'].
            sensor_pos (str): The position of the sensor. Must be one of ['Frontal', 'Rear', 'Side', 'Custom'].
            output_decision (str): The output decision.
            perceptions (List[str], optional): List of perception tasks. Assigned automatically if not provided.
        """
        
        ## Check for sensor type and position 
        if sensor_type.capitalize() not in self.SENSOR_TYPES:
            raise ValueError(f"Invalid sensor_type '{sensor_type}'. Must be one of {self.SENSOR_TYPES}.")
        
        
        if sensor_position.capitalize() not in self.SENSOR_POSITIONS:
            raise ValueError(f"Invalid sensor_pos '{sensor_position}'. Must be one of {self.SENSOR_POSITIONS}.")
        
        
        ## Check for perceptions values
        if sensor_type == SensorType.CUSTOM.value or sensor_position == SensorPosition.CUSTOM.value:
                if perceptions is None or len(perceptions) == 0:
                    raise ValueError("Perceptions must be provided manually when sensor_type or sensor_pos is 'Custom'.")
        else:
            if perceptions is None:
                perceptions = self._assign_default_perceptions(sensor_type, sensor_position)
            
        
        self.input_sensor = input_sensor
        self.sensor_type = sensor_type
        self.sensor_position = sensor_position
        self.perceptions = perceptions
        self.output_decision = output_decision

    
    
    @staticmethod
    def _assign_default_perceptions(sensor_type: str, sensor_pos: str) -> List[str]:
        """
        Assign default perceptions based on sensor type and position.
        """
        if sensor_type == SensorType.CAMERA.value:
            if sensor_pos == SensorPosition.FRONTAL.value:
                return ["lane", "signals", "objects", "distance"]
            elif sensor_pos == SensorPosition.REAR.value:
                return ["objects","distance"]
            elif sensor_pos == SensorPosition.SIDE.value:
                return ["objects"]
            elif sensor_pos == SensorPosition.CUSTOM.value:
                return []
        else:
            return []
        
        # None of the above cases match
        return []