from PySide6 import QtWidgets, QtCore
import _UI_Playpause


class PlayPause(QtWidgets.QMainWindow, _UI_Playpause.Ui_PLAYPAUSE):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.b_Pause.setText('\U000023F5')
        self.b_Pause.setStyleSheet('background-color:rgb(204,255,204)')
        self.b_Pause.clicked.connect(self.button_pressed)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def button_pressed(self):
        _sender = self.sender().objectName()
        self._controller.handle_button_pressed(_sender, 'd')