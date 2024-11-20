from OpenDrive.modules.decision_making.alerts.camera.distance_estimator import estimate_distance

def close_calls_function( x1, x2, y1, y2, height, width, proximity_threshold=80, type="Front"):
    """
    Calculate how close and the position of an object based on the camera type

    Args:
        x1, x2, y1, y2: bounding_box.
        height (int): Altura del frame.
        width (int): Ancho del frame.
        proximity_threshold (int): Umbral para determinar si un objeto está cerca.
        type (str): Tipo de cámara ('Front', 'Rear', 'Left', 'Right').

    Returns:
        tuple: Distancia estimada y posición del objeto.
    """
    cx = (x1 + x2) // 2
    
    bbox_width = x2 - x1
    bbox_height = y2 - y1  

    distance = estimate_distance(bbox_width, bbox_height)
    position = None  # Undefined by default

    if type in ["Front", "Rear"]:
        # Verify the rear and front camera
        if y2 > height - proximity_threshold:
            center_tolerance = 0.1 * width  # Center tolerance

            if abs(cx - width // 2) <= center_tolerance:
                position = "center"
            elif cx < width // 2:
                position = "left" if type == "Front" else "right"
            else:
                position = "right" if type == "Front" else "left"

    elif type in ["Left", "Right"]:
        # Lateral cameras, only matter if an object is close 
        if y2 > height - proximity_threshold:
            position = "center"  # For lateral cameras consider only center value

    return distance, position
