import time
import cv2
from quixstreams import Application

def main():
    app = Application(
        broker_address="localhost:9092",
    )
    messages_topic = app.topic(name="Sensor_Data_1", value_serializer="bytes")

    with app.get_producer() as producer:
        cap = cv2.VideoCapture(1)
            
        while True:
            print("Producing sensor data")
            if cap.isOpened():
                ret, frame = cap.read()
                
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                kafka_msg_value = buffer.tobytes()
                
                producer.produce(
                    topic = messages_topic.name,
                    key = "1",
                    value = kafka_msg_value,
                )
                
            else:
                print("error serializing frame")
            
            time.sleep(3)
    
if __name__ == "__main__":
    main()