from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QComboBox, QCheckBox

from widgets.HWidgets import HWidgets


class LeftToolbar(QToolBar):
    def __init__(self, windows_num, open_file_dialog, on_combobox_change, on_checkbox_change, subwindows, *args):
        QToolBar.__init__(self, *args)
        self.setFloatable(True)
        self.setMovable(True)

        self.scroll_widget = QWidget(self)
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_widget.setMinimumWidth(350)

        button = QPushButton("&Load data")
        button.clicked.connect(open_file_dialog)
        self.scroll_layout.addWidget(button)

        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('Windows number:')

        combo = QComboBox()
        combo.addItem('1')
        for num in range(2, 10, 2):
            combo.addItem(str(num))
        index = combo.findText(str(windows_num))
        combo.setCurrentIndex(index)
        combo.currentTextChanged.connect(on_combobox_change)
        combo.setMaximumWidth(70)

        checkbox = QCheckBox("Synchronize windows")
        checkbox.setMinimumHeight(30)
        checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")
        checkbox.toggled.connect(on_checkbox_change(checkbox))

        wid = HWidgets([label, combo, checkbox])
        self.scroll_layout.addWidget(wid)

        for subwindow in subwindows:
            for widget in subwindow.tool_bar.widgets:
                self.scroll_layout.addWidget(widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.addWidget(self.scroll_area)
