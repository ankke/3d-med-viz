from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from utils.vtk_utils import *


class IsoAction(object):
    def __init__(self, path='../data/mr_brainixA'):
        _, image_data = read_dicom_images(path)

        self.contour_filter = contour_filter(image_data, 150)
        actor = vtk_actor(poly_data_mapper(self.contour_filter))

        self.renderer = get_renderer(actor, background=(.8, .8, .8))
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
        slider.setMaximum(255)
        slider.setValue(128)
        slider.valueChanged.connect(lambda x: self.change_iso_value())
        self.slider = slider

    def change_iso_value(self):
        value = self.slider.value()
        self.contour_filter.SetValue(0, value)
        self.iren.GetRenderWindow().Render()
