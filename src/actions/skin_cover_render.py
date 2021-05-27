import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel

from utils.vtk_utils import read_dicom_images, add_style, get_renderer_with_multiple_actors


class SkinCoverAction(object):
    def __init__(self, measurement_on=False, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.widgets = []
        self.colors = vtk.vtkNamedColors()

        self.colors.SetColor('SkinColor', [240, 184, 160, 255])
        self.colors.SetColor('BackfaceColor', [255, 229, 200, 255])
        self.colors.SetColor('BkgColor', [51, 77, 102, 255])

        self.init_skin_extractor(reader)
        self.init_skin_mapper()
        self.init_skin_actor()
        self.init_outline_data(reader)
        self.init_outline_map()
        self.init_outline_actor()
        actors = [self.outline_actor, self.skin_actor]
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
        label.setText('Skin')
        label.setMinimumHeight(30)
        self.widgets.append(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(1000)
        slider.setValue(500)
        slider.setMinimumHeight(40)
        slider.sliderReleased.connect(self.change_value)
        self.slider = slider
        self.widgets.append(slider)

    def init_skin_extractor(self, reader):
        try:
            self.skin_extractor = vtk.vtkFlyingEdges3D()
        except AttributeError:
            self.skin_extractor = vtk.vtkMarchingCubes()

        self.skin_extractor.SetInputConnection(reader.GetOutputPort())
        self.skin_extractor.SetValue(0, 500)

    def init_skin_mapper(self):
        self.skin_mapper = vtk.vtkPolyDataMapper()
        self.skin_mapper.SetInputConnection(self.skin_extractor.GetOutputPort())
        self.skin_mapper.ScalarVisibilityOff()


    def init_skin_actor(self):
        self.skin_actor = vtk.vtkActor()
        self.skin_actor.SetMapper(self.skin_mapper)
        self.skin_actor.GetProperty().SetDiffuseColor(self.colors.GetColor3d('SkinColor'))
        back_prop = vtk.vtkProperty()
        back_prop.SetDiffuseColor(self.colors.GetColor3d('BackfaceColor'))
        self.skin_actor.SetBackfaceProperty(back_prop)

    def init_outline_data(self, reader):
        self.outline_data = vtk.vtkOutlineFilter()
        self.outline_data.SetInputConnection(reader.GetOutputPort())

    def init_outline_map(self):
        self.map_outline = vtk.vtkPolyDataMapper()
        self.map_outline.SetInputConnection(self.outline_data.GetOutputPort())

    def init_outline_actor(self):
        self.outline_actor = vtk.vtkActor()
        self.outline_actor.SetMapper(self.map_outline)
        self.outline_actor.GetProperty().SetColor(self.colors.GetColor3d('Black'))

    def change_value(self):
        value = self.slider.value()
        self.skin_extractor.SetValue(0, value)
        self.skin_extractor.Update()

