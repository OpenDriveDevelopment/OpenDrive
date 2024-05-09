import time
# from sensors import camera as c
# import sensors.camera as c
from sensors.camera import Camera
import cv2


class Image_acquisition():
    def __init__(self):
        self.sample_rate = 0
        
    def get_images(self, cam, sam_rate):
        # cam.enable_sensor()
        # ret, frame = cam.cap.read()
        # cv2.imwrite('./frameworkPhoto.jpg', frame)
        # cam.cap.release()
        # return frame
        
        cam.enable_sensor()
        while True:
            ret, frame = cam.cap.read()
            cv2.imwrite('./frameworkPhoto.jpg', frame)
            
            cv2.imshow('Webcam', frame)
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            
            time.sleep(sam_rate / 1000)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir con 'q' (opcional)
                break
            
        cam.cap.release()
        cv2.destroyAllWindows()


        
    def check_camera_status(self, cam):
        return cam.get_state()
        
    