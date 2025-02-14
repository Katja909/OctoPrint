import numpy as np
import cv2
from PIL import Image
import tflite_runtime.interpreter as tflite

class ai_model:
    def __init__(self, model_path):
        """Initializes the TFLite model with the provided path."""
        try:
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()

            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        except Exception as e:
            print(f"Failed to initialize TFLite model: {e}")
            self.interpreter = None

    def preprocess_image(self, image_path):
        """
        Loads and preprocesses the image for inference.
        Adjust resizing and normalization as needed by your model.
        """
        # Load image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found or unable to load.")
        # Resize to expected input size (assumed 640x640; adjust if needed)
        input_shape = self.input_details[0]['shape'][1:3]
        img_resized = cv2.resize(img, (input_shape[1], input_shape[0]))
        # Normalize: convert to float32 and scale [0, 255] -> [0, 1]
        img_normalized = img_resized.astype(np.float32) / 255.0
        # Convert HWC to CHW if necessary (depends on your model)
        img_transposed = np.transpose(img_normalized, (2, 0, 1))
        # Add a batch dimension
        input_tensor = np.expand_dims(img_transposed, axis=0)
        return input_tensor

    def detect_error(self, image_path):
        """
        Runs inference on the image and checks if any detection has confidence > 30%.
        Note: You will likely need to adjust postprocessing to match your TFLite model's output.
        """
        if not self.interpreter:
            print("Model not initialized.")
            return False
        try:
            # Preprocess the image
            input_tensor = self.preprocess_image(image_path)
            # Set the input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
            # Run inference
            self.interpreter.invoke()
            # Get the output tensor(s)
            outputs = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Example postprocessing: assume outputs shape is [1, num_detections, 6]
            # where each detection is [x1, y1, x2, y2, confidence, class]
            detections = outputs  # adjust if your model returns multiple outputs
            for detection in detections[0]:
                confidence = detection[4]
                if confidence * 100 > 30:
                    return True
            return False
        except Exception as e:
            print(f"Error during error detection: {e}")
            return False
