# coding=utf-8
from __future__ import absolute_import
from .print import MyPlugin
import octoprint.plugin

__plugin_name__ = "Error Detection for 3D Printer with AI Model"
__plugin_version__ = "0.1.0"
__plugin_description__ = "An OctoPrint plugin for detecting errors during printing with help of an AI Model"
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__, __plugin_hooks__
    __plugin_implementation__ = MyPlugin()
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
