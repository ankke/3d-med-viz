import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from utils.vtk_utils import read_dicom_images, add_style, get_renderer_with_multiple_actors, named_colors, \
    body_extractor, body_mapper, body_actor, outline_data, outline_mapper, outline_actor
from widgets.Slider import Slider


class SkinCoverAction(object):
    def __init__(self, path, measurement_on=False):
        reader, image_data = read_dicom_images(path)

        self.widgets = []
        self.colors = named_colors()

        self.skin_extractor = body_extractor(reader, 500)
        self.skin_mapper = body_mapper(self.skin_extractor)
        self.init_skin_actor()
        self.outline_data = outline_data(reader)
        self.outline_mapper = outline_mapper(self.outline_data)
        self.outline_actor = outline_actor(self.outline_mapper, self.colors)
        actors = [self.outline_actor, self.skin_actor]
        self.renderer = get_renderer_with_multiple_actors(actors, background=(0.8, 0.8, 0.8))
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
        label.setText('Skin')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        self.slider = Slider(0, 1000, 500, self.change_value)
        self.widgets.append(self.slider)

    def init_skin_actor(self):
        self.skin_actor = body_actor(self.skin_mapper, self.colors, 'SkinColor')
        back_prop = vtk.vtkProperty()
        back_prop.SetDiffuseColor(self.colors.GetColor3d('BackfaceColor'))
        self.skin_actor.SetBackfaceProperty(back_prop)

    def change_value(self, value):
        self.skin_extractor.SetValue(0, value)
        self.skin_extractor.Update()
        self.iren.GetRenderWindow().Render()


