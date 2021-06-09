import vtk


def get_renderer_with_multiple_actors(actor_list, background):
    renderer_ = vtk.vtkRenderer()
    for actor in actor_list:
        renderer_.AddActor(actor)
    renderer_.SetBackground(background)
    return renderer_


def named_colors():
    colors = vtk.vtkNamedColors()
    colors.SetColor('SkinColor', [240, 184, 160, 255])
    colors.SetColor('BackfaceColor', [255, 229, 200, 255])
    colors.SetColor('BkgColor', [51, 77, 102, 255])
    return colors


def body_extractor(reader, init_value):
    try:
        skin_extractor = vtk.vtkFlyingEdges3D()
    except AttributeError:
        skin_extractor = vtk.vtkMarchingCubes()

    skin_extractor.SetInputConnection(reader.GetOutputPort())
    skin_extractor.SetValue(0, init_value)
    skin_extractor.Update()
    return skin_extractor


def body_stripper(extractor):
    body_stripper = vtk.vtkStripper()
    body_stripper.SetInputConnection(extractor.GetOutputPort())
    body_stripper.Update()
    return body_stripper


def body_mapper(tool):
    skin_mapper = vtk.vtkPolyDataMapper()
    skin_mapper.SetInputConnection(tool.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()
    return skin_mapper


def body_actor(mapper, colors, color3d):
    skin_actor = vtk.vtkActor()
    skin_actor.SetMapper(mapper)
    skin_actor.GetProperty().SetDiffuseColor(colors.GetColor3d(color3d))
    return skin_actor


def image_actor_colors(reader, lookup_table):
    image_actor_colors = vtk.vtkImageMapToColors()
    image_actor_colors.SetInputConnection(reader.GetOutputPort())
    image_actor_colors.SetLookupTable(lookup_table)
    image_actor_colors.Update()
    return image_actor_colors


def image_actor(input_colors, x_min, x_max, y_min, y_max, z_min, z_max):
    actor = vtk.vtkImageActor()
    actor.GetMapper().SetInputConnection(input_colors.GetOutputPort())
    actor.SetDisplayExtent(x_min, x_max, y_min, y_max, z_min, z_max)
    actor.ForceOpaqueOn()
    return actor


def outline_data(reader):
    outline_data = vtk.vtkOutlineFilter()
    outline_data.SetInputConnection(reader.GetOutputPort())
    outline_data.Update()
    return outline_data


def outline_mapper(outline_data):
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_data.GetOutputPort())
    return outline_mapper


def outline_actor(outline_mapper, outline_colors):
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(outline_colors.GetColor3d('Black'))
    return outline_actor
