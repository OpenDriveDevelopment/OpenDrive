from OpenDrive.modules.decision_making.alerts.camera.close_calls_objects import close_calls_function

def front_road_obstacles(objects, coordinates, height, width):
    """
    Process front road obstacles and generate structured output.
    """
    data_objects_info = close_calls_function(coordinates, objects ,height, width, type="Front", distance_threshold= 8)
    obstacles = []

    for idx, (distance, position) in enumerate(data_objects_info):
        if position:
            action = "break" if position == "center" else "caution"
            obstacles.append({
                "type": objects[idx][0],
                "precision": objects[idx][1],
                "distance (mts)": round(distance, 2),
                "close_to_side": position,
                "action": action
            })
    
    return {"front_road_obstacles": obstacles}

def side_road_obstacles(objects, coordinates, height, width, side):
    """
    Process side road obstacles and generate structured output.
    """
    data_objects_info = close_calls_function(coordinates, objects, height, width, type=side)
    obstacles = []

    for idx, (distance, position) in enumerate(data_objects_info):
        if position:  # Only add objects near the proximity threshold
            obstacles.append({
                "side": side.lower(),
                "type": objects[idx][0],
                "precision": objects[idx][1],
                "action": "caution"
            })
    
    return {"side_obstacles": obstacles}

def rear_road_obstacles(objects, coordinates, height, width):
    """
    Process rear road obstacles and generate structured output.
    """
    data_objects_info = close_calls_function(coordinates, objects, height, width, type="Rear")
    obstacles = []

    for idx, (distance, position) in enumerate(data_objects_info):
        if position:
            action = "avoid_sudden_break" if position == "center" else "caution"
            obstacles.append({
                "type": objects[idx][0],
                "precision": objects[idx][1],
                "distance (mts)": round(distance, 2),
                "close_to_side": position,
                "action": action
            })
    
    return {"rear_road_obstacles": obstacles}
