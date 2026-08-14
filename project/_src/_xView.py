from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg
import _UI_Xview

class XV(QtWidgets.QMainWindow, _UI_Xview.Ui_XVIEW):
    def __init__(self, screen_resolution):
        super().__init__()
        self._screen_resolution = screen_resolution
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.xview.setMenuEnabled(False)
        # set form
        self.move(544, 0)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlag(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.resize(int((screen_resolution.width() - 544) / 2), int(screen_resolution.height() / 2))

        # set up appearance
        self.l_Tide.setStyleSheet('color: red')
        self.l_Progress.setStyleSheet('color: red')
        self.l_KP.setStyleSheet('color: red')
        self.l_Time.setStyleSheet('color: red')
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_fbwd.setText('\u25C0\u25C0')
        self.b_fbwd.setToolTip('To start (Home)')
        self.b_fbwd.setToolTipDuration(2000)
        self.b_bwd.setText('\u25C0')
        self.b_bwd.setToolTip('One profile back (Z)')
        self.b_bwd.setToolTipDuration(2000)
        self.b_fwd.setText('\u25B6')
        self.b_fwd.setToolTip('One profile forward (X)')
        self.b_fwd.setToolTipDuration(2000)
        self.b_ffwd.setText('\u25B6\u25B6')
        self.b_ffwd.setToolTip('To end (End)')
        self.b_ffwd.setToolTipDuration(2000)
        self.b_endvisit.setText('\u261B')
        self.b_endvisit.setToolTip('To last visited (E)')
        self.b_endvisit.setToolTipDuration(2000)
        self.b_resetfwd.setText('\u2205')
        self.b_resetfwd.setToolTip('Reset flags to end (0)')
        self.b_resetfwd.setToolTipDuration(2000)
        self.b_assist.setText('\u2742')
        self.b_assist.setStyleSheet('color: red')
        self.b_assist.setToolTip('Show pipe (C)')
        self.b_assist.setToolTipDuration(2000)
        self.b_hwm.setToolTip('Decrease horisontal window')
        self.b_hwm.setToolTipDuration(2000)
        self.b_hwp.setToolTip('Increase horisontal window')
        self.b_hwp.setToolTipDuration(2000)
        self.b_vwm.setToolTip('Decrease vertical window')
        self.b_vwm.setToolTipDuration(2000)
        self.b_vwp.setToolTip('Increase vertical window')
        self.b_vwp.setToolTipDuration(2000)
        self.b_Auto.setText('\U0001FA84')
        self.b_Auto.setToolTip('Auto')
        self.b_Auto.setToolTipDuration(2000)
        self.b_asam.setToolTip('Decrease AS mask sector')
        self.b_asam.setToolTipDuration(2000)
        self.b_asap.setToolTip('Increase AS mask sector')
        self.b_asap.setToolTipDuration(2000)

        # connecting signals
        self.xview.scene().sigMouseMoved.connect(self.mouse_moved)
        self.xview.scene().sigMouseClicked.connect(self.mouse_pressed)
        self.b_POI.clicked.connect(self.button_pressed)
        self.b_fbwd.clicked.connect(self.button_pressed)
        self.b_bwd.clicked.connect(self.button_pressed)
        self.b_fwd.clicked.connect(self.button_pressed)
        self.b_ffwd.clicked.connect(self.button_pressed)
        self.b_endvisit.clicked.connect(self.button_pressed)
        self.b_resetfwd.clicked.connect(self.button_pressed)
        self.b_assist.clicked.connect(self.button_pressed)
        self.b_hwm.clicked.connect(self.val_changed)
        self.b_hwp.clicked.connect(self.val_changed)
        self.b_vwm.clicked.connect(self.val_changed)
        self.b_vwp.clicked.connect(self.val_changed)
        self.b_asam.clicked.connect(self.val_changed)
        self.b_asap.clicked.connect(self.val_changed)
        self.b_Auto.clicked.connect(self.button_pressed)
        self.ch_Center.stateChanged.connect(self.val_changed)
        self.ch_ShowPatch.stateChanged.connect(self.val_changed)
        self.ch_ShowAntiSpoof.stateChanged.connect(self.val_changed)

        # set plot items
        #self.xview.getViewBox().invertY(True)   # invert Y (depth)
        self.vb_xview = self.xview.plotItem.vb          # for correct mouse tracking !!!!!

        # adding empty data graphs to plot parent_box
        self.x_parent_box = pg.PlotDataItem()
        self.xview.addItem(self.x_parent_box)
        # profile
        self.x_prof = pg.PlotDataItem([], [],
                                      pen=None, symbol='o', symbolPen=None, symbolSize=2.5)
        # pipe/inwall/outwall/antispoof/assist
        self.pipe_P = pg.PlotCurveItem([], [])
        self.pipe_I = pg.PlotCurveItem([], [])
        self.pipe_O = pg.PlotCurveItem([], [])
        self.pipe_A = pg.PlotCurveItem([], [])
        self.pipeassist = pg.PlotCurveItem([], [])
        # top/bot/cl
        self.pipe_top = pg.InfiniteLine(0, angle=0, movable=False)
        self.pipe_bot = pg.InfiniteLine(0, angle=0, movable=False)
        self.pipe_cl = pg.InfiniteLine(0, angle=90, movable=False)
        # flags
        self.x_l_inner = pg.ArrowItem(angle=-120, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
        self.x_r_inner = pg.ArrowItem(angle=-60, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
        self.x_l_outer = pg.ArrowItem(angle=-90, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
        self.x_r_outer = pg.ArrowItem(angle=-90, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
        # flag patches l/r
        self.x_patch_l = pg.PlotDataItem([], [],
                                         pen=None, symbol='o',
                                         symbolPen=None, symbolSize=2.5, symbolBrush='deepskyblue')
        self.x_patch_r = pg.PlotDataItem([], [],
                                         pen=None, symbol='o',
                                         symbolPen=None, symbolSize=2.5, symbolBrush='deepskyblue')
        # profile search range
        self.port_p_win = pg.InfiniteLine(0, angle=90, movable=False)
        self.stbd_p_win = pg.InfiniteLine(0, angle=90, movable=False)
        # pipe search window
        self.c_win = pg.PlotCurveItem([], [])
        # visited mark
        self.done = pg.PlotDataItem([], [],
                                    pen=None, symbol='x', symbolSize=10, symbolBrush='yellow')

        for item in [self.x_prof, self.x_patch_l, self.x_patch_r,
                     self.pipe_P, self.pipe_I, self.pipe_O, self.pipe_A, self.pipeassist,
                     self.x_l_inner, self.x_r_inner, self.x_l_outer, self.x_r_outer,
                     self.pipe_top, self.pipe_bot, self.pipe_cl,
                     self.port_p_win, self.stbd_p_win,
                     self.c_win, self.done]:
            item.setParentItem(self.x_parent_box)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        _fName = e.mimeData().text().strip().replace('file:///', '')
        self._controller.handle_load_data(_fName)


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e, 'x')


    def mouse_moved(self, e):
        _cursor = self.vb_xview.mapSceneToView(e)
        self._controller.handle_mouse_moved(e, _cursor, 'x')


    def mouse_pressed(self, e):
        self._controller.handle_mouse_pressed(e, 'x')


    def val_changed(self):
        _sender = self.sender().objectName()
        self._controller.handle_val_changed(_sender)


    def button_pressed(self):
        _sender = self.sender().objectName()
        self._controller.handle_button_pressed(_sender, 'x')
