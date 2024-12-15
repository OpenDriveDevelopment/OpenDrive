from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.sensors_prep.pipeline_definition.sensors_stream_control import start_sensors_streaming

def main():
    customCam = Camera(port = 2, sensing_speed = .6)
    customCam.enable_sensor()

    start_sensors_streaming(
        sensors = [customCam],
        loglevel= 0
    )
        
    
if __name__ == "__main__":
    main()
    
    