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

        self.action = None
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        checkbox = QCheckBox("measurement")
        checkbox.setChecked(False)
        checkbox.toggled.connect(lambda: self.on_checkbox_change(checkbox))

        inner_layout = QHBoxLayout()
        inner_layout.addWidget(combo)
        inner_layout.addWidget(checkbox)

        layout = QVBoxLayout()
        layout.addLayout(inner_layout)
        layout.addWidget(self.vtkWidget)
        self.setLayout(layout)

        self.iren.Initialize()

    def on_combobox_changed(self, value):
        self.action = actions.get(value)()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.action.renderer.ResetCamera()

    def on_checkbox_change(self, box):
        if box.isChecked():
            self.action.meas_widget.On()
        else:
            self.action.meas_widget.Off()
