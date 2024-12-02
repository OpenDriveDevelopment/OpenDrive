import cv2
import asyncio
from OpenDrive.modules.sensors_prep.sensors.sensor import Sensor
from OpenDrive.modules.stream_processing.producer import DataProducer
import json
import base64
import platform

class Camera(Sensor):
    def __init__(self, port, sensing_speed: int = 0.1):
        super().__init__() 
        self.port = port
        self.sensing_speed = sensing_speed
        self.streaming = False
        
    def enable_sensor(self):
        """Enables camera sensing by instantiating the cap(capture) instance variable and assigning it a port"""
        try:
            # self.cap = cv2.VideoCapture(self.port)
            # self.cap = cv2.VideoCapture(self.port, cv2.CAP_MSMF)
            # self.cap = cv2.VideoCapture(self.port, cv2.CAP_DSHOW)
            # print(platform.system())
            
            if platform.system() == "Windows": # Windows Operative System
                self.cap = cv2.VideoCapture(self.port, cv2.CAP_DSHOW)
            elif platform.system() == "Linux" or platform.system() == "Darwin":  # Linux y macOS operative system
                self.cap = cv2.VideoCapture(self.port)
            else:
                raise OSError("[ERROR] Operative System not Supported")
            
            if not self.cap.isOpened():
                raise Exception(f"[ERROR] Failed to open the camera on port {self.port}.")
            
            self.state = "Enabled"
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"[INFO] Camera on port {self.port} is enabled.")
            print(f"[INFO] Camera resolution: {width}x{height}.")
                      
        except Exception as e:
            self.state = "Error"
            print(f"[ERROR] Error enabling the camera on port {self.port} : {e}")
            self.cap = None
            
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

    async def start_data_streaming(self, start_time, loglevel):
        
        if not self.cap or not self.cap.isOpened():
            print(f"[ERROR] Camera on port {self.port} is not ready for streaming.")
            self.streaming = False
            return
        
        self.streaming = True
        producer = DataProducer("sensor", "camera", self.port, loglevel=loglevel) 
        
        sensing_interval_ns = int(self.sensing_speed * 1e9)
        recurrent_time = start_time
        
        if loglevel == 0:
            print(f"[INFO] Camera from port {self.port} is producing data")
        
        while self.streaming:
            if loglevel == 1:
                print(f"[INFO] Camera from port {self.port} producing data")
            
            ret, frame = self.cap.read()
            if ret:
                success, buffer = cv2.imencode('.jpg', frame)
                if success:
                    #serializamos el frame
                    message_value = buffer.tobytes()
                    encoded_message  = base64.b64encode(message_value).decode('utf-8')
                    
                    #Obtenemos el alto y ancho del frame
                    height, width, _ = frame.shape
                    
                    recurrent_time += sensing_interval_ns
                    #creamos objeto que representara la data generada
                    result_payload = {
                        "timestamp": int(recurrent_time),
                        "sensor_data": encoded_message,
                        "width": int(width),
                        "height": int(height)
                    }
                    
                    serialized_result = json.dumps(result_payload).encode('utf-8')
                    
                    # Offload send_data to a thread to avoid blocking
                    await asyncio.get_running_loop().run_in_executor(
                        None, producer.send_data, serialized_result
                    )
                else:
                    print("Error serializing frame")
            else:
                print(f"[ERROR] Error capturing frame on port {self.port}")
        

            await asyncio.sleep(self.sensing_speed)

        print("Data streaming stopped")

    def stop_data_streaming(self):
        """Sets the flag to stop the data streaming."""
        print("Stopping Data streaming")
        self.streaming = False
        
    def test_camera(self):
        """     """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            cv2.imshow(f'Webcam from port {self.port}', frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        self.cap.release()
        cv2.destroyAllWindows()
        
    def get_state(self):
        return self.state
        