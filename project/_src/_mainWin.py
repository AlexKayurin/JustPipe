from PySide6 import QtWidgets
# from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QFileDialog
import _UI_Control

OPTIONS = QFileDialog.Options()

class MainWin(QtWidgets.QMainWindow, _UI_Control.Ui_CONTROL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # set form
        self.move(0, 0)
        # self.setWindowFlag(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # set up le validators
        for _te in [self.t_D, self.t_IW, self.t_OW, self.t_HW, self.t_VW, self.t_RES,
                    self.t_Fl, self.t_FlPt, self.t_AntiSpoof, self.t_AdPad, self.t_FoDist, self.t_FoPers,
                    self.t_CamOffset]:
            _te.setValidator(QDoubleValidator())

        # # set up signals
        self.actionLoad_profiles.triggered.connect(self.menu_loadfile)
        self.actionLoad_GeoTiff.triggered.connect(self.menu_loadfile)
        self.actionLoad_tide.triggered.connect(self.menu_loadfile)
        self.actionLoad_pipetracker.triggered.connect(self.menu_loadfile)
        self.actionLoad_saved_work.triggered.connect(self.menu_loadfile)
        self.actionSave_work.triggered.connect(self.menu_savefile)
        self.actionExport_EIVA.triggered.connect(self.menu_savefile)
        self.actionExport_SFX.triggered.connect(self.menu_savefile)
        self.actionBuild_Playlist.triggered.connect(self.menu_savefile)
        # self.actionLoad_playlist.triggered.connect(self.menu_select)
        self.actionXView.triggered.connect(self.menu_show_view)
        self.actionPView.triggered.connect(self.menu_show_view)
        self.actionLView.triggered.connect(self.menu_show_view)
        self.actionSettings.triggered.connect(self.menu_show_view)
        self.actionDV_Control.triggered.connect(self.menu_show_view)
        #
        self.actionManual.triggered.connect(self.menu_show_view)
        #
        # self.b_Pause.clicked.connect(self.dvPause)
        self.t_D.textEdited.connect(self.val_changed)
        self.t_IW.textEdited.connect(self.val_changed)
        self.t_OW.textEdited.connect(self.val_changed)
        self.t_HW.textEdited.connect(self.val_changed)
        self.t_VW.textEdited.connect(self.val_changed)
        self.t_RES.textEdited.connect(self.val_changed)
        self.sp_Weed.valueChanged.connect(self.val_changed)
        self.t_Fl.textEdited.connect(self.val_changed)
        self.t_FlPt.textEdited.connect(self.val_changed)
        self.t_FoDist.textEdited.connect(self.val_changed)
        self.t_FoPers.textEdited.connect(self.val_changed)
        self.t_AntiSpoof.textEdited.connect(self.val_changed)
        self.t_AdPad.textEdited.connect(self.val_changed)
        self.t_CamOffset.textEdited.connect(self.val_changed)
        self.spb_Timezone.valueChanged.connect(self.val_changed)
        self.ch_FiSnap.stateChanged.connect(self.val_changed)
        self.rb_Fmin.clicked.connect(self.val_changed)
        self.rb_Fmax.clicked.connect(self.val_changed)
        self.rb_Fmean.clicked.connect(self.val_changed)
        self.rb_Fadapt.clicked.connect(self.val_changed)
        self.rb_FoDist.clicked.connect(self.val_changed)
        self.rb_FoPers.clicked.connect(self.val_changed)
        self.ch_FoSnap.stateChanged.connect(self.val_changed)
        self.ch_FoShow.stateChanged.connect(self.val_changed)
        self.ch_ApplyTide.stateChanged.connect(self.val_changed)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def closeEvent(self, e):
        self._controller.handle_close_ui()


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e, 'm')


    def menu_loadfile(self):
        _menus = ['Load profiles',
                  'Load geoimage',
                  'Load tide',
                  'Load pipetracker',
                  'Load saved work',
                  'Load playlist',
                  ]
        _exts = ['SITRAS profiles (*.cr2);;XPA profiles (*.xpa);;All Files (*)',
                 'GeoTiff files (*.tif);;GeoTiff files (*.tiff);;PNG files (*.png);;All Files (*)',
                 'Tide files (*.tid);;All Files (*)',
                 'justPipe Pipetracker files (*.spt);;EIVA Pipetracker files (*.pip);;SFX Pipetracker files (*.fug);;All Files (*)',
                 'Work files (*.wrk);;All Files (*)',
                 'Palylists (*.pll);;All files (*)',
                 ]

        _sender = self.sender().text()
        _ix = _menus.index(_sender)
        # open file dialog
        _fName, _ = QFileDialog.getOpenFileName(self, _menus[_ix], '', _exts[_ix])

        if _fName:
            self._controller.handle_load_data(_fName)


    def menu_savefile(self):
        _menus = ['Export EIVA',
                  'Export SFX',
                  'Build playlist',
                  'Save work',
                  ]
        _funcs = ['exporteiva',
                  'exportsfx',
                  'buildDVplaylistfile',
                  'savework',
                  ]

        _exts = ['EIVA line files (*.dig);;All Files (*)',
                 'SFX files (*.csv);;All Files (*)',
                 ]

        _sender = self.sender().text()
        _ix = _menus.index(_sender)
        # save file dialog
        if _ix < 2:
            _fName, _ = QFileDialog.getSaveFileName(self, _menus[_ix], '', _exts[_ix]) #, options=OPTIONS)
        # select folder dialog
        else:
            _fName = QFileDialog.getExistingDirectory(self) #, options=OPTIONS)

        if _fName:
            self._controller.handle_save_data(_funcs[_ix], _fName)


    def val_changed(self):
        _sender = self.sender().objectName()
        self._controller.handle_val_changed(_sender)


    def menu_show_view(self):
        _sender = self.sender().objectName()
        self._controller.handle_show_view(_sender)
