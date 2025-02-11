from setuptools import setup

# The unique identifier for your plugin, used internally by OctoPrint
PLUGIN_IDENTIFIER = "octoprint_error_detection"

# The name of the Python package for your plugin
PLUGIN_PACKAGE = "octoprint_error_detection"

# The human-readable name of your plugin
PLUGIN_NAME = "OctoPrint-AI Error Detector"

# The version of your plugin
PLUGIN_VERSION = "0.1.0"

# A brief description of your plugin
PLUGIN_DESCRIPTION = "An OctoPrint plugin for detecting errors during printing with help of an AI Model"

# Your name (the plugin author)
PLUGIN_AUTHOR = "Toluhan Balci, Polina Kriuchkova, Ekaterina Pomazanova, Darya Igonina, Tatyana Grigorjevschi"

# Your email address
PLUGIN_AUTHOR_EMAIL = ""

# URL to the plugin's repository or homepage (optional)
PLUGIN_URL = "https://github.com/Katja909/OctoPrint/tree/master/plugins/error_detection"

# The license for your plugin (e.g., AGPLv3 is recommended for OctoPrint plugins)
PLUGIN_LICENSE = "AGPLv3"

# The Python packages required for your plugin to work
PLUGIN_REQUIREMENTS = [
    "octoprint" ,
    "yolov11",  # YOLOv11 wrapper, if required
    "time",
    "threading",
    "Pillow",
    "opencv-python",
    "numpy",
    "requests"
]

# Plugin setup configuration
setup(
    name=PLUGIN_NAME,  # The name of your plugin
    version=PLUGIN_VERSION,  # The version of your plugin
    description=PLUGIN_DESCRIPTION,  # A short description
    author=PLUGIN_AUTHOR,  # Author's name
    author_email=PLUGIN_AUTHOR_EMAIL,  # Author's email
    url=PLUGIN_URL,  # Plugin URL (optional)
    license=PLUGIN_LICENSE,  # Plugin license
    packages=[PLUGIN_PACKAGE],  # List of packages to include in the distribution
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=PLUGIN_REQUIREMENTS,  # Dependencies to install alongside the plugin
    entry_points={
        # Entry point for OctoPrint to recognize the plugin
        "octoprint.plugin": [
            f"{PLUGIN_IDENTIFIER} = {PLUGIN_PACKAGE}"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version required
)
