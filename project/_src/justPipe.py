# justPipe on MVP pattern v3; 12/08/2026 All working well; need DV option added and Manual & License update

import os
import sys
from PySide6 import QtWidgets
from _control import Controller
from _model import Model
from _mainWin import MainWin
from _xView import XV
from _pView import PV
from _lView import LV
from _config import Config


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # if not QtWidgets.QApplication.instance():
    #     app = QtWidgets.QApplication(sys.argv)
    # else:
    #     app = QtWidgets.QApplication.instance()

    app.setStyle('fusion')

    screen_resolution = app.primaryScreen().size()

    mainWin = MainWin()
    xv = XV(screen_resolution)
    pv = PV(screen_resolution)
    lv = LV(screen_resolution)
    model = Model()
    config = Config()
    controller = Controller(model, mainWin, xv, pv, lv, config,
                            os.path.dirname(sys.argv[0]))

    for w in [mainWin, xv, pv, lv]:
        w.show()

    sys.exit(app.exec())