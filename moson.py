import json
import logging
import platform


class ConfigurationProcessor:
    """ Esta clase es usada para poder leer el archivo de configuración """

    def __load_configuration_file(self) -> None:
        """ Este método es el encargado de cargar el archivo de configuraciones """
        try:
            with open(self.__file_name) as file:
                self.__data_file = json.load(file)
        except FileNotFoundError:
            self.__load_default_config()
            with open(self.__file_name) as file:
                self.__data_file = json.load(file)

    def get(self, key):
        """ Este método es usado para devolver una key del archivo de configuración """
        return self.__data_file[key]

    def set(self, key, value) -> None:
        self.__data_file[key] = value
        self.write(self.__data_file, "config.json")

    def write(self, data, name):
        with open(name, "w") as file:
            json.dump(data, file, indent=4)

    def __load_default_config(self):
        """ Este método escribe el archivo de configuración en caso de no existir """
        logging.info("Creating new configuration file with default configuration...")
        os_name = platform.system().lower()
        if os_name.__contains__("linux"):
            font_name = "Ubuntu"
        else:
            font_name = "Arial"
        config = {
            "delay": 0.2,
            "font": {
                "family": font_name,
                "style": "Normal",
                "size": 15
            },
            "language": {
                "source": "en",
                "target": "es"
            },
            "edit-text": {
                "source": {
                    "background": "#ffffff",
                    "foreground": "#000000"
                },
                "target": {
                    "background": "#ffffff",
                    "foreground": "#000000"
                }
            }
        }
        self.write(config, "config.json")

    def __init__(self, file_name='config.json'):
        """ Constructor el cual carga y lee el archivo de configuraciones """
        self.__file_name = file_name
        self.__load_configuration_file()
