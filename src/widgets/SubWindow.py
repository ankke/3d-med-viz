from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.transfer_fun_render import TransferFunAction
from widgets.ToolBar import ToolBar

actions = {'iso': IsoAction, 'transfer': TransferFunAction}


class SubWindow(QWidget):
    def __init__(self, parent, name, *args, **kwargs):
        super(SubWindow, self).__init__(*args, **kwargs)
        self.parent = parent

        label_text = f'Window {name}'
        self.tool_bar = ToolBar(label_text)

        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText(label_text)

        combo = QComboBox()
        combo.addItem('')
        for name in actions.keys():
            combo.addItem(name)
        combo.currentTextChanged.connect(self.on_combobox_changed)
        self.combo = combo

        checkbox = QCheckBox("measure")
        checkbox.setCheckable(False)
        checkbox.toggled.connect(self.on_checkbox_change)
        self.checkbox = checkbox

        inner_layout = QHBoxLayout()
        inner_layout.addWidget(label)
        inner_layout.addWidget(combo)
        inner_layout.addWidget(checkbox)

        self.vtkWidget = QVTKRenderWindowInteractor()

        layout = QVBoxLayout()
        layout.addLayout(inner_layout)
        layout.addWidget(self.vtkWidget)
        self.setLayout(layout)

        self.action = None
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.iren.Initialize()

    def on_combobox_changed(self, value):
        if value is '':
            self.checkbox.setCheckable(False)
        else:
            self.checkbox.setCheckable(True)
        self.action = actions.get(value)(measurement_on=self.checkbox.isChecked())
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.refresh_tool_bar()
        self.action.renderer.ResetCamera()

    def on_checkbox_change(self):
        if self.checkbox.isChecked():
            self.action.meas_widget.On()
        else:
            self.action.meas_widget.Off()

    def refresh_tool_bar(self):
        self.tool_bar.set_up_action(self.action)
        self.parent.refresh_tool_bar()



