# import asyncio
# import json
# from functools import partial
# from quixstreams import Application
# import cv2
# import numpy as np
# import time

# import random
# import string


# from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection
# from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection
# from OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection import get_sign_detection

# function_mapping = {
#     "signals": get_sign_detection,
#     "objects": get_obj_detection,
#     "lane": get_lane_detection,
# }

# def execute_operation(message, pipeline, app):
#     print("PIPELINE COMING " + pipeline.input_sensor)
#     print("****************************************************")
    
#     # Se obtiene la lista de los modelos por los cuales debe pasar la informacion del sensor
#     functions_to_execute = pipeline.vision_models
    
    
#     np_array = np.frombuffer(message, dtype=np.uint8)
#     frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
#     if frame is None:
#         print("Couldn't get frame")
#         return

#     for func_name in functions_to_execute:
        
#         if func_name in function_mapping:
            
#             # start_time = time.perf_counter()
            
#             result = function_mapping[func_name](frame)
            
#             # end_time = time.perf_counter()
            
            
#             # elapsed_time = end_time - start_time
#             # print(f"El código tardó {elapsed_time:.4f} segundos en ejecutarse.")
            
#             print(f"Result type: {type(result)}")
#             print(f"Result content: {result}")

#             if isinstance(result, dict):
#                 serialized_result = json.dumps(result)
#             elif isinstance(result, list):
#                 # Serializar la lista completa como JSON
#                 serialized_result = json.dumps(result)
#             else:
#                 try:
#                     serialized_result = result.tojson()
#                 except AttributeError:
#                     print(f"Unexpected result type: {type(result)}")
#                     return

      
#             # print("Serialized Result:", serialized_result)
            
#             messages_topic = app.topic(name="output_topic_name", value_serializer="bytes")
            
#             with app.get_producer() as producer:
#                 producer.produce(
#                     topic = messages_topic.name,
#                     key = "1",
#                     value = serialized_result.encode('utf-8')
#                 )
                  
#         else:
#             print(f"Function for '{func_name}' not defined.")
    
    
# async def control_perception_streaming(pipelines):
    
#     if not pipelines:
#         print("No perception pipelines have been provided for streaming")
#         return
    
    
#     longitud = 10

# # Caracteres a utilizar
#     caracteres = string.ascii_letters + string.digits  # Letras y números

#     # Generar el string aleatorio
#     string_random = ''.join(random.choices(caracteres, k=longitud))
    
#     app = Application(
#         broker_address="localhost:9092",
#         auto_offset_reset="latest",
#         consumer_group= string_random
#     )
    
#     for pipeline in pipelines:
#         input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
#         sdf = app.dataframe(input_topic)
#         sdf = sdf.update(partial(execute_operation, pipeline=pipeline, app=app)) ## Es necesario utilizar el partial para que los parametros de la funcion sean pasados correctamente
        
#     app.run()




##########################################################

# import multiprocessing
# import json
# import os
# from quixstreams import Application
# import cv2
# import numpy as np
# import string
# import random

# from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection
# from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection
# from OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection import get_sign_detection

# # Deshabilitar la configuración de señales en Quix
# os.environ["QUIXSTREAMS_DISABLE_SIGNAL_HANDLERS"] = "1"

# # Mapeo de funciones de modelos
# function_mapping = {
#     "signals": get_sign_detection,
#     "objects": get_obj_detection,
#     "lane": get_lane_detection,
# }

# def execute_operation(message, pipeline):
#     print("======================")
#     print(f"Processing pipeline for sensor: {pipeline.input_sensor}")
#     print("======================")
    
#     # Convertir el mensaje a un frame
#     np_array = np.frombuffer(message, dtype=np.uint8)
#     frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#     if frame is None:
#         print("Couldn't decode frame")
#         return

#     # Ejecutar las funciones mapeadas
#     for func_name in pipeline.vision_models:
#         if func_name in function_mapping:
#             result = function_mapping[func_name](frame)
#             print(f"Processed {func_name}: {result}")

#             # Serialización del resultado
#             try:
#                 serialized_result = json.dumps(result) if isinstance(result, (dict, list)) else result.tojson()
#             except AttributeError:
#                 print(f"Unexpected result type for {func_name}: {type(result)}")
#                 continue

#             # Enviar el resultado al topic de salida
#             print(f"Result for {func_name}: {serialized_result}")

# def run_app(pipeline):
#     """
#     Configura y ejecuta la aplicación Quix Streams en un proceso independiente.
#     """
#     # Crear una instancia de Application con un consumer_group único
#     app = Application(
#         broker_address="localhost:9092",
#         auto_offset_reset="latest",
#         consumer_group=_generate_random_group_id()  # Generar un grupo único
#     )
    
#     # Configurar el topic de entrada
#     input_topic = app.topic(name=pipeline.input_sensor, value_deserializer="bytes")
#     sdf = app.dataframe(input_topic)

#     # Configurar la función de procesamiento
#     def process_message(message):
#         execute_operation(message, pipeline)

#     sdf = sdf.update(process_message)
#     print(f"Consumer running for pipeline: {pipeline.input_sensor}")
    
#     # Ejecutar la aplicación
#     app.run()

# def control_perception_streaming(pipelines):
#     """
#     Crea procesos independientes para cada pipeline.
#     """
#     processes = []

#     for pipeline in pipelines:
#         # Crear un nuevo proceso para cada pipeline
#         process = multiprocessing.Process(target=run_app, args=(pipeline,))
#         process.start()
#         processes.append(process)

#     # Esperar a que los procesos terminen (normalmente no lo harán porque `app.run()` es bloqueante)
#     for process in processes:
#         process.join()

# def _generate_random_group_id(length=10):
#     """
#     Genera un identificador único para el grupo de consumidores.
#     """
#     chars = string.ascii_letters + string.digits
#     return ''.join(random.choices(chars, k=length))

##############################################################

import multiprocessing
import json
import os
from quixstreams import Application
import cv2
import numpy as np
import string
import random
import time



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

def execute_operation(message, pipeline, app):
    print(f"Processing pipeline for sensor: {pipeline.input_sensor}")
    
    # Convertir el mensaje a un frame
    np_array = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if frame is None:
        print("Couldn't decode frame")
        return

    # Ejecutar las funciones mapeadas
    for func_name in pipeline.vision_models:
        if func_name in function_mapping:
            
            start_time = time.time()
            result = function_mapping[func_name](frame)
            end_time = time.time()
            
            elapsed_time = end_time - start_time
            print(f"Tiempo de sensor {pipeline.input_sensor} de funcion {pipeline.vision_models[0]}  fue de : {elapsed_time:.5f} segundos")   
            
            print(f"Processed {func_name}: {result}")



            #####################333
            # Serialización del resultado
            try:
                serialized_result = json.dumps(result) if isinstance(result, (dict, list)) else result.tojson()
            except AttributeError:
                print(f"Unexpected result type for {func_name}: {type(result)}")
                continue
            
            ###############################
            try:
                if isinstance(result, dict):
                    result["input_sensor"] = pipeline.input_sensor
                elif isinstance(result, list):
                    result = {"input_sensor": pipeline.input_sensor, "data": result}
                else:
                    # En caso de que el resultado no sea dict ni lista, manejar como un string genérico
                    result = {"input_sensor": pipeline.input_sensor, "data": str(result)}
                
                # Serialización del resultado
                serialized_result = json.dumps(result)
            except AttributeError:
                print(f"Unexpected result type for {func_name}: {type(result)}")
                continue
            

            # Enviar el resultado al topic de salida
            try:
                # producer = app.get_producer(topic_name=pipeline.output_decision)
                # producer.produce(key="result", value=serialized_result.encode("utf-8"))
                # print(f"Result for {func_name} sent to topic: {pipeline.output_decision}")
                
                messages_topic = app.topic(name=pipeline.output_decision, value_serializer="bytes")
            
                with app.get_producer() as producer:
                    producer.produce(
                        topic = messages_topic.name,
                        key = "1",
                        value = serialized_result.encode('utf-8')
                    )
                    
            except Exception as e:
                print(f"Error sending result to topic {pipeline.output_decision}: {e}")

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
    print(f"Consumer running for pipeline: {pipeline.input_sensor}")
    
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
