import octoprint.plugin
import time
import threading
import logging
import octoprint_error_detection.ai_model as ai_model  

class MyPlugin(octoprint.plugin.OctoPrintPlugin):
    def initialize(self):
        model_path = "octoprint_error_detection\best.pt"
        self.error_model = ai_model(model_path)  # Error detection model
        self._monitoring = False  # Monitoring status

        # Configure the logger
        self._logger = self._logger
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

        self._logger.info("Plugin initialized.")
        
    def get_update_information(self):
        # Return None or an empty dictionary to disable update checks
        return None
    
    """Check if the monitoring process started"""
    def check_monitoring(self):
        if self._monitoring:
            self._monitoring = False
            self._logger.info("Monitoring stopped")
        else:
            self._monitoring - True
            threading.Thread(target=self.monitor_print, daemon=True).start()
            self._logger.info("Monitoring started")
    

    def monitor_print(self):
        """Continuously monitors the print process for errors."""
        while self._monitoring:
            try:
                # Example: Get the image from the printer camera (use your method to capture the print image)
                image = self.get_print_image()

                # Detect error in the captured image
                if self.error_model.detect_error(image):
                    self._logger.warning("Error detected in the print process!")
                    self.notify_user("Error detected!")
                    self._monitoring = False  # Stop monitoring
                    self._printer.cancel_print()  # Cancel the print
            except Exception as e:
                self._logger.error(f"Error in monitoring process: {e}")
            time.sleep(1)  # Adjustable monitoring frequency

    def notify_user(self, message):
        """Sends a notification to the user."""
        self._plugin_manager.send_plugin_message(self._identifier, dict(type="error", message=message))