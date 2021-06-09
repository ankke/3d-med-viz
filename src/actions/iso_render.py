import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from vtk_utils.iso import contour_filter, poly_data_mapper, vtk_actor
from vtk_utils.utils import read_dicom_images, get_renderer, add_style, init_measurement
from widgets.Slider import Slider


class IsoAction(object):
    def __init__(self, path, iren, measurement_on=False):
        self.iren = iren
        _, image_data = read_dicom_images(path)

        self.contour_filter = contour_filter(image_data, 150)
        actor = vtk_actor(poly_data_mapper(self.contour_filter))

        self.renderer = get_renderer(actor, background=(.8, .8, .8))
        self.widgets = []
        self.slider = None
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
        label.setText('ISO')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        self.slider = Slider(0, 155, 128, self.change_iso_value)
        self.widgets.append(self.slider)

    def change_iso_value(self, value):
        self.contour_filter.SetValue(0, value)
        self.iren.GetRenderWindow().Render()
