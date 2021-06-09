from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from vtk_utils.transfer_fun import volume_mapper, piecewise_fun, volume_actor
from vtk_utils.utils import read_dicom_images, get_renderer, add_style, init_measurement
from widgets.Slider import Slider


class TransferFunAction(object):

    def __init__(self, path, iren, measurement_on=False):
        self.iren = iren

        reader, image_data = read_dicom_images(path)

        self.point = 180

        self.mapper = volume_mapper(reader)
        self.piecewise = piecewise_fun(((0, 0), (self.point, 1), (self.point + 1, 1), (255, 0)))
        self.actor = volume_actor(self.mapper, self.piecewise)

        self.renderer = get_renderer(self.actor, background=(0.8, 0.8, 0.8))
        self.slider = None
        self.widgets = []
        self.meas_widget = None
        self.measurement_on = measurement_on
        self.init_action()

    def init_action(self):
        add_style(self.iren)
        self.meas_widget = init_measurement(self.measurement_on, self.iren)
        self.init_slider()

    def init_slider(self):
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('Transfer function')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        self.slider = Slider(0, 100, 50, self.change_transfer_fun, scale=0.01)
        self.widgets.append(self.slider)

    def change_transfer_fun(self, value):
        self.change_piecewise(value)
        self.iren.GetRenderWindow().Render()

    def change_piecewise(self, value):
        self.piecewise.RemoveAllPoints()
        self.piecewise.AddPoint(0, 0)
        self.piecewise.AddPoint(self.point, value / 100)
        self.piecewise.AddPoint(self.point + 1, value / 100)
        self.piecewise.AddPoint(255, 0)
