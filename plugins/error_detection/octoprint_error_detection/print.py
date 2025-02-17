# print.py
import octoprint.plugin
import threading
import time
import logging

from .ai_model import ai_model
import octoprint_error_detection.capture_image as capture_image


class MyPlugin(octoprint.plugin.SimpleApiPlugin,
               octoprint.plugin.EventHandlerPlugin,
               octoprint.plugin.OctoPrintPlugin):

    def initialize(self):
        # Path to the TFLite model
        model_path = r"plugins/error_detection/octoprint_error_detection/model_weights/train_100_epochs/best-fp16.tflite"
        self.error_model = ai_model(model_path)  # Initialize the AI error detection model

        self._monitoring = False
        self.last_z = None  # Used to track the Z position for 1mm intervals

        # Configure logging to display in octoprint.log
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.info("AI Error Detection plugin initialized.")

    def get_update_information(self):
        # Disable update checks for now
        return None

    def get_api_commands(self):
        # Expose an API command for a manual trigger
        return dict(trigger_monitor=[])

    def on_api_command(self, command, data):
        if command == "trigger_monitor":
            self._logger.info("Manual trigger of monitoring loop received.")
            if not self._monitoring:
                self._monitoring = True
                threading.Thread(target=self.monitor_print, daemon=True).start()
            return dict(status="DEBUG: monitoring started")

    def on_event(self, event, payload):
        """
        Listen to print events so that we start monitoring when a print starts
        and stop when it finishes or is canceled.
        """
        if event == "PrintStarted":
            self._logger.info("Print started, error detection monitors printing.")
            self._monitoring = True
            self.last_z = None  # Reset the baseline for the Z position
            threading.Thread(target=self.monitor_print, daemon=True).start()
        elif event in ("PrintDone", "PrintCancelled", "PrintFailed"):
            self._logger.info("Print ended (%s), error detection stopped monitoring.", event)
            self._monitoring = False

    def monitor_print(self):
        """
        Continuously monitor the print process by checking the printer's Z position.
        Every time the head moves 1mm or more, capture an image and run error detection.
        If an error is detected, log the message, notify the user, and cancel the print.
        """
        while self._monitoring:
            try:
                # Capture an image from the printer's camera
                image = capture_image.get_print_image(self)
                if image is not None:
                    # Use the AI model to detect an error in the captured image
                    if self.error_model.detect_error(image):
                        # self._logger.warning("Error detected at Z=%.2f!", current_z)
                        self.notify_user("Error detected in the print process!")
                        self._printer.cancel_print()
                        self._monitoring = False
                        break
                else:
                    self._logger.warning("Failed to capture image.")
            except Exception as e:
                self._logger.error("Error during monitoring: %s", e)

            time.sleep(0.5)

    def notify_user(self, message):
        """
        Send a notification to the user.
        Currently, this simply logs the error to octoprint.log.
        """
        self._logger.error(message)
