from OpenDrive.modules.decision_making.pipeline_definition.consumer import start_data_reception

def main():
    start_data_reception(
        models_to_received = 5, 
        topic = "output_topic_objects1", 
        output_mode = "console", 
        function_mode = "four_cameras", 
        kafka_topic = "processed_data_output"
    )
    

if __name__ == '__main__':
    main()