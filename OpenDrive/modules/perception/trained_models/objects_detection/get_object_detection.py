import cv2
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
            
            if model.names[class_id] in objects_detected and score > 0.55:
                # Dibujar la caja en el frame
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{model.names[class_id]}: {score:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image


#### TESTING FUNCTION #####

def estimate_distance( bbox_width ):

    focal_length = 20  # Example focal length
    known_width = 0.3  # Approximate width of the car (in meters)
    distance = (known_width * focal_length) / bbox_width
    
    return distance

from OpenDrive.modules.decision_making.alerts.camera.distance_estimator import estimate_distance

def close_calls_function(x1, x2, y1, y2, height, width, proximity_threshold=80, type="Front"):
    """
    Calculate how close and the position of an object based on the camera type and distance.

    Args:
        x1, x2, y1, y2: bounding_box coordinates.
        height (int): Frame height.
        width (int): Frame width.
        proximity_threshold (int): Threshold to determine if an object is close.
        type (str): Camera type ('Front', 'Rear', 'Left', 'Right').

    Returns:
        tuple: Estimated distance (in meters) and position ('center', 'left', 'right').
    """
    cx = (x1 + x2) // 2  # Center of the bounding box
    bbox_width = x2 - x1
    # Calculate the distance using bounding box width
    distance = estimate_distance(bbox_width)
    position = None  # Default position

    # Adjust proximity thresholds dynamically based on distance
    distance_threshold = 2  # Example: focus on objects within 10 meters

    if distance <= distance_threshold:
        if type in ["Front", "Rear"]:
            # Determine position based on center tolerance
            center_tolerance = 0.1 * width  # Tolerance as a fraction of frame width

            if abs(cx - width // 2) <= center_tolerance:
                position = "center"
            elif cx < width // 2:
                position = "left" if type == "Front" else "right"
            else:
                position = "right" if type == "Front" else "left"

        elif type in ["Left", "Right"]:
            # For lateral cameras, focus on objects within proximity threshold
            if y2 > height - proximity_threshold:
                position = "center"

    return distance, position

def get_obj_detection_image_TESTING(image):

    # Realizar la predicción en el frame capturado
    results = model(image, verbose = False)
    # Obtener alto y ancho de la imagen
    height, width = image.shape[:2]
    # Dibujar las predicciones en el frame
    for result in results:
        boxes = result.boxes  # Lista de bounding boxes detectadas
        for box in boxes:
            # Obtener las coordenadas de la caja y la clase detectada
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            class_id = int(box.cls[0])  # ID de la clase predicha
            score = box.conf[0]  # Confianza de la predicción
            
            if model.names[class_id] in objects_detected and score > 0.55:
                # Dibujar la caja en el frame
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                distance, position = close_calls_function( x1, x2, y1, y2, height, width )
                label = f"{model.names[class_id]}: {score:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                distance_label = f'Distance: {distance:.2f}m'
                cv2.putText(image, distance_label, (x1, y2 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                ## Si el objeto está cerca mostrar el mensaje
                if position: cv2.putText(image, f"Vehiculo cerca {position}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    return image


############################################

    
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