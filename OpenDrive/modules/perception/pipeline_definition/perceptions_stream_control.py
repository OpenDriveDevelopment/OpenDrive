import multiprocessing
import json
import os
from quixstreams import Application
import cv2
import numpy as np
import string
import random
import base64
import importlib

from OpenDrive.modules.perception.pipeline_definition.percep_pipeline import SensorToModelPipeline

# Deshabilitar la configuración de señales en Quix
os.environ["QUIXSTREAMS_DISABLE_SIGNAL_HANDLERS"] = "1"

loglevel_map = {
    0: None,
    1: None,
    2: "INFO"
}

frame_counter = 0

def dynamic_function_mapping(func_name):
    mapping = {
        "signals": "OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection.get_sign_detection",
        "objects": "OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection.get_obj_detection",
        "lane": "OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection.get_lane_detection",
    }
    if func_name not in mapping:
        raise ValueError(f"[ERROR] Function '{func_name}' not available for pipeline")

    module_path, function_name = mapping[func_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, function_name)

# Función para inicializar el caché de funciones
def initialize_function_mapping(perceptions):
    function_cache = {}
    for func_name in perceptions:
        if func_name not in function_cache:
            function_cache[func_name] = dynamic_function_mapping(func_name)
    return function_cache

def execute_operation(message, pipeline, app, loglevel, function_mapping ):
    
    global frame_counter
    
    deserialized_result = json.loads(message.decode('utf-8'))
    
    timestamp = deserialized_result['timestamp']
    sensor_data = deserialized_result['sensor_data']
    sensor_data = base64.b64decode(sensor_data)
    width = deserialized_result['width']
    height = deserialized_result['height']
    
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
    if not pipeline.perceptions:
        print(f"[WARNING] No functions assigned to pipeline: {pipeline.input_sensor}")
        return

    # Ejecutar las funciones asignadas en el pipeline
    func_name = pipeline.perceptions[0]
          
    try:
        # Ejecutar la funcion
        result = function_mapping[func_name](frame)
        
        # Preparar y serializar el resultado
        result_payload = {
            "id": pipeline.input_sensor + "_" + func_name,
            "input_sensor": pipeline.input_sensor,
            "position_sensor": pipeline.sensor_position,
            "type_sensor": pipeline.sensor_type,
            "type_perception": pipeline.perceptions[0],
            "data": result if isinstance(result, (dict, list)) else str(result),
            "timestamp": timestamp,
            "frame_width": width,
            "frame_height": height
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
            if loglevel == 1 or loglevel == 2:
                print(f"[INFO] {pipeline.perceptions[0]} result from {pipeline.input_sensor} sent to : {pipeline.output_decision}")
        except Exception as e:
            print(f"[ERROR] Failed to send result to topic {pipeline.output_decision}: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to process function {func_name} for sensor {pipeline.input_sensor}: {e}")

def run_app(pipeline, loglevel):
    """
    Configura y ejecuta la aplicación Quix Streams en un proceso independiente.
    """
    function_mapping = initialize_function_mapping(pipeline.perceptions)
    
    # Crear una instancia de Application con un consumer_group único
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="latest",
        consumer_group=_generate_random_group_id(),  # Generar un grupo único
        loglevel= loglevel_map[loglevel]
    )
        
    # Configurar el topic de entrada
    input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
    sdf = app.dataframe(input_topic)
    
    # Configurar la función de procesamiento
    def process_message(message):
        execute_operation(message, pipeline, app, loglevel, function_mapping)

    sdf = sdf.update(process_message)
    
    print(f"[INFO] Consumer running for pipeline: {pipeline.input_sensor} consuming {pipeline.perceptions} model")
    
    # Ejecutar la aplicación
    app.run()

def control_perception_streaming(pipelines, loglevel: int = 1):
    """
    Crea procesos independientes para cada pipeline.
    """
    processes = []
    
    final_pipelines = pipelines_transformation(pipelines)
    
    for pipeline in final_pipelines:
        # Crear un nuevo proceso para cada pipeline
        process = multiprocessing.Process(target=run_app, args=(pipeline,loglevel,))
        process.start()
        processes.append(process)

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("[INFO] Terminating perception stream")
        for process in processes:
            process.terminate()


def _generate_random_group_id(length=10):
    """
    Genera un identificador único para el grupo de consumidores.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def pipelines_transformation(pipelines):
    transformed_pipelines = []
    for pipeline in pipelines:
        for perception in pipeline.perceptions:
            new_pipeline = SensorToModelPipeline(
                input_sensor=pipeline.input_sensor,
                sensor_type=pipeline.sensor_type,
                sensor_position=pipeline.sensor_position,
                perceptions=[perception],
                output_decision=pipeline.output_decision
            )
            transformed_pipelines.append(new_pipeline)
    return transformed_pipelines