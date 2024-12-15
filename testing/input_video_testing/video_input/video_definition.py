from OpenDrive.modules.sensors_prep.video_sensor.video import Video
from OpenDrive.modules.sensors_prep.video_sensor.video_stream_control import start_videos_streaming

def main():
    videoFront = Video(
        video_path= "C:\\TT\\videos\\GrabacionNocheFrontal.mp4", 
        sensing_speed = .6,
        data_type = "video", 
        data_subtype = "Front", 
        producer_id = "1"
    )
    videoFront.enable_video()
    
    videoRear = Video(
        video_path= "C:\\TT\\videos\\GrabacionNocheTrasero.mp4", 
        sensing_speed = .6,
        data_type = "video", 
        data_subtype = "Rear", 
        producer_id = "1"
    )
    videoRear.enable_video()
    
    videoLeft = Video(
        video_path= "C:\\TT\\videos\\GrabacionNocheIzquierdo.mp4", 
        sensing_speed = .6,
        data_type = "video", 
        data_subtype = "Left", 
        producer_id = "1"
    )
    videoLeft.enable_video()
    
    videoRight = Video(
        video_path= "C:\\TT\\videos\\GrabacionNocheDerecho.mp4", 
        sensing_speed = .6,
        data_type = "video", 
        data_subtype = "Right", 
        producer_id = "1"
    )
    videoRight.enable_video()
    

    start_videos_streaming(
        videos = [videoFront, videoRear, videoLeft, videoRight],
        loglevel= 0
    )
    
    start_videos_streaming(
        videos = [videoFront],
        loglevel= 0
    )
      
    
if __name__ == "__main__":
    main()
    