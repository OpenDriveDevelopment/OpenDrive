import json
from functools import partial
from quixstreams import Application
import traceback

received_data = {}
data_by_sensor_and_model = {}

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

        # Si data es un string JSON, convertirlo en un objeto Python
        """

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error al deserializar data: {e}")
                return None, None

        """

        print(f"Frame ID: {frame_id}")
        print(f"Timestamp: {timestamp}")
        # print(f"Data: {data}")

        # Procesar el frame_id y actualizar received_data
        # Asegurar la inicialización del conjunto en received_data
        received_data.setdefault(timestamp, set()).add((frame_id, str(data)))

        if len(received_data[timestamp]) == 3:
            # Lo que sea que se haga cuando se tiene la data junta al fin se pondra aqui
            # print(received_data[timestamp])
            print("All data for this frame received")

            for cosa in received_data[timestamp]:
                data_by_sensor_and_model.setdefault(cosa[0], []).append(cosa[1])

            del received_data[timestamp]
        else:
            print("Waiting for the rest of the frame data to arrive")

        # Procesar el frame o realizar otras operaciones
        return frame_id, data

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        traceback.print_exc()
        return None, None


def main():

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
        
    app.run() 

if __name__ == '__main__':
    main()