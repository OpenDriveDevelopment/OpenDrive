import cv2
import asyncio
from matplotlib import pyplot as plt
from OpenDrive.modules.sensors_prep.sensors.sensor import Sensor
from OpenDrive.modules.stream_processing.producer import DataProducer

class Camera(Sensor):
    def __init__(self, port, resolution):
        self.port = port
        self.resolution = resolution
        self.streaming = False
        
    def enable_sensor(self):
        """Enables camera sensing by instantiating the cap(capture) instance variable and assigning it a port"""
        self.cap = cv2.VideoCapture(self.port)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Resolución actual de la cámara: {width}x{height}")
        
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

    async def start_data_streaming(self):
        self.streaming = True
        producer = DataProducer("sensor", "camera", self.port)
        
        while self.streaming:
            print("Producing sensor data")
            
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if ret:
                        message_value = buffer.tobytes()
                        # Offload send_data to a thread to avoid blocking
                        await asyncio.get_running_loop().run_in_executor(
                            None, producer.send_data, message_value
                        )
                    else:
                        print("Error serializing frame")
                else:
                    print("Error capturing frame")
            else:
                print("Camera not open")

            await asyncio.sleep(3)

        print("Data streaming stopped")

    def stop_data_streaming(self):
        """Sets the flag to stop the data streaming."""
        print("Stopping Data streaming")
        self.streaming = False
        
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
        