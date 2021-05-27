import vtk


def read_dicom_images(path):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(path)
    reader.Update()
    image_data = reader.GetOutput()
    return reader, image_data


def get_frames_num(image_data):
    return image_data.GetDimensions()[2]


def shift_scale_filter(reader, win_center, win_width):
    filter = vtk.vtkImageShiftScale()
    filter.SetOutputScalarTypeToUnsignedChar()
    filter.SetInputConnection(reader.GetOutputPort())
    filter.SetShift(-win_center + 0.5 * win_width)
    filter.SetScale(255.0 / win_width)
    filter.SetClampOverflow(True)
    return filter


def contour_filter(image_data, value):
    filter = vtk.vtkContourFilter()
    filter.SetInputData(image_data)
    filter.ComputeNormalsOn()
    filter.SetValue(0, value)
    return filter


def transfer_fun(points=((0, 1, 1, 1), (255, 0, 0, 0))):
    lut = vtk.vtkColorTransferFunction()
    for x, r, b, g in points:
        lut.AddRGBPoint(x, r, b, g)
    return lut

def piecewise_fun(point_vals):
    piecewise = vtk.vtkPiecewiseFunction()
    for point, val in point_vals:
        piecewise.AddPoint(point, val)
    return piecewise


def poly_data_mapper(contour_filter_, transfer_function=transfer_fun()):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(contour_filter_.GetOutputPort())
    mapper.SetLookupTable(transfer_function)
    return mapper


def volume_mapper(reader):
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    return mapper


def vtk_actor(mapper, initial_opacity=.3):
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(initial_opacity)
    return actor


def volume_actor(mapper, piecewise, transfer_function=transfer_fun()):
    actor = vtk.vtkVolume()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(transfer_function)
    actor.GetProperty().SetScalarOpacity(piecewise)
    return actor


def get_renderer(actor, background):
    renderer_ = vtk.vtkRenderer()
    renderer_.AddActor(actor)
    renderer_.SetBackground(background)
    return renderer_

def get_renderer_with_multiple_actors(actor_list, background):
    renderer_ = vtk.vtkRenderer()
    for actor in actor_list:
        renderer_.AddActor(actor)
    renderer_.SetBackground(background)
    return renderer_

def window_renderer(renderer_, height, width):
    win_renderer = vtk.vtkRenderWindow()
    win_renderer.AddRenderer(renderer_)
    win_renderer.SetSize(height, width)
    return win_renderer


def get_interactor(win_renderer):
    inter = vtk.vtkRenderWindowInteractor()
    inter.SetRenderWindow(win_renderer)
    return inter


def add_slider(point_1, point_2, min_val, max_val, title, inter, callback, event='EndInteractionEvent'):
    slider_repr = vtk.vtkSliderRepresentation2D()
    slider_repr.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider_repr.GetPoint1Coordinate().SetValue(point_1[0], point_1[1])
    slider_repr.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider_repr.GetPoint2Coordinate().SetValue(point_2[0], point_2[1])
    slider_repr.SetMinimumValue(min_val)
    slider_repr.SetMaximumValue(max_val)
    slider_repr.SetValue((min_val + max_val) / 2)
    slider_repr.SetTitleText(title)

    slider_ = vtk.vtkSliderWidget()
    slider_.SetInteractor(inter)
    slider_.SetRepresentation(slider_repr)
    slider_.SetAnimationModeToAnimate()
    slider_.EnabledOn()
    slider_.AddObserver(event, callback)


def add_style(inter):
    style = vtk.vtkInteractorStyleTrackballCamera()
    inter.SetInteractorStyle(style)


def start_render(inter):
    inter.Initialize()
    inter.Start()


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
