def load_image(image_path):
    from PIL import Image
    import os

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")

    image = Image.open(image_path)
    return image


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