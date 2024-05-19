import csv
import os
import cv2
from deepface import DeepFace
import tensorflow as tf


index = 0


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Set a fixed amount of GPU memory (in MB)
        for gpu in gpus:
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3700)]
            )
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

def crop_and_save(img, facial_area, save_path):
    x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
    cropped_image = img[y:y+h, x:x+w]
    cv2.imwrite(save_path, cropped_image)

def get_face_embeddings(image_path):
    img = cv2.imread(image_path)
    embeddings = DeepFace.represent(img, model_name='Facenet512', detector_backend='retinaface')
    
    face_regions = [emb["facial_area"] for emb in embeddings]
    for i, face in enumerate(face_regions):
        crop_and_save(img, face, f"./faces/{index+i}-{index}.{i}.jpg")
    
    
    embeddings = [emb["embedding"] for emb in embeddings]

    # Save embeddings to CSV
    with open('embeddings.csv', 'a') as csvfile:
        fieldnames = ['index', 'embedding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i, embedding in enumerate(embeddings):
            writer.writerow({'index': index+i, 'embedding': ','.join(map(str, embedding))})

 


if __name__ == "__main__":
    input_directory = "./images"
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_directory, filename)
            get_face_embeddings(image_path)
            print(image_path)
            index += 1
    
    
