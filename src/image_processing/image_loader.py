from PIL import Image
import os

def load_image(image_path):
    # Convert relative path to absolute path based on project root
    if not os.path.isabs(image_path):
        # Get the project root directory (assuming src is one level deep)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(project_root, image_path)
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")
    
    # Load the image using PIL
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def convert_image_to_rgb(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image


def preprocess_image(image):
    # Placeholder for any preprocessing steps if needed
    return image


def load_and_preprocess_image(image_path):
    image = load_image(image_path)
    image = convert_image_to_rgb(image)
    image = preprocess_image(image)
    return image