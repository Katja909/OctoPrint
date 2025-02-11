from yolov5 import YOLOv5
from PIL import Image

class AIModel:
    def __init__(self, model_path):
        """Initializes the model with the provided path."""
        self.model_path = model_path
        self.model = YOLOv5(model_path)  # Load the YOLOv5 model

    def detect_error(self, image):
        """
        Detects errors in the given image.

        :param image: The input image to analyze.
        :return: The raw detection results.
        """
        try:
            # Run inference on the image
            results = self.model.predict(image)

            # Return the results
            return results
        except Exception as e:
            print(f"Error during error detection: {e}")
            return None