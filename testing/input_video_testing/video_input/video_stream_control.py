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

async def start_sensors_streaming_internal(videos, loglevel):
    
    # # Crear un evento de parada para controlar la transmisión
    stop_event = asyncio.Event()
    
    streaming_task_list = []
    
    videos_start_time = int(datetime.now().timestamp() * 1e9)

    for video in videos:
        # # Iniciar la transmisión de datos en un hilo separado
        streaming_task = asyncio.create_task(video.start_data_streaming(videos_start_time, loglevel)) # Ejecuta start_data_streaming sin esperar
        streaming_task_list.append(streaming_task)

    stop_command_task = asyncio.create_task(wait_for_stop_command(stop_event))
    # Esperar hasta que el usuario escriba "stop"
    await stop_event.wait()
    
    for video in videos:
        video.stop_data_streaming()

    for task in streaming_task_list:
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass
            
    stop_command_task.cancel()
    
    
def start_videos_streaming(videos, loglevel= 0):
    
    if not videos:
        print("[ERROR] No sensors have been provided for streaming")
        return
   
    
    asyncio.run(start_sensors_streaming_internal(videos, loglevel))
   