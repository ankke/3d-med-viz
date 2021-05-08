import vtk

# --- source: read data
dir = '../data/mr_brainixA'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir)
reader.Update()
imageData = reader.GetOutput()

# print(imageData.GetScalarRange())
# print(imageData.GetDimensions())
# print(imageData)

nFrames = imageData.GetDimensions()[2]
winWidth = 750
winCenter = 100

# --- filter: apply winWidth and winCenter
shiftScaleFilter = vtk.vtkImageShiftScale()
shiftScaleFilter.SetOutputScalarTypeToUnsignedChar()            # output type
shiftScaleFilter.SetInputConnection(reader.GetOutputPort())     # input connection
shiftScaleFilter.SetShift(-winCenter  + 0.5 * winWidth)
shiftScaleFilter.SetScale(255.0 / winWidth)
shiftScaleFilter.SetClampOverflow(True)

max_val = 1
min_val = 0
point = 180

# --- mapper
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(reader.GetOutputPort())

lut = vtk.vtkColorTransferFunction()
lut.AddRGBPoint(0, 1, 1, 1)
lut.AddRGBPoint(255, 0, 0, 0)

piecewise = vtk.vtkPiecewiseFunction()
piecewise.AddPoint(0, 0)
piecewise.AddPoint(point, 1)
piecewise.AddPoint(point + 1, 1)
piecewise.AddPoint(255, 0)

actor = vtk.vtkVolume()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(lut)
actor.GetProperty().SetScalarOpacity(piecewise)

print(actor.GetProperty())

# --- renderer
ren1 = vtk.vtkRenderer()
ren1.AddActor(actor)
ren1.SetBackground(.8, .8, .8)

# --- window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800, 600)

# --- interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# --- slider to change frame: callback class, sliderRepresentation, slider
class FrameCallback(object):
    def __init__(self, actor, renWin):
        self.renWin = renWin
        self.actor = actor
    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        piecewise.RemoveAllPoints()
        piecewise.AddPoint(0, 0)
        piecewise.AddPoint(point, value)
        piecewise.AddPoint(point + 1, value)
        piecewise.AddPoint(255, 0)
        self.renWin.Render()

sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(.1, .1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(.9, .1)
sliderRep.SetMinimumValue(min_val)
sliderRep.SetMaximumValue(max_val)
sliderRep.SetValue((min_val + max_val) / 2)
sliderRep.SetTitleText("transfer function")

slider = vtk.vtkSliderWidget()
slider.SetInteractor(iren)
slider.SetRepresentation(sliderRep)
slider.SetAnimationModeToAnimate()
slider.EnabledOn()
slider.AddObserver('EndInteractionEvent', FrameCallback(actor, renWin))

# --- run
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
