from OpenDrive.modules.decision_making.alerts.camera.distance_estimator import estimate_distance

def close_calls_function(x1, x2, y1, y2, height, width, proximity_threshold=80, type="Front", distance_threshold = 2):
    """
    Calculate how close and the position of an object based on the camera type and distance.

    Args:
        x1, x2, y1, y2: bounding_box coordinates.
        height (int): Frame height.
        width (int): Frame width.
        proximity_threshold (int): Threshold to determine if an object is close.
        type (str): Camera type ('Front', 'Rear', 'Left', 'Right').

    Returns:
        tuple: Estimated distance (in meters) and position ('center', 'left', 'right').
    """
    cx = (x1 + x2) // 2  # Center of the bounding box
    bbox_width = x2 - x1
    # Calculate the distance using bounding box width
    distance = estimate_distance(bbox_width)
    position = None  # Default position

    if distance <= distance_threshold:
        if type in ["Front", "Rear"]:
            # Determine position based on center tolerance
            center_tolerance = 0.1 * width  # Tolerance as a fraction of frame width

            if abs(cx - width // 2) <= center_tolerance:
                position = "center"
            elif cx < width // 2:
                position = "left" if type == "Front" else "right"
            else:
                position = "right" if type == "Front" else "left"

        elif type in ["Left", "Right"]:
            # For lateral cameras, focus on objects within proximity threshold
            if y2 > height - proximity_threshold:
                position = "center"

    return distance, position