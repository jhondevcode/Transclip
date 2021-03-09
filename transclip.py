from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QStatusBar, QTextEdit, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QWidget, QLabel
from monitor import ClipboardContentTranslator, ClipboardMonitor
from moson import ConfigurationProcessor
from widgets import ConfigurationDialog

PLAY_BUTTON_ICON = "resources/img/play-button.png"
STOP_BUTTON_ICON = "resources/img/stop-button.png"
CLEAN_BUTTON_ICON = "resources/img/clean-button.png"
SETTINGS_BUTTON_ICON = "resources/img/settings-button.png"
SHUTDOWN_BUTTON_ICON = "resources/img/shutdown-button.png"


# noinspection PyAttributeOutsideInit
class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.__configuration_file = ConfigurationProcessor()
        self.__main_layout: QVBoxLayout
        self.initialize_ui()
        self.setLayout(self.__main_layout)

    def initialize_ui(self):
        self.setWindowIcon(QIcon("resources/img/favicon.png"))
        self.setWindowTitle("Transclip")
        self.resize(800, 400)
        self.__main_layout = QVBoxLayout()
        self.initialize_options_layout()

        # Init the text pane
        self.text_edit = QTextEdit()
        font = self.__configuration_file.get('font')
        self.set_editor_font(QFont(font['family'], font['size']))
        self.text_edit.textChanged.connect(self.text_changed_event)
        self.__main_layout.addWidget(self.text_edit)
        # Init the status bar
        self.initialize_status_bar()

    def initialize_options_layout(self):
        buttons_layout = QHBoxLayout()

        self.start_button = QPushButton(QIcon(QPixmap(PLAY_BUTTON_ICON)), "Start")
        self.start_button.setDefault(True)
        self.start_button.setToolTip("Start clipboard monitoring")
        self.start_button.clicked.connect(self.star_button_action)
        buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton(QIcon(QPixmap(STOP_BUTTON_ICON)), "Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.setToolTip("Stop clipboard monitoring")
        self.stop_button.clicked.connect(self.stop_button_action)
        buttons_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton(QIcon(QPixmap(CLEAN_BUTTON_ICON)), "Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.setToolTip("Clean the text pane")
        self.clear_button.clicked.connect(self.clear_edit_text)
        buttons_layout.addWidget(self.clear_button)

        self.config_button = QPushButton(QIcon(QPixmap(SETTINGS_BUTTON_ICON)), "Configure")
        self.config_button.setToolTip("Configure transclip")
        self.config_button.clicked.connect(self.config_button_action)
        buttons_layout.addWidget(self.config_button)

        self.exit_button = QPushButton(QIcon(QPixmap(SHUTDOWN_BUTTON_ICON)), "Exit")
        self.exit_button.setToolTip("Turn off the program and exit")
        self.exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.exit_button)

        self.__main_layout.addLayout(buttons_layout)

    def text_changed_event(self):
        self.clear_button.setEnabled(len(self.text_edit.toPlainText()) > 0)

    def initialize_status_bar(self):
        self.status_bar = QStatusBar()
        self.__main_layout.addWidget(self.status_bar)
        self.state_label = QLabel()
        self.set_connection_status()
        self.status_bar.addWidget(self.state_label)

    def close(self) -> None:
        super(MainWindow, self).close()

    def paste_text(self, string: str) -> None:
        if string != "":
            self.text_edit.setPlainText(string)

    def set_connection_status(self, state: bool = False, other: str = "") -> None:
        if other != "":
            self.state_label.setText(f"State: {other}")
        else:
            if state:
                self.state_label.setText("State: Connected")
            else:
                self.state_label.setText("State: Disconnected")

    def star_button_action(self) -> None:
        try:
            try:
                delay_time = float(self.__configuration_file.get('delay'))
            except ValueError:
                delay_time = 0.5
            source = self.__configuration_file.get('language')['source']
            target = self.__configuration_file.get('language')['target']
            self.translator = ClipboardContentTranslator(source, target)
            self.clip_thread = ClipboardMonitor(delay_time, self.translator)
            self.stop_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.clip_thread.text_edit_signal.connect(self.paste_text)
            self.clip_thread.start()
            self.set_connection_status(True)
        except Exception as ex:
            print(f"Error: {ex}")

    def stop_button_action(self) -> None:
        try:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.clip_thread.stop_action()
            self.set_connection_status(False)
        except Exception as ex:
            print(f"Error: {ex}")

    def clear_edit_text(self) -> None:
        self.text_edit.clear()

    def config_button_action(self) -> None:
        try:
            win = ConfigurationDialog(self)
            win.show()
        except Exception as ex:
            print(ex)

    def set_editor_font(self, font) -> None:
        if font is not None:
            self.text_edit.setFont(font)

    # noinspection PyMethodMayBeStatic
    def set_sleep_time(self, interval) -> None:
        if interval > 0:
            pass

    def set_lang(self, source, target) -> None:
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        quit_message = QMessageBox.question(self, "Confirm exit", "Are you sure you want to exit?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if quit_message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
