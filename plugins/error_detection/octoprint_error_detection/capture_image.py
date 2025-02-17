import os
import cv2
import logging

# Configure the error detection logger for OctoPrint
logger = logging.getLogger("octoprint.plugins.ai_error_detection")  # Plugin-specific logger

def get_print_image(self):
    """
    Fetch the most recent print image from the Octolapse snapshot directory.
    Logs messages to OctoPrint's log file.
    """
    # octolapse_path = "C:/Users/daria/.octoprint/data/octolapse/tmp/octolapse_snapshots_tmp/"
    octolapse_path = "/home/AI2SB/.octoprint/data/octolapse/tmp/octolapse_snapshots_tmp/"
    
    try:
        # Check if the directory exists
        if not os.path.exists(octolapse_path):
            logger.error(f"Directory not found for fetching print images: {octolapse_path}")
            return None

        # List all files in the directory
        files = os.listdir(octolapse_path)
        logger.info(f"Fetching print images... Files in octolapse directory: {files}")

        if not files:
            logger.warning("No image files found in the octolapse directory.")
            return None

        # Filter only image files (jpg, jpeg, png)
        image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if not image_files:
            logger.warning("No image files (jpg/png) found in the octolapse directory.")
            return None

        # Sort files by modification time (latest first)
        image_files.sort(key=lambda f: os.path.getmtime(os.path.join(octolapse_path, f)), reverse=True)

        # Get the latest image file
        latest_image_path = os.path.join(octolapse_path, image_files[0])
        logger.info(f"Latest image selected: {latest_image_path}")

        # Read the image using OpenCV
        image = cv2.imread(latest_image_path)
        if image is None:
            logger.error("Failed to read image with OpenCV.")
            return None

        return image
    except Exception as e:
        logger.exception(f"Error in get_print_image: {e}")
        return None

# # Test
# if __name__ == "__main__":
#     image = get_print_image(None)
#     if image is not None:
#         logger.info("Image captured successfully.")
#     else:
#         logger.error("No image captured.")
