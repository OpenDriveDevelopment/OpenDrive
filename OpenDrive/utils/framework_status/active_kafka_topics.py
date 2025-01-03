def list_active_topics_simulated():
    """
    Simula la lista de topics activos en un cluster de Kafka con nombres realistas y mensajes detallados.
    """
    simulated_topics = [
        "sensors_camera_1", 
        "sensors_camera_2", 
        "sensors_camera_3", 
        "sensors_camera_4", 
        "decision_input_topic", 
        "test_topics",
        "system.logs"
    ]

    print("========== Topics Activos en Kafka ==========")
    print("Conectando al cluster de Kafka...")
    print("Conexión exitosa al cluster en: kafka://localhost:9092\n")

    print("Topics activos detectados:")
    print("----------------------------------------------------------")
    for i, topic in enumerate(simulated_topics, start=1):
        print(f"{i}. Topic: {topic}")
    print("----------------------------------------------------------")
    print(f"Total de topics activos: {len(simulated_topics)}")
    print("==========================================================\n")


# Ejecución de la simulación
if __name__ == "__main__":
    list_active_topics_simulated()
