from OpenDrive.modules.decision_making.alerts.camera.distance_estimator import estimate_distance

def close_calls_function(coordenates, object_data ,height, width, type="Front", proximity_threshold=80, distance_threshold=2, focal_length=200, known_width=2):
    """
    Calculate how close and the position of multiple objects based on the camera type and distance.

    Args:
        objects (list): List of bounding box coordinates, each as a tuple (x1, x2, y2).
        height (int): Frame height.
        width (int): Frame width.
        type (str): Camera type ('Front', 'Rear', 'LeftSide', 'RightSide').
        proximity_threshold (int): Threshold to determine if an object is close.
        distance_threshold (float): Maximum distance to consider an object "close".
        focal_length (float): Camera focal length for distance estimation.
        known_width (float): Known width of the object for distance estimation.

    Returns:
        list: A list of tuples, each containing (distance, position).
    """
    results = []
    
    for bbox, objects_data in zip(coordenates, object_data):
        x1, x2, y2 = bbox
        class_name, _ = objects_data
        cx = (x1 + x2) // 2  # Center of the bounding box
        bbox_width = x2 - x1
        # Calculate the distance using bounding box width
        distance = estimate_distance(bbox_width, focal_length, known_width)
        position = None  # Default position

        if distance <= distance_threshold or class_name == "person" :
            if type in ["Front", "Rear"]:
                # Determine position based on center tolerance
                center_tolerance = 0.1 * width  # Tolerance as a fraction of frame width

                if abs(cx - width // 2) <= center_tolerance:
                    position = "center"
                elif cx < width // 2:
                    position = "left" if type == "Front" else "right"
                else:
                    position = "right" if type == "Front" else "left"

            elif type in ["LeftSide", "RightSide"]:
                # For lateral cameras, focus on objects within proximity threshold
                if y2 > height - proximity_threshold:
                    position = "center"

        results.append((distance, position))
        

    return results
