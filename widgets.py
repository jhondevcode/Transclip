"""
This module provides custom widgets for certain functions
"""

import wx
from wx.adv import AboutDialogInfo, AboutBox

import logger
from loaders import ConfigurationLoader, IconLoader
from util import img_load_scaled_bitmap, check_button_bitmap


class ConfigWizard(wx.Dialog):
    """Represents the configuration wizard"""

    def __init__(self, owner: wx.Frame):
        """Starts the builder with the base settings of a Dialog"""
        super(ConfigWizard, self).__init__()
        self.__owner = owner

    def _init_widgets(self):
        """Launch the widgets of the wizard"""
        pass


# noinspection PyUnusedLocal
class TextContainer(wx.BoxSizer):
    """This widget is used to provide a text container next to the respective buttons that will allow manipulation"""

    def __init__(self, parent: wx.Panel):
        """This constructor starts by storing the parent and then calling the methods that will start the respective
        widgets """
        super(TextContainer, self).__init__(wx.VERTICAL)
        self.__parent = parent
        self.__init_widgets()

    def __init_widgets(self) -> None:
        """Calls the methods that start the widgets, the button container, and the text container"""
        self._init_container_options()
        self._init_text_container()

    def _init_container_options(self) -> None:
        """Create the respective buttons to operate on the text container"""
        buttons_layout = wx.BoxSizer(wx.HORIZONTAL)

        self.__clear_button = wx.Button(self.__parent, label="Clear")
        check_button_bitmap(self.__clear_button, img_load_scaled_bitmap("clean-button.png", 16, 16))
        self.__clear_button.Bind(wx.EVT_BUTTON, self._clear_button_event)
        self.__clear_button.Enable(enable=False)
        buttons_layout.Add(self.__clear_button, 0, wx.EXPAND, 5)

        self.Add(buttons_layout)

    def _init_text_container(self) -> None:
        """Create the text container"""
        self.__text_container = wx.TextCtrl(self.__parent, style=wx.TE_MULTILINE)
        self.__text_container.Bind(wx.EVT_TEXT, self._text_push_event)
        self.Add(self.__text_container, 1, wx.EXPAND | wx.CENTER)

    def get_text_container(self) -> wx.TextCtrl:
        """Returns the text container"""
        return self.__text_container

    def _text_push_event(self, event: wx.CommandEvent):
        if len(event.GetString()) > 0:
            self.__clear_button.Enable(enable=True)
        else:
            self.__clear_button.Enable(enable=False)

    def _clear_button_event(self, event: wx.CommandEvent):
        """Clean button action"""
        self.__text_container.Clear()


class InformationBar(wx.BoxSizer):
    """Provides a notification bar in which there are labels that indicate status and a progress bar which indicates
    the process of an operation """

    def __init__(self, parent: wx.Panel):
        """Register the panel and call the method that starts the widgets"""
        super(InformationBar, self).__init__(wx.HORIZONTAL)
        self.__parent = parent
        self.__init_widgets()

    def __init_widgets(self):
        """Perform the operations to register the widgets"""
        self._init_state_labels()

    def _init_state_labels(self):
        labels_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.__state_message: wx.StaticText = wx.StaticText(self.__parent, label="Network: Disconnected")
        labels_layout.Add(self.__state_message, 0, wx.ALL, 5)

        try:
            lang = ConfigurationLoader().get("language")
            source: str = str(lang["source"]).lower()
            target: str = str(lang["target"]).lower()
            del lang
        except Exception as ex:
            logger.log(ex)
            source: str = "undefined"
            target: str = "undefined"

        self.__source_label = wx.StaticText(self.__parent, label=f"Source: {source}")
        labels_layout.Add(self.__source_label, 0, wx.ALL, 5)

        self.__target_label = wx.StaticText(self.__parent, label=f"Target: {target}")
        labels_layout.Add(self.__target_label, 0, wx.ALL, 5)

        self.Add(labels_layout, 0, wx.ALL, 5)

    def set_state(self, state: str):
        if state is not None and state != "":
            self.__state_message.SetLabel(f"Network: {state.capitalize()}")

    def set_source(self, source: str):
        if source is not None and source != "":
            self.__source_label.SetLabel(f"Source: {source.capitalize()}")

    def set_target(self, target: str):
        if target is not None and target != "":
            self.__target_label.SetLabel(f"Target: {target.capitalize()}")


class AboutDialog:

    def __init__(self, parent):
        super(AboutDialog, self).__init__()
        self.__parent = parent
        self.info = AboutDialogInfo()
        self.info.SetIcon(IconLoader(name="favicon.png").get())
        self.info.SetName("Transclip")
        self.info.SetVersion("1.0.0", "Beta release")
        self.info.SetCopyright("(C) 2020 jhondev-code")
        self.info.SetDescription(desc="A small utility to translate clipboard content")
        self.info.SetWebSite("https://github.com/jhondev-code/transclip")
        self.info.AddDeveloper("Jhon fernandez")
        # self.info.AddDocWriter("Jhon fernandez")
        # self.info.AddTranslator("Jhon fernandez")

    def show(self):
        AboutBox(self.info, parent=self.__parent)
