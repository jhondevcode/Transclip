"""Classes to monitor the clipboard and translate its content"""
# -*- coding: utf-8 -*-

# The sleep function will be used to stop monitoring for an interval of time.
from time import sleep

# PyQt6 library components.
from PyQt5.QtCore import QThread  # Used to create a thread for the monitor.
from PyQt5.QtWidgets import QMessageBox  # Used to display a notification window.
from PyQt5.QtCore import pyqtSignal
# This class is used to translate the clipboard content.
from deep_translator import GoogleTranslator
# The copy() and paste() functions are used to manipulate the contents of the clipboard.
from pyperclip import copy, paste

# Used to display custom exceptions if necessary.
from excepts import LangConfigurationsError


class ClipboardContentTranslator:
    """ Esta clase provee las funcionalidades para traducir texto """

    def set_source(self, source) -> None:
        """ Este método cambia el source y crea un nuevo traductor con las configuraciones especificadas """
        if source != self.__source and source != self.__target:
            self.__source = source
            del self.__translator
            self.__create_translator()
        else:
            raise LangConfigurationsError()

    def set_target(self, target) -> None:
        """ Este método cambia el target y crea un nuevo traductor con las configuraciones especificadas """
        if target != self.__target and target != self.__source:
            print("Creating translator")
            self.__target = target
            del self.__translator
            self.__create_translator()
        else:
            raise LangConfigurationsError()

    def __create_translator(self) -> None:
        """ Este método crea un traductor con el source y target especificado """
        self.__translator: GoogleTranslator = GoogleTranslator(self.__source, self.__target)

    def translate(self, text: str) -> str:
        """ Este método se encarga de traducir el texto que se le pase por parámetro """
        return self.__translator.translate(text)

    def __init__(self, source: str = 'en', target: str = 'es'):
        """ Este constructor inicia los atributos básicos """
        if target != source:
            self.__source = source
            self.__target = target
            self.__create_translator()
        else:
            raise LangConfigurationsError()


class ClipboardMonitor(QThread):
    """ Class Description """

    text_edit_signal = pyqtSignal(str)

    def __init__(self, delay: float, translator: ClipboardContentTranslator):
        """ Este constructor inicia con el tiempo de espera y el requeridor de contenido """
        super(ClipboardMonitor, self).__init__()
        self.delay_time: float = delay
        self.translator = translator
        self.state = False

    def set_delay_time(self, delay: float) -> None:
        self.delay_time = delay

    def set_translator(self, translator: ClipboardContentTranslator) -> None:
        self.translator = translator

    def start(self, priority=None) -> None:
        """ Este método inicia el proceso de lectura del portapapeles """
        self.state = True
        super(ClipboardMonitor, self).start()

    def stop_action(self) -> None:
        """ Este método detiene el proceso de lectura del portapapeles """
        if self.is_running():
            try:
                self.state = False
            except Exception as ex:
                QMessageBox.warning(None, 'Error', f"A problem as occurred: {ex}")

    def is_running(self) -> bool:
        """ Este método sirve para verificar si el monitor se esta ejecutando """
        return self.state

    def run(self) -> None:
        """ Este método inicia el ciclo que constantemente lee el contenido del portapapeles """
        while self.is_running():
            clipboard_content: str = paste()
            if (clipboard_content is not None) and (clipboard_content.__len__() > 0):
                if '\n' in clipboard_content:
                    try:
                        new_content = clipboard_content.replace('\r', "").replace('\n', ' ')
                        copy(new_content)
                        try:
                            translated = self.translator.translate(new_content)
                            self.text_edit_signal.emit(translated)
                        except Exception as ex:
                            self.text_edit_signal.emit(f"A error as occurred {ex}")
                    except TypeError as e:
                        print(e)
                        QMessageBox.warning(None, "TypeError", f"A problem as occurred: {e}")
            sleep(self.delay_time)
