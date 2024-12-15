from quixstreams import Application

class DataProducer:
    """
    A class for producing data to a Quix topic.

    Attributes:
        data_type (str): The type of data being produced.
        data_subtype (str): The subtype of data being produced.
        producer_id (str): The unique ID of the producer.
        broker_address (str): The address of the Kafka broker.
    """

    def __init__(self, data_type: str, data_subtype: str, producer_id: str, broker_address: str = "localhost:9092", loglevel: int = 1):
        """
        Initializes a new instance of the DataProducer class.

        Args:
            data_type (str): The type of data being produced.
            data_subtype (str): The subtype of data being produced.
            producer_id (str): The unique ID of the producer.
            broker_address (str, optional): The address of the Kafka broker. Defaults to "localhost:9092".
        """
        logingstring = None
        if loglevel == 1:
            logingstring = "INFO"
             
        self.data_type = data_type
        self.data_subtype = data_subtype
        self.producer_id = producer_id
        self.app = Application(broker_address=broker_address, loglevel= logingstring)
        self.topic = self.app.topic(name=self._build_topic_name(), value_serializer="bytes")
        self.producer = self.app.get_producer()

    def _build_topic_name(self) -> str:
        """
        Builds the topic name based on the data type, subtype, and producer ID.

        Returns:
            str: The generated topic name.
        """
        return f"{self.data_type}_{self.data_subtype}_{self.producer_id}"

    def send_data(self, message_value: bytes, message_key: str = "1") -> None:
        """
        Sends data to the specified topic.

        Args:
            message_value (bytes): The value of the message to send.
            message_key (str, optional): The key for the message. Defaults to "1".
        """
        self.producer.produce(
            topic=self.topic.name,
            key=message_key,
            value=message_value,
        )
