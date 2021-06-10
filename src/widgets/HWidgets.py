from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout


class HWidgets(QWidget):

    def __init__(self, widgets, label_text=None, spacing=10):
        super().__init__()

        hbox = QHBoxLayout()
        for widget in widgets:
            hbox.addWidget(widget)
            hbox.addSpacing(spacing)

        if label_text is not None:
            label = QLabel(f'{label_text}', self)
            label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addLayout(hbox)
            self.setLayout(vbox)
        else:
            self.setLayout(hbox)
