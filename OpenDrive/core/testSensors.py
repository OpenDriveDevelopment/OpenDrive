from OpenDrive.modules.sensors.camera import Camera
import asyncio

async def stop_streaming_after_delay(cam, delay):
    await asyncio.sleep(delay)
    cam.stop_data_streaming()

async def main():
    cam1 = Camera(0, 0)
    cam1.enable_sensor()

    # Iniciar la transmisión de datos en un hilo separado
    asyncio.create_task(stop_streaming_after_delay(cam1, 10))  # Tarea para detener streaming
    await cam1.start_data_streaming()  # Iniciar en hilo separado

# Ejecutar la función principal
asyncio.run(main())