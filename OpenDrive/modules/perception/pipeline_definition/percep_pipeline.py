class SensorToModelPipeline:
    
    def __init__(self, input_sensor, vision_models, output_decision):
        
        self.input_sensor = input_sensor
        self.vision_models = vision_models
        self.output_decision = output_decision