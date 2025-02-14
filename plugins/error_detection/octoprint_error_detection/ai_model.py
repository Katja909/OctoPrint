from yolov5 import YOLOv5
from PIL import Image

class ai_model:
    def __init__(self, model_path):
        """Initializes the model with the provided path."""
        self.model_path = model_path
        self.model = YOLOv5(model_path)  # Load the YOLOv11 model

    def detect_error(self, image):
        """
        Detects errors in the given image based on the confidence score.

        :param image: The input image to analyze.
        :return: True if confidence > 30, False otherwise.
        """
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