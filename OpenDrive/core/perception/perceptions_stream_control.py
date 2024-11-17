import asyncio
from functools import partial
from quixstreams import Application
import cv2
import numpy as np

def execute_operation(message, pipeline, app):
    print("PIPELINE COMING" + pipeline.input_sensor)
    
    processed_message = f"Processed data from {pipeline.input_sensor}"
    serialized_message = processed_message.encode('utf-8')
 
    messages_topic = app.topic(name="output_topic_name", value_serializer="bytes")
    
    with app.get_producer() as producer:
        producer.produce(
            topic = messages_topic.name,
            key = "1",
            value = serialized_message,
        )
        

async def control_perception_streaming(pipelines):
    
    if not pipelines:
        print("No perception pipelines have been provided for streaming")
        return
    
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group="unique_consumer_group_nam3"
    )
    
    # streaming_task_list = []
    # sdf_list= []
    
    for pipeline in pipelines:
        input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
        output_topic = app.topic(name="output_topic_name", value_serializer="bytes")
        sdf = app.dataframe(input_topic)
        sdf = sdf.update(partial(execute_operation, pipeline=pipeline, app=app)) ## Es necesario utilizar el partial para que los parametros de la funcion sean pasados correctamente
        
        
        # sdf = sdf.update(lambda message: execute_operation(message, pipeline))
        # streaming_task_list.append(input_topic)
        # sdf_list.append(sdf)

    app.run()
        
    