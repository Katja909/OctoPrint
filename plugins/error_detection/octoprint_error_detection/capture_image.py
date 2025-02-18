# capture_image.py
import os
import cv2
import logging

# Configure the error detection logger for OctoPrint
logger = logging.getLogger("octoprint.plugins.ai_error_detection")

def get_print_image(self):
    """
    Fetch the most recent print image from the Octolapse snapshot directory.
    Only JPEG files with "thumb" in the filename are considered.
    Returns a tuple (image, image_path) or None if no valid image is found.
    """
    # The Octolapse snapshot directory
    octolapse_path = "/home/AI2SB/.octoprint/data/octolapse/tmp/octolapse_snapshots_tmp/"
    
    try:
        # Check if the directory exists
        if not os.path.exists(octolapse_path):
            logger.error(f"Directory not found for fetching print images: {octolapse_path}. Did you enable Octolapse?")
            return None

        # List all files in the directory
        files = os.listdir(octolapse_path)
        # logger.info(f"Fetching print images... Files in octolapse directory: {files}")

        if not files:
            logger.warning("No image files found in the octolapse directory. Did you enable Octolapse?")
            return None

        # Filter only .jpeg files that have "thumb" in the filename (case-insensitive)

        # Thumb is for code sustainability purposes. Like this it allows the user
        # to integrate multiple cameras, as the "main" image in this directory is only being "rewritten"
        # under xxxThumbxxx.jpeg.
        image_files = [f for f in files if f.lower().endswith(".jpeg") and "thumb" in f.lower()]
        if not image_files:
            logger.warning("No matching 'thumb' .jpeg files found in the octolapse directory.")
            return None

        # Sort files by modification time (latest first)
        image_files.sort(key=lambda f: os.path.getmtime(os.path.join(octolapse_path, f)), reverse=True)

        # Get the latest image file
        latest_image_path = os.path.join(octolapse_path, image_files[0])
        # logger.info(f"Latest image selected: {latest_image_path}")

        # Read the image using OpenCV
        image = cv2.imread(latest_image_path)
        if image is None:
            logger.error("Failed to read image with OpenCV.")
            return None

        return image, latest_image_path
    except Exception as e:
        logger.exception(f"Error in get_print_image: {e}")
        return None
