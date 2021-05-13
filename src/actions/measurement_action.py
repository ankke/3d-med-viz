import vtk

from utils.vtk_utils import read_dicom_images, add_style, vtk_actor, poly_data_mapper, contour_filter


class MeasurementAction(object):

    def __init__(self, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.contour_filter = contour_filter(image_data, 150)
        self.actor = vtk_actor(poly_data_mapper(self.contour_filter))
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)

        self.iren = None
        self.slider = None

    def init_action(self, iren):
        self.iren = iren
        self.widget = vtk.vtkDistanceWidget()
        self.widget.SetInteractor(self.iren)
        self.widget.CreateDefaultRepresentation()
        self.widget.On()

        self.representation = vtk.vtkDistanceRepresentation3D()
        self.widget.SetRepresentation(self.representation)

        add_style(self.iren)
