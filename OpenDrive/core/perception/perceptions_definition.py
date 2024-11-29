from OpenDrive.modules.perception.pipeline_definition.percep_pipeline import SensorToModelPipeline
from OpenDrive.modules.perception.pipeline_definition.perceptions_stream_control import control_perception_streaming

def main():
    pipelines = [
    SensorToModelPipeline(
        input_sensor="sensor_camera_0", 
        sensor_type = "Camera",
        sensor_position = "Frontal",
        output_decision="output_topic_objects1"
        ),
    SensorToModelPipeline(
        input_sensor="sensor_camera_1", 
        sensor_type = "Camera",
        sensor_position = "Side",
        output_decision="output_topic_objects1"
        )
    ]

    control_perception_streaming(pipelines)

if __name__ == "__main__":
    main()
    
    