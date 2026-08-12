from PySide6 import QtWidgets
from PySide6.QtWidgets import QColorDialog
import _UI_Options

class Config(QtWidgets.QMainWindow, _UI_Options.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # set up signals
        for b in [self.b_Profile, self.b_Pipe, self.b_LeftM, self.b_RightM,
                  self.b_Vis, self.b_MADJ, self.b_MSBL,
                  self.b_Pipetracker, self.b_CurrentProf, self.b_Background]:
            b.clicked.connect(self._colorselect)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def _colorselect(self):
        _selectors = ['b_Profile', 'b_Pipe', 'b_LeftM', 'b_RightM',
                      'b_Vis', 'b_MADJ', 'b_MSBL', 'b_Pipetracker',
                      'b_CurrentProf', 'b_Background']
        _palettes = [self.w_Profile, self.w_Pipe, self.w_LeftM, self.w_RightM,
                     self.w_Vis, self.w_MADJ, self.w_MSBL, self.w_Pipetracker,
                     self.w_CurrentProf, self.w_Background]


        _sender = self.sender().objectName()
        _ix = _selectors.index(_sender)
        _color = QColorDialog.getColor()

        if _color.isValid():
            _selectedcolor = _color.getRgb()
            _palettes[_ix].setStyleSheet(f'background-color: rgba{_selectedcolor}')

            self._controller.handle_colors(_ix, _selectedcolor)




