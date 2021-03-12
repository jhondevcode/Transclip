from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QStatusBar, QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel
from monitor import ClipboardContentTranslator, ClipboardMonitor
from moson import ConfigurationProcessor
from widgets import ConfigurationDialog, EditText

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
        self.initialize_text_containers()
        # Init the status bar
        self.initialize_status_bar()

    def initialize_text_containers(self):
        # loading edit text configurations
        font = self.__configuration_file.get('font')
        style_sheet = self.__configuration_file.get("edit-text")
        # Init the original text panel
        original_edit_text = EditText(self, title="Original text")
        self.original_edit = original_edit_text.get_edit_text()
        self.set_original_edit_font(QFont(font['family'], font['size']))
        style = "QTextEdit {color: " + style_sheet["source"]["foreground"] +\
                "; background-color: " + style_sheet["source"]["background"] + ";}"
        original_edit_text.get_edit_text().setStyleSheet(style)
        self.__main_layout.addWidget(original_edit_text.get_widget())

        # Init the translated text panel
        translated_edit_text = EditText(self, title="Translated text")
        self.translated_edit = translated_edit_text.get_edit_text()
        self.set_editor_font(QFont(font['family'], font['size']))
        style = "QTextEdit {color: " + style_sheet["target"]["foreground"] + \
                "; background-color: " + style_sheet["target"]["background"] + ";}"
        translated_edit_text.get_edit_text().setStyleSheet(style)
        self.__main_layout.addWidget(translated_edit_text.get_widget())

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

        self.config_button = QPushButton(QIcon(QPixmap(SETTINGS_BUTTON_ICON)), "Configure")
        self.config_button.setToolTip("Configure transclip")
        self.config_button.clicked.connect(self.config_button_action)
        buttons_layout.addWidget(self.config_button)

        self.exit_button = QPushButton(QIcon(QPixmap(SHUTDOWN_BUTTON_ICON)), "Exit")
        self.exit_button.setToolTip("Turn off the program and exit")
        self.exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.exit_button)

        self.__main_layout.addLayout(buttons_layout)

    def initialize_status_bar(self):
        self.status_bar = QStatusBar()
        self.__main_layout.addWidget(self.status_bar)
        self.state_label = QLabel()
        self.set_connection_status()
        self.status_bar.addWidget(self.state_label)

    def close(self) -> None:
        super(MainWindow, self).close()

    def set_target_text(self, string: str) -> None:
        if string != "":
            self.translated_edit.setPlainText(string)

    def set_source_text(self, original: str) -> None:
        if original != "":
            self.original_edit.setPlainText(original)

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
            self.clip_thread.source_signal.connect(self.set_source_text)
            self.clip_thread.target_signal.connect(self.set_target_text)
            self.clip_thread.start()
            self.set_connection_status(True)
        except Exception as ex:
            print(f"Error: {ex} jajaja")

    def stop_button_action(self) -> None:
        try:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.clip_thread.stop_action()
            self.set_connection_status(False)
        except Exception as ex:
            print(f"Error: {ex}")

    def config_button_action(self) -> None:
        try:
            win = ConfigurationDialog(self)
            win.show()
        except Exception as ex:
            print(ex)

    def set_editor_font(self, font) -> None:
        if font is not None:
            self.translated_edit.setFont(font)

    def set_original_edit_font(self, font) -> None:
        if font is not None:
            self.original_edit.setFont(font)

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
