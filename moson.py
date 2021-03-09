import json
import logging
import platform


class ConfigurationProcessor:
    """ Esta clase es usada para poder leer el archivo de configuracion """

    def __load_configuration_file(self) -> None:
        """ Este metodo es el encargado de cargar el archivo de configuraciones """
        try:
            self.__json_file = open(self.__file_name)
        except FileNotFoundError:
            self.__load_default_config()
            self.__json_file = open(self.__file_name)

    def __read_configuration_file(self) -> None:
        """ Este metodo lee el archivo de configuracion """
        self.__data_file = json.load(self.__json_file)
        self.__json_file.close()

    def get(self, key):
        """ Este metodo es usado para devolver una key del archivo de configuracion """
        return self.__data_file[key]

    def set(self, key, value) -> None:
        self.__data_file[key] = value
        self.write(self.__data_file, "config.json")

    def write(self, data, name):
        with open(name, "w") as file:
            json.dump(data, file, indent=4)

    def __load_default_config(self):
        """ Este metodo escribe el archivo de configuracion en caso de no existir """
        logging.info("Creating new configuration file with default configuration...")
        os_name = platform.system().lower()
        if os_name.__contains__("linux"):
            font_name = "Ubuntu"
        else:
            font_name = "Arial"
        config = {
            "delay": 0.5,
            "font": {
                "family": font_name,
                "style": "Bold",
                "size": 12,
                "color": "#000000"
            },
            "language": {
                "source": "en",
                "target": "es"
            }
        }
        self.write(config, "config.json")

    def __init__(self, file_name='config.json'):
        """ Constructor el cual carga y lee el archivo de configuraciones """
        self.__file_name = file_name
        self.__load_configuration_file()
        self.__read_configuration_file()
