import numpy as np
import cv2

def resize_image_CV(frame, output_size=(556, 556)):
    """
    Redimensiona un frame (imagen de OpenCV) a un tamaño específico manteniendo la proporción.
    
    :param frame: Frame de entrada generado por OpenCV.
    :param output_size: Tamaño de salida en formato (ancho, alto).
    :return: La imagen redimensionada como frame de OpenCV.
    """
    # Obtener las proporciones originales
    h, w = frame.shape[:2]
    new_w, new_h = output_size
    
    # Calcular las nuevas dimensiones manteniendo la proporción
    aspect_ratio = w / h
    if aspect_ratio > 1:
        # Ancho mayor
        new_h = int(new_w / aspect_ratio)
    else:
        # Alto mayor
        new_w = int(new_h * aspect_ratio)
    
    # Redimensionar la imagen sin distorsionar
    resized_frame = cv2.resize(frame, (new_w, new_h))
    
    # Crear una nueva imagen con bordes blancos para rellenar
    new_frame = cv2.copyMakeBorder(resized_frame, 
                                    (new_h - resized_frame.shape[0]) // 2, 
                                    (new_h - resized_frame.shape[0]) // 2,
                                    (new_w - resized_frame.shape[1]) // 2, 
                                    (new_w - resized_frame.shape[1]) // 2, 
                                    cv2.BORDER_CONSTANT, 
                                    value=(255, 255, 255))  # Color blanco
    
    return new_frame


def scale_pixel_values(frame, new_min=0, new_max=1):
    """
    Escala los valores de los píxeles de la imagen al rango [new_min, new_max].
    
    :param image: La imagen de entrada (en formato NumPy array, de OpenCV).
    :param new_min: El valor mínimo de la escala.
    :param new_max: El valor máximo de la escala.
    :return: La imagen con los valores de píxeles escalados.
    """
    # Convertir la imagen a tipo float para evitar overflow al escalar
    frame_float = frame.astype(np.float32)
    
    # Encontrar el valor mínimo y máximo de los píxeles en la imagen original
    min_val = np.min(frame_float)
    max_val = np.max(frame_float)
    
    # Escalar la imagen a un rango entre new_min y new_max
    scaled_frame = (frame_float - min_val) / (max_val - min_val)  # Normalización al rango [0, 1]
    scaled_frame = scaled_frame * (new_max - new_min) + new_min  # Reescalar al rango [new_min, new_max]
    
    # Convertir de vuelta a la escala original (si es necesario)
    scaled_frame = np.clip(scaled_frame, new_min, new_max)  # Asegurarse de que los valores no se salgan de rango
    
    return scaled_frame

def dynamic_normalization(frame, alpha=1.2, beta=20, saturation_scale=1.2, threshold=50):
    """
    Normaliza una imagen de forma condicional, solo si está fuera de los parámetros óptimos.
    
    :param frame: Imagen o frame en formato BGR.
    :param alpha: Factor de contraste.
    :param beta: Factor de brillo.
    :param saturation_scale: Escala de saturación.
    :param threshold: Límite del histograma para aplicar normalización.
    :return: Imagen normalizada o la original si ya está en buen estado.
    """
    # Evaluar brillo promedio de la imagen
    brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    print(brightness)
    print(threshold)
    if brightness <= threshold:
        # Ajustar contraste y brillo si la imagen es demasiado oscura
        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        
        # Ajustar saturación en espacio HSV
        hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
        hsv = hsv.astype(np.float32)
        hsv[:, :, 1] *= saturation_scale
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv = hsv.astype(np.uint8)
        
        # Volver a BGR
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    else:
        # Imagen ya está en buen estado, no ajustar
        return frame

# Ejemplo de uso 
#Reading a video from file
cap = cv2.VideoCapture('video2.mp4') 

while(cap.isOpened()):

    # capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display a frame
        
        frame_2 = scale_pixel_values(frame)
        cv2.imshow('Frame', frame_2)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Release the capture object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()

##############

# Uso en un frame
# frame = resize_image_CV(cv2.imread("juan.png"))
# output = dynamic_normalization(frame)
# cv2.imshow("Original", frame)
# cv2.imshow("Normalizado", output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()