from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import Qt

from utils.vtk_utils import *


class IsoAction(object):
    def __init__(self, path='../data/mr_brainixA'):
        _, image_data = read_dicom_images(path)

        self.contour_filter = contour_filter(image_data, 150)
        actor = vtk_actor(poly_data_mapper(self.contour_filter))

        self.renderer = get_renderer(actor, background=(.8, .8, .8))
        self.iren = None
        self.slider = None
        self.label = None

    def init_action(self, iren):
        self.iren = iren
        add_style(self.iren)
        self.init_measurement()
        self.init_slider()

    def init_measurement(self):
        self.meas_widget = vtk.vtkDistanceWidget()
        self.meas_widget.SetInteractor(self.iren)
        self.meas_widget.CreateDefaultRepresentation()
        self.meas_widget.SetRepresentation(vtk.vtkDistanceRepresentation3D())

    def init_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.setValue(128)
        slider.setMinimumHeight(40)
        slider.sliderReleased.connect(self.change_iso_value)
        self.slider = slider
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('ISO')
        label.setMinimumHeight(30)
        self.label = label

    def change_iso_value(self):
        value = self.slider.value()
        self.contour_filter.SetValue(0, value)
        self.iren.GetRenderWindow().Render()
