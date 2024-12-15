# import cv2
# import asyncio
# from OpenDrive.modules.sensors_prep.sensors.sensor import Sensor
# from OpenDrive.modules.stream_processing.producer import DataProducer
# import json
# import base64
# import platform

# class Video(Sensor):
#     def __init__(self, video_path, sensing_speed: int = 1):
#         super().__init__() 
#         self.video_path = video_path
#         self.sensing_speed = sensing_speed  # Define el intervalo entre frames en segundos
#         self.streaming = False
        
#     def enable_video(self):
#         """Enables video sensing by instantiating the cap (capture) instance variable with the video path"""
#         try:
#             self.cap = cv2.VideoCapture(self.video_path)
            
#             if not self.cap.isOpened():
#                 raise Exception(f"[ERROR] Failed to open the video file {self.video_path}.")
            
#             self.state = "Enabled"
#             print(f"[INFO] Video from {self.video_path} is enabled.")
        
#         except Exception as e:
#             self.state = "Error"
#             print(f"[ERROR] Error enabling the video: {e}")
#             self.cap = None

#     def disable_video(self):
#         """Disables video capture by releasing the video capture object."""
#         if self.cap:
#             self.cap.release()
    
#     def start_sensing(self):
#         """    """
#         self.state = "Running"
#         print("Iniciando la detección de la cámara.")

#     def stop_sensing(self):
#         """     """
#         self.state = "Paused"
#         print("Deteniendo la detección de la cámara.")

#     async def start_data_streaming(self, start_time, loglevel):
#         """Starts streaming data from the video at intervals defined by sensing_speed."""
#         if not self.cap or not self.cap.isOpened():
#             print(f"[ERROR] Video from {self.video_path} is not ready for streaming.")
#             self.streaming = False
#             return
        
#         self.streaming = True
#         producer = DataProducer("sensor", "video", "0", loglevel=loglevel) 
        
#         # Calculamos el intervalo en nanosegundos
#         sensing_interval_ns = int(self.sensing_speed * 1e9)
#         recurrent_time = start_time
        
#         if loglevel == 0:
#             print(f"[INFO] Video from {self.video_path} is producing data.")
        
#         # Obtenemos el número total de frames en el video
#         total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         fps = self.cap.get(cv2.CAP_PROP_FPS)  # Obtener FPS del video
        
#         # Calculamos el tiempo de cada frame en segundos
#         frame_time = 1 / fps

#         while self.streaming:
#             print("esta entrando al while")
#             # Calculamos el tiempo exacto en el que debemos capturar el siguiente frame
#             target_time = recurrent_time / 1e9  # Convertir de nanosegundos a segundos
#             current_frame_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Obtener el tiempo actual en segundos
            
#             # Si el tiempo actual está dentro del rango del target_time, se captura el frame
#             if abs(current_frame_time - target_time) < (frame_time / 2):
#                 ret, frame = self.cap.read()
#                 if ret:
#                     cv2.imshow(f"Video Stream - {self.video_path}", frame)
#                     # Convert the frame to JPEG format for transmission
#                     success, buffer = cv2.imencode('.jpg', frame)
#                     if success:
#                         # Serialize the frame
#                         message_value = buffer.tobytes()
#                         encoded_message = base64.b64encode(message_value).decode('utf-8')
                        
#                         # Get frame dimensions
#                         height, width, _ = frame.shape
                        
#                         # Create the data payload for streaming
#                         result_payload = {
#                             "timestamp": int(recurrent_time),
#                             "sensor_data": encoded_message,
#                             "width": int(width),
#                             "height": int(height)
#                         }
                        
#                         # Serialize the result
#                         serialized_result = json.dumps(result_payload).encode('utf-8')
                        
#                         # Offload the sending of data to a thread to avoid blocking
#                         # await asyncio.get_running_loop().run_in_executor(
#                         #     None, producer.send_data, serialized_result
#                         # )
#                     else:
#                         print(f"[ERROR] Error serializing frame from video {self.video_path}")
#                 else:
#                     print(f"[ERROR] Error capturing frame from video {self.video_path}")
            
#             # Incrementamos el tiempo para capturar el siguiente frame en el intervalo deseado
#             recurrent_time += sensing_interval_ns
            
#             # Pausar el flujo hasta el próximo frame a extraer
#             await asyncio.sleep(self.sensing_speed)

#         print("Data streaming stopped")
#         cv2.destroyAllWindows()  # Cerrar las ventanas de OpenCV al finalizar

#     def stop_data_streaming(self):
#         """Sets the flag to stop the data streaming."""
#         print("Stopping data streaming")
#         self.streaming = False

#     def get_state(self):
#         """Returns the current state of the video sensor."""
#         return self.state
import cv2
import asyncio
import os
from OpenDrive.modules.sensors_prep.sensors.sensor import Sensor
from OpenDrive.modules.stream_processing.producer import DataProducer
from OpenDrive.modules.sensors_prep.data_preprocessing.image_normalization import resize_image_CV
import json
import base64
import platform



class Video(Sensor):
    def __init__(self, video_path ,data_type: str, data_subtype: str, producer_id: str, sensing_speed: int = 1):
        super().__init__() 
        self.video_path = video_path
        self.sensing_speed = sensing_speed  # Define el intervalo entre frames en segundos
        self.streaming = False
        self.frames_array = []
        
        
        self.data_type = data_type
        self.data_subtype = data_subtype
        self.producer_id = producer_id
        
        

    def enable_video(self):
        """Enables video sensing by instantiating the cap (capture) instance variable with the video path"""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            
            if not self.cap.isOpened():
                raise Exception(f"[ERROR] Failed to open the video file {self.video_path}.")
            
            self.state = "Enabled"
            print(f"[INFO] Video from {self.video_path} is enabled.")
            
            ##logica para guardar los frames del video
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_time = 1 / fps
            step_frames = self.sensing_speed // frame_time
            
            frames_processed = 0
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
             
            while frames_processed <= total_frames:
                
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frames_processed)
                print(frames_processed)
                ret, frame = self.cap.read()
                if ret:
                    frame_normalizated = resize_image_CV(frame, (680, 480))
                    self.frames_array.append(frame_normalizated)
                    frames_processed += step_frames
                    
            print("tamano de frames guardados:")
            print(len(self.frames_array))
               
            # Verificar FPS y el total de frames
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"[INFO] FPS: {fps}, Total Frames: {total_frames}")
        
        except Exception as e:
            self.state = "Error"
            print(f"[ERROR] Error enabling the video: {e}")
            self.cap = None

    def disable_video(self):
        """Disables video capture by releasing the video capture object."""
        if self.cap:
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
        """Starts streaming data from the video at intervals defined by sensing_speed."""
        if not self.cap or not self.cap.isOpened():
            print(f"[ERROR] Video from {self.video_path} is not ready for streaming.")
            self.streaming = False
            return
        
        self.streaming = True
        producer = DataProducer(data_type= self.data_type, data_subtype=self.data_subtype, producer_id=self.producer_id, loglevel=loglevel) 
    
        if loglevel == 0:
            print(f"[INFO] Video from {self.video_path} is producing data.")
        
      
        sensing_interval_ns = int(self.sensing_speed * 1e9)
        recurrent_time = start_time
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        
        if fps == 0:
            print("[ERROR] FPS is 0, video might not be valid or cannot be read properly.")
            return
        
        frames_processed = 0

        # Calculamos el tiempo de cada frame en segundos
        while frames_processed <= len(self.frames_array):
            # Establecer la posición del video al frame deseado, basado en step_frames
                curr_frame = self.frames_array[frames_processed]
                # Convert the frame to JPEG format for transmission
                success, buffer = cv2.imencode('.jpg', curr_frame)
                if success:
                    # Serialize the frame
                    message_value = buffer.tobytes()
                    encoded_message = base64.b64encode(message_value).decode('utf-8')
                    
                    # Get frame dimensions
                    height, width, _ = curr_frame.shape
                    
                    # Create the data payload for streaming
                    result_payload = {
                        "timestamp": int(recurrent_time),
                        "sensor_data": encoded_message,
                        "width": int(width),
                        "height": int(height)
                    }
                    
                    # Serialize the result
                    serialized_result = json.dumps(result_payload).encode('utf-8')
                    
                    # Offload the sending of data to a thread to avoid blocking
                    await asyncio.get_running_loop().run_in_executor(
                        None, producer.send_data, serialized_result
                    )
                else:
                    print(f"[ERROR] Error serializing frame from video {self.video_path}")
           
            
            # Incrementamos el tiempo para capturar el siguiente frame en el intervalo deseado
                recurrent_time += sensing_interval_ns
                frames_processed += 1
            # Pausar el flujo hasta el próximo frame a extraer
                await asyncio.sleep(self.sensing_speed)

        print("Data streaming stopped")


    def stop_data_streaming(self):
        """Sets the flag to stop the data streaming."""
        print("Stopping data streaming")
        self.streaming = False

    def get_state(self):
        """Returns the current state of the video sensor."""
        return self.state
