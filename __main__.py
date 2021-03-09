import platform
from PyQt5.QtWidgets import QApplication
import sys

from transclip import MainWindow

OS_NAME = platform.system()
OS_VERSION = platform.version()
OS_RELEASE = platform.release()
OS_MACHINE = platform.machine()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    print("Welcome to transclip")
    print(f"Running on: {OS_NAME} {OS_RELEASE} {OS_MACHINE}")
    main()
