def synchronize(vtkWidget, vtk_widgets):
    vtkWidget.tag = vtkWidget.vtk_widget.AddObserver("InteractionEvent",
                                                     lambda obj, event: sync_render(obj, event, vtk_widgets))


def unsynchronize(vtkWidget):
    vtkWidget.vtk_widget.RemoveObserver(vtkWidget.tag)


def sync_render(obj, _event, irens):
    camera = obj.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()
    for i in irens:
        i.action.renderer.SetActiveCamera(camera)
    for i in irens:
        i.vtk_widget.Render()