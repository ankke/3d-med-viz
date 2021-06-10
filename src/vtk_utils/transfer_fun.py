import vtk


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


def volume_mapper(reader):
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    return mapper


def volume_actor(mapper, piecewise, transfer_function=transfer_fun()):
    actor = vtk.vtkVolume()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(transfer_function)
    actor.GetProperty().SetScalarOpacity(piecewise)
    return actor
