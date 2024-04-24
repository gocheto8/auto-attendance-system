import time

import cv2
import publisher
import tensorflow as tf
from deepface import DeepFace

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3700)],
            )
        logical_gpus = tf.config.experimental.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)

cap = cv2.VideoCapture(0)

# DEVICE_ID = f'class{os. getpid()}'
DEVICE_ID = "room201"


def publish_embedding(embedding) -> None:
    data = {"id": DEVICE_ID, "time": time.time(), "embedding": embedding}
    publisher.send_message(data=data)


while True:
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)

    embeddings = None
    try:
        embeddings = DeepFace.represent(
            frame, model_name="Facenet512", detector_backend="retinaface"
        )
        print(f"{len(embeddings)} faces detected.")
    except ValueError:
        print("No face.")
        continue

    for embedding in embeddings:
        current_embedding = embedding["embedding"]
        publish_embedding(current_embedding)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
