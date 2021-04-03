import wx

import logger
from transclip import AppWindow
from pyperclip import copy


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
        logger.info("Cleanning the clipboard...")
        copy("")
    except Exception as ex:
        logger.error("A error has ocurred while cleanning the clipboard")
        logger.log(ex)
    try:
        logger.info("Running the application")
        app = App()
        app.MainLoop()
    except Exception as ex:
        logger.log(ex)


if __name__ == '__main__':
    main()
