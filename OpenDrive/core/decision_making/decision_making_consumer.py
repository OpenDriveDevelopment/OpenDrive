import asyncio
import json
from functools import partial
from quixstreams import Application
import cv2
import numpy as np
import time

received_data = {}
last_used_frame = 0

def execute_operation(message, pipeline, app):
    """
    Procesa un mensaje Kafka, deserializa los datos y extrae el frame_id y la data.
    """

    global last_used_frame

    try:
        # Deserializar el mensaje recibido
        message_decoded = message.decode("utf-8")
        message_json = json.loads(message_decoded)

        # Extraer frame_id y data
        frame_id = message_json.get("id")
        data = message_json.get("data")

        # Validar frame_id
        if not frame_id or len(frame_id.split("_")) < 5:
            print("frame_id no tiene el formato esperado")
            return None, None

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
        print(f"Last f: {last_used_frame}")
        # print(f"Data: {data}")

        # Procesar el frame_id y actualizar received_data
        id_parts = frame_id.split("_")
        cadena_final = "_".join(id_parts[:4])

        # Asegurar la inicialización del conjunto en received_data
        received_data.setdefault(id_parts[4], set()).add((cadena_final, data))

        if len(received_data[id_parts[4]]) == 3 and last_used_frame < int(id_parts[4]):
            last_used_frame = int(id_parts[4])
            # Lo que sea que se haga cuando se tiene la data junta al fin se pondra aqui
            print("All data for this frame received")
        else:
            print("Waiting for the rest of the frame data to arrive")

        # Procesar el frame o realizar otras operaciones
        return frame_id, data

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        return None, None


def main():

    topics = ["output_topic_name"]
    
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