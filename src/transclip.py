import platform
from threading import Thread

import wx

import logger
from __version__ import __title__, __version__
from impl import Requester
from loaders import IconLoader, ConfigurationLoader, BitMapLoader
from monitoring import ClipboardMonitor
from pyperclip import copy
from util import img_load_scaled_bitmap, check_button_bitmap
from widgets import TextContainer, InformationBar, AboutDialog


class WindowMenuBar(wx.MenuBar):
    def __init__(self, frame):
        super(WindowMenuBar, self).__init__()
        self.parent = frame
        try:
            self.initialize_components()
        except Exception as ex:
            logger.error(str(ex))
            logger.log(ex)

    def initialize_components(self):
        self.file_menu = wx.Menu()
        self.initialize_file_menu_items()
        self.Append(self.file_menu, "&File")

        self.tools_menu = wx.Menu()
        self.initialize_tools_menu_item()
        self.Append(self.tools_menu, "&Tools")

        self.help_menu = wx.Menu()
        self.initialize_help_menu_item()
        self.Append(self.help_menu, "&Help")

    def initialize_file_menu_items(self):
        save_item = self.create(
            self.file_menu, wx.ID_SAVEAS, "Save", "Save translation", "export.png"
        )
        self.file_menu.Append(save_item)
        self.Bind(wx.EVT_MENU, self.parent.save, save_item)

        self.file_menu.AppendSeparator()

        exit_item = self.create(
            self.file_menu, wx.ID_EXIT, "Exit", "Close and exit", "shutdown.png"
        )
        self.file_menu.Append(exit_item)
        self.Bind(wx.EVT_MENU, self.parent.exit_button_action, exit_item)

    def initialize_tools_menu_item(self):
        clean_item = self.create(
            self.tools_menu,
            wx.ID_ANY,
            "Clear clipboard",
            "Clean the clipboard",
            "clear.png",
        )
        self.tools_menu.Append(clean_item)
        self.Bind(wx.EVT_MENU, lambda x: copy(""), clean_item)
        settings_item = self.create(
            self.tools_menu,
            wx.ID_SETUP,
            "Settings",
            "Configure the program",
            "settings.png",
        )
        self.tools_menu.Append(settings_item)

    def initialize_help_menu_item(self):
        about_item = self.create(
            self.help_menu, wx.ID_ABOUT, "About of", "Program information", "about.png"
        )
        self.help_menu.Append(about_item)
        self.Bind(wx.EVT_MENU, self.parent.about_button_action, about_item)

    def create(self, parent, wid, label, state, icon) -> wx.MenuItem:
        os_name = platform.system()
        if os_name == "Windows":
            menu_item = wx.MenuItem(parent, wid, label, state)
            bitmap = BitMapLoader(icon, "menubar", "icon").get()
            if bitmap is not None:
                try:
                    menu_item.SetBitmap(bitmap)
                except Exception as ex:
                    logger.log(ex)
            return menu_item
        else:
            return wx.MenuItem(parent, wid, label, state)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class AppWindow(wx.Frame, Requester):
    """This class creates the main program window as well as start the widgets"""

    def __init__(self):
        """Launch settings and widgets"""
        super(AppWindow, self).__init__(
            None, title=f"{__title__} {__version__} wx version"
        )
        width, height = wx.GetDisplaySize()
        # self.SetSize(width=width/2, height=height/2)
        self.SetMinSize(size=(width / 2.5, height / 2.5))
        self.__panel = wx.Panel(self)
        self.__widget_layout = wx.BoxSizer(wx.VERTICAL)
        self.__clipboard_monitor = None
        try:
            self.__enabled_source_preview = bool(
                ConfigurationLoader().get("core")["source-preview"]
            )
        except Exception as ex:
            logger.log(ex)
            self.__enabled_source_preview = True
        self.setup_events()
        self.initialize_window_features()
        self.initialize_ui()
        self.__panel.SetSizer(self.__widget_layout)

    def setup_events(self):
        """Records window events"""
        logger.info("Logging window events")
        self.Bind(wx.EVT_CLOSE, self.on_destroy)

    def load_window_icon(self):
        icon = IconLoader("favicon.png")
        if icon is not None:
            try:
                self.SetIcon(wx.Icon(icon.get_path()))
            except Exception as ex:
                logger.error(str(ex))
                logger.log(ex)

    def initialize_window_features(self) -> None:
        """Configure the window characteristics"""
        logger.info("Initializing window features")
        self.SetMenuBar(WindowMenuBar(self))
        self.load_window_icon()

    def initialize_ui(self):
        """comment"""
        logger.info("Initializing ui widgets")
        self._init_options_panel()
        self._init_text_containers()
        self._init_notification_bar()

    def _init_options_panel(self):
        """comment"""
        logger.info("Initializing option container")
        # initialize options container
        option_layout = wx.BoxSizer(wx.HORIZONTAL)
        # initialize option buttons
        self.start_button: wx.Button = wx.Button(self.__panel, label="Start")
        check_button_bitmap(
            self.start_button, img_load_scaled_bitmap("play-button.png", 16, 16)
        )
        self.start_button.Bind(wx.EVT_BUTTON, self.__start_button_action)
        option_layout.Add(self.start_button, 0, wx.ALL, 5)

        self.stop_button: wx.Button = wx.Button(self.__panel, label="Stop")
        check_button_bitmap(
            self.stop_button, img_load_scaled_bitmap("stop-button.png", 16, 16)
        )
        self.stop_button.Bind(wx.EVT_BUTTON, self.__stop_button_action)
        self.stop_button.Enable(enable=False)
        option_layout.Add(self.stop_button, 0, wx.ALL, 5)

        self.__widget_layout.Add(option_layout, 0, wx.CENTER)

    def _init_text_containers(self):
        """Start the text containers"""
        logger.info("Initializing text containers")

        if self.__enabled_source_preview:
            self.source_container = TextContainer(self.__panel)
            self.__widget_layout.Add(self.source_container, 1, wx.CENTER | wx.EXPAND)

        self.target_container = TextContainer(self.__panel)
        self.__widget_layout.Add(self.target_container, 1, wx.CENTER | wx.EXPAND)

    def _init_notification_bar(self):
        """Start the information bar"""
        logger.info("Initializing notification bar")
        self.notification_bar = InformationBar(self.__panel)
        self.__widget_layout.Add(self.notification_bar, 0, wx.CENTER)

    def set_content(self, target: str, content: str):
        """Modify the text of the textual containers"""
        if target == "source" and self.__enabled_source_preview:
            self.source_container.get_text_container().SetValue(content)
        elif target == "target":
            self.target_container.get_text_container().SetValue(content)

    def connect_to_server(self):
        try:
            wx.CallAfter(self.start_button.Enable, False)
            config = ConfigurationLoader()
            from translation import PlainTextTranslator

            try:
                source: str = config.get("language")["source"]
                target: str = config.get("language")["target"]
            except Exception as ex:
                source: str = "en"
                target: str = "es"
                logger.log(ex)
            try:
                delay_time: float = float(config.get("core")["delay"])
                logger.info(f"Delay time established in {delay_time} seconds")
            except Exception as ex:
                logger.log(ex)
                delay_time: float = 0.5
            self.__clipboard_monitor = ClipboardMonitor(
                self, PlainTextTranslator(source, target), delay_time
            )
            wx.CallAfter(self.notification_bar.set_source, source)
            wx.CallAfter(self.notification_bar.set_target, target)
            self.__clipboard_monitor.start_monitoring()
            wx.CallAfter(self.notification_bar.set_state, "Connected")
            wx.CallAfter(self.stop_button.Enable, True)
        except Exception as ex:
            wx.CallAfter(self.notification_bar.set_state, "Bad network")
            wx.MessageDialog(
                self,
                message="Can't connect to the network",
                caption="Error",
                style=wx.OK | wx.ICON_ERROR,
                pos=wx.DefaultPosition,
            ).ShowModal()
            wx.CallAfter(self.start_button.Enable, True)
            wx.CallAfter(self.stop_button.Enable, False)
            logger.log(ex)

    def __start_button_action(self, event: wx.CommandEvent):
        self.notification_bar.set_state("Connecting...")
        connection = Thread(target=self.connect_to_server)
        connection.start()

    def disconnect_from_server(self):
        logger.info("Disconnecting...")
        try:
            logger.info("Checking the monitor")
            if self.__clipboard_monitor is not None:
                logger.info("Notifying the disconnection")
                wx.CallAfter(self.notification_bar.set_state, "Disconnecting...")
                logger.info("Stopping the monitor")
                self.__clipboard_monitor.stop_monitoring()
                logger.info("Notifying the stop of the monitor")
                wx.CallAfter(self.notification_bar.set_state, "Disconnected")
                logger.info("Disconnection completed")
            wx.CallAfter(self.start_button.Enable, True)
            wx.CallAfter(self.stop_button.Enable, False)
            logger.info("Resetting the buttons")
        except AttributeError as ae:
            logger.warn("The monitor has not started")
            logger.log(ae)
        except Exception as ex:
            logger.error("An exception was reported when stopping the monitor")
            logger.log(ex)
            wx.CallAfter(self.notification_bar.set_state, "Thread error")

    def __stop_button_action(self, event: wx.CommandEvent = None):
        # disconnect = Thread(target=self.disconnect_from_server)
        # disconnect.start()
        self.disconnect_from_server()

    def __conf_button_action(self, event: wx.CommandEvent):
        pass

    def about_button_action(self, event: wx.CommandEvent):
        AboutDialog(self).show()

    def exit_button_action(self, event: wx.CommandEvent):
        self.Close()

    def save(self, event: wx.CommandEvent):
        text = self.target_container.get_text_container().GetValue()
        if text != "":
            with wx.FileDialog(
                self,
                "Save file",
                wildcard="Plain Text File (*.txt)|*.txt",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            ) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind
                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(pathname, "w") as file:
                        file.write(text)
                except IOError:
                    wx.LogError(f"Cannot save current data in file '{pathname}'.")
        else:
            wx.MessageDialog(
                self,
                message="No content to save",
                caption="Error",
                style=wx.OK | wx.ICON_ERROR,
                pos=wx.DefaultPosition,
            ).ShowModal()

    def on_destroy(self, event):
        """This event is called when you want to close the program"""
        logger.info("Exit event called")
        dialog = wx.MessageDialog(
            self,
            message="Are you sure you want to quit?",
            caption="Confirm exit",
            style=wx.YES_NO | wx.ICON_WARNING,
            pos=wx.DefaultPosition,
        )
        response = dialog.ShowModal()
        if response == wx.ID_YES:
            try:
                if self.__clipboard_monitor is not None:
                    if self.__clipboard_monitor.is_running():
                        self.__clipboard_monitor.stop_monitoring()
                    else:
                        logger.info("The monitor had already been stopped before")
                else:
                    logger.info("Monitor has never been started")
            except Exception as ex:
                logger.log(ex)
            self.Destroy()
        else:
            event.StopPropagation()
