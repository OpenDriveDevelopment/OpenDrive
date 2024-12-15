def traffic_signs(objects):
    """
    Process detected traffic signs and generate structured output.

    Args:
        objects (list): List of tuples (detected_sign_type, precision) representing detected traffic signs.

    Returns:
        dict: Structured data for traffic signs.
    """
    actions_map = {
        "Green Light": None,  # No action required
        "Red Light": "stop",
        "Stop": "stop",
    }

    # Add speed limit actions dynamically
    for speed in range(10, 130, 10):  # Generate speed limits 10 to 120
        actions_map[f"Speed Limit {speed}"] = f"reduce speed to {speed}"

    traffic_signs_data = []

    for obj, precision in objects:
        action = actions_map.get(obj, "Signal Caution") 
        
        traffic_signs_data.append({
            "type": obj.lower(),
            "precision": precision,
            "action": action
        })
    
    return {"traffic_signs": traffic_signs_data}
