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
        # Load the image if a file path is provided
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
            if img is None:
                raise ValueError("AI Model: Image not found or unable to load.")
        else:
            img = image_input

        # Retrieve the expected input shape from the model.
        # Typical shapes are either [1, height, width, channels] (NHWC) or [1, channels, height, width] (NCHW).
        input_shape = self.input_details[0]['shape']
        logger.info(f"AI Model: Expected model input shape: {input_shape}")
        
        if len(input_shape) != 4:
            raise ValueError("AI Model: Unexpected input tensor shape.")

        # Determine whether the model expects NHWC or NCHW.
        # If the last dimension is 3, we assume NHWC.
        if input_shape[3] == 3:
            # Model expects NHWC.
            target_height, target_width = input_shape[1], input_shape[2]
            img_resized = cv2.resize(img, (target_width, target_height))
            img_normalized = img_resized.astype(np.float32) / 255.0
            # Add batch dimension. Shape becomes [1, height, width, 3].
            input_tensor = np.expand_dims(img_normalized, axis=0)
        elif input_shape[1] == 3:
            # Model expects NCHW.
            target_height, target_width = input_shape[2], input_shape[3]
            img_resized = cv2.resize(img, (target_width, target_height))
            img_normalized = img_resized.astype(np.float32) / 255.0
            # Convert from HWC to CHW.
            img_transposed = np.transpose(img_normalized, (2, 0, 1))
            # Add batch dimension. Shape becomes [1, 3, height, width].
            input_tensor = np.expand_dims(img_transposed, axis=0)
        else:
            # Fallback: assume NHWC
            target_height, target_width = input_shape[1], input_shape[2]
            img_resized = cv2.resize(img, (target_width, target_height))
            img_normalized = img_resized.astype(np.float32) / 255.0
            input_tensor = np.expand_dims(img_normalized, axis=0)

        logger.info("AI Model: Image preprocessed for inference.")
        return input_tensor

    def detect_error(self, image_input):
        """
        Runs inference on the image and checks if any detection has confidence > 30%.
        Adjust postprocessing to match your TFLite model's output.
        """
        if not self.interpreter:
            logger.error("AI Model not initialized, interpreter is not configured.")
            return False
        try:
            # Preprocess the image (using file path or array)
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
            logger.info("AI Model output generated.")
            for detection in detections[0]:
                confidence = detection[4]
                # logger.info(f"AI Model: Confidence: {confidence * 100:.2f}%")
                if confidence * 100 > 5:
                    logger.info(f"AI Model: Detected error with confidence: {confidence * 100:.2f}%")
                    return True
            return False
        except Exception as e:
            logger.error(f"AI Model: Error during error detection: {e}")
            return False
