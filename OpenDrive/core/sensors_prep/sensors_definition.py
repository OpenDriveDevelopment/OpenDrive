from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.sensors_prep.pipeline_definition.sensors_stream_control import start_sensors_streaming
import cv2

def main():
    cam1 = Camera(1,.3)
    cam1.enable_sensor()

    cam2 = Camera(2, .3)
    cam2.enable_sensor()
    
    # cam3 = Camera(3,.3)
    # cam3.enable_sensor()
    
    # cam4 = Camera(4, .3)
    # cam4.enable_sensor()
    
    start_sensors_streaming(
        sensors = [cam2, cam1],
        loglevel= 1
    )
    
if __name__ == "__main__":
    main()
    
    