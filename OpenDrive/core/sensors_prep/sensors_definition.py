import asyncio
from OpenDrive.modules.sensors_prep.sensors.camera import Camera
from OpenDrive.core.sensors_prep.sensors_stream_control import start_sensors_streaming

async def main():
    cam1 = Camera(1, 0)
    cam1.enable_sensor()
    
    cam2 = Camera(0, 0)
    cam2.enable_sensor()
    
    await start_sensors_streaming([cam1,cam2])
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
