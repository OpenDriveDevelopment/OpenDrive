from data_acquisition.image_acquisition import Image_acquisition
from sensors.camera import Camera

c1 = Camera(0,1)
c1.enable_sensor()
c1.test_camera()

c2 = Camera(1,1)
c2.enable_sensor()
c2.test_camera()

