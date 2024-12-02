import time
import cv2
from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection
from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection_image
from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection

# cam1 = Camera(1,1)
# cam1.enable_sensor()

# while cam1.cap.isOpened():
#     ret, frame = cam1.cap.read()
    
#     start_time = time.perf_counter()
    
#     result = get_obj_detection(frame)
    
#     end_time = time.perf_counter()
    
#     print("SE TERMINO DE DETECTAR OBJETO")
#     elapsed_time = end_time - start_time
#     print(f"El código tardó {elapsed_time:.4f} segundos en ejecutarse.")
        
# cam1.cap.release()
# cv2.destroyAllWindows()


########################################################################

cam1 = Camera(1,1)
cam1.enable_sensor()

while cam1.cap.isOpened():
    ret, frame = cam1.cap.read()
    
    start_time = time.perf_counter()
    image_processed = get_lane_detection(frame)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"El código tardó {elapsed_time:.4f} segundos en ejecutarse.")
    
    
    
    if 0xFF == ord('q'):
        break
        
cam1.cap.release()
cv2.destroyAllWindows()