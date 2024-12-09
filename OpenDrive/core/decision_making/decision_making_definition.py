from OpenDrive.modules.decision_making.pipeline_definition.consumer import start_data_reception

def main():
    start_data_reception(models_to_received = 6, output_mode = "document", )


if __name__ == '__main__':
    main()