from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """
    Extracts text from the given image using Tesseract OCR.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        str: The extracted text from the image.
    """
    # Load the image from the specified path
    image = Image.open(image_path)
    
    # Use Tesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(image)
    
    return extracted_text

def extract_text_from_images(image_paths):
    """
    Extracts text from a list of images.

    Parameters:
        image_paths (list): A list of paths to image files.

    Returns:
        list: A list of extracted texts from the images.
    """
    texts = []
    for path in image_paths:
        text = extract_text_from_image(path)
        texts.append(text)
    return texts

def extract_text(image):
    """
    Extracts text from a PIL Image object using Tesseract OCR.
    
    Parameters:
        image (PIL.Image): The image to process.
        
    Returns:
        str: The extracted text from the image.
    """
    return pytesseract.image_to_string(image)