
def estimate_distance( bbox_width ):

    focal_length = 200  # Example focal length
    known_width = 2.0  # Approximate width of the car (in meters)
    distance = (known_width * focal_length) / bbox_width
    
    return distance