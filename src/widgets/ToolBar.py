from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFrame


class ToolBar(QWidget):
    def __init__(self, label_text, *args, **kwargs):
        super(ToolBar, self).__init__(*args, **kwargs)
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText(label_text)
        label.setFont(QFont('Arial', 16, QFont.DemiBold))
        self.label = label

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.line = line

        self.widgets = []

    def set_up_action(self, action):
        self.widgets = [self.label]
        self.widgets.extend(action.widgets)
        self.widgets.append(self.line)
