# print.py
import octoprint.plugin
import threading
import time
import logging
import os  # Needed for checking file modification time

from .ai_model import ai_model
import octoprint_error_detection.capture_image as capture_image


class MyPlugin(octoprint.plugin.SimpleApiPlugin,
               octoprint.plugin.EventHandlerPlugin,
               octoprint.plugin.OctoPrintPlugin):

    def initialize(self):
        # Compute the absolute path to the TFLite model based on this file's location.
        self_dir = os.path.dirname(__file__)
        model_path = os.path.join(self_dir, "model_weights", "train_100_epochs", "best-fp16.tflite")
        self._logger.info(f"Using TFLite model at: {model_path}")
        self.error_model = ai_model(model_path)  # Initialize the AI error detection model

        self._monitoring = False
        self.last_processed_mtime = 0  # To track the modification time of the last processed image

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
            self._logger.info("Print started, starting error detection monitoring.")
            self._monitoring = True
            self.last_processed_mtime = 0  # Reset the last processed modification time
            threading.Thread(target=self.monitor_print, daemon=True).start()
        elif event == "PrintResumed":
            self._logger.info("Print resumed, restarting error detection monitoring.")
            if not self._monitoring:
                self._monitoring = True
                threading.Thread(target=self.monitor_print, daemon=True).start()
        elif event in ("PrintDone", "PrintCancelled", "PrintFailed"):
            self._logger.info("Print ended (%s), stopping error detection monitoring.", event)
            self._monitoring = False

    def monitor_print(self):
        """
        Continuously monitor the Octolapse snapshot directory for new images.
        When a new image (a .jpeg with 'thumb' in the filename) is detected based on its
        modification time, pass it to the AI model for error detection. If an error is detected,
        log the message, notify the user, and pause the print.
        """
        while self._monitoring:
            try:
                # Retrieve the latest snapshot from the Octolapse directory.
                # The function returns a tuple: (image, image_path)
                result = capture_image.get_print_image(self)
                if result is not None:
                    image, image_path = result
                    current_mtime = os.path.getmtime(image_path)
                    # Process the image if it is new (i.e. has a newer modification time)
                    if current_mtime > self.last_processed_mtime:
                        self.last_processed_mtime = current_mtime
                        self._logger.info("New image detected: %s. Processing...", image_path)
                        if self.error_model.detect_error(image):
                            self._logger.warning("Error detected in the print process! Pausing printing.")
                            self.notify_user("Error detected in the print process! Pausing printing.")
                            self._printer.pause_print()
                            self._monitoring = False
                            break
                        else:
                            self._logger.info("No error detected, continue monitoring.")
                else:
                    self._logger.debug("No valid image found in Octolapse directory.")
            except Exception as e:
                self._logger.error("Error during monitoring: %s", e)
            # Check every 10 seconds for a new image
            time.sleep(10)

    def notify_user(self, message):
        """
        Send a notification to the user.
        Currently, this simply logs the error to octoprint.log.
        """
        self._logger.error(message)