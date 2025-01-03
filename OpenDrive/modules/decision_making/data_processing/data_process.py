from datetime import datetime
import json
import random
import string
import traceback
from datetime import datetime
from collections import defaultdict
from quixstreams import Application
from OpenDrive.modules.decision_making.alerts.camera.close_calls_objects import close_calls_function
from OpenDrive.modules.decision_making.alerts.camera.lane_change import free_lane_change

from OpenDrive.modules.decision_making.alerts.camera.road_obstacles import front_road_obstacles, rear_road_obstacles, side_road_obstacles
from OpenDrive.modules.decision_making.alerts.camera.signals_actions import traffic_signs

last_processed_frame = -1

def _generate_random_group_id(length=10):
    """
    Genera un identificador único para el grupo de consumidores.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def process_data(received_data, models_to_received, output_mode, function_mode, kafka_topic):
    
    """
    Processes received data, ensuring each frame has data from three sensors 
    and meets timestamp requirements.
    """

    global last_processed_frame

    try:
        timestamps_to_delete = []

        # Process timestamps in chronological order
        for timestamp in sorted(received_data.keys()):

            if len(received_data[timestamp]) == models_to_received:


                if last_processed_frame < timestamp:

                    close_objects_position_type_camera = defaultdict( list )
                    processed_data = []
    
                    for sensor_data in received_data[timestamp]:

                        parts = sensor_data[0].split("_")

                        # print(f"Tipo: {parts[0]}")
                        # print(f"Sub-tipo: {parts[1]}")
                        # print(f"Puerto: {parts[2]}")
                        # print(f"Modelo: {parts[3]}")
                        # print(f"Lado: {parts[4]}")
                        # print(f"Height: {parts[5]}")
                        # print(f"Width: {parts[6]}")
                        # print(f"Data: {sensor_data[1]}")

                        # current_timestamp = int(datetime.now().timestamp() * 1e9)
                        # Calcular la diferencia en milisegundos
                        # difference_ms = (current_timestamp - timestamp) / 1_000_000
                        # Imprimir la diferencia
                        # print(f"Diferencia en milisegundos: {difference_ms} ms")

                        ################## FEATURE SPACE ##########################

                        data_objects = sensor_data[1]

                        coordenates = [] 
                        objects = []
                        

                        if parts[3] != "lane":
                            for data_object in data_objects:
                                    
                                x1, x2 = data_object["bounding_box"]["x1"], data_object["bounding_box"]["x2"]
                                y2 = data_object["bounding_box"]["y2"]
                                coordenates.append( ( x1, x2, y2 ) )
                                objects.append( ( data_object["class_name"], data_object["confidence"] ) )


                        height = int(parts[5])
                        width =  int(parts[6])

                        if parts[3] == "objects":

                            close_objects = close_calls_function( coordenates, objects ,height, width, type = parts[4] )
                            close_objects_position = [ position[1] for position in close_objects ]
                            close_objects_position_type_camera[ parts[ 4 ] ] = close_objects_position  

                            if parts[4] == "Front":

                                front_obstacles = front_road_obstacles(objects, coordenates, height, width)
                                if front_obstacles["front_road_obstacles"]:
                                    processed_data.append(front_obstacles)

                            elif parts[4] == "Rear":

                                rear_obstacles = rear_road_obstacles(objects, coordenates, height, width)
                                if rear_obstacles["rear_road_obstacles"]:
                                    processed_data.append(rear_obstacles)

                            elif parts[4] in ["LeftSide", "RightSide"]:

                                side_obstacles = side_road_obstacles(objects, coordenates, height, width, parts[4])
                                if side_obstacles["side_obstacles"]:
                                    processed_data.append(side_obstacles)

                        if parts[3] == "signals":

                            output_signals = traffic_signs( objects )
                            if output_signals['traffic_signs']:
                                processed_data.append(output_signals)

                    if close_objects_position_type_camera and "Rear" in close_objects_position_type_camera: 

                        lane_change = free_lane_change( close_objects_position_type_camera )
                        processed_data.append(lane_change)

                        
                    ###########################################################
                    readable_time = datetime.fromtimestamp(timestamp / 1e9)

                    if output_mode == "console":
                        print("-------------------------------------------------------------------")
                        print(f"Processing frame at timestamp {readable_time.strftime('%Y-%m-%d %H:%M:%S.%f')}:")
                        for information in processed_data:
                            print(information)
                    elif output_mode == "document":
                        print("Generating document")
                        with open("OpenDrive/outputs/output.txt", "a") as file:
                            file.write(f"Processing frame at timestamp {readable_time.strftime('%Y-%m-%d %H:%M:%S.%f')}:\n")
                            for information in processed_data:
                                file.write(f"{information}\n")  # Escribe cada elemento seguido de un salto de línea

                    elif output_mode == "kafka":
                        print("Publishing in new kafka topic")
                        app = Application(
                            broker_address="localhost:9092",
                            auto_offset_reset="latest",
                            consumer_group=_generate_random_group_id(),  # Generar un grupo único
                        )

                        result_payload = {
                            "data": str(processed_data),
                            "timestamp": timestamp
                        }
                        serialized_result = json.dumps(result_payload)

                        try:
                            messages_topic = app.topic(name=kafka_topic, value_serializer="bytes")
                            with app.get_producer() as producer:
                                producer.produce(
                                    topic = messages_topic.name,
                                    key = sensor_data[0],
                                    value = serialized_result.encode('utf-8')
                                )
                        except Exception as e:
                            print(f"[ERROR] Failed to send result to topic {kafka_topic}: {e}")

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
