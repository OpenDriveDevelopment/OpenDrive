####################################
### USE OF LINE DETECTION
####################################

# import cv2
# from OpenDrive.modules.sensors.camera import Camera
# from OpenDrive.modules.perception.trained_models.lane_detection import get_lane_detection

# cam1 = Camera(0,1)
# cam1.enable_sensor()


# while cam1.cap.isOpened():
#     ret, frame = cam1.cap.read()
#     fheight, fwidth, channels = frame.shape
#     image_processed = get_lane_detection.process_image(frame, fwidth, fheight )
            
#     cv2.imshow('Webcam', image_processed)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
        
            
# cam1.cap.release()
# cv2.destroyAllWindows()

####################################
### USE OG OBJECT DETECTION
####################################

import cv2
from OpenDrive.modules.sensors.camera import Camera
from OpenDrive.modules.perception.trained_models.traffic_sign_detection import get_traffic_sign_detection


cam1 = Camera(0,1)
cam1.enable_sensor()

while cam1.cap.isOpened():
    ret, frame = cam1.cap.read()
    image_processed = get_traffic_sign_detection.real_time_prediction(frame)
            
    cv2.imshow('Webcam', image_processed)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cam1.cap.release()
cv2.destroyAllWindows()


####################################
#### USE OF TRAFFIC SIGNS DETECTION
####################################


# import cv2
# from OpenDrive.modules.sensors.camera import Camera
# from OpenDrive.modules.perception.trained_models.objects_detection import get_object_detection

# cam1 = Camera(0,1)
# cam1.enable_sensor()

# while cam1.cap.isOpened():
#     ret, frame = cam1.cap.read()
#     image_processed = get_object_detection.real_time_prediction(frame)
            
#     cv2.imshow('Webcam', image_processed)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
        
# cam1.cap.release()
# cv2.destroyAllWindows()