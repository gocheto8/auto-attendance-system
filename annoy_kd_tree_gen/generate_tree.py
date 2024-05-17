import os
import cv2
from deepface import DeepFace
from annoy import AnnoyIndex
from datetime import datetime
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

def get_face_embedding(image_path):
    img = cv2.imread(image_path)
    

    return DeepFace.represent(img, model_name='Facenet512', detector_backend='retinaface')
    

def build_annoy_index(directory, output_file):
    embedding_dimension = 512
    # Create Annoy index for face embeddings
    annoy_index = AnnoyIndex(embedding_dimension, 'euclidean')

    # Iterate through images in the directory
    index = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            face_embedding = get_face_embedding(image_path)
            print(index, image_path)
            
            if face_embedding is not None:
                # Add face embedding to the Annoy index
                annoy_index.add_item(index, face_embedding)
            index += 1

    # Build the Annoy index after adding all face embeddings
    annoy_index.build(n_trees=10)  # You can experiment with the number of trees

    # Save the Annoy index to a file
    annoy_index.save(output_file)

if __name__ == "__main__":
    # Specify the directory containing images
    input_directory = "/home/gosho/Projects/GitHub/auto-attendance-system/annoy_tree_tests/images"

    # Specify the output file for the Annoy index
    current_datetime = datetime.now()
    output_file = f"face_embeddings_index_{current_datetime.isoformat()}.ann"

    # Build Annoy index and save to a file
    build_annoy_index(input_directory, output_file)
