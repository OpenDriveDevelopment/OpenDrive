import json
from functools import partial
from quixstreams import Application
import traceback

from OpenDrive.modules.decision_making.data_processing.data_process import process_data

received_data = {}

def execute_operation(message, pipeline, app, models_to_received, output_mode, function_mode):
    """
    Processes a Kafka message, deserializes data, and extracts frame_id and associated data.
    """
    try:
        # Deserialize the incoming message
        message_decoded = message.decode("utf-8")
        message_json = json.loads(message_decoded)

        # Extract frame_id, data, timestamp, and position_sensor
        frame_id = message_json.get("id")
        data = message_json.get("data")
        timestamp = message_json.get("timestamp")
        position_sensor = message_json.get("position_sensor")
        frame_height = message_json.get("frame_height")
        frame_width = message_json.get("frame_width")

        # Update the shared dictionary
        received_data.setdefault(timestamp, []).append((frame_id + "_" + position_sensor + "_" + str(frame_height) + "_" + str(frame_width), data))

        process_data(received_data, models_to_received, output_mode, function_mode)
        return frame_id, data

    except Exception as e:
        print(f"Error processing message: {e}")
        traceback.print_exc()
        return None, None

def start_data_reception(models_to_received, output_mode = "console", function_mode = "four_cameras"):

    topic = "output_topic_objects1"
    
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group="unique_consumer_group_nam3"
    )
    
    input_topic = app.topic(name=topic, value_deserializer="bytes")
    sdf = app.dataframe(input_topic)
    sdf = sdf.update(partial(execute_operation, pipeline=topic, app=app, models_to_received=models_to_received, output_mode=output_mode, function_mode=function_mode))
        
    app.run()