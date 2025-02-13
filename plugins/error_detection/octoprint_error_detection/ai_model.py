# from yolov11 import YOLOv11
from PIL import Image
from ultralytics import YOLO
import logging

class ai_model:
    def __init__(self, model_path):
        """Initializes the model with the provided path."""
        try:
            self.model = YOLO(model_path)  # Load the YOLO model
        except Exception as e:
            print(f"Failed to initialize YOLO model: {e}")
            self.model = None

    def detect_error(self, image):
        """
        Detects errors in the given image based on the confidence score.

        :param image: The input image to analyze.
        :return: True if confidence > 30, False otherwise.
        """
        if not self.model:
            print("Model not initialized.")
            return False
        try:
            # Run inference on the image
            results = self.model.predict(image)

            confidences = results.pandas().xyxy[0]["confidence"].tolist()  # Assuming YOLOv5 returns this structure
            
            # Check if any confidence exceeds the threshold
            for confidence in confidences:
                if confidence * 100 > 30:  # Confidence is a decimal (e.g., 0.85 for 85%)
                    return True
            return False
        except Exception as e:
            print(f"Error during error detection: {e}")
            return False