from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.sensors_prep.pipeline_definition.sensors_stream_control import start_sensors_streaming

def main():
    camRear = Camera(port = 2, sensing_speed = .6)
    camRear.enable_sensor()

    camFront = Camera(port = 1, sensing_speed = .6)
    camFront.enable_sensor()

    camRight = Camera(port = 3, sensing_speed = .6)
    camRight.enable_sensor()
    
    camLeft = Camera(port = 4, sensing_speed = .6)
    camLeft.enable_sensor()
     
    start_sensors_streaming(
        sensors = [camFront, camRear, camRight, camLeft],
        loglevel= 0
    )
        
    
if __name__ == "__main__":
    main()
    