# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin

class ErrorDetectionPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    def get_settings_defaults(self):
        return {
            "detection_enabled": True,
            "confidence_threshold": 0.5
        }

    def get_assets(self):
        return {
            "js": ["js/error_detection.js"],
            "css": ["css/error_detection.css"]
        }

    def get_update_information(self):
        return {
            "error_detection": {
                "displayName": "OctoPrint-AI Error Detector",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "Katja909",
                "repo": "error_detection_with_AI",
                "current": self._plugin_version,
                "pip": "https://github.com/Katja909/error_detection_with_AI/archive/{target_version}.zip",
            }
        }

__plugin_name__ = "OctoPrint-AI Error Detector"
__plugin_version__ = "0.1.0"
__plugin_description__ = "An OctoPrint plugin for detecting errors during printing with the help of an AI model."
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ErrorDetectionPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }