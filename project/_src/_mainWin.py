from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QFileDialog
import _UI_Control


class MainWin(QtWidgets.QMainWindow, _UI_Control.Ui_CONTROL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # set form
        self.move(0, 0)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # set up le validators
        for _le in [self.t_D, self.t_IW, self.t_OW, self.t_HW, self.t_VW, self.t_RES,
                    self.t_FlPt, self.t_AntiSpoof, self.t_AdPad, self.t_FoDist,
                    self.t_PtGap,
                    self.t_CamOffset]:
            _le.setValidator(QDoubleValidator())
        for _le in [self.t_AntiSpoof_A, self.t_smW]:
            _le.setValidator(QIntValidator())

        # set up tooldox colors
        self.toolBoxPipe.setStyleSheet('color: darkblue')
        self.toolBoxFlags.setStyleSheet('color: darkgreen')
        self.toolBoxPtSet.setStyleSheet('color: darkblue')
        self.gB1.setStyleSheet('color: darkgreen')
        self.ch_ApplyTide.setStyleSheet('color: darkred')
        self.b_smoothPT_p_MA.setText('S\u02E3\u02B8')
        self.b_smoothPT_l_MA.setText('S\u1DBB')
        self.b_levelPT.setText('\u21F3')
        self.b_savePT.setText('\U0001F4BE')


        # # set up signals
        self.actionLoad_profiles.triggered.connect(self.menu_loadfile)
        self.actionLoad_GeoTiff.triggered.connect(self.menu_loadfile)
        self.actionLoad_tide.triggered.connect(self.menu_loadfile)
        self.actionLoad_pipetracker.triggered.connect(self.menu_loadfile)
        self.actionLoad_saved_work.triggered.connect(self.menu_loadfile)
        self.actionSave_work.triggered.connect(self.menu_savefile)
        self.actionExport_EIVA.triggered.connect(self.menu_savefile)
        self.actionExport_SFX.triggered.connect(self.menu_savefile)
        self.actionBuild_Playlist.triggered.connect(self.val_changed)
        self.actionLoad_playlist.triggered.connect(self.menu_loadfile)
        self.actionXView.triggered.connect(self.menu_show_view)
        self.actionPView.triggered.connect(self.menu_show_view)
        self.actionLView.triggered.connect(self.menu_show_view)
        self.actionSettings.triggered.connect(self.menu_show_view)
        self.actionDV_Control.triggered.connect(self.menu_show_view)
        self.actionManual.triggered.connect(self.menu_show_view)
        self.actionLicense.triggered.connect(self.menu_show_view)
        self.t_D.textEdited.connect(self.val_changed)
        self.t_IW.textEdited.connect(self.val_changed)
        self.t_OW.textEdited.connect(self.val_changed)
        self.t_HW.textEdited.connect(self.val_changed)
        self.t_VW.textEdited.connect(self.val_changed)
        self.t_RES.textEdited.connect(self.val_changed)
        self.sp_Weed.valueChanged.connect(self.val_changed)
        self.t_FlPt.textEdited.connect(self.val_changed)
        self.t_FoDist.textEdited.connect(self.val_changed)
        self.t_AntiSpoof.textEdited.connect(self.val_changed)
        self.t_AntiSpoof_A.textEdited.connect(self.val_changed)
        self.t_AdPad.textEdited.connect(self.val_changed)
        self.t_CamOffset.textEdited.connect(self.val_changed)
        self.spb_Timezone.valueChanged.connect(self.val_changed)
        self.ch_FiSnap.stateChanged.connect(self.val_changed)
        self.rb_Fmin.clicked.connect(self.val_changed)
        self.rb_Fmax.clicked.connect(self.val_changed)
        self.rb_Fmean.clicked.connect(self.val_changed)
        self.rb_Fadapt.clicked.connect(self.val_changed)
        self.ch_FoSnap.stateChanged.connect(self.val_changed)
        self.ch_ApplyTide.stateChanged.connect(self.val_changed)
        self.sp_Pt_Weed.valueChanged.connect(self.val_changed)
        self.t_smW.textEdited.connect(self.val_changed)
        self.b_smoothPT_p_MA.clicked.connect(self.val_changed)
        self.b_smoothPT_l_MA.clicked.connect(self.val_changed)
        self.t_Lev.textEdited.connect(self.val_changed)
        self.b_levelPT.clicked.connect(self.val_changed)
        self.b_savePT.clicked.connect(self.val_changed)
        self.b_analysePtShift.clicked.connect(self.val_changed)
        self.ch_ShowCamOffset.stateChanged.connect(self.val_changed)

        # pipe tab
        self.toolBoxPipe.currentChanged.connect(self.toolbox_select)
        self.toolBoxFlags.currentChanged.connect(self.toolbox_select)
        self.toolBoxPtSet.currentChanged.connect(self.toolbox_select)
        self.toolBoxVideo.currentChanged.connect(self.toolbox_select)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def closeEvent(self, e):
        self._controller.handle_close_ui()


    def toolbox_select(self):
        _sender = self.sender()
        _ix = _sender.currentIndex()

        if _sender.objectName() == 'toolBoxPipe':
            _widgets = [self.t_D, self.t_IW, self.t_OW,
                            self.t_HW, self.t_VW, self.t_RES, self.sp_Weed,]
            _widgets[_ix].selectAll()
            _widgets[_ix].setFocus()
        elif _sender.objectName() == 'toolBoxFlags':
            _widgets = [self.t_FlPt, self.t_AdPad,
                            self.t_AntiSpoof, self.t_AntiSpoof_A, self.t_FoDist,]
            _widgets[_ix].selectAll()
            _widgets[_ix].setFocus()
        elif _sender.objectName() == 'toolBoxPtSet':
            _widgets = [self.sp_Pt_Weed, self.t_PtGap, self.t_smW, self.t_Lev,]
            _widgets[_ix].selectAll()
            _widgets[_ix].setFocus()


    def keyPressEvent(self, e):
        self._controller.handle_key_pressed(e, 'm')


    def menu_loadfile(self):
        _menus = ['Load profiles',
                  'Load geoimage',
                  'Load tide',
                  'Load pipetracker',
                  'Load saved work',
                  'Load DV index',
                  ]
        _exts = ['SITRAS profiles (*.cr2);;XPA profiles (*.xpa);;All Files (*)',
                 'GeoTiff files (*.tif);;GeoTiff files (*.tiff);;PNG files (*.png);;All Files (*)',
                 'Tide files (*.tid);;All Files (*)',
                 'justPipe Pipetracker files (*.ptr);;EIVA Pipetracker files (*.pip);;SFX Pipetracker files (*.fug);;All Files (*)',
                 'Work files (*.wrk);;All Files (*)',
                 'DV index (*.dvi);;All files (*)',
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
                  'Save work',
                  ]
        _funcs = ['exporteiva',
                  'exportsfx',
                  'savework',
                  ]

        _exts = ['EIVA line files (*.dig);;All Files (*)',
                 'SFX files (*.csv);;All Files (*)',
                 ]

        _sender = self.sender().text()
        _ix = _menus.index(_sender)
        # save file dialog
        if _ix < 2:
            _fName, _ = QFileDialog.getSaveFileName(self, _menus[_ix], '', _exts[_ix])
        # select folder dialog
        else:
            _fName = QFileDialog.getExistingDirectory(self)

        if _fName:
            self._controller.handle_save_data(_funcs[_ix], _fName)


    def val_changed(self):
        _sender = self.sender().objectName()
        self._controller.handle_val_changed(_sender)


    def menu_show_view(self):
        _sender = self.sender().objectName()
        self._controller.handle_show_view(_sender)
