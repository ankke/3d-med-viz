import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from utils.vtk_utils import volume_mapper, piecewise_fun, volume_actor, read_dicom_images, get_renderer, add_style
from widgets.HWidgets import HWidgets
from widgets.Slider import Slider


class TransferFunMultAction(object):

    def __init__(self, measurement_on=False, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.points = [(100, 0.5), (180, 1), (200, 0.5)]

        self.mapper = volume_mapper(reader)
        self.piecewise = piecewise_fun(((0, 0), *self.points, (255, 0)))
        self.actor = volume_actor(self.mapper, self.piecewise)

        self.renderer = get_renderer(self.actor, background=(0.8, 0.8, 0.8))
        self.iren = None
        self.slider = None
        self.widgets = []
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
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('Transfer function')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        for i in range(len(self.points)):
            x_slider = Slider(0, 255, self.points[i][0], lambda val: self.input_change(i, val), label_text='x:')
            y_slider = Slider(0, 100, self.points[i][1] * 100, lambda val: self.change_transfer_fun(i, val), scale=0.01, label_text='y:')
            double_slider = HWidgets([x_slider, y_slider], label_text=f'{i + 1} point')
            self.widgets.append(double_slider)

    def change_transfer_fun(self, i, value):
        self.change_piecewise(i, value)

    def change_piecewise(self, i, value):
        self.points[i] = (self.points[i][0], float(value))
        self.update()

    def input_change(self, i, value):
        self.points[i] = (float(value), self.points[i][1])
        self.update()

    def update(self):
        self.piecewise.RemoveAllPoints()
        self.piecewise.AddPoint(0, 0)
        for point, val in self.points:
            self.piecewise.AddPoint(point, val / 100)
            self.piecewise.AddPoint(point + 1, val / 100)
        self.piecewise.AddPoint(255, 0)
        self.iren.GetRenderWindow().Render()
