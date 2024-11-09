import cv2
import wandb
from ultralytics import YOLO
import os

"""Load the model"""
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'signDetection.pt')

model = YOLO(model_path)


def real_time_prediction(image):
        # Realizar la predicción en el frame capturado
        results = model(image)
        
        # Dibujar las predicciones en el frame
        for result in results:
            boxes = result.boxes  # Lista de bounding boxes detectadas
            for box in boxes:
                # Obtener las coordenadas de la caja y la clase detectada
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
                class_id = int(box.cls[0])  # ID de la clase predicha
                score = box.conf[0]  # Confianza de la predicción
                
                # Dibujar la caja en el frame
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{model.names[class_id]}: {score:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image