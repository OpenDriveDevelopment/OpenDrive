import os
import cv2

from .get_lane_detection import process_image


def video_testing( video_name, fps = 24 ):

    """ Load the video and the input folder where the video is located """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    testing_videos_dir = os.path.join(current_dir, 'testing_videos')

    name_file = video_name
    video_path = os.path.join(testing_videos_dir, name_file)
    original_video = cv2.VideoCapture(video_path)

    """ Check that the video was open correctly """

    if not original_video.isOpened():

        print(f"Error: It was no possible to open the video: {video_path}")
    
    else:

        """ Get the dimensions of the original video """
        frame_width = int(original_video.get(3))
        frame_height = int(original_video.get(4))

        print( frame_width )

        """ Define the codec and the object VideoWriter """
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        output_dir = os.path.join(current_dir, "testing_videos_output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, name_file)
        output = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        """ Process the video """

        while original_video.isOpened():

            ret, frame = original_video.read()

            if ret:

                output.write(process_image( image = frame, width = frame_width, height= frame_height ))
            else:

                break

        # Libera los recursos
        original_video.release()
        output.release()