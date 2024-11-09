from OpenDrive.modules.sensors_prep.sensors.camera import Camera
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

async def main():
    cam1 = Camera(1, 0)
    cam1.enable_sensor()
    
    cam2 = Camera(0, 0)
    cam2.enable_sensor()
    
    # # Crear un evento de parada para controlar la transmisión
    stop_event = asyncio.Event()

    # # Iniciar la transmisión de datos en un hilo separado
    streaming_task1 = asyncio.create_task(cam1.start_data_streaming())  # Ejecuta start_data_streaming sin esperar
    streaming_task2 = asyncio.create_task(cam2.start_data_streaming())  # Ejecuta start_data_streaming sin esperar
    
    stop_command_task = asyncio.create_task(wait_for_stop_command(stop_event))
    

    # Esperar hasta que el usuario escriba "stop"
    await stop_event.wait()

    # Detener la transmisión
    cam1.stop_data_streaming()
    cam2.stop_data_streaming()

    # Cancelar tareas si todavía están en ejecución
    streaming_task1.cancel()
    streaming_task2.cancel()
    
    stop_command_task.cancel()

# Ejecutar la función principal
asyncio.run(main())
