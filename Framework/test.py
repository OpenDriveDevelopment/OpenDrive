from data_acquisition.image_acquisition import Image_acquisition
from sensors.camera import Camera

from perception_models.lane_detection.testing_video import video_testing

# c1 = Camera(0,1)
# c1.enable_sensor()
# c1.test_camera()

# c2 = Camera(1,1)
# c2.enable_sensor()
# c2.test_camera()


video_testing( video_name = "videoTest.mp4", fps = 24 )
