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
        self.map_outline = None
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

        self.init_named_colors()
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

        self.slider = Slider(0, 800, 400, self.change_value)
        self.widgets.append(self.slider)

    def init_skin_tools(self, reader):
        self.init_skin_extractor(reader)
        self.init_skin_stripper()
        self.init_skin_mapper()
        self.init_skin_actor()

    def init_named_colors(self):
        self.colors = vtk.vtkNamedColors()
        self.colors.SetColor('SkinColor', [240, 184, 160, 255])
        self.colors.SetColor('BkgColor', [51, 77, 102, 255])

    def init_skin_extractor(self, reader):
        try:
            self.skin_extractor = vtk.vtkFlyingEdges3D()
        except AttributeError:
            self.skin_extractor = vtk.vtkMarchingCubes()

        self.skin_extractor.SetInputConnection(reader.GetOutputPort())
        self.skin_extractor.SetValue(0, 1000)
        self.skin_extractor.Update()

    def init_skin_stripper(self):
        self.skin_stripper = vtk.vtkStripper()
        self.skin_stripper.SetInputConnection(self.skin_extractor.GetOutputPort())
        self.skin_stripper.Update()

    def init_skin_mapper(self):
        self.skin_mapper = vtk.vtkPolyDataMapper()
        self.skin_mapper.SetInputConnection(self.skin_stripper.GetOutputPort())
        self.skin_mapper.ScalarVisibilityOff()

    def init_skin_actor(self):
        self.skin_actor = vtk.vtkActor()
        self.skin_actor.SetMapper(self.skin_mapper)
        self.skin_actor.GetProperty().SetDiffuseColor(self.colors.GetColor3d('SkinColor'))
        self.skin_actor.GetProperty().SetSpecular(0.3)
        self.skin_actor.GetProperty().SetSpecularPower(20)

    def init_bone_tools(self, reader):
        self.init_bone_extractor(reader)
        self.init_bone_stripper()
        self.init_bone_mapper()
        self.init_bone_actor()

    def init_bone_extractor(self, reader):
        try:
            self.bone_extractor = vtk.vtkFlyingEdges3D()
        except AttributeError:
            self.bone_extractor = vtk.vtkMarchingCubes()

        self.bone_extractor.SetInputConnection(reader.GetOutputPort())
        self.bone_extractor.SetValue(0, 1150)

    def init_bone_stripper(self):
        self.bone_stripper = vtk.vtkStripper()
        self.bone_stripper.SetInputConnection(self.bone_extractor.GetOutputPort())

    def init_bone_mapper(self):
        self.bone_mapper = vtk.vtkPolyDataMapper()
        self.bone_mapper.SetInputConnection(self.bone_stripper.GetOutputPort())
        self.bone_mapper.ScalarVisibilityOff()

    def init_bone_actor(self):
        self.bone_actor = vtk.vtkActor()
        self.bone_actor.SetMapper(self.bone_mapper)
        self.bone_actor.GetProperty().SetDiffuseColor(self.colors.GetColor3d('Ivory'))

    def init_outline_tools(self, reader):
        self.init_outline_data(reader)
        self.init_outline_map()
        self.init_outline_actor()

    def init_outline_data(self, reader):
        self.outline_data = vtk.vtkOutlineFilter()
        self.outline_data.SetInputConnection(reader.GetOutputPort())
        self.outline_data.Update()

    def init_outline_map(self):
        self.map_outline = vtk.vtkPolyDataMapper()
        self.map_outline.SetInputConnection(self.outline_data.GetOutputPort())

    def init_outline_actor(self):
        self.outline_actor = vtk.vtkActor()
        self.outline_actor.SetMapper(self.map_outline)
        self.outline_actor.GetProperty().SetColor(self.colors.GetColor3d('Black'))

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
        self.init_sagittal_colors(reader)
        self.init_sagittal(reader)
        self.init_axial_colors(reader)
        self.init_axial(reader)
        self.init_coronal_colors(reader)
        self.init_coronal(reader)

    def init_sagittal_colors(self, reader):
        self.sagittal_colors = vtk.vtkImageMapToColors()
        self.sagittal_colors.SetInputConnection(reader.GetOutputPort())
        self.sagittal_colors.SetLookupTable(self.bw_lut)
        self.sagittal_colors.Update()

    #Sagittal, mają być w połowie szerokości - empirycznie testowane
    def init_sagittal(self, reader):
        self.sagittal = vtk.vtkImageActor()
        self.sagittal.GetMapper().SetInputConnection(self.sagittal_colors.GetOutputPort())
        self.sagittal.SetDisplayExtent(int(reader.GetWidth()/2), int(reader.GetWidth()/2), 0, reader.GetHeight(), 0, self.image_amount)
        self.sagittal.ForceOpaqueOn()

    def init_axial_colors(self, reader):
        self.axial_colors = vtk.vtkImageMapToColors()
        self.axial_colors.SetInputConnection(reader.GetOutputPort())
        self.axial_colors.SetLookupTable(self.hue_lut)
        self.axial_colors.Update()

    def init_axial(self, reader):
        self.axial = vtk.vtkImageActor()
        self.axial.GetMapper().SetInputConnection(self.axial_colors.GetOutputPort())
        self.axial.SetDisplayExtent(0, reader.GetWidth(), 0, reader.GetHeight(), int(self.image_amount/2), int(self.image_amount/2))
        self.axial.ForceOpaqueOn()

    def init_coronal_colors(self, reader):
        self.coronal_colors = vtk.vtkImageMapToColors()
        self.coronal_colors.SetInputConnection(reader.GetOutputPort())
        self.coronal_colors.SetLookupTable(self.sat_lut)
        self.coronal_colors.Update()

    #Coronal to białe, mają być w połowie wysokości - empirycznie testowane
    def init_coronal(self, reader):
        self.coronal = vtk.vtkImageActor()
        self.coronal.GetMapper().SetInputConnection(self.coronal_colors.GetOutputPort())
        self.coronal.SetDisplayExtent(0, reader.GetHeight(), int(reader.GetHeight()/2), int(reader.GetHeight()/2), 0, self.image_amount)
        self.coronal.ForceOpaqueOn()

    def change_value(self, value):
        self.skin_extractor.SetValue(0, value)
        self.skin_extractor.Update()
        self.iren.GetRenderWindow().Render()

