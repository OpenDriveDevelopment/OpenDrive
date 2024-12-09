from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.sensors_prep.pipeline_definition.sensors_stream_control import start_sensors_streaming

def main():
    cam1 = Camera(port = 1, sensing_speed = 1)
    cam1.enable_sensor()

    cam2 = Camera(port = 2, sensing_speed = 1)
    cam2.enable_sensor()
    
    cam3 = Camera(port = 3, sensing_speed = 1)
    cam3.enable_sensor()
    
    cam4 = Camera(port = 4, sensing_speed = 1)
    cam4.enable_sensor()
    
    
      
    start_sensors_streaming(
        sensors = [cam2, cam1, cam3, cam4],
        loglevel= 1
    )
    
if __name__ == "__main__":
    main()
    
    