from datetime import datetime
import json
from functools import partial
from quixstreams import Application
import traceback

received_data = {}
models_that_went_throu = {}
last_processed_frame = -1

def execute_operation(message, pipeline, app):
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

        # Update the shared dictionary
        received_data.setdefault(timestamp, []).append((frame_id + "_" + position_sensor, data))

        process_data()
        return frame_id, data

    except Exception as e:
        print(f"Error processing message: {e}")
        traceback.print_exc()
        return None, None
    
def process_data():
    """
    Processes received data, ensuring each frame has data from three sensors 
    and meets timestamp requirements.
    """
    global last_processed_frame

    try:
        timestamps_to_delete = []

        # Process timestamps in chronological order
        for timestamp in sorted(received_data.keys()):

            if len(received_data[timestamp]) == 3:
                if last_processed_frame < timestamp:
                    #print(f"Processing frame at timestamp {timestamp}:")
                    for sensor_data in received_data[timestamp]:
                        parts = sensor_data[0].split("_")

                        # print(f"Tipo: {parts[0]}")
                        # print(f"Sub-tipo: {parts[1]}")
                        # print(f"Puerto: {parts[2]}")
                        # print(f"Modelo: {parts[3]}")
                        # print(f"Lado: {parts[4]}")
                        # print(f"Data: {sensor_data[1]}")

                    # current_timestamp = int(datetime.now().timestamp() * 1e9)
                    # Calcular la diferencia en milisegundos
                    # difference_ms = (current_timestamp - timestamp) / 1_000_000
                    # Imprimir la diferencia
                    # print(f"Diferencia en milisegundos: {difference_ms} ms")

                    last_processed_frame = timestamp
                    timestamps_to_delete.append(timestamp)
                else:
                    print(f"Frame at {timestamp} already processed or received late.")
                    timestamps_to_delete.append(timestamp)
            else:
                if(last_processed_frame > timestamp):
                    print(f"Frame at {timestamp} already processed or received late.")
                    timestamps_to_delete.append(timestamp)

        # Delete processed timestamps
        for timestamp in timestamps_to_delete:
            del received_data[timestamp]

        # Write back to the shared namespace
    except Exception as e:
        print(f"Error in process_data: {e}")
        traceback.print_exc()


def main():

    topics = ["output_topic_objects1"]
    
    if not topics:
        print("No perception pipelines have been provided for streaming")
        return
    
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group="unique_consumer_group_nam3"
    )
    
    for topic in topics:
        input_topic = app.topic(name=topic, value_deserializer="bytes")
        sdf = app.dataframe(input_topic)
        sdf = sdf.update(partial(execute_operation, pipeline=topic, app=app)) ## Es necesario utilizar el partial para que los parametros de la funcion sean pasados correctamente
        
    app.run() 

if __name__ == '__main__':
    main()