# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import time
import threading
import logging
import octoprint_error_detection.ai_model as ai_model  
import plugins.error_detection.octoprint_error_detection.capture_image as capture_image

# initial implementation of the plugin is imported beneath
# import plugins.error_detection.octoprint_error_detection.print as plugin

class AIErrorDetectionPlugin(
    # base plugin class
    octoprint.plugin.OctoPrintPlugin,
    # for UI purposes, for embedding JS and CSS
    octoprint.plugin.AssetPlugin,
    # for UI purposes, for plugin to be able to modify webinterface
    octoprint.plugin.TemplatePlugin,
    # for adding starting up functionality
    octoprint.plugin.StartupPlugin,
    # for adding shutting down functionality
    octoprint.plugin.ShutdownPlugin):

    def initialize(self):
        self._logger.setLevel(logging.INFO)
        self._logger.info("AI Error Detection Plugin initialized.")

        # Load the AI model
        model_path = "model_weights/train_100_epochs/best.pt"
        try:
            self.error_model = ai_model(model_path)
            self._logger.info("Model loaded successfully.")
        except Exception as e:
            self._logger.error(f"Failed to load AI model: {e}")
            self.error_model = None

        self._monitoring = False

    def on_after_startup(self):
        self._logger.info("Hello World! I initialized correctly")

    # retrieve the UI functionality    
    def get_assets(self):
        return dict(
        js=['plugins\error_detection\octoprint_error_detection\static\js\error_detection.js',
            'plugins\error_detection\octoprint_error_detection\static\js\error_detection_v2.js'],
        # clientjs=['clientjs/my_file.js'],
        # css=['css/my_styles.css'],
        # less=['less/my_styles.less']
        )
    
    # create a tab in the octoprint webinterface
    def get_template_configs(self):
        return dict(type="tab", 
                    template="plugins\error_detection\octoprint_error_detection\templates\tab_error_detection_dashboard.jinja2")
    
    # from Katya's init
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "error_detection": {
                "displayName": "Error_detection Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "Katja909",
                "repo": "error_detection_with_AI",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/Katja909/error_detection_with_AI/archive/{target_version}.zip",
            }
        }
    
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
                # image = self.get_print_image()
                image = capture_image.get_print_image()

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
        # TODO: send_plugin_message method may not be initialized
        self._plugin_manager.send_plugin_message(self._identifier, dict(type="error", message=message))
        self._logger.error(message)

__plugin_name__ = "Error Detection for 3D Printer with AI Model"
__plugin_version__ = "0.1.1"
__plugin_description__ = "An OctoPrint plugin for detecting errors during printing with help of an AI Model"
__plugin_implementation__ = AIErrorDetectionPlugin()
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3