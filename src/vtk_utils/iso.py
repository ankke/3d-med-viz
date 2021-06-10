import vtk

from vtk_utils.transfer_fun import transfer_fun


def contour_filter(image_data, value):
    filter = vtk.vtkContourFilter()
    filter.SetInputData(image_data)
    filter.ComputeNormalsOn()
    filter.SetValue(0, value)
    return filter


def poly_data_mapper(contour_filter_, transfer_function=transfer_fun()):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(contour_filter_.GetOutputPort())
    mapper.SetLookupTable(transfer_function)
    return mapper


def vtk_actor(mapper, initial_opacity=.3):
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(initial_opacity)
    return actor
