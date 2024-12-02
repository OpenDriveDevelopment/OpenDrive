
def free_lane_change( space_detections : object):

    """
    Two cases:

        1) Only with rear information
        2) With rear, left and right ( ideal situation ) : 

    INPUT:

        Object: Where the key is the type of camera and the value is a list of non free space positons, example [ "" ]

    OUTPUT:

        Object that indicates if its possible to change the line in the right and left side

    """

    output = {

        "left_change": True,
        "right_change": True

    }

    ## Ideal situation

    if all(side in space_detections for side in ["Rear", "LeftSide", "RightSide"]):
        
        if "left" in space_detections["Rear"]: output["right_change"] = False
        if "right" in space_detections["Rear"]: output["left_change"] = False

        if "center" in space_detections["RightSide"]: output["right_change"] = False
        if "center" in space_detections["LeftSide"]: output["left_change"] = False

    elif "Rear" in space_detections:

        if "left" in space_detections["Rear"]: output["right_change"] = False
        if "right" in space_detections["Rear"]: output["left_change"] = False
    
    else:

        raise ValueError("Error: Is necessary to have at least rear camera type")

    return output

        



    

