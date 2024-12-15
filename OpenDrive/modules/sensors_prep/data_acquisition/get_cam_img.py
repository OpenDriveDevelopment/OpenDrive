import cv2

def get_cam_frame(camera_index=0):
    # Open the camera with the given index (default is the primary camera)
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"[ERROR] Could not access the camera with index {camera_index}")
        return None

    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Release the camera regardless of the result
    cap.release()
    
    # If the frame was successfully retrieved, return it; otherwise, return None
    if ret:
        return frame
    else:
        print("[ERROR] Could not read a frame from the camera")
        return None