import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QFileDialog, QApplication

from vtk_utils.sync import synchronize, unsynchronize
from widgets.SubWindow import SubWindow
from widgets.ToolBar import LeftToolbar


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.frame = QFrame()
        self.layout = QGridLayout()
        self.subwindows = []
        self.toolBar = None
        self.windows_num = 4
        self.dir_path = None
        self.init_subwindows()
        self.create_tool_bar()
        self.statusbar = self.statusBar()
        self.showMaximized()

    def init_subwindows(self):
        self.subwindows = [SubWindow(self, i + 1, path=self.dir_path) for i in range(self.windows_num)]
        cols_num = self.windows_num // 2 if self.windows_num > 1 else 1
        positions = [(i, j) for i in range(2) for j in range(cols_num)]
        for position, widget in zip(positions, self.subwindows):
            self.layout.addWidget(widget, *position)

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

    def create_tool_bar(self):
        self.toolBar = LeftToolbar(self.windows_num, self.open_file_dialog, self.on_combobox_change,
                                   self.on_checkbox_change, self.subwindows)
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)

    def open_file_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select directory')
        if dir_path != '':
            self.dir_path = dir_path
            self.re_init_subwindows()
        else:
            pass

    def re_init_subwindows(self):
        for subwindow in self.subwindows:
            subwindow.close()
        self.init_subwindows()
        self.refresh_tool_bar()

    def on_combobox_change(self, value):
        self.windows_num = int(value)
        self.re_init_subwindows()

    def refresh_tool_bar(self):
        self.remove_tool_bar()
        self.create_tool_bar()
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
