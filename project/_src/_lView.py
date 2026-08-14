from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIntValidator, QDoubleValidator
import pyqtgraph as pg
import _UI_Lview


class LV(QtWidgets.QMainWindow, _UI_Lview.Ui_LVIEW):
    def __init__(self, screen_resolution):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.lview.setMenuEnabled(False)
        # set form
        self.move(544, int(screen_resolution.height() / 1.9))
        self.resize(int(screen_resolution.width() - 544), int(screen_resolution.height() / 3))
        # set flags
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlag(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.vb_lview = self.lview.plotItem.vb              # for correct mouse tracking
        self.lview.viewport().installEventFilter(self)      # eventFilter for tracking mouse wheel scroll

        # set variables
        self.aspect_change_flag = False                     # True if 'Ctrl' key held down / False if released
        # lock scale 1:1 / determine aspect
        self.aspect = 1
        self.ch_Aspect.setChecked(True)
        self.lview.setAspectLocked(True, 1)

        # set up appearance
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_Interpolate.setText('I\u02E3\u02B8\u1DBB')
        self.b_Interpolate.setToolTip('Interpolate TOP 3D (I)')
        self.b_Interpolate.setToolTipDuration(2000)

        self.l_scale.setStyleSheet('color: red')
        self.l_scale.setText(f'SCALE 1:{1 / self.aspect:.2f}')
        self.b_snap_v.setText('\u21F2\u1DBB')
        self.b_snap_v.setToolTip('Snap TOP Z to pipetracker')
        self.b_snap_v.setToolTipDuration(2000)

        # # connecting signals
        self.lview.scene().sigMouseMoved.connect(self.mouse_moved)
        self.lview.scene().sigMouseClicked.connect(self.mouse_pressed)
        self.ch_Aspect.stateChanged.connect(self.val_changed)
        self.ch_Time_Chn.stateChanged.connect(self.val_changed)
        self.b_POI.clicked.connect(self.button_pressed)
        self.b_Interpolate.clicked.connect(self.button_pressed)
        self.b_snap_v.clicked.connect(self.val_changed)
        self.ch_ShowTOP.stateChanged.connect(self.val_changed)
        self.ch_ShowFlags.stateChanged.connect(self.val_changed)
        self.ch_ShowPT.stateChanged.connect(self.val_changed)

        # adding empty data graphs to plot parent_box
        self.l_parent_box = pg.PlotDataItem()
        self.lview.addItem(self.l_parent_box)
        # current position
        self.here = pg.PlotDataItem([], [],
                                    symbol='x', symbolSize=15)
        # pipe top visited/from_pipetracker
        self.visited_top = pg.PlotDataItem([], [],
                                           symbol='o', symbolSize=3)
        self.visited_bot = pg.PlotDataItem([], [],
                                           symbol=None)
        self.from_pt = pg.PlotDataItem([], [],
                                       symbol=None)
        # levels
        self.madj = pg.PlotDataItem([], [],
                                    symbol=None)
        self.msbl = pg.PlotDataItem([], [],
                                    symbol=None)
        # POI
        self.POI = pg.PlotDataItem([], [],
                                   pen=None, symbol='x', symbolSize=20, symbolBrush='red')
        # pipetracker
        self.pt_acc = pg.PlotDataItem([], [],
                                      symbol='o', symbolSize=2)
        self.pt_selector = pg.PlotCurveItem([], [], width=2)

        # selected chunk
        self.chunk_point = pg.PlotDataItem([], [],
                                           pen=pg.mkPen('b', width=1),
                                           symbol='o', symbolSize=10, symbolBrush='yellow')
        self.chunk = pg.PlotDataItem([], [],
                                     pen=pg.mkPen('yellow', width=5), symbol=None)

        for item in [self.here,
                     self.visited_top, self.visited_bot, self.from_pt,
                     self.madj, self.msbl,
                     self.POI,
                     self.pt_acc, self.pt_selector,
                     self.chunk_point, self.chunk]:
            item.setParentItem(self.l_parent_box)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        _fName = e.mimeData().text().strip().replace('file:///', '')
        self._controller.handle_load_data(_fName)


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e, 'l')


    def keyReleaseEvent(self, e):
        self._controller.handle_key_pressed(e, 'l')


    def eventFilter(self, source, e):
        # set event filter for changing Lview aspect
        if e.type() == QtCore.QEvent.Wheel and self.aspect_change_flag:
            # xRange; yRange and v centre before wheel scroll
            _initial_h_range =self.lview.viewRange()[0]

            if e.angleDelta().y() > 0:
                self.aspect *= 1.25
            else:
                self.aspect /= 1.25

            self.lview.getViewBox().setAspectLocked(True, ratio=self.aspect)
            self.lview.setXRange(_initial_h_range[0], _initial_h_range[1], padding=0)

            self.l_scale.setText(f'SCALE 1:{1 / self.aspect:.2f}')

        return False


    def mouse_moved(self, e):
        _cursor = self.vb_lview.mapSceneToView(e)
        self._controller.handle_mouse_moved(e, _cursor, 'l')


    def mouse_pressed(self, e):
        self._controller.handle_mouse_pressed(e, 'l')


    def val_changed(self):
        _sender = self.sender().objectName()
        self._controller.handle_val_changed(_sender)


    def button_pressed(self):
        _sender = self.sender().objectName()
        self._controller.handle_button_pressed(_sender, 'l')