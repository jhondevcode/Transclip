"""
    This module provides classes designed to load configuration files,
    images, icons and test resources.
"""

import json
import sys

import wx
from wx import Image, Icon

import logger
from __version__ import __version__
from impl import AbstractLoader

# The value for this variable will be added from the make.py file
INSTALL_DIR = None


# noinspection PyMethodMayBeStatic
class ConfigurationLoader(AbstractLoader):
    """This class is used to obtain information from the configuration file for the program"""

    def __init__(self, file_name="/home/jhon/.local/share/transclip/config.json"):
        """This constructor starts by loading the config file"""
        super(ConfigurationLoader, self).__init__()
        self.__file_name = file_name
        self.__load_configuration_file()

    def __load_configuration_file(self) -> None:
        """Read the configuration file, if it does not exist, create one with a default configuration"""
        try:
            with open(self.__file_name) as file:
                self.__data_file = json.load(file)
        except FileNotFoundError:
            logger.error("Configuration file not found")
            self.__load_default_config()
            with open(self.__file_name) as file:
                self.__data_file = json.load(file)

    def get(self, key) -> object:
        """Returns a value a from the configuration file through the indicated key"""
        return self.__data_file[key]

    def set(self, key, value) -> None:
        """Set a new value for a key in the configuration file"""
        self.__data_file[key] = value
        self.write(self.__data_file, "/home/jhon/.local/share/transclip/config.json")

    def write(self, data, name):
        """Used to dump the data to the configuration file"""
        with open(name, "w") as file:
            json.dump(data, file, indent=4)

    def __load_default_config(self):
        """This method is responsible for creating a configuration file with a default configuration"""
        logger.info("Creating default configuration file")
        config = {
            # These options allow you to configure the following actions:
            # delay: set the time interval to monitor the clipboard.
            # example: "delay": 0.2     200 millisenconds.
            #
            # source-preview: tells the program whether or not to show the original text.
            # example:
            #     true: the program sets the field to see the original text.
            #     false: the program hides the original text field
            # font-size: indicates to the program the font size that the program's text containers will have.
            "core": {
                "version": __version__,
                "delay": 0.5,
                "source-preview": True,
                "font-size": 15,
            },
            # If you want to modify the target and the source, you can do it by
            # editing these lines or else in the config.json file
            # example:
            # "source": "en"    spanish
            # "target": "ru"    russian
            "language": {"source": "en", "target": "es"},
            # Description of resources:
            # If you move or rearrange the resources folder, you can edit this
            # lines to indicate the new location of the resources
            # example:
            # /home/user/pictures/resources/img     for linux
            # C:/Users/user/resources/image         for windows
            "resources": {"img": f"{INSTALL_DIR}/resources/img", "icon": f"{INSTALL_DIR}/resources/icon"},
        }
        self.write(config, f"{INSTALL_DIR}/config.json")


# noinspection PyTypeChecker
class ImageLoader(AbstractLoader):
    """This class is used to load images which are found in the resource directory"""

    def __init__(self, name: str, parent="root"):
        """This constructor starts by checking if the image is in the images directory or in a subdirectory"""
        super(ImageLoader, self).__init__()
        self.__resources = ConfigurationLoader().get("resources")["img"]
        self._image_name = name
        if parent != "root":
            self.__path = self.__resources + "/" + parent + "/" + self._image_name
        else:
            self.__path = self.__resources + "/" + self._image_name

    def get(self, key=None) -> Image:
        """Returns the image of the specified path"""
        try:
            with open(self.__path):
                logger.info(self.__path)
                return Image(self.__path)
        except FileNotFoundError as ex:
            logger.error(f"Image file '{self._image_name}' not found", ex)
            return None

    def get_path(self) -> str:
        """Returns the path of the image"""
        try:
            with open(self.__path):
                return self.__path
        except FileNotFoundError as ex:
            logger.error(f"Image file '{self._image_name}' not found", ex)
            return None


# noinspection PyTypeChecker
class IconLoader(AbstractLoader):
    """This class is used to load icons which are found in the resource directory"""

    def __init__(self, name: str, parent="root"):
        """This constructor starts by checking if the icon is in the images directory or in a subdirectory"""
        super(IconLoader, self).__init__()
        self.__resources = ConfigurationLoader().get("resources")["icon"]
        self._icon_name = name
        if parent != "root":
            self.__path = self.__resources + "/" + parent + "/" + self._icon_name
        else:
            self.__path = self.__resources + "/" + self._icon_name

    def get(self, key=None) -> Icon:
        """Returns the icon of the specified path"""
        try:
            with open(self.__path):
                logger.info(self.__path)
                return Icon(self.__path)
        except FileNotFoundError as ex:
            logger.error(f"Icon file '{self._icon_name}' not found", ex)
            return None

    def get_path(self) -> str:
        return self.__path


# noinspection PyTypeChecker
class BitMapLoader(AbstractLoader):
    def __init__(self, name: str, parent="root", b_type="image"):
        super(BitMapLoader, self).__init__()
        self._bitmap_name = name
        self.__path = None
        if b_type == "icon":
            self.__resources = ConfigurationLoader().get("resources")["icon"]
        elif b_type == "image":
            self.__resources = ConfigurationLoader().get("resources")["img"]
        else:
            logger.error("A error as occurred")
            logger.warn("Exiting...")
            sys.exit(1)
        if parent != "root":
            self.__path = self.__resources + "/" + parent + "/" + self._bitmap_name
        else:
            self.__path = self.__resources + "/" + self._bitmap_name

    def get(self, key=None) -> wx.Bitmap:
        """Returns the image icon of the specified path"""
        try:
            with open(self.get_path()):
                logger.info(self.get_path())
                return wx.Bitmap(self.get_path())
        except FileNotFoundError as ex:
            logger.error(f"Icon file '{self._bitmap_name}' not found", ex)
            return None

    def get_path(self) -> str:
        return self.__path
