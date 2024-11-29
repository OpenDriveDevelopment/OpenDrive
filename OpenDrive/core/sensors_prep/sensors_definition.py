from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.modules.sensors_prep.pipeline_definition.sensors_stream_control import start_sensors_streaming

def main():
    cam1 = Camera(1,.3)
    cam1.enable_sensor()

    cam2 = Camera(0,.3)
    cam2.enable_sensor()

    start_sensors_streaming([cam2, cam1])
    
if __name__ == "__main__":
    main()
    
    