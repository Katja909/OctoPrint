import requests
from PIL import Image
from io import BytesIO

#ToDo: find camera API URL

def get_print_image(self):
    """Fetch the current print image from the camera."""
    # Use the appropriate OctoPrint API to get the camera image (assuming you have access to it)
    response = requests.get("http://127.0.0.1:8080/?action=snapshot")  # camera API URL
    image = Image.open(BytesIO(response.content))  # Open the image from the response content
    return image