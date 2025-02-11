from setuptools import setup, find_packages

# Plugin Metadata
PLUGIN_IDENTIFIER = "octoprint_error_detection"
PLUGIN_PACKAGE = "octoprint_error_detection"
PLUGIN_NAME = "OctoPrint-AI Error Detector"
PLUGIN_VERSION = "0.1.0"
PLUGIN_DESCRIPTION = "An OctoPrint plugin for detecting errors during printing with the help of an AI model."
PLUGIN_AUTHOR = "Ваше Имя"
PLUGIN_AUTHOR_EMAIL = "Ваш Email"
PLUGIN_URL = "https://github.com/ваш репозиторий"
PLUGIN_LICENSE = "AGPLv3"

# Dependencies
PLUGIN_REQUIREMENTS = [
    "octoprint>=1.8.0",
    "Pillow>=8.0.0",
    "opencv-python>=4.5.0,<5.0.0",
    "numpy>=1.21.0",
    "requests>=2.25.0"
]

# Plugin setup configuration
setup(
    name=PLUGIN_NAME,
    version=PLUGIN_VERSION,
    description=PLUGIN_DESCRIPTION,
    author=PLUGIN_AUTHOR,
    author_email=PLUGIN_AUTHOR_EMAIL,
    url=PLUGIN_URL,
    license=PLUGIN_LICENSE,
    packages=find_packages(),
    include_package_data=True,
    install_requires=PLUGIN_REQUIREMENTS,
    entry_points={
        "octoprint.plugin": [
            f"{PLUGIN_IDENTIFIER} = {PLUGIN_PACKAGE}"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7,<4",
)