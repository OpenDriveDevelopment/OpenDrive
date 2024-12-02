import asyncio
from datetime import datetime

async def wait_for_stop_command(stop_event):
    """Wait for the user to type 'stop' or press Ctrl+C to stop the streaming."""
    try:
        while True:
            try:
                command = await asyncio.to_thread(input, "Type 'stop' or 'ctrl + c' to stop the streaming: ")
                if command.strip().lower() == "stop":
                    stop_event.set()  # Trigger the stop event
                    break
                else:
                    print("Invalid command. Type 'stop' or 'ctrl + c' to stop the streaming.")
            except EOFError:
                print("\n[WARNING] Error detected, triggering stop event.")
                stop_event.set()
                break
    except KeyboardInterrupt:
        print("\n[WARNING] Ctrl+C pressed, stopping streaming...")
        stop_event.set()

    finally:
        stop_event.set()

async def start_sensors_streaming_internal(sensors, loglevel):
    
    # # Crear un evento de parada para controlar la transmisión
    stop_event = asyncio.Event()
    
    streaming_task_list = []
    
    sensors_start_time = int(datetime.now().timestamp() * 1e9)

    for sensor in sensors:
        # # Iniciar la transmisión de datos en un hilo separado
        streaming_task = asyncio.create_task(sensor.start_data_streaming(sensors_start_time, loglevel)) # Ejecuta start_data_streaming sin esperar
        streaming_task_list.append(streaming_task)

    stop_command_task = asyncio.create_task(wait_for_stop_command(stop_event))
    # Esperar hasta que el usuario escriba "stop"
    await stop_event.wait()
    
    for sensor in sensors:
        sensor.stop_data_streaming()

    for task in streaming_task_list:
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass
            
    stop_command_task.cancel()
    
    
def start_sensors_streaming(sensors, loglevel= 0):
    
    if not sensors:
        print("[ERROR] No sensors have been provided for streaming")
        return
   
    try:
        for sensor in sensors:
            if sensor.state != "Enabled":
                raise RuntimeError(f"[ERROR] The sensor {sensor.sensor_id} it is not enabled.")

        asyncio.run(start_sensors_streaming_internal(sensors, loglevel))
    except KeyboardInterrupt:
        print("\n[WARNING] Streaming stoped by user.")