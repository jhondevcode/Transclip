from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFont, QDoubleValidator
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QDialogButtonBox, QGroupBox, \
    QLineEdit, QSpinBox, QColorDialog, QFontDialog, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout
from moson import ConfigurationProcessor

COLOR_BUTTON_ICON = "resources/img/config/color-button.png"
FONT_BUTTON_ICON = "resources/img/config/font-button.png"


# noinspection PyAttributeOutsideInit
class ConfigurationDialog(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.setModal(True)
        self.configuration = ConfigurationProcessor()
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.initialize_gui()

    def initialize_gui(self):
        """ Llama a los métodos que inician los componentes """
        self.setWindowTitle("Configurations")
        self.create_internal_box()
        self.create_editor_box()
        self.create_language_box()
        self.create_button_box()
        self.setLayout(self.main_layout)

    def create_internal_box(self):
        """ Crea la caja de configuraciones centrales """
        internal_box = QGroupBox("Internal")
        layout = QFormLayout()
        self.delay_input = QLineEdit(str(self.configuration.get('delay')))
        self.delay_input.setValidator(QDoubleValidator(0, 100, 1, self))
        layout.addRow(QLabel("Delay time:"), self.delay_input)

        internal_box.setLayout(layout)
        self.main_layout.addWidget(internal_box)

    def create_editor_box(self):
        """ Crea la caja de configuraciones para el editor """
        editor_box = QGroupBox("Editor")
        layout = QFormLayout()

        font_configuration: dict = self.configuration.get('font')

        components_layout = QHBoxLayout()
        self.font_input: QLineEdit = QLineEdit(str(font_configuration['family']))
        components_layout.addWidget(self.font_input)

        option_button = QPushButton(QIcon(QPixmap(FONT_BUTTON_ICON)), "")
        option_button.clicked.connect(self.font_selection)
        components_layout.addWidget(option_button)
        layout.addRow(QLabel("Font family:"), components_layout)

        self.font_size: QSpinBox = QSpinBox()
        self.font_size.setValue(int(font_configuration['size']))
        layout.addRow(QLabel("Font size:"), self.font_size)

        editor_box.setLayout(layout)
        self.main_layout.addWidget(editor_box)

    def create_language_box(self):
        """ Crea la caja de configuraciones para los lenguajes """
        language_box = QGroupBox("Language")
        layout = QFormLayout()
        lang_configurations: dict = self.configuration.get('language')
        self.source_input = QLineEdit(str(lang_configurations['source']))
        layout.addRow(QLabel("Source:"), self.source_input)
        self.target_input = QLineEdit(str(lang_configurations['target']))
        layout.addRow(QLabel("Target:"), self.target_input)

        language_box.setLayout(layout)
        self.main_layout.addWidget(language_box)

    def create_button_box(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(button_box)

    def font_selection(self):
        font, accept = QFontDialog().getFont(QFont(self.font_input.text(), self.font_size.value()), self.parent())
        if accept:
            self.font_input.setText(font.family())
            self.font_size.setValue(int(font.pointSize()))
            self.parent().set_editor_font(font)

    @pyqtSlot()
    def color_selection(self):
        color = QColorDialog().getColor(QColor(str(self.configuration.get('font')['color'])), self.parent())
        if color.isValid():
            self.font_color.setText(color.name())

    def accept(self) -> None:
        try:
            self.configuration.set("delay", float(self.delay_input.text()))
        except ValueError:
            QMessageBox.warning(self, "Error", "Unexpected char in delay input", QMessageBox.Ok)
        self.configuration.set("font", {
            "family": self.font_input.text(),
            "size": self.font_size.value()})
        self.configuration.set("language", {"source": self.source_input.text(), "target": self.target_input.text()})
        super().accept()

    def reject(self) -> None:
        super().reject()


from PyQt5.QtWidgets import QTextEdit

CLEAN_BUTTON_ICON = "resources/img/clean-button.png"


class EditText:

    BACKGROUND_COLOR = "#ffffff"
    FOREGROUND_COLOR = "#000000"

    def __init__(self, parent, title="None"):
        super(EditText, self).__init__()
        self.__parent = parent
        self.__title = title
        self.__edit_text = QTextEdit()
        self.__main_layout = QVBoxLayout()
        self.__buttons_layout = QHBoxLayout()
        self.initialize_ui()

    def initialize_buttons(self):
        self.__widget = QGroupBox(self.__title)
        self.clear_button = QPushButton(QIcon(QPixmap(CLEAN_BUTTON_ICON)), "Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.setToolTip("Clean the text pane")
        self.clear_button.clicked.connect(lambda: self.__edit_text.clear())
        self.__buttons_layout.addWidget(self.clear_button)

        self.foreground_color_button = QPushButton(QIcon(QPixmap(COLOR_BUTTON_ICON)), "Foreground")
        self.foreground_color_button.setToolTip("Change background color")
        self.foreground_color_button.clicked.connect(self.__change_foreground)
        self.__buttons_layout.addWidget(self.foreground_color_button)

        self.background_color_button = QPushButton(QIcon(QPixmap(COLOR_BUTTON_ICON)), "Background")
        self.background_color_button.setToolTip("Change foreground color")
        self.background_color_button.clicked.connect(self.__change_background)
        self.__buttons_layout.addWidget(self.background_color_button)

        self.__widget.setLayout(self.__main_layout)

    def initialize_ui(self) -> None:
        # Initialize the event for the edit text
        self.__edit_text.textChanged.connect(
            lambda: self.clear_button.setEnabled(len(self.__edit_text.toPlainText()) > 0))
        # initializing the buttons
        self.initialize_buttons()
        # Adding components to main layout
        self.__main_layout.addLayout(self.__buttons_layout)
        self.__main_layout.addWidget(self.__edit_text)

    def __change_foreground(self):
        foreground_color = QColorDialog().getColor(QColor(str("#000000")), self.__parent)
        if foreground_color.isValid():
            self.FOREGROUND_COLOR = foreground_color.name()
            style = "QTextEdit {color: " + foreground_color.name() + "; background-color: " + self.BACKGROUND_COLOR + ";}"
            self.__edit_text.setStyleSheet(style)

    def __change_background(self):
        background_color = QColorDialog().getColor(QColor(str("#000000")), self.__parent)
        if background_color.isValid():
            self.BACKGROUND_COLOR = background_color.name()
            style = "QTextEdit {color: " + self.FOREGROUND_COLOR + "; background-color: " + background_color.name() + ";}"
            self.__edit_text.setStyleSheet(style)

    def get_widget(self) -> QGroupBox:
        return self.__widget

    def get_edit_text(self) -> QTextEdit:
        return self.__edit_text
