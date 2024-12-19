import cv2

def get_cameras_info(max_index=10):
    """
    Detect connected cameras and retrieve details for each, such as resolution.
    
    Args:
        max_index (int): Maximum number of camera indices to check.
    
    Returns:
        list: Details of available cameras.
    """
    available_cameras = []

    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        
        # If the camera opens successfully
        if cap.isOpened():
            # Get camera details
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # Width
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Height
            fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second (FPS)
            
            # Store camera information
            available_cameras.append({
                "index": index,
                "width": width,
                "height": height,
                "fps": fps,
                "device_node": f"/dev/video{index}"  # Linux, adjust according to the system
            })
            
            cap.release()  # Release the device after getting the information

    return available_cameras


# Detect available cameras and get their details
cameras = get_cameras_info(4)

# Display the details of the detected cameras
if cameras:
    print("Detected cameras:")
    for cam in cameras:
        print(f"  - Camera at index {cam['index']} | Resolution: {cam['width']}x{cam['height']} | FPS: {cam['fps']} | Device: {cam['device_node']}")
else:
    print("No cameras detected.")