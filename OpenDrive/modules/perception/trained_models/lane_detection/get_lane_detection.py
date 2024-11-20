from tensorflow import keras
import cv2
import numpy as np
import os

IMG_SIZE = 128

"""Load the model"""
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'laneDetection.h5')
model = keras.models.load_model(model_path)

""" Function to calculate mask over image """
def weighted_img(img, initial_img, α=1., β=0.5, γ=0.):
    return cv2.addWeighted(initial_img, α, img, β, γ)

""" Function to process an individual image """
def get_lane_detection_image(image, width, height):
    """Preprocess image"""
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    """Get the binary mask"""

    pred_mask = model.predict(np.expand_dims(image, axis = 0)) 
    mask = np.round_(pred_mask[0])
    
    """Convert to mask image"""

    zero_image = np.zeros_like(mask)
    mask = np.dstack((mask, zero_image, zero_image)) * 255
    mask = np.asarray(mask, np.uint8)
    
    """Get the final image"""

    final_image = weighted_img(mask, image, α = 1, β = 0.5, γ = 0.1)
    final_image = cv2.resize(final_image, (width, height))

    return final_image

def get_lane_detection(image):
    # Preprocesar la imagen
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    # Obtener la máscara binaria predicha por el modelo
    pred_mask = model.predict(np.expand_dims(image, axis=0))
    # Redondear la máscara predicha para obtener valores binarios (0 o 1)
    mask = np.round_(pred_mask[0])
    # Convertir la máscara a una lista de listas para compatibilidad con JSON
    mask_list = mask.tolist()
    # Empaquetar la máscara en un diccionario
    metadata = {
        "lane_mask": mask_list
    }
    return metadata