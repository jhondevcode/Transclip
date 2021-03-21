import wx
import logger
from monitoring import Requester, ClipboardMonitor
from loaders import IconLoader, ConfigurationLoader
from widgets import TextContainer, InformationBar, AboutDialog
from util import img_load_scaled_bitmap, check_button_bitmap


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class AppWindow(wx.Frame, Requester):
    """This class creates the main program window as well as start the widgets"""

    def __init__(self):
        """Launch settings and widgets"""
        super(AppWindow, self).__init__(None, title="Transclip 1.0.0 wx version")
        width, height = wx.GetDisplaySize()
        # self.SetSize(width=width/2, height=height/2)
        self.SetMinSize(size=(width / 2.5, height / 2.5))
        self.__panel = wx.Panel(self)
        self.__widget_layout = wx.BoxSizer(wx.VERTICAL)
        self.setup_events()
        self.initialize_window_features()
        self.initialize_ui()
        self.__panel.SetSizer(self.__widget_layout)

    def setup_events(self):
        """Records window events"""
        logger.info("Logging window events")
        self.Bind(wx.EVT_CLOSE, self.on_destroy)

    def initialize_window_features(self) -> None:
        """Configure the window characteristics"""
        logger.info("Initializing window features")
        icon = IconLoader("favicon.png").get()
        if icon is not None:
            self.SetIcon(icon)

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
        check_button_bitmap(self.start_button, img_load_scaled_bitmap("play-button.png", 16, 16))
        self.start_button.Bind(wx.EVT_BUTTON, self.__start_button_action)
        option_layout.Add(self.start_button, 0, wx.ALL, 5)

        self.stop_button: wx.Button = wx.Button(self.__panel, label="Stop")
        check_button_bitmap(self.stop_button, img_load_scaled_bitmap("stop-button.png", 16, 16))
        self.stop_button.Bind(wx.EVT_BUTTON, self.__stop_button_action)
        self.stop_button.Enable(enable=False)
        option_layout.Add(self.stop_button, 0, wx.ALL, 5)

        self.conf_button: wx.Button = wx.Button(self.__panel, label="Configure")
        check_button_bitmap(self.conf_button, img_load_scaled_bitmap("settings-button.png", 16, 16))
        self.conf_button.Bind(wx.EVT_BUTTON, self.__conf_button_action)
        option_layout.Add(self.conf_button, 0, wx.ALL, 5)

        self.about_button: wx.Button = wx.Button(self.__panel, label="About")
        check_button_bitmap(self.about_button, img_load_scaled_bitmap("about-button.png", 16, 16))
        self.about_button.Bind(wx.EVT_BUTTON, self.__about_button_action)
        option_layout.Add(self.about_button, 0, wx.ALL, 5)

        self.exit_button: wx.Button = wx.Button(self.__panel, label="Exit")
        check_button_bitmap(self.exit_button, img_load_scaled_bitmap("shutdown-button.png", 16, 16))
        self.exit_button.Bind(wx.EVT_BUTTON, self.__exit_button_action)
        option_layout.Add(self.exit_button, 0, wx.ALL, 5)
        self.__widget_layout.Add(option_layout, 0, wx.CENTER)

    def _init_text_containers(self):
        """Start the text containers"""
        logger.info("Initializing text containers")
        self.source_container = TextContainer(self.__panel)
        self.__widget_layout.Add(self.source_container, 1, wx.CENTER | wx.EXPAND)
        self.source_container.get_text_container().SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        self.target_container = TextContainer(self.__panel)
        self.target_container.get_text_container().SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.__widget_layout.Add(self.target_container, 1, wx.CENTER | wx.EXPAND)

    def _init_notification_bar(self):
        """Start the information bar"""
        logger.info("Initializing notification bar")
        self.notification_bar = InformationBar(self.__panel)
        self.__widget_layout.Add(self.notification_bar, 0, wx.CENTER)

    def set_content(self, target: str, content: str):
        """Modify the text of the textual containers"""
        if target == "source":
            self.source_container.get_text_container().SetValue(content)
        elif target == "target":
            self.target_container.get_text_container().SetValue(content)

    def __start_button_action(self, event: wx.CommandEvent):
        try:
            self.start_button.Enable(enable=False)
            self.stop_button.Enable(enable=True)
            self.notification_bar.set_state("Connecting...")
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
            self.__clipboard_monitor = ClipboardMonitor(self, PlainTextTranslator(source, target), delay_time)
            self.notification_bar.set_source(source)
            self.notification_bar.set_target(target)
            self.__clipboard_monitor.start_monitoring()
            self.notification_bar.set_state("Connected")
        except Exception as ex:
            self.notification_bar.set_state("Bad network")
            wx.MessageDialog(self, message="Can't connect to the network",
                             caption="Error", style=wx.OK | wx.ICON_ERROR,
                             pos=wx.DefaultPosition).ShowModal()
            self.start_button.Enable(enable=True)
            self.stop_button.Enable(enable=False)
            logger.log(ex)

    def __stop_button_action(self, event: wx.CommandEvent = None):
        try:
            if self.__clipboard_monitor is not None:
                self.notification_bar.set_state("Disconnecting...")
                self.__clipboard_monitor.stop_monitoring()
                self.notification_bar.set_state("Disconnected")
            self.start_button.Enable(enable=True)
            self.stop_button.Enable(enable=False)
        except Exception as ex:
            self.start_button.Enable(enable=False)
            self.stop_button.Enable(enable=True)
            self.notification_bar.set_state("Thread error")
            logger.log(ex)

    def __conf_button_action(self, event: wx.CommandEvent):
        pass

    def __about_button_action(self, event: wx.CommandEvent):
        AboutDialog(self).show()

    def __exit_button_action(self, event: wx.CommandEvent):
        self.Close()

    def on_destroy(self, event):
        """This event is called when you want to close the program"""
        logger.info("Exit event called")
        dialog = wx.MessageDialog(self, message="Are you sure you want to quit?",
                                  caption="Confirm exit", style=wx.YES_NO | wx.ICON_QUESTION,
                                  pos=wx.DefaultPosition)
        response = dialog.ShowModal()
        if response == wx.ID_YES:
            self.__stop_button_action()
            self.Destroy()
        else:
            event.StopPropagation()
