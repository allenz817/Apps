import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def enhance_image(image):
    """
    Enhance the image for better OCR results.
    
    Args:
        image (PIL.Image): The input image
        
    Returns:
        PIL.Image: The enhanced image
    """
    if not image:
        return None
        
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')
    
    # Apply sharpening
    image = image.filter(ImageFilter.SHARPEN)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    # Apply adaptive thresholding
    img_array = np.array(image)
    
    # Apply Gaussian blur to reduce noise
    img_array = cv2.GaussianBlur(img_array, (5, 5), 0)
    
    # Apply adaptive thresholding
    img_array = cv2.adaptiveThreshold(
        img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Convert back to PIL Image
    enhanced_image = Image.fromarray(img_array)
    
    return enhanced_image

def preprocess_image(image_path):
    """
    Load, enhance, and preprocess an image for OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        PIL.Image: The preprocessed image
    """
    try:
        # Load the image
        image = Image.open(image_path)
        
        # Enhance the image
        enhanced_image = enhance_image(image)
        
        return enhanced_image
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        return None

def save_processed_image(image, output_path):
    """
    Save a processed image to the specified path.
    
    Args:
        image (PIL.Image): The image to save
        output_path (str): Path where the image should be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return False