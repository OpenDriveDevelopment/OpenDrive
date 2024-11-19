import asyncio
from OpenDrive.modules.perception.pipeline_definition.percep_pipeline import SensorToModelPipeline
from OpenDrive.core.perception.perceptions_stream_control import control_perception_streaming


async def main():
    pipeline0 = SensorToModelPipeline(input_sensor="sensor_camera_0", 
                                    vision_models=["objects"],
                                    output_decision="output_topic_name")

    # pipeline1 = SensorToModelPipeline(input_sensor="sensor_camera_1", 
    #                                 vision_models=["signals"],
    #                                 output_decision="output_topic_name")

    await control_perception_streaming([pipeline0])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
