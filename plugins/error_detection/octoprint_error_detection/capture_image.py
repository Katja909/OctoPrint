'''import requests
from PIL import Image
from io import BytesIO

def get_print_image(self):
    """Fetch the current print image from the camera."""
    # Use the appropriate OctoPrint API to get the camera image (assuming you have access to it)
    response = requests.get("http://127.0.0.1:8080/?action=snapshot")  # camera API URL
    image = Image.open(BytesIO(response.content))  # Open the image from the response content
    return image'''

import requests
import cv2
import numpy as np

def get_print_image(self):
    """Fetch the current print image from the camera using OpenCV."""
    try:
        # Fetch the image from the camera API
        response = requests.get("http://127.0.0.1:8080/?action=snapshot")  # camera API URL
        if response.status_code != 200:
            raise Exception(f"Error fetching image: HTTP {response.status_code}")
        
        # Convert the response content into a NumPy array
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        
        # Decode the image using OpenCV
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise Exception("Failed to decode image with OpenCV.")
        
        return image
    except Exception as e:
        print(f"Error: {e}")
        return None
