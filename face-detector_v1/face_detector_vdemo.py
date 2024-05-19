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

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("./Diplomna_demo.mp4")


# NOTE for demo
# fourcc = cv2.VideoWriter.fourcc(*'XVID')
# out = cv2.VideoWriter('out.avi', fourcc, 30, (1280, 720))
# NOTE end demo

# DEVICE_ID = f'class{os. getpid()}'
DEVICE_ID = "room201"


def publish_embedding(embedding) -> None:
    data = {"id": DEVICE_ID, "time": time.time(), "embedding": embedding}
    publisher.send_message(data=data)


while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

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
        confidence = embedding["face_confidence"]
        if confidence < 1:
            continue
        
        # NOTE This part of the code is strictly for the demo
        # area = embedding["facial_area"]
        # cv2.rectangle(
        #     frame,
        #     (area["x"], area["y"]),
        #     (area["x"] + area["w"], area["y"] + area["h"]),
        #     (0, 255, 0),
        #     2,
        # )

        
        # confidence_text = f"Conf: {confidence*100}%"
        # cv2.putText(
        #     frame,
        #     confidence_text,
        #     (area["x"], area["y"] + area["h"] + 20),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5,
        #     (0, 255, 0),
        #     2,
        # )
        #  NOTE EOF code for demo
        
        publish_embedding(embedding["embedding"])

    # cv2.imshow("Webcam", frame)
    
    # NOTE for demo
    # out.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
