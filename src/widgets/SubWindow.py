from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QCheckBox, QHBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.transfer_fun_render import TransferFunAction

actions = {'iso': IsoAction, 'transfer': TransferFunAction}


class SubWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(SubWindow, self).__init__(*args, **kwargs)

        combo = QComboBox()
        combo.addItem('')
        for name in actions.keys():
            combo.addItem(name)
        combo.currentTextChanged.connect(self.on_combobox_changed)
        self.combo = combo

        checkbox = QCheckBox("measurement")
        checkbox.setCheckable(False)
        checkbox.toggled.connect(self.on_checkbox_change)
        self.checkbox = checkbox

        inner_layout = QHBoxLayout()
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
        if not self.checkbox.isCheckable():
            self.checkbox.setCheckable(True)
        self.action = actions.get(value)(measurement_on=self.checkbox.isChecked())
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.action.renderer.ResetCamera()

    def on_checkbox_change(self):
        if self.checkbox.isChecked():
            self.action.meas_widget.On()
        else:
            self.action.meas_widget.Off()
