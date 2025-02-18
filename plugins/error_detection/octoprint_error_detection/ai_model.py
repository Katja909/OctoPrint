import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
import logging

logger = logging.getLogger("octoprint.plugins.ai_error_detection")

class ai_model:
    def __init__(self, model_path):
        """Initializes the TFLite model with the provided path."""
        try:
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()

            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            logger.info(f"Initialized TFLite model with input shape: {self.input_details[0]['shape']}")
        except Exception as e:
            logger.error(f"Failed to initialize TFLite model: {e}")
            self.interpreter = None

    def preprocess_image(self, image_input):
        """
        Preprocesses the image for inference.
        Accepts either a file path (str) or an image array (numpy.ndarray).
        Adjust resizing and normalization as needed by your model.
        """
        # If a file path is provided, load the image using OpenCV
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
            if img is None:
                raise ValueError("AI Model: Image not found or unable to load.")
        else:
            # Assume the image is already loaded as a NumPy array
            img = image_input

        # Resize to expected input size (assumed 640x640; adjust if needed)
        input_shape = self.input_details[0]['shape'][1:3]
        img_resized = cv2.resize(img, (input_shape[1], input_shape[0]))
        # Normalize: convert to float32 and scale from [0, 255] to [0, 1]
        img_normalized = img_resized.astype(np.float32) / 255.0
        # Convert HWC to CHW if required by your model
        img_transposed = np.transpose(img_normalized, (2, 0, 1))
        # Add a batch dimension
        input_tensor = np.expand_dims(img_transposed, axis=0)
        logger.info(f"AI Model: Image preprocessed for inference.")
        return input_tensor

    def detect_error(self, image_input):
        """
        Runs inference on the image and checks if any detection has confidence > 30%.
        Adjust postprocessing to match your TFLite model's output.
        """
        if not self.interpreter:
            logger.error("AI Model not initialized, interpretr is not configured.")
            return False
        try:
            # Preprocess the image (whether file path or array)
            input_tensor = self.preprocess_image(image_input)
            # Set the input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
            # Run inference
            self.interpreter.invoke()
            # Get the output tensor(s)
            outputs = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Example postprocessing: assume outputs shape is [1, num_detections, 6]
            # where each detection is [x1, y1, x2, y2, confidence, class]
            detections = outputs  # Adjust if your model returns multiple outputs
            logger.info(f"Model output generated.")
            for detection in detections[0]:
                confidence = detection[4]
                if confidence * 100 > 30:
                    logger.info(f"Detected error with confidence: {confidence * 100:.2f}%")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error during error detection: {e}")
            return False
