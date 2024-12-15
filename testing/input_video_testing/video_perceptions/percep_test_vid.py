from OpenDrive.modules.perception.pipeline_definition.percep_pipeline import SensorToModelPipeline
from OpenDrive.modules.perception.pipeline_definition.perceptions_stream_control import control_perception_streaming

def main():
    pipelines = [
    SensorToModelPipeline(
        input_sensor="video_Front_1", 
        sensor_type = "Camera",
        sensor_position = "Front",
        output_decision="output_topic_objects1"
        ),
    SensorToModelPipeline(
        input_sensor="video_Rear_1",
        sensor_type = "Camera",
        sensor_position = "Rear",
        output_decision="output_topic_objects1"
        ),
    SensorToModelPipeline(
        input_sensor="video_Right_1", 
        sensor_type = "Camera",
        sensor_position = "RightSide",
        output_decision="output_topic_objects1"
        ),
    SensorToModelPipeline(
        input_sensor="video_Left_1", 
        sensor_type = "Camera",
        sensor_position = "LeftSide",
        output_decision="output_topic_objects1"
        ),
    ]

    control_perception_streaming(
        pipelines = pipelines,
        loglevel= 0
    )

if __name__ == "__main__":
    main()
    