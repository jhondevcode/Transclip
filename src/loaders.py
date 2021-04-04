"""
    This module provides classes designed to load configuration files,
    images, icons and test resources.
"""

import json
import logger
import platform
from impl import AbstractLoader
from wx import Icon, Image


# noinspection PyMethodMayBeStatic
class ConfigurationLoader(AbstractLoader):
    """This class is used to obtain information from the configuration file for the program"""

    def __init__(self, file_name='config.json'):
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
        self.write(self.__data_file, "config.json")

    def write(self, data, name):
        """Used to dump the data to the configuration file"""
        with open(name, "w") as file:
            json.dump(data, file, indent=4)

    def __load_default_config(self):
        """This method is responsible for creating a configuration file with a default configuration"""
        logger.info("Creating default configuration file")
        os_name = platform.system().lower()
        if os_name.__contains__("linux"):
            font_name = "Ubuntu"
        else:
            font_name = "Arial"
        config = {
            "core": {
                "version": "1.1.2",
                "delay": 0.5
            },
            "language": {
                "source": "en",
                "target": "es"
            },
            "resources": {
                "img": "src/resources/img",
                "icon": "src/resources/icon"
            }
        }
        self.write(config, "config.json")


# noinspection PyTypeChecker
class ImageLoader(AbstractLoader):
    """This class is used to load images which are found in the resource directory"""

    __resources__ = "resources/img"

    def __init__(self, name: str, parent="root"):
        """This constructor starts by checking if the image is in the images directory or in a subdirectory"""
        super(ImageLoader, self).__init__()
        self._image_name = name
        if parent != "root":
            self.__path = self.__resources__ + "/" + parent + "/" + self._image_name
        else:
            self.__path = self.__resources__ + "/" + self._image_name

    def get(self) -> Image:
        """Returns the image of the specified path"""
        try:
            with open(self.__path):
                logger.warn(self.__path)
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

    __resources__ = "resources/icon"

    def __init__(self, name: str,  parent="root"):
        """This constructor starts by checking if the icon is in the images directory or in a subdirectory"""
        super(IconLoader, self).__init__()
        self._icon_name = name
        if parent != "root":
            self.__path = self.__resources__ + "/" + parent + "/" + self._icon_name
        else:
            self.__path = self.__resources__ + "/" + self._icon_name

    def get(self) -> Icon:
        """Returns the icon of the specified path"""
        try:
            with open(self.__path):
                logger.warn(self.__path)
                return Icon(self.__path)
        except FileNotFoundError as ex:
            logger.error(f"Icon file '{self._icon_name}' not found", ex)
            return None
