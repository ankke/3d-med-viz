from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QLabel, QVBoxLayout


class Slider(QWidget):

    def __init__(self, min, max, init, callback, label_text=None, scale=1.0, spacing=5):
        super().__init__()
        self.scale = scale
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(min, max)
        slider.setValue(init)
        slider.setMinimumHeight(30)
        slider.valueChanged.connect(self.updateLabel)
        slider.sliderReleased.connect(lambda: callback(self.slider.value()))

        self.slider = slider

        value_label = QLabel("{:.2f}".format(init * self.scale), self)
        value_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        value_label.setMinimumWidth(50)
        self.value_label = value_label

        hbox = QHBoxLayout()
        if label_text is not None:
            label = QLabel(f'{label_text}', self)
            hbox.addWidget(label)
            hbox.addSpacing(spacing)
        hbox.addWidget(self.slider)
        hbox.addSpacing(spacing)
        hbox.addWidget(self.value_label)

        self.setLayout(hbox)

    def updateLabel(self, value):
        self.value_label.setText("{:.2f}".format(value * self.scale))
