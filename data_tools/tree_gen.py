import cv2
import psycopg2
import numpy as np
from deepface import DeepFace
from annoy import AnnoyIndex
from datetime import datetime
import tensorflow as tf

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


# Configure GPU memory usage for TensorFlow
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

conn_params = {
    "dbname": "aas_db",
    "user": "postgres",
    "password": "123456789",
    "host": "localhost",
    "port": "5432",
}


def get_face_embedding(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    embeddings = DeepFace.represent(
        img, model_name="Facenet512", detector_backend="retinaface"
    )

    if embeddings:
        return embeddings[0]["embedding"]
    else:
        return None


def build_annoy_index_from_db(output_file):
    embedding_dimension = 512
    annoy_index = AnnoyIndex(embedding_dimension, "euclidean")

    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    cur.execute("SELECT student_id, photo FROM Student")
    rows = cur.fetchall()

    print(f"Generating a kd tree with {len(rows)} entries.")
    for row in rows:
        student_id, photo = row
        face_embedding = get_face_embedding(photo)

        if face_embedding is not None:
            # Use student_id as the index (parsed as integer)
            student_id_int = int(student_id)
            print(f"Adding student with id {student_id}")
            annoy_index.add_item(student_id_int, face_embedding)

    annoy_index.build(n_trees=10, n_jobs=10)

    # Save the Annoy index to a file
    annoy_index.save(output_file)

    # Close the cursor and connection
    cur.close()
    conn.close()

    print("Annoy index built and saved successfully.")


if __name__ == "__main__":
    output_file = f'tree_{datetime.now().isoformat(sep="_")}.ann'
    build_annoy_index_from_db(output_file)
