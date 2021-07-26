from abc import ABC, abstractmethod
from subprocess import call
from platform import system
from os import chdir, mkdir
from sys import argv


class OsUtil(ABC):
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def _clear_console(self):
        pass


class LinuxUtils(OsUtil):
    
    def __init__(self):
        super().__init__()

    def build(self):
        pass

    def clean(self):
        call(["rm", "-r", "src/__pycache__"])
        call(["rm", "-r", "src/build"])
        call(["rm", "-r", "src/dist"])
        call(["rm", "-r", "src/__main__.spec"])
    
    def install(self):
        pass

    def _clear_console(self):
        call(["clear"])


class WindowsUtils(OsUtil):
    
    def __init__():
        super().__init__()

    def build(self):
        pass

    def clean(self):
        pass

    def install(self):
        pass

    def _clear_console(self):
        call(["cls"])


def main():
    os_helper: OsUtil = None
    if system() == "Linux":
        os_helper = LinuxUtils()
    elif system() == "Windows":
        os_helper = WindowsUtils()
    else:
        print("Your system is not supported :(\n")
        print("Please help us to support users with the same system")
        print("Any help is welcome :)")

    if os_helper is not None:
        print("You system has been checked")

    
if __name__ == '__main__':
    main()
