from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.transfer_fun_render import TransferFunAction

actions = {'iso': IsoAction, 'transfer': TransferFunAction}


class SubWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(SubWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        combo = QComboBox()
        combo.addItem('')
        for name in actions.keys():
            combo.addItem(name)
        combo.currentTextChanged.connect(self.on_combobox_changed)
        self.combo = combo
        self.action = None
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        layout.addWidget(combo)
        layout.addWidget(self.vtkWidget)
        self.setLayout(layout)

        self.iren.Initialize()

    def on_combobox_changed(self, value):
        self.action = actions.get(value)()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.action.renderer.ResetCamera()
