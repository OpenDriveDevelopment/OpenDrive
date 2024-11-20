import cv2
import wandb
from ultralytics import YOLO
import os

"""Load the model"""
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'yolov8n.pt')

model = YOLO(model_path)

objects_detected = ["person", "car", "bicycle", "motorcycle", "bus", "truck", "traffic light"]

def get_obj_detection_image(image):
    # Realizar la predicción en el frame capturado
    results = model(image, verbose = False)
    
    # Dibujar las predicciones en el frame
    for result in results:
        boxes = result.boxes  # Lista de bounding boxes detectadas
        for box in boxes:
            # Obtener las coordenadas de la caja y la clase detectada
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            class_id = int(box.cls[0])  # ID de la clase predicha
            score = box.conf[0]  # Confianza de la predicción
            
<<<<<<< Updated upstream
            if model.names[class_id] in objects_detected and score > 0.55:
=======
            if model.names[class_id] in objects_detected:
>>>>>>> Stashed changes
                # Dibujar la caja en el frame
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{model.names[class_id]}: {score:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image


    
def get_obj_detection(image):
    results = model(image, verbose=False)
    metadata = []
        
    for result in results:
        boxes = result.boxes  # Lista de bounding boxes detectadas
        for box in boxes:
            # Convertir coordenadas y valores a tipos nativos de Python
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Asegurar que sean enteros
            class_id = int(box.cls[0].item())  # Convertir a entero
            score = float(box.conf[0].item())  # Convertir a flotante
            class_name = model.names[class_id]
<<<<<<< Updated upstream
          
=======
>>>>>>> Stashed changes
            
            if model.names[class_id] in objects_detected:
            # Crear un diccionario con los datos de la detección
                detection_data = {
                    "bounding_box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": score
                }

                metadata.append(detection_data)
               
    return metadata