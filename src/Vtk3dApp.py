import sys

from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QGridLayout

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

    # def remove_tool_bar(self):
    #     try:
    #         self.removeToolBar(self.toolBar)
    #     except:
    #         pass
    #
    # def create_tool_bar(self, slider, label):
    #     tools = QToolBar()
    #     tools.setMinimumWidth(250)
    #     tools.addWidget(label)
    #     tools.addWidget(slider)
    #     self.addToolBar(Qt.LeftToolBarArea, tools)
    #     self.toolBar = tools


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("VTK 3D App")
    window.show()

    sys.exit(app.exec_())
