# coding=utf-8
from __future__ import absolute_import
#from <ai_file> import <name_of_trained_ai_model>

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import plugins.error_detection.octoprint_error_detection.print as plugin

class Error_detectionPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    def on_after_startup(self):
        self._logger.info("Hello World!")

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ Softwareupdate hook

    # not necessary, delete
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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.

__plugin_name__ = "Error Detection for 3D Printer with AI Model"
__plugin_version__ = "0.1.1"
__plugin_description__ = "An OctoPrint plugin for detecting errors during printing with help of an AI Model"
# __plugin_implementation__ = plugin.MyPlugin()


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Error_detectionPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

# TODO: https://docs.octoprint.org/en/master/plugins/concepts.html#:~:text=When%20a%20plugin%20gets%20enabled%2C%20OctoPrint%20will%20also%20call%20the%20on_plugin_enabled()%20callback%20on%20its%20implementation%20(if%20it%20exists).%20Likewise%2C%20when%20a%20plugin%20gets%20disabled%20OctoPrint%20will%20call%20the%20on_plugin_disabled()%20callback%20on%20its%20implementation%20(again%2C%20if%20it%20exists).
