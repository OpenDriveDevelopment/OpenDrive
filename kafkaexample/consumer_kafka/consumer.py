import cv2
import time
import numpy as np
from quixstreams import Application

def main():
# Create an Application - the main configuration entry point
    app = Application(
        broker_address="localhost:9092",
        auto_offset_reset="earliest"
    )

    # Define a topic with chat messages in JSON format
    messages_topic = app.topic(name="Sensor_Data_1", value_deserializer="bytes")

    with app.get_consumer() as consumer:
        consumer.subscribe(["Sensor_Data_1"])
        
        while True:
            msg = consumer.poll(1)
            
            if msg is None:
                print("Waiting for sensor data")
            elif msg.error() is not None:
                raise Exception(msg.error())
            else:
                kafka_value = msg.value()
                np_array = np.frombuffer(kafka_value, dtype=np.uint8)
                frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR) 
                
                if frame is not None:
                    cv2.imshow('Webcam', frame)
                    cv2.waitKey(500)
                    cv2.destroyAllWindows() 
                else:
                    print("Error deserializing frame")
            
                    
                    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass