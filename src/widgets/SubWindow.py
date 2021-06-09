from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from actions.iso_render import IsoAction
from actions.skin_cover_render import SkinCoverAction
from actions.transfer_fun_render import TransferFunAction
from actions.skin_display_render import SkinDisplayAction
from actions.transfer_mult_point import TransferFunMultAction
from widgets.ToolBarWidgets import ToolBarWidgets

actions = {'iso': IsoAction,
           'transfer': TransferFunMultAction,
           'transfer one point': TransferFunAction,
           'translucent skin': SkinDisplayAction,
           'skin': SkinCoverAction}


class SubWindow(QWidget):
    def __init__(self, parent, name, path=None, *args, **kwargs):
        super(SubWindow, self).__init__(*args, **kwargs)
        self.parent = parent
        self.path = path

        label_text = f'Window {name}'
        self.tool_bar = ToolBarWidgets(label_text)

        label = QLabel()
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setText(label_text)

        combo = QComboBox()
        combo.addItem('')
        if path is None:
            combo.setEnabled(False)
        for name in actions.keys():
            combo.addItem(name)
        combo.currentTextChanged.connect(self.on_combobox_change)
        self.combo = combo

        checkbox = QCheckBox("measure")
        checkbox.setCheckable(False)
        checkbox.toggled.connect(self.on_checkbox_change)
        self.checkbox = checkbox

        inner_layout = QHBoxLayout()
        inner_layout.addWidget(label)
        inner_layout.addWidget(combo)
        inner_layout.addWidget(checkbox)

        self.vtk_widget = QVTKRenderWindowInteractor()

        layout = QVBoxLayout()
        layout.addLayout(inner_layout)
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

        self.action = None
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.tag = None
        self.iren.Initialize()

    def on_combobox_change(self, value):
        if value is '':
            self.checkbox.setCheckable(False)
        else:
            self.checkbox.setCheckable(True)

        self.action = actions.get(value)(measurement_on=self.checkbox.isChecked(), path=self.path)
        self.vtk_widget.GetRenderWindow().AddRenderer(self.action.renderer)
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.action.init_action(self.iren)
        self.action.renderer.ResetCamera()

        self.refresh_tool_bar()

    def on_checkbox_change(self):
        if self.checkbox.isChecked():
            self.action.meas_widget.On()
        else:
            self.action.meas_widget.Off()

    def refresh_tool_bar(self):
        self.tool_bar.set_up_action(self.action)
        self.parent.refresh_tool_bar()
