"""
This module provides what is necessary to monitor the clipboard and process the content.
"""
import wx
import logger
from pyperclip import copy, paste
from time import sleep
from threading import Thread
from impl import AbstractMonitor
from formatters import PlainTextFormatter


class ClipboardMonitor(Thread, AbstractMonitor):
    """This class is in charge of processing the clipboard content to later be translated into another language."""

    def __init__(self, requester, translator, delay_time: float):
        """This builder starts by requesting a content requester to submit the original and translated content"""
        super(ClipboardMonitor, self).__init__()
        self.__requester = requester
        self.__translator = translator
        self.__delay_time = delay_time
        self.__formatter = PlainTextFormatter()

    def start_monitoring(self) -> None:
        """Starts the thread to monitor the clipboard."""
        super().start_monitoring()
        self.start()

    def stop_monitoring(self) -> None:
        """Stops the thread used to monitor the clipboard"""
        if self.is_running():
            logger.info("Stopping the run cycle")
            super().stop_monitoring()
        if self.is_alive():
            logger.info("Ending the thread")
            self.join()
            logger.info("Thread completed successfully")
        else:
            logger.error("The thread had already finished previously")

    def invoke_translate(self, content: str, old: str):
        wx.CallAfter(self.__requester.set_content, "source", content)
        wx.CallAfter(self.__requester.set_content, "target", "Translating...")
        try:
            translated = self.__translator.translate(content)
            wx.CallAfter(self.__requester.set_content, "target", translated)
            copy(content)
            return content
        except Exception as ex:
            logger.log(ex)
            return old

    def run(self):
        """This method implements the code necessary to keep the clipboard monitoring"""
        old_content = ""
        while self.is_running():
            clipboard_content: str = paste()
            if (clipboard_content is not None) and (clipboard_content.__len__() > 0):
                clipboard_content = self.__formatter.format(clipboard_content)
                if clipboard_content != old_content:
                    old_content = self.invoke_translate(clipboard_content, old_content)
                else:
                    if old_content == "":
                        old_content = self.invoke_translate(
                            clipboard_content, old_content
                        )
            sleep(self.__delay_time)
