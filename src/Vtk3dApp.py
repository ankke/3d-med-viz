import sys

import vtk
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QStatusBar, QSlider
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.utils import vtk_utils
from src.utils.callbacks import ContourCallback
from src.utils.vtk_utils import contour_filter, read_dicom_images, volume_mapper, piecewise_fun, volume_actor, \
    transfer_fun, \
    shift_scale_filter, vtk_actor, poly_data_mapper


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.createMenu()
        # self.createStatusBar()

        self.displayIsoRender()

        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.iren.Initialize()

    def createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction("&Iso", self.displayIsoRender)
        self.menu.addAction("&Transfer fun", self.displayTransferFun)

    def createToolBar(self, slider):
        try:
            self.removeToolBar(self.toolBar)
        except:
            pass

        tools = QToolBar()
        tools.addWidget(slider)
        self.addToolBar(tools)
        self.toolBar = tools

    def createStatusBar(self):
        status = QStatusBar()
        status.showMessage("")
        self.setStatusBar(status)

    def displayIsoRender(self):
        path = '../data/mr_brainixA'
        reader, image_data = read_dicom_images(path)

        win_width = 750
        win_center = 100

        max_value = 1
        min_value = 0
        point = 180

        self.contour_filter = vtk_utils.contour_filter(image_data, 150)
        actor = vtk_actor(poly_data_mapper(self.contour_filter))

        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)
        renderer.SetBackground((.8, .8, .8))

        self.ren = renderer
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(128)
        self.slider.valueChanged.connect(lambda x: self.changeIsoValue())

        self.createToolBar(self.slider)

    def changeIsoValue(self):
        value = self.slider.value()
        self.contour_filter.SetValue(0, value)
        self.iren.GetRenderWindow().Render()

    def displayTransferFun(self):
        path = '../data/mr_brainixA'
        reader, image_data = read_dicom_images(path)

        nFrames = image_data.GetDimensions()[2]
        winWidth = 750
        winCenter = 100

        # --- filter: apply winWidth and winCenter
        shiftScaleFilter = shift_scale_filter(reader, winCenter, winWidth)

        self.point = 180

        mapper = volume_mapper(reader)

        self.lut = transfer_fun()

        self.piecewise = piecewise_fun(((0, 0), (self.point, 1), (self.point + 1, 1), (255, 0)))

        actor = volume_actor(mapper, self.piecewise, self.lut)

        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(actor)
        self.ren.SetBackground(.8, .8, .8)
        self.ren.ResetCamera()

        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(lambda x: self.changeTransferFun())

        self.createToolBar(self.slider)


    def changeTransferFun(self):
        value = self.slider.value()
        self.changePiecewise(value)
        self.iren.GetRenderWindow().Render()

    def changePiecewise(self, value):
        self.piecewise.RemoveAllPoints()
        self.piecewise.AddPoint(0, 0)
        self.piecewise.AddPoint(self.point, value/100)
        self.piecewise.AddPoint(self.point + 1, value/100)
        self.piecewise.AddPoint(255, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("VTK 3D App")
    window.show()

    sys.exit(app.exec_())
