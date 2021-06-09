from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QLabel


class Slider(QWidget):

    def __init__(self, min, max, init, callback, scale=1.0, input=None):
        super().__init__()
        self.scale = scale
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(min, max)
        slider.setValue(init)
        slider.setMinimumHeight(30)
        slider.valueChanged.connect(self.updateLabel)
        slider.sliderReleased.connect(lambda: callback(self.slider.value()))

        self.slider = slider

        label = QLabel("{:.2f}".format(init * self.scale), self)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setMinimumWidth(50)
        self.label = label

        hbox = QHBoxLayout()
        if input is not None:
            hbox.addWidget(input)
            hbox.addSpacing(10)
        hbox.addWidget(self.slider)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

    def updateLabel(self, value):
        self.label.setText("{:.2f}".format(value * self.scale))
