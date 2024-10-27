
from OpenDrive.modules.sensors import camera


cam1 = camera.Camera(0,0)
cam1.enable_sensor()
cam1.test_camera()