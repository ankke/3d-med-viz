import vtk
from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import Qt

from utils.vtk_utils import volume_mapper, piecewise_fun, volume_actor, read_dicom_images, window_renderer, \
    get_renderer, add_style


class TransferFunAction(object):

    def __init__(self, measurement_on=False, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.point = 180

        self.mapper = volume_mapper(reader)
        self.piecewise = piecewise_fun(((0, 0), (self.point, 1), (self.point + 1, 1), (255, 0)))
        self.actor = volume_actor(self.mapper, self.piecewise)

        self.renderer = get_renderer(self.actor, background=(0.8, 0.8, 0.8))
        self.win_renderer = window_renderer(self.renderer, 800, 600)
        self.iren = None
        self.slider = None
        self.label = None
        self.meas_widget = None
        self.measurement_on = measurement_on

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
        if self.measurement_on:
            self.meas_widget.On()

    def init_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setMinimumHeight(40)
        slider.sliderReleased.connect(self.change_transfer_fun)
        self.slider = slider
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('Transfer function')
        label.setMinimumHeight(30)
        self.label = label

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

