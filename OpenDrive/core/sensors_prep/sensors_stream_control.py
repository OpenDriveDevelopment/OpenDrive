import asyncio

async def wait_for_stop_command(stop_event):
    # Esperar a que el usuario introduzca "stop" sin bloquear el bucle principal
    while True:
        command = await asyncio.to_thread(input, "Escribe 'stop' para detener la transmisión: ")
        if command.strip().lower() == "stop":
            stop_event.set()  # Activar el evento de parada
            break
        else:
            print("Comando no válido. Escribe 'stop' para detener la transmisión.")

async def start_sensors_streaming(sensors):
    
    if not sensors:
        print("[ERROR] No sensors have been provided for streaming")
        return
     
    # # Crear un evento de parada para controlar la transmisión
    stop_event = asyncio.Event()
    
    streaming_task_list = []

    for sensor in sensors:
        # # Iniciar la transmisión de datos en un hilo separado
        streaming_task = asyncio.create_task(sensor.start_data_streaming()) # Ejecuta start_data_streaming sin esperar
        streaming_task_list.append(streaming_task)

    stop_command_task = asyncio.create_task(wait_for_stop_command(stop_event))
    # Esperar hasta que el usuario escriba "stop"
    await stop_event.wait()
    
    for sensor in sensors:
        sensor.stop_data_streaming()

    for task in streaming_task_list:
        # Cancelar tareas si todavía están en ejecución
        task.cancel()
        
    stop_command_task.cancel()