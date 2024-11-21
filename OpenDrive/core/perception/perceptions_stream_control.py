import multiprocessing
import json
import os
from quixstreams import Application
import cv2
import numpy as np
import string
import random
import base64

from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection
from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection
from OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection import get_sign_detection

# Deshabilitar la configuración de señales en Quix
os.environ["QUIXSTREAMS_DISABLE_SIGNAL_HANDLERS"] = "1"

# Mapeo de funciones de modelos
function_mapping = {
    "signals": get_sign_detection,
    "objects": get_obj_detection,
    "lane": get_lane_detection,
}

# Contador global para los IDs de los frames
frame_counter = 0

def execute_operation(message, pipeline, app):
    
    global frame_counter
    
    deserialized_result = json.loads(message.decode('utf-8'))
    
    timestamp = deserialized_result['timestamp']
    sensor_data = deserialized_result['sensor_data']
    sensor_data = base64.b64decode(sensor_data)
    
    # Convertir el mensaje a un frame
    np_array = np.frombuffer(sensor_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if frame is None:
        print(f"[ERROR] Couldn't decode frame for sensor {pipeline.input_sensor}")
        return
    
    # Incrementar el contador de frames
    frame_counter += 1
    frame_id = frame_counter
    
    # Validar que haya funciones asignadas en el pipeline
    if not pipeline.vision_models:
        print(f"[WARNING] No functions assigned to pipeline: {pipeline.input_sensor}")
        return

    # Ejecutar las funciones asignadas en el pipeline
    for func_name in pipeline.vision_models:
        
        if func_name not in function_mapping:
            print(f"[WARNING] Function '{func_name}' not available for pipeline {pipeline.input_sensor}")
            continue
        
        try:
            # Ejecutar la funcion
            result = function_mapping[func_name](frame)
            
            # Preparar y serializar el resultado
            result_payload = {
                "id": pipeline.input_sensor + "_" + func_name,
                "input_sensor": pipeline.input_sensor,
                "data": result if isinstance(result, (dict, list)) else str(result),
                "timestamp": timestamp
            }
            serialized_result = json.dumps(result_payload)

            # Enviar el resultado al topic de salida
            try:
                messages_topic = app.topic(name=pipeline.output_decision, value_serializer="bytes")
                with app.get_producer() as producer:
                    producer.produce(
                        topic = messages_topic.name,
                        key = str(frame_id),
                        value = serialized_result.encode('utf-8')
                    )
                print(f"[INFO] Result for {func_name} sent to topic: {pipeline.output_decision}")
            except Exception as e:
                print(f"[ERROR] Failed to send result to topic {pipeline.output_decision}: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to process function {func_name} for sensor {pipeline.input_sensor}: {e}")

def run_app(pipeline):
    """
    Configura y ejecuta la aplicación Quix Streams en un proceso independiente.
    """
    # Crear una instancia de Application con un consumer_group único
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group=_generate_random_group_id()  # Generar un grupo único
    )
    
    # Configurar el topic de entrada
    input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
    sdf = app.dataframe(input_topic)

    # Configurar la función de procesamiento
    def process_message(message):
        execute_operation(message, pipeline, app)

    sdf = sdf.update(process_message)
    print(f"[INFO] Consumer running for pipeline: {pipeline.input_sensor} consuming {pipeline.vision_models} model")
    
    # Ejecutar la aplicación
    app.run()

def control_perception_streaming(pipelines):
    """
    Crea procesos independientes para cada pipeline.
    """
    processes = []

    for pipeline in pipelines:
        # Crear un nuevo proceso para cada pipeline
        process = multiprocessing.Process(target=run_app, args=(pipeline,))
        process.start()
        processes.append(process)

    # Esperar a que los procesos terminen (normalmente no lo harán porque `app.run()` es bloqueante)
    for process in processes:
        process.join()

def _generate_random_group_id(length=10):
    """
    Genera un identificador único para el grupo de consumidores.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))
