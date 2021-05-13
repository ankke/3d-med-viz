import vtk

from utils.vtk_utils import read_dicom_images, add_style, vtk_actor, poly_data_mapper, contour_filter


class MeasurementAction2(object):

    def __init__(self, path='../data/mr_brainixA'):
        reader, image_data = read_dicom_images(path)

        self.contour_filter = contour_filter(image_data, 150)
        self.actor = vtk_actor(poly_data_mapper(self.contour_filter))
        self.renderer = vtk.vtkRenderer()
        self.win_renderer = vtk.vtkRenderWindow()
        self.win_renderer.AddRenderer(self.renderer)
        self.renderer.AddActor(self.actor)

        self.iren = None

    def init_action(self, iren):
        self.iren = iren
        add_style(self.iren)

        self.distanceRep = vtk.vtkDistanceRepresentation3D()
        self.distanceRep.SetLabelFormat("%-#6.3g mm")

        self.distanceWidget = vtk.vtkDistanceWidget()
        self.distanceWidget.SetInteractor(self.iren)
        self.distanceWidget.SetWidgetStateToManipulate()
        self.distanceWidget.CreateDefaultRepresentation()
        self.distanceWidget.SetRepresentation(self.distanceRep)
        self.distanceWidget.SetEnabled(0)

        self.distanceWidget.AddObserver("StartInteractionEvent", self.dwStartInteraction)
        self.distanceWidget.AddObserver("InteractionEvent", self.dwUpdateMeasurement)
        self.distanceWidget.AddObserver("EndInteractionEvent", self.dwEndInteraction)

        self.distanceText = vtk.vtkTextActor()
        self.distanceText.SetDisplayPosition(900, 10)
        self.distanceText.SetInput("distance = ")

        self.distanceWidget.SetWidgetStateToManipulate()
        self.distanceWidget.EnabledOn()
        self.distanceWidget.ProcessEventsOn()
        self.distanceWidget.SetEnabled(1)

    def dwStartInteraction(self, obj, event):
        self.win_renderer.SetDesiredUpdateRate(10)

    def dwEndInteraction(self, obj, event):
        self.distanceText.SetInput("distance = %-#6.3g mm" % obj.GetDistanceRepresentation().GetDistance())
        self.win_renderer.SetDesiredUpdateRate(0.001)

    def dwUpdateMeasurement(self, obj, event):
        self.distanceText.SetInput("distance = %-#6.3g mm" % obj.GetDistanceRepresentation().GetDistance())


