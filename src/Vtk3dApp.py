import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QToolBar, QCheckBox, QPushButton, QFileDialog, \
    QApplication

from utils.vtk_utils import synchronize, unsynchronize
from widgets.SubWindow import SubWindow


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.frame = QFrame()
        self.layout = QGridLayout()
        self.subwindows = []
        self.toolBar = None
        self.init_subwindows('../data/mr_brainixA')
        self.statusbar = self.statusBar()

    def init_subwindows(self, dir_path=None):
        self.subwindows = [SubWindow(self, i + 1, path=dir_path) for i in range(4)]
        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, widget in zip(positions, self.subwindows):
            self.layout.addWidget(widget, *position)
        self.frame.setLayout(self.layout)
        self.toolBar = self.create_tool_bar()
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)

        self.setCentralWidget(self.frame)

    def create_tool_bar(self):
        self.remove_tool_bar()
        tools = QToolBar()
        tools.setMinimumWidth(250)

        button = QPushButton("&Load data")
        button.clicked.connect(self.open_file_dialog)
        tools.addWidget(button)

        checkbox = QCheckBox("Synchronize windows")
        checkbox.setMinimumHeight(30)
        checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")
        checkbox.toggled.connect(self.on_checkbox_change(checkbox))
        tools.addWidget(checkbox)

        for subwindow in self.subwindows:
            for widget in subwindow.tool_bar.widgets:
                tools.addWidget(widget)

        return tools

    def open_file_dialog(self):
        # try:
        dir_path = QFileDialog.getExistingDirectory(self, 'Select directory')
        if dir_path != '':
            self.re_init_subwindows(dir_path)
        else:
            pass
        # except:
        #     self.statusbar.showMessage("Unable to open directory. Maybe it's not a DICOM series", 3000)


    def re_init_subwindows(self, dir_path):
        for subwindow in self.subwindows:
            subwindow.close()
        self.init_subwindows(dir_path)

    def refresh_tool_bar(self):
        self.remove_tool_bar()
        self.toolBar = self.create_tool_bar()
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        for subwindow in self.subwindows:
            unsynchronize(subwindow)

    def remove_tool_bar(self):
        try:
            self.removeToolBar(self.toolBar)
        except:
            pass

    def on_checkbox_change(self, checkbox):
        def callback(_event):
            if checkbox.isChecked():
                vtk_widgets = []
                for subwindow in self.subwindows:
                    if subwindow.action is not None:
                        vtk_widgets.append(subwindow)
                print(vtk_widgets)
                for subwindow in self.subwindows:
                    synchronize(subwindow, vtk_widgets)
            else:
                for subwindow in self.subwindows:
                    unsynchronize(subwindow)

        return callback


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("VTK 3D App")
    window.show()

    sys.exit(app.exec_())
