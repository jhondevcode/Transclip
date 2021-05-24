"""
    This module provides the basic functionalities to issue records.

    At the moment this module emits the registers in 2 ways:
        -> in files
        -> in the console
"""

import os
import datetime
import threading
import traceback
from colorama import init, Fore


class Logger:
    """
    This class provides a logger to issue 3 different log levels:
    -> info: information logs
    -> warn: warning logs
    -> error: error logs

    The class is able to write the registers in the terminal as well as in plain text files.
    If the logger is configured to write to files, the log names will be based on the current system date.
    In case the logger is configured to write to the console, the messages
    will be colored according to the log level.
    """

    def __init__(self, file=False):
        """Start by checking if the logger is configured to write to files or to the terminal"""
        if file:
            try:
                os.mkdir("logs")
            except OSError:
                pass
            self.__log_file = f"logs/log-{datetime.datetime.now().date()}.log"
            try:
                with open(self.__log_file, "x") as log_file:
                    log_file.write(
                        f"{'='*30}[{datetime.datetime.now().date()}]{'='*30}\n\n"
                        f"{'='*15}[{datetime.datetime.now().time()}]{'='*15}\n"
                    )
            except FileExistsError:
                self.__write(f"\n{'='*15}[{datetime.datetime.now().time()}]{'='*15}\n")
        else:
            init(autoreset=True)
            self.__log_file = None

    def __write(self, message: str):
        with open(self.__log_file, "a") as file:
            file.write(message)

    def log(self, message: str, level="info"):
        """This method is in charge of registering the data classifying them according to the level"""
        if level == "warn":
            if self.__log_file is not None:
                self.__write(
                    f"{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Warn]: {message}\n"
                )
            else:
                print(
                    f"{Fore.YELLOW}"
                    f"{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Warn]: {message}"
                )
        elif level == "error":
            if self.__log_file is not None:
                self.__write(
                    f"{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Error]: {message}\n"
                )
            else:
                print(
                    f"{Fore.RED}{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Error]: {message}"
                )
        elif level == "except":
            if self.__log_file is not None:
                self.__write(
                    f"{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Except]: {message}\n"
                )
            else:
                print(
                    f"{Fore.RED}{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Except]: {message}"
                )
        else:
            if self.__log_file is not None:
                self.__write(
                    f"{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Info]: {message}\n"
                )
            else:
                print(
                    f"{Fore.CYAN}{datetime.datetime.now()} [{threading.currentThread().getName()}]\n[Info]: {message}"
                )


# Logger object, started with a default configuration.
__logger__ = Logger(file=True)


def info(message, exception=None):
    """Log information messages"""
    if exception is not None:
        __logger__.log(f"{message}:\n{traceback.format_exc()}", "info")
    else:
        __logger__.log(f"{message}", "info")


def warn(message, exception=None):
    """Log warning messages"""
    if exception is not None:
        __logger__.log(f"{message}:\n{traceback.format_exc()}", "warn")
    else:
        __logger__.log(f"{message}", "warn")


def error(message: str, exception=None):
    """Log error messages"""
    if exception is not None:
        __logger__.log(f"{message}:\n{traceback.format_exc()}", "error")
    else:
        __logger__.log(f"{message}", "error")


def log(exception: Exception):
    """Log exceptions with the error level"""
    __logger__.log(f"{traceback.format_exc()}", "except")
