from OpenDrive.modules.perception.pipeline_definition.percep_pipeline import SensorToModelPipeline
from OpenDrive.modules.perception.pipeline_definition.perceptions_stream_control import control_perception_streaming

def main():
    pipelines = [
    SensorToModelPipeline(
        input_sensor="sensor_camera_2", 
        sensor_type = "Camera",
        sensor_position = "Custom",
        perceptions = ["signals", "lane"],
        output_decision="output_topic_objects1"
        ),
    ]

    control_perception_streaming(
        pipelines = pipelines,
        loglevel= 0
    )

if __name__ == "__main__":
    main()
    