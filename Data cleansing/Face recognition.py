from deepface import DeepFace
import os
import shutil

def load_reference_faces(reference_folder, model_name='VGG-Face'):
    reference_encodings = []

    for image_file in os.listdir(reference_folder):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(reference_folder, image_file)
            try:
                # Extract face encoding using DeepFace
                encoding = DeepFace.represent(img_path=image_path, model_name=model_name, enforce_detection=False)
                reference_encodings.append(encoding)
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
                continue

    return reference_encodings

def copy_matching_images(target_folder, reference_encodings, destination_folder, model_name='VGG-Face', threshold=0.4):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for image_file in os.listdir(target_folder):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(target_folder, image_file)
            try:
                result = DeepFace.find(img_path=image_path, db_path=reference_folder, model_name=model_name, enforce_detection=False, distance_metric='cosine')
                if len(result) > 0:
                    print(f"Copying matching image: {image_file}")
                    shutil.copy(image_path, os.path.join(destination_folder, image_file))
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
                continue

def main(reference_folder, target_folder, destination_folder, model_name='VGG-Face'):
    reference_encodings = load_reference_faces(reference_folder, model_name=model_name)
    copy_matching_images(target_folder, reference_encodings, destination_folder, model_name=model_name)

# Example usage
reference_folder = "Data cleansing/Jeff face images"      # Folder containing reference images of the person's face
target_folder = "Web Scraper/scraped data/images"            # Folder containing images to be checked
destination_folder = "Data cleansing/Cleansed data/images/"      # Folder where matched images will be copied
main(reference_folder, target_folder, destination_folder)