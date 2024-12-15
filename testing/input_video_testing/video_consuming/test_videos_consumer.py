import multiprocessing
import json
import os
from quixstreams import Application
import cv2
import numpy as np
import base64
import importlib


def execute_operation(message):
    """Procesa el mensaje recibido y muestra un mensaje con el timestamp."""
    print("Llego data")
    # Aquí puedes hacer lo que necesites con el mensaje recibido
    deserialized_result = json.loads(message.decode('utf-8'))
    
    timestamp = deserialized_result['timestamp']
    sensor_data = deserialized_result['sensor_data']
    sensor_data = base64.b64decode(sensor_data)
    width = deserialized_result['width']
    height = deserialized_result['height']
    
    # Convertir el mensaje a un frame
    np_array = np.frombuffer(sensor_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Mostrar el frame en una ventana
    if frame is not None:
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)  # Espera 1ms para refrescar la ventana
    else:
        print("No se pudo decodificar el frame.")
    
    

app = Application(
    broker_address="localhost:9092",
    auto_offset_reset="latest",
)

# Definimos el topic
input_topic = app.topic(name="video_Front_1", value_deserializer="bytes")

# Creamos el StreamDataFrame para almacenar los datos recibidos
sdf = app.dataframe(input_topic)

# Esta función procesa el mensaje que recibe el StreamDataFrame
def process_message(message):
    execute_operation(message)


# Usamos el método 'update' del StreamDataFrame para actualizar el procesamiento de los mensajes
sdf.update(process_message)

# Iniciar el consumidor y procesar mensajes de forma continua
app.run()  # Esto mantendrá la aplicación corriendo y procesando los mensajes
