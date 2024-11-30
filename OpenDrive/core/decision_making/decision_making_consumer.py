import json
from functools import partial
from quixstreams import Application
import traceback
import asyncio

received_data = {}
data_by_sensor_and_model = {}
last_processed_frame = -1

def execute_operation(message, pipeline, app):
    """
    Procesa un mensaje Kafka, deserializa los datos y extrae el frame_id y la data.
    """

    try:
        # Deserializar el mensaje recibido
        message_decoded = message.decode("utf-8")
        message_json = json.loads(message_decoded)

        # Extraer frame_id y data
        frame_id = message_json.get("id")
        data = message_json.get("data")
        timestamp = message_json.get("timestamp")
        side = message_json.get("side")

        # Cosa magica
        # Split the string by underscores
        parts = frame_id.split("_")

        model = parts[-1]
        sensor = "_".join(parts[:-1])


        """
        # Print metadata
        print(f"\n{sensor} at time {timestamp}:")
        if model == "signals":
            for signal in data:
                print(f"Detected a signal of type {signal['class_name']} with a confidence of {signal['confidence'] * 100:.2f}%")
        elif model == "lane":
            print("Received the matrix representing the lane")
        elif model == "objects":
            for obj in data:
                print(f"Detected an object of type {obj['class_name']} with a confidence of {obj['confidence'] * 100:.2f}%")

        print("\n")
        """


        # Procesar el frame_id y actualizar received_data
        # Asegurar la inicialización del conjunto en received_data
        received_data.setdefault(timestamp, set()).add((frame_id + "_" + side, str(data)))

        print("B")

        # Procesar el frame o realizar otras operaciones
        return frame_id, data

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        traceback.print_exc()
        return None, None
    
async def process_data():
    """
    Process the received data, ensuring each frame has exactly three sensors' data
    and meets the timestamp requirement. Deletes already processed or incomplete frames
    to maintain optimal performance.
    """
    global last_processed_frame

    # List to keep track of timestamps to be deleted
    timestamps_to_delete = []

    print("A")

    # Process frames in chronological order
    for timestamp in sorted(received_data.keys()):
        print(f"Processing timestamp: {timestamp}")

        if len(received_data[timestamp]) == 3:
            if last_processed_frame < timestamp:
                # Process the frame
                for sensor_data in received_data[timestamp]:
                    print(f"Sensor: {sensor_data[0]}")
                    # Uncomment the following line to display data
                    # print(f"Data: {sensor_data[1]}")
                last_processed_frame = timestamp  # Update the last processed frame
                timestamps_to_delete.append(timestamp)  # Mark for deletion
            else:
                print(f"Frame at {timestamp} already processed or data received too late. Deleting it.")
                timestamps_to_delete.append(timestamp)  # Mark for deletion
        else:
            print(f"Frame at {timestamp} is not ready to be processed.")

    # Delete marked timestamps
    for timestamp in timestamps_to_delete:
        print(f"Frame at {timestamp} is being deleted.")
        del received_data[timestamp]

    return None

async def tarea_periodica():
    while True:
        await process_data()
        await asyncio.sleep(0.1) 


async def run_app():

    topics = ["output_topic_objects"]
    
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
        
    asyncio.create_task(tarea_periodica())

    app.run()

if __name__ == '__main__':
    asyncio.run(main())