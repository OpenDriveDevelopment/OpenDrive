import cv2
import numpy as np
from quixstreams import Application

class DataConsumer:
    """
    A class for producing data to a Quix topic.

    Attributes:
        data_type (str): The type of data being produced.
        data_subtype (str): The subtype of data being produced.
        producer_id (str): The unique ID of the producer.
        broker_address (str): The address of the Kafka broker.
    """

    def __init__(self, data_type: str, data_subtype: str, producer_id: str, broker_address: str = "localhost:9092"):
        """
        Initializes a new instance of the DataProducer class.

        Args:
            data_type (str): The type of data being produced.
            data_subtype (str): The subtype of data being produced.
            producer_id (str): The unique ID of the producer.
            broker_address (str, optional): The address of the Kafka broker. Defaults to "localhost:9092".
        """
        self.data_type = data_type
        self.data_subtype = data_subtype
        self.producer_id = producer_id
        self.app = Application(broker_address=broker_address)
        self.consumer = self.app.get_consumer()
        self.consumer.subscribe([self._build_topic_name()])

    def _build_topic_name(self) -> str:
        """
        Builds the topic name based on the data type, subtype, and producer ID.

        Returns:
            str: The generated topic name.
        """
        return f"{self.data_type}_{self.data_subtype}_{self.producer_id}"

    def get_data(self, message_key: str = "1") -> bytes:
        """
        Sends data to the specified topic.

        Args:
            message_value (bytes): The value of the message to send.
            message_key (str, optional): The key for the message. Defaults to "1".
        """
        msg = self.consumer.poll(message_key)
        
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

            return kafka_value
