from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel


class ToolBar(QWidget):
    def __init__(self, label_text, *args, **kwargs):
        super(ToolBar, self).__init__(*args, **kwargs)
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText(label_text)
        self.label = label
        self.widgets = [label]

    def set_up_action(self, action):
        self.widgets = [self.label]
        self.widgets.extend(action.widgets)
