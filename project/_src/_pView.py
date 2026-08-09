from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIntValidator, QDoubleValidator
import pyqtgraph as pg
import _UI_Pview

class PV(QtWidgets.QMainWindow, _UI_Pview.Ui_PVIEW):
    def __init__(self, screen_resolution):
        super().__init__()
        self._screen_resolution = screen_resolution
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        # set form
        self.move(int(544 + (screen_resolution.width() - 544) / 2), 0)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlag(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.resize(int((screen_resolution.width() - 544) / 2), int(screen_resolution.height() / 2))
        self.pview.ui.roiBtn.hide()
        self.pview.ui.menuBtn.hide()
        self.pview.ui.roiPlot.hide()
        self.pview.ui.histogram.hide()
        self.pview.getView().setMenuEnabled(False)
        self.pview.getView().invertX(False)
        self.pview.getView().invertY(False)

        # set up le validators
        self.t_PtGap.setValidator(QDoubleValidator())
        self.t_EdSpot.setValidator(QDoubleValidator())
        self.t_smW.setValidator(QIntValidator())

        # set up appearance
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_Interpolate.setToolTip('Interpolate TOP 3D (I)')
        self.b_Interpolate.setToolTipDuration(2000)
        self.b_Interpolate.setText('I\u02E3\u02B8\u1DBB')
        self.b_EditMode.setToolTip('Change edit mode Pipe/Pipetracker')
        self.b_EditMode.setToolTipDuration(2000)
        self.b_EditMode.setText('\u3030')
        self.b_smoothPT_p.setToolTip('Smooth pipetracker XY')
        self.b_smoothPT_p.setToolTipDuration(2000)
        self.b_smoothPT_p.setText('S\u02E3\u02B8')
        self.b_snap_h.setText('\u21F2\u02E3\u02B8')
        self.b_snap_h.setToolTip('Snap TOP XY to pipetracker')
        self.b_snap_h.setToolTipDuration(2000)

        # # connecting signals
        self.pview.scene.sigMouseMoved.connect(self.mouse_moved)
        self.pview.scene.sigMouseClicked.connect(self.mouse_pressed)
        self.b_POI.clicked.connect(self.button_pressed)
        self.b_Interpolate.clicked.connect(self.button_pressed)
        self.b_EditMode.clicked.connect(self.val_changed)
        self.sp_Pt_Weed.valueChanged.connect(self.val_changed)
        self.b_smoothPT_p.clicked.connect(self.val_changed)
        self.b_snap_h.clicked.connect(self.val_changed)
        self.t_EdSpot.textEdited.connect(self.val_changed)
        self.t_smW.textEdited.connect(self.val_changed)
        self.ch_ShowPT.stateChanged.connect(self.val_changed)
        self.rb_RejectPT.clicked.connect(self.val_changed)
        self.rb_AcceptPT.clicked.connect(self.val_changed)

        # adding empty data graphs to plot parent_box
        self.p_parent_box = pg.PlotDataItem()
        self.pview.addItem(self.p_parent_box)
        # current position
        self.here = pg.PlotDataItem([], [],
                                    symbol='x', symbolSize=15)
        # pipe top visited/notvisited
        self.notvisited = pg.PlotDataItem([], [],
                                          pen=None, symbol='o', symbolSize=5)
        self.visited = pg.PlotDataItem([], [],
                                       symbol=None)
        # flags
        self.li = pg.PlotDataItem([], [],
                                  symbol='o', symbolSize=2)
        self.ri = pg.PlotDataItem([], [],
                                  symbol='o', symbolSize=2)
        self.lo = pg.PlotDataItem([], [],
                                  symbol='o', symbolSize=2)
        self.ro = pg.PlotDataItem([], [],
                                  symbol='o', symbolSize=2)
        # POI
        self.POI = pg.PlotDataItem([], [],
                                   pen=None, symbol='x', symbolSize=20, symbolBrush=(255, 0, 0, 255))
        # pipetracker
        self.pt_acc = pg.PlotDataItem([], [],
                                      symbol='o', symbolSize=4)
        self.pt_rej = pg.PlotDataItem([], [],
                                      pen=None, symbol='o', symbolSize=4, symbolBrush=(255, 0, 0, 255))
        self.pt_all = pg.PlotDataItem([], [],
                                      pen=None, symbol='o', symbolSize=1, symbolBrush=(100, 100, 100, 255))
        self.pt_selector = pg.PlotCurveItem([], [], width=2)

        # selected chunk
        self.chunk_point = pg.PlotDataItem([], [],
                                           pen=pg.mkPen('b', width=1),
                                           symbol='o', symbolSize=10, symbolBrush='yellow')
        self.chunk = pg.PlotDataItem([], [],
                                     pen=pg.mkPen('yellow', width=5), symbol=None)

        for item in [self.here, self.notvisited, self.visited,
                     self.li, self.ri, self.lo, self.ro,
                     self.POI,
                     self.pt_acc, self.pt_rej, self.pt_all, self.pt_selector,
                     self.chunk_point, self.chunk]:
            item.setParentItem(self.p_parent_box)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        _fName = e.mimeData().text().strip().replace('file:///', '')
        self._controller.handle_load_data(_fName)


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e, 'p')


    def mouse_moved(self, e):
        _cursor = self.pview.view.mapSceneToView(e)
        self._controller.handle_mouse_moved(_cursor, 'p')


    def mouse_pressed(self, e):
        self._controller.handle_mouse_pressed(e, 'p')


    def val_changed(self):
        _sender = self.sender().objectName()
        self._controller.handle_val_changed(_sender)


    def button_pressed(self):
        _sender = self.sender().objectName()
        self._controller.handle_button_pressed(_sender, 'p')