from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFont, QDoubleValidator
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QDialogButtonBox, QGroupBox, \
    QLineEdit, QSpinBox, QColorDialog, QFontDialog, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout
from moson import ConfigurationProcessor

COLOR_BUTTON_ICON = "resources/img/config/color-button.png"
FONT_BUTTON_ICON = "resources/img/config/font-button.png"
FONT_STYLES = ['Normal', 'Italic', 'Oblique']


# noinspection PyAttributeOutsideInit
class ConfigurationDialog(QDialog):

    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.setModal(True)
        self.configuration = ConfigurationProcessor()
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.initialize_gui()

    def initialize_gui(self):
        """ Llama a los metodos que inician los componentes """
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

        self.font_style: QComboBox = QComboBox()
        saved_style = str(font_configuration['style'])
        self.font_style.addItem(saved_style)
        for style in FONT_STYLES:
            if style != saved_style:
                self.font_style.addItem(style)
        layout.addRow(QLabel("Font style:"), self.font_style)

        components_layout = QHBoxLayout()
        self.font_color: QLineEdit = QLineEdit(str(font_configuration['color']))
        components_layout.addWidget(self.font_color)
        option_button: QPushButton = QPushButton(QIcon(QPixmap(COLOR_BUTTON_ICON)), "")
        option_button.clicked.connect(self.color_selection)
        components_layout.addWidget(option_button)
        layout.addRow(QLabel("Font Color:"), components_layout)

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
            "style": "Normal",
            "size": self.font_size.value(),
            "color": self.font_color.text()})
        self.configuration.set("language", {"source": self.source_input.text(), "target": self.target_input.text()})
        super().accept()

    def reject(self) -> None:
        super().reject()
