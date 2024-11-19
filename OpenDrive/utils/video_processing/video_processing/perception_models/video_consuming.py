from OpenDrive.modules.perception.trained_models.objects_detection.get_object_detection import get_obj_detection_image
from OpenDrive.modules.perception.trained_models.lane_detection.get_lane_detection import get_lane_detection_image
from OpenDrive.modules.perception.trained_models.traffic_sign_detection.get_traffic_sign_detection import get_sign_detection_image
from OpenDrive.modules.sensors_prep.data_preprocessing.image_normalization import resize_image_CV
import cv2
import threading
def camara_Frontal():
    print("Funciones de captura")
    captureFrame = cv2.VideoCapture('OpenDrive/utils/video_processing/input_videos/simulador1-Frontal.mp4') 
    # Obtener propiedades del video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el formato .mp4
    width = int(captureFrame.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(captureFrame.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captureFrame.get(cv2.CAP_PROP_FPS))
    output_video = cv2.VideoWriter('OpenDrive/utils/video_processing/output_videos/simulador1-Frontal-O.mp4', fourcc, fps, (556, 556))
    while captureFrame.isOpened():
        ret, frame = captureFrame.read()
        if ret == True:
            image_processed = get_obj_detection_image(frame)
            image_processed_sings = get_sign_detection_image(image_processed)
            # output_video.write(image_processed_sings)
            cv2.imshow('Frame_Frontal', resize_image_CV(image_processed_sings))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            print("No se leyeron mas frames")
            break        
    captureFrame.release()
    output_video.release()
    

def camara_Trasero():
    print("Funciones de captura")
    captureFrame = cv2.VideoCapture('OpenDrive/utils/video_processing/input_videos/simulador1-Trasero.mp4') 
    # Obtener propiedades del video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el formato .mp4
    width = int(captureFrame.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(captureFrame.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captureFrame.get(cv2.CAP_PROP_FPS))
    output_video = cv2.VideoWriter('OpenDrive/utils/video_processing/output_videos/simulador1-Trasero-O.mp4', fourcc, fps, (556, 556))
    while captureFrame.isOpened():
        ret, frame = captureFrame.read()
        if ret == True:
            image_processed = get_obj_detection_image(frame)
            image_processed_sings = get_sign_detection_image(image_processed)
            # output_video.write(image_processed_sings)

            cv2.imshow('Frame_Trasero', resize_image_CV(image_processed_sings))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            print("No se leyeron mas frames")
            break        
    captureFrame.release()
    output_video.release()
    
def camara_Izquierda():
    print("Funciones de captura")
    captureFrame = cv2.VideoCapture('OpenDrive/utils/video_processing/input_videos/simulador1-Izquierdo.mp4') 
    # Obtener propiedades del video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el formato .mp4
    width = int(captureFrame.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(captureFrame.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captureFrame.get(cv2.CAP_PROP_FPS))
    output_video = cv2.VideoWriter('OpenDrive/utils/video_processing/output_videos/simulador1-Trasero-O.mp4', fourcc, fps, (556, 556))
    while captureFrame.isOpened():
        ret, frame = captureFrame.read()
        if ret == True:
            image_processed = get_obj_detection_image(frame)
            image_processed_sings = get_sign_detection_image(image_processed)
            # output_video.write(image_processed_sings)

            cv2.imshow('Frame_Izquierdo', resize_image_CV(image_processed_sings))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            print("No se leyeron mas frames")
            break        
    captureFrame.release()
    output_video.release()

def camara_Derecha():
    print("Funciones de captura")
    captureFrame = cv2.VideoCapture('OpenDrive/utils/video_processing/input_videos/simulador1-Derecho.mp4') 
    # Obtener propiedades del video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el formato .mp4
    width = int(captureFrame.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(captureFrame.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captureFrame.get(cv2.CAP_PROP_FPS))
    output_video = cv2.VideoWriter('OpenDrive/utils/video_processing/output_videos/simulador1-Trasero-O.mp4', fourcc, fps, (556, 556))
    while captureFrame.isOpened():
        ret, frame = captureFrame.read()
        if ret == True:
            image_processed = get_obj_detection_image(frame)
            image_processed_sings = get_sign_detection_image(image_processed)
            # output_video.write(image_processed_sings)

            cv2.imshow('Frame_Derecho', resize_image_CV(image_processed_sings))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            print("No se leyeron mas frames")
            break        
    captureFrame.release()
    output_video.release()


thread1 = threading.Thread(target=camara_Frontal)
thread2 = threading.Thread(target=camara_Trasero)
thread3 = threading.Thread(target=camara_Derecha)
thread4 = threading.Thread(target=camara_Izquierda)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Esperar a que los hilos terminen
thread1.join()
thread2.join()
thread3.join()
thread4.join()