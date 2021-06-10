import vtk


def read_dicom_images(path):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(path)
    reader.Update()
    image_data = reader.GetOutput()
    return reader, image_data


def get_renderer(actor, background):
    renderer_ = vtk.vtkRenderer()
    renderer_.AddActor(actor)
    renderer_.SetBackground(background)
    return renderer_


def add_style(inter):
    style = vtk.vtkInteractorStyleTrackballCamera()
    inter.SetInteractorStyle(style)


def init_measurement(measurement_on, iren):
    meas_widget = vtk.vtkDistanceWidget()
    meas_widget.SetInteractor(iren)
    meas_widget.CreateDefaultRepresentation()
    meas_widget.SetRepresentation(vtk.vtkDistanceRepresentation3D())
    if measurement_on:
        meas_widget.On()
    return meas_widget