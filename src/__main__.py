import wx

import sys
import logger
from transclip import AppWindow
from clipboard import clear, UnsupportedOperation


# noinspection PyAttributeOutsideInit
class App(wx.App):
    """This class starts the application"""

    def __init__(self):
        """Call the constructor of Object"""
        super(App, self).__init__()

    def OnInit(self) -> bool:
        """This method is used to start the application"""
        try:
            logger.info("Initializing application")
            self.frame = AppWindow()
            self.frame.Show()
            self.SetTopWindow(self.frame)
            return True
        except Exception as ex:
            logger.log(ex)
            return False


def main():
    """Run the app"""
    try:
        logger.info("Running the application")
        app = App()
        try:
            logger.info("Cleaning the clipboard...")
            clear()
        except UnsupportedOperation as ex:
            logger.error("A error has occurred while cleaning the clipboard")
            logger.log(ex)
            sys.exit(1)
        app.MainLoop()
    except Exception as ex:
        logger.log(ex)


if __name__ == "__main__":
    main()
