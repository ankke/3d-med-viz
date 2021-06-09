import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from vtk_utils.skin import named_colors, body_extractor, body_mapper, body_actor, outline_data, outline_mapper, \
    outline_actor, get_renderer_with_multiple_actors
from vtk_utils.utils import read_dicom_images, add_style, init_measurement
from widgets.Slider import Slider


class SkinCoverAction(object):
    def __init__(self, path, iren, measurement_on=False):
        self.iren = iren

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
        self.init_action()

    def init_action(self):
        add_style(self.iren)
        self.meas_widget = init_measurement(self.measurement_on, self.iren)
        self.init_slider()

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
