from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from utils.vtk_utils import volume_mapper, piecewise_fun, volume_actor, read_dicom_images, window_renderer, \
    get_renderer, add_style


class TransferFunAction(object):

    def __init__(self, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.point = 180

        self.mapper = volume_mapper(reader)
        self.piecewise = piecewise_fun(((0, 0), (self.point, 1), (self.point + 1, 1), (255, 0)))
        self.actor = volume_actor(self.mapper, self.piecewise)

        self.renderer = get_renderer(self.actor, background=(0.8, 0.8, 0.8))
        self.win_renderer = window_renderer(self.renderer, 800, 600)
        self.iren = None
        self.slider = None

    def init_action(self, iren):
        self.iren = iren
        add_style(self.iren)
        self.init_slider()

    def init_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.valueChanged.connect(lambda x: self.change_transfer_fun())
        self.slider = slider

    def change_transfer_fun(self):
        value = self.slider.value()
        self.change_piecewise(value)
        self.iren.GetRenderWindow().Render()

    def change_piecewise(self, value):
        self.piecewise.RemoveAllPoints()
        self.piecewise.AddPoint(0, 0)
        self.piecewise.AddPoint(self.point, value / 100)
        self.piecewise.AddPoint(self.point + 1, value / 100)
        self.piecewise.AddPoint(255, 0)
