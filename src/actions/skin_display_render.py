import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from utils.vtk_utils import *
from widgets.Slider import Slider


class SkinDisplayAction(object):
    def __init__(self, measurement_on=False, path='../data/mr_brainixA'):
        _, _, files = next(os.walk(path))
        self.image_amount = len(files)
        reader, image_data = read_dicom_images(path)
        self.iren = None
        self.widgets = []
        self.slider = None
        self.label = None
        self.meas_widget = None
        self.colors = None
        self.skin_extractor = None
        self.skin_stripper = None
        self.skin_mapper = None
        self.skin_actor = None
        self.bone_extractor = None
        self.bone_stripper = None
        self.bone_mapper = None
        self.bone_actor = None
        self.outline_data = None
        self.outline_mapper = None
        self.outline_actor = None
        self.bw_lut = None
        self.hue_lut = None
        self.sat_lut = None
        self.sagittal_colors = None
        self.sagittal = None
        self.axial_colors = None
        self.axial = None
        self.coronal_colors = None
        self.coronal = None

        self.colors = named_colors()
        self.init_skin_tools(reader)
        self.init_bone_tools(reader)
        self.init_outline_tools(reader)
        self.init_lookup_table()
        self.init_colors(reader)

        self.bone_actor.VisibilityOff()
        self.skin_actor.GetProperty().SetOpacity(0.5)

        actors = [self.outline_actor, self.sagittal, self.axial, self.coronal, self.skin_actor, self.bone_actor]
        self.renderer = get_renderer_with_multiple_actors(actors, background=(0.8, 0.8, 0.8))

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
        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText('Translucent skin - ISO')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        self.slider = Slider(0, 1000, 500, self.change_value)
        self.widgets.append(self.slider)

    def init_skin_tools(self, reader):
        self.skin_extractor = body_extractor(reader, 500)
        self.skin_stripper = body_stripper(self.skin_extractor)
        self.skin_mapper = body_mapper(self.skin_stripper)
        self.init_skin_actor()

    def init_skin_actor(self):
        self.skin_actor = body_actor(self.skin_mapper, self.colors, 'SkinColor')
        self.skin_actor.GetProperty().SetSpecular(0.3)
        self.skin_actor.GetProperty().SetSpecularPower(20)

    def init_bone_tools(self, reader):
        self.bone_extractor = body_extractor(reader, 1150)
        self.bone_stripper = body_stripper(self.bone_extractor)
        self.bone_mapper = body_mapper(self.bone_stripper)
        self.bone_actor = body_actor(self.bone_mapper, self.colors, 'Ivory')

    def init_outline_tools(self, reader):
        self.outline_data = outline_data(reader)
        self.outline_mapper = outline_mapper(self.outline_data)
        self.outline_actor = outline_actor(self.outline_mapper, self.colors)

    def init_lookup_table(self):
        self.init_bw_lookup_table()
        self.init_hue_lookup_table()
        self.init_sat_lookup_table()

    def init_bw_lookup_table(self):
        self.bw_lut = vtk.vtkLookupTable()
        self.bw_lut.SetTableRange(0, 2000)
        self.bw_lut.SetSaturationRange(0, 0)
        self.bw_lut.SetHueRange(0, 0)
        self.bw_lut.SetValueRange(0, 1)
        self.bw_lut.Build()

    def init_hue_lookup_table(self):
        self.hue_lut = vtk.vtkLookupTable()
        self.hue_lut.SetTableRange(0, 2000)
        self.hue_lut.SetHueRange(0, 1)
        self.hue_lut.SetSaturationRange(1, 1)
        self.hue_lut.SetValueRange(1, 1)
        self.hue_lut.Build()

    def init_sat_lookup_table(self):
        self.sat_lut = vtk.vtkLookupTable()
        self.sat_lut.SetTableRange(0, 2000)
        self.sat_lut.SetHueRange(0.6, 0.6)
        self.sat_lut.SetSaturationRange(0, 1)
        self.sat_lut.SetValueRange(1, 1)
        self.sat_lut.Build()

    def init_colors(self, reader):
        self.sagittal_colors = image_actor_colors(reader, self.bw_lut)
        self.sagittal = image_actor(self.sagittal_colors, int(reader.GetWidth()/2), int(reader.GetWidth()/2), 0, reader.GetHeight(), 0, self.image_amount)
        self.axial_colors = image_actor_colors(reader, self.hue_lut)
        self.axial = image_actor(self.axial_colors, 0, reader.GetWidth(), 0, reader.GetHeight(), int(self.image_amount/2), int(self.image_amount/2))
        self.coronal_colors = image_actor_colors(reader, self.sat_lut)
        self.coronal = image_actor(self.coronal_colors, 0, reader.GetHeight(), int(reader.GetHeight()/2), int(reader.GetHeight()/2), 0, self.image_amount)

    def change_value(self, value):
        self.skin_extractor.SetValue(0, value)
        self.skin_extractor.Update()
        self.iren.GetRenderWindow().Render()

