# from sensors import sensor as s
from sensors.sensor import Sensor
import cv2
from matplotlib import pyplot as plt

class Camera(Sensor):
    def __init__(self, port, resolution):
        self.port = port
        self.resolution = resolution
        
    def enable_sensor(self):
        """Enables camera sensing by instantiating the cap(capture) instance variable and assigning it a port"""
        self.cap = cv2.VideoCapture(self.port)
        
    def disable_sensor(self):
        """ """
        self.cap.release()
        
    def start_sensing(self):
        """    """
        self.state = "Running"
        print("Iniciando la detección de la cámara.")

    def stop_sensing(self):
        """     """
        self.state = "Paused"
        print("Deteniendo la detección de la cámara.")
        
    def test_camera(self):
        """     """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            cv2.imshow('Webcam', frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        self.cap.release()
        cv2.destroyAllWindows()
        
    def get_state(self):
        return self.state
        