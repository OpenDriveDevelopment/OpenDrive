import asyncio
import json
from functools import partial
from quixstreams import Application
import cv2
import numpy as np
import time

from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection
from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection
from OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection import get_sign_detection

function_mapping = {
    "signals": get_sign_detection,
    "objects": get_obj_detection,
    "lane": get_lane_detection,
}

def execute_operation(message, pipeline, app):
    print("PIPELINE COMING " + pipeline.input_sensor)
    print("****************************************************")
    
    # Se obtiene la lista de los modelos por los cuales debe pasar la informacion del sensor
    functions_to_execute = pipeline.vision_models
    
    
    np_array = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if frame is None:
        print("Couldn't get frame")
        return

    for func_name in functions_to_execute:
        
        if func_name in function_mapping:
            
            # start_time = time.perf_counter()
            
            result = function_mapping[func_name](frame)
            
            # end_time = time.perf_counter()
            
            
            # elapsed_time = end_time - start_time
            # print(f"El código tardó {elapsed_time:.4f} segundos en ejecutarse.")
            
            print(f"Result type: {type(result)}")
            print(f"Result content: {result}")

            if isinstance(result, dict):
                serialized_result = json.dumps(result)
            elif isinstance(result, list):
                # Serializar la lista completa como JSON
                serialized_result = json.dumps(result)
            else:
                try:
                    serialized_result = result.tojson()
                except AttributeError:
                    print(f"Unexpected result type: {type(result)}")
                    return

      
            # print("Serialized Result:", serialized_result)
            
            messages_topic = app.topic(name="output_topic_name", value_serializer="bytes")
            
            with app.get_producer() as producer:
                producer.produce(
                    topic = messages_topic.name,
                    key = "1",
                    value = serialized_result.encode('utf-8')
                )
                  
        else:
            print(f"Function for '{func_name}' not defined.")
    
    
async def control_perception_streaming(pipelines):
    
    if not pipelines:
        print("No perception pipelines have been provided for streaming")
        return
    
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group="unique_consumer_group_nam3"
    )
    
    for pipeline in pipelines:
        input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
        sdf = app.dataframe(input_topic)
        sdf = sdf.update(partial(execute_operation, pipeline=pipeline, app=app)) ## Es necesario utilizar el partial para que los parametros de la funcion sean pasados correctamente
        
    app.run()
