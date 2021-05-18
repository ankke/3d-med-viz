import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QStatusBar, QHBoxLayout, QMainWindow, QFrame, QApplication, QLabel, QGridLayout, \
    QComboBox
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.measurement_action import MeasurementAction
from actions.transfer_fun_render import TransferFunAction
from widgets.SubWindow import SubWindow


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.frame = QFrame()

        self.layout = QGridLayout()
        self.vtk_widgets = [SubWindow(), SubWindow(),
                            SubWindow(), SubWindow()]
        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, widget in zip(positions, self.vtk_widgets):
            self.layout.addWidget(widget, *position)

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

    # def create_menu(self):
    #     menu = self.menuBar().addMenu("&Menu")
    #     menu.addAction("&Iso", self.display_iso_render)
    #     menu.addAction("&Transfer fun", self.display_transfer_fun)
    #     menu.addAction("&Measurement", self.display_measurement)


    # def create_status_bar(self):
    #     status = QStatusBar()
    #     status.showMessage("")
    #     self.setStatusBar(status)

    def display_iso_render(self):
        self.action = IsoAction()
        self.restart_window_with_slider()

    def display_transfer_fun(self):
        self.action = TransferFunAction()
        self.restart_window_with_slider()

    def display_measurement(self):
        self.action = MeasurementAction()
        self.restart_window()

    def restart_window(self):
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.remove_tool_bar()
        self.action.renderer.ResetCamera()

    def restart_window_with_slider(self):
        self.restart_window()
        self.create_tool_bar(self.action.slider, self.action.label)

    def remove_tool_bar(self):
        try:
            self.removeToolBar(self.toolBar)
        except:
            pass

    def create_tool_bar(self, slider, label):
        tools = QToolBar()
        tools.setMinimumWidth(250)
        tools.addWidget(label)
        tools.addWidget(slider)
        self.addToolBar(Qt.LeftToolBarArea, tools)
        self.toolBar = tools


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("VTK 3D App")
    window.show()

    sys.exit(app.exec_())
