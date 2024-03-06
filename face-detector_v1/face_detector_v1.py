import time
import cv2
from deepface import DeepFace
import publisher
import os

import tensorflow as tf
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

# Open the webcam
cap = cv2.VideoCapture(0)

DEVICE_ID = f'class{os. getpid()}'


def publish_embedding(embedding) -> None:
    data = {'id': DEVICE_ID,
            'time': time.time(),
            'embedding': embedding}
    publisher.send_message(data=data)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    cv2.imshow('Webcam', frame)    
    
    embeddings = None
    try:
        embeddings = DeepFace.represent(frame, model_name='Facenet512', detector_backend='retinaface')
        print(f"{len(embeddings)} faces detected.")
    except ValueError:
        print("No face.")
        continue
    
    # Check if the face is different from the stored faces
    for embedding in embeddings:
        current_embedding = embedding["embedding"]
        publish_embedding(current_embedding)
    
    # time.sleep(0.05)
        
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
# print(len(stored_embeddings))
