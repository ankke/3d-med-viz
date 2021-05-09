import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.utils.callbacks import OpacityCallback
from src.utils.vtk_utils import read_dicom_images, volume_mapper, piecewise_fun, volume_actor, window_renderer, \
    add_slider, add_style, start_render


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        path = '../data/mr_brainixA'
        reader, image_data = read_dicom_images(path)

        win_width = 750
        win_center = 100

        max_value = 1
        min_value = 0
        point = 180

        mapper = volume_mapper(reader)
        piecewise = piecewise_fun(((0, 0), (point, 1), (point + 1, 1), (255, 0)))
        actor = volume_actor(mapper, piecewise)

        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)
        renderer.SetBackground((.8, .8, .8))


        self.ren = renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())