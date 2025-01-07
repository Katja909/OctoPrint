from yolov5 import YOLOv5
from PIL import Image

class ai_model:
    def __init__(self, model_path):
        """Initializes the model with the provided path."""
        self.model = YOLOv5(model_path)  # Load the YOLOv5 model