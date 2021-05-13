import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QToolBar, QStatusBar
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.measurement_2_action import MeasurementAction2
from actions.measurement_action import MeasurementAction
from actions.transfer_fun_render import TransferFunAction


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.create_menu()
        self.action = None
        self.display_measurement()

        self.action.renderer.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.iren.Initialize()

    def create_menu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Iso", self.display_iso_render)
        menu.addAction("&Transfer fun", self.display_transfer_fun)
        menu.addAction("&Measurement", self.display_measurement)
        menu.addAction("&Measurement 2", self.display_measurement_2)


    def create_status_bar(self):
        status = QStatusBar()
        status.showMessage("")
        self.setStatusBar(status)

    def display_iso_render(self):
        self.action = IsoAction()
        self.restart_window_with_slider()

    def display_transfer_fun(self):
        self.action = TransferFunAction()
        self.restart_window_with_slider()

    def display_measurement(self):
        self.action = MeasurementAction()
        self.restart_window()

    def display_measurement_2(self):
        self.action = MeasurementAction2()
        self.restart_window()

    def restart_window(self):
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.remove_tool_bar()
        self.action.renderer.ResetCamera()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

    def restart_window_with_slider(self):
        self.restart_window()
        self.slider = self.action.slider
        self.create_tool_bar(self.slider)

    def remove_tool_bar(self):
        try:
            self.removeToolBar(self.toolBar)
        except:
            pass

    def create_tool_bar(self, slider):
        tools = QToolBar()
        tools.addWidget(slider)
        self.addToolBar(tools)
        self.toolBar = tools


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("VTK 3D App")
    window.show()

    sys.exit(app.exec_())
