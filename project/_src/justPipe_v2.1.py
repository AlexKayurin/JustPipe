"""
06 Feb 2026 global v 2.1
"""

"""
EIVA EXPORT STRING:
JP XPROF|xpa|,|<r><Enter>|Pipe - Time (YYYYMMDDhhmmssd)^yyyyMMddHHmmss.fff|Rov - Easting^3|Rov - Northing^3|Rov - Gyro^3|Pipe - Heading in Degree^3|Pipe - KP^6|Rov - Raw point Cross Profile (dx,z)^4|

"""


'''
DATA FILETYPES (all files can be drag'n'dropped into Xview):
    Profiles:
        .xpa - export from EIVA (new, no heads separation, contains KP):
        0: xpa - datetime %Y%m%d%H%M%S.%f
        1: ref (ROV) easting
        2: ref (ROV) northing
        3: (ROV) heading
        4: (PIPE) direction
        4: KP
        5-: dx
        6-: Z

        .cr2 - SITRAS export from SFX DataIO
        
        .**** - VisualSoft (RAW) form EIVA

    Geoimages:
        .tif(+.tfw) - georeferenced image

        .png(+.pgw) - georeferenced image

    Pipetracker:
        .fug
        Time,CorrEasting,CorrNorthing,ReducedWaterDepth
        11/07/2024 13:03:34.304,434945.253,6020854.699,74.070
        
        .pip
        2024:08:27:12:34:56.770	526472.838	4435822.973	0.30996	119.927	16    

    Tide:
        .tid
        14/06/2024 11:45:00.000,2.756

GENERATED FILETYPES (all files can be drag'n'dropped into Xview):
    .wrk 'work' file - work & UI settings, 'profiles', 'flush':
        dump = [views_geometry, self.prno,
            self.profName, self.no_of_prof, self.profiles, self.flush,
            self.pipeD, self.pipeR, self.inWall, self.outWall, self.Sect,
            self.HWin, self.VWin, self.Res,
            self.FlD, self.FlP, self.AntiSpoof,
            self.FoDist, self.FoPers,
            self.Tideflag, self.Appliedflag,
            self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
            self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground]

    .spt pipetracker file - 'pipetracker':
        dump = pipetracker

    .lyt 'layout' file - work & UI settings:
        dump = [views_geometry,
        self.pipeD, self.pipeR, self.inWall, self.outWall,
        self.HWin, self.VWin, self.Res,
        self.FlD, self.FlP, self.AntiSpoof,
        self.FoDist, self.FoPers,
        self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
        self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground]

    .plt 'palette' file - UI color settings:
        dump = [mc.cProfile, mc.cPipe, mc.cLeftM, mc.cRightM,
            mc.cNotVis, mc.cVis, mc.cMADJ, mc.cMSBL, mc.cPipetracker, mc.cCurrentProf, self.cBackground]

    .pll 'playlist' file - DV data:
        [[os.path.join(root, fname), duration, tstamp, tstamp + duration, parsed_fname[-2]], channelset]

ARRAYS ELEMENTS:
    'profile':
        0->: dx
        1->: Z

    'flush':
        0: ref_east - easting of profile centre
        1: ref_north - northing of profile centre
        2: hdg - heading
        3: top_x - TOP x
        4: top_y - TOP y
        5: li_x - left inner flag x
        6: li_y - left inner flag y
        7: ri_x - right inner flag x
        8: ri_y - right inner flag y
        9: top east
        10: top north
        11: visited flag - flag that profile already visited (0 - not visited / 1 - visited)
        12: KP - KP / chainage
        13: ping no (sequential)
        14: timestamp
        15: tide
        16: lo_x - left outer flag x
        17: lo_y - left outer flag y
        18: ro_x - right outer flag x
        19: ro_y - right outer flag y
        20: li_e - left inner flag easting
        21: li_n - left inner flag northing
        22: ri_e - right inner flag easting
        23: ri_n - right inner flag northing
        24: lo_e - left outer flag easting
        25: lo_n - left outer flag northing
        26: ro_e - right outer flag easting
        27: ro_n - right outer flag northing
        28: p_hdg - pipe direction
        29: POI flag
        30: visited flag diff (for plotting visited parts)

    'pipetracker':
        0: timestamp
        1: raw easting
        2: raw northing
        3: raw depth
        4: smoothed easting
        5: smoothed norting
        6: smoothed depth
        7: tide
        8: KP
        9: flag (0 - accepted / 1 - rejected)
        10: point no
        11: v shift
        12: chainage
        13: chainage diff (for calculation of gaps)

DRAG&DROP (to Xview):
    Profiles:
        xpa, prf, cr2
    Geoimages:
        tif, png
    Pipetracker:
        pip (EIVA), fug (SFX), spt (internal)
    Tide:
        tid
    Work:
        wrk (internal) - layout, settings, profiles, tide
    Layout:
        lyt (internal) - layout, settings
    Palette:
        plt (internal) - colors
    Playlist:
        pll (internal) - DV palylist

HOTKEYS:
        X - profile fwd
        Z - profile bkwd
        Home - to first pofile
        End - to last profile
        E - to last visited in visited section
        0 - reset all profiles fwd
        Space - auto-snap TOP
        I - 3D interpolate
        C - Show/Hide pipe assistant
        Ctrl+S - fast save (work and pipetracker)
        Alt - in PT edit mode - switch Accept/Reject
        -_ / += - change Lview exaggeration
MOUSE:
    Xview:
        LMB - force TOP
        RMB - force inner flags
        Ctrl+RMB - force outer flags
    Pview / Lview:
        LMB (double) - jump to profile
        RMB - select chunk
'''


import os
from pathlib import Path
import subprocess
import math
import pickle
import sys
from datetime import datetime, timezone
import platform
from decimal import Decimal
import PIL.Image
from PIL import Image
from PIL.TiffTags import TAGS
import numpy as np
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QFileDialog, QMessageBox, QColorDialog, QWidget, QGridLayout
from PySide6.QtCore import Qt, QThread, QObject, QEvent
# from PySide6.QtGui import QWheelEvent
import pyqtgraph as pg
# from pyqtgraph import Vector
import _UI_Control
import _UI_Xview
import _UI_Pview
import _UI_Lview
import _UI_Options
import _F_funcs
import _F_kp_to_point
import _F_playList
import _QtPl

# override PIL max image size
PIL.Image.MAX_IMAGE_PIXELS = 10000000000


class BuildDVPlaylistThread(QThread):
    def __init__(self, foldName, convention, fName):
        super().__init__()
        self.foldName = foldName
        self.convention = convention
        self.fName = fName

    def run(self):
        data = _F_playList.buildplaylist(self.foldName, self.convention)
        # fileslist = data[0]
        # chlist = data[1]

        if self.fName:
            dumpfilename = self.fName

            with open(dumpfilename, 'wb') as dumpfile:
                dump = data
                pickle.dump(dump, dumpfile)


class Colors(QtWidgets.QMainWindow, _UI_Options.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.w_Profile.setStyleSheet(f'background-color: rgba{mc.cProfile.getRgb()}')
        self.w_Pipe.setStyleSheet(f'background-color: rgba{mc.cPipe.getRgb()}')
        self.w_LeftM.setStyleSheet(f'background-color: rgba{mc.cLeftM.getRgb()}')
        self.w_RightM.setStyleSheet(f'background-color: rgba{mc.cRightM.getRgb()}')
        self.w_NotVis.setStyleSheet(f'background-color: rgba{mc.cNotVis.getRgb()}')
        self.w_Vis.setStyleSheet(f'background-color: rgba{mc.cVis.getRgb()}')
        self.w_MADJ.setStyleSheet(f'background-color: rgba{mc.cMADJ.getRgb()}')
        self.w_MSBL.setStyleSheet(f'background-color: rgba{mc.cMSBL.getRgb()}')
        self.w_Pipetracker.setStyleSheet(f'background-color: rgba{mc.cPipetracker.getRgb()}')
        self.w_CurrentProf.setStyleSheet(f'background-color: rgba{mc.cCurrentProf.getRgb()}')
        self.w_Background.setStyleSheet(f'background-color: rgba{mc.cBackground.getRgb()}')

        for b in [self.b_Profile, self.b_Pipe, self.b_LeftM, self.b_RightM,
                  self.b_NotVis, self.b_Vis, self.b_MADJ, self.b_MSBL,
                  self.b_Pipetracker, self.b_CurrentProf, self.b_Background]:
            b.clicked.connect(self.colorselect)

    def colorselect(self):
        selectors = ['b_Profile', 'b_Pipe', 'b_LeftM', 'b_RightM',
                     'b_NotVis', 'b_Vis', 'b_MADJ', 'b_MSBL', 'b_Pipetracker', 'b_CurrentProf', 'b_Background']
        palettes = [self.w_Profile, self.w_Pipe, self.w_LeftM, self.w_RightM,
                    self.w_NotVis, self.w_Vis, self.w_MADJ, self.w_MSBL, self.w_Pipetracker, self.w_CurrentProf, self.w_Background]
        objcolors= [mc.cProfile, mc.cPipe, mc.cLeftM, mc.cRightM,
                     mc.cNotVis, mc.cVis, mc.cMADJ, mc.cMSBL, mc.cPipetracker, mc.cCurrentProf, mc.cBackground]

        sender = self.sender().objectName()
        ix = selectors.index(sender)

        color = QColorDialog.getColor()

        if color.isValid():
            selectedcolor = color.getRgb()
            objcolors[ix].setRgb(*selectedcolor)
            palettes[ix].setStyleSheet(f'background-color: rgba{selectedcolor}')

        pg.GraphicsView.setBackground(xv.xview, mc.cBackground)
        pg.GraphicsView.setBackground(lv.lview, mc.cBackground)
        pv.pview.getView().setBackgroundColor(mc.cBackground)

        xv.UpdateX()


class MainWindow(QtWidgets.QMainWindow, _UI_Control.Ui_CONTROL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # set form
        self.move(0, 0)                                     # initial window position
        # set variables
        self.prno = 0                                       # profile no
        self.pipeD = float(self.t_D.text())                 # pipe D
        self.pipeR = self.pipeD / 2                         # pipe R
        self.inWall = float(self.t_IW.text())               # in wall
        self.outWall = float(self.t_OW.text())              # out wall
        self.HWin = float(self.t_HW.text())                 # horizontal search window
        self.VWin = float(self.t_VW.text())                 # vertical search window (from the highest sounding in H window)
        self.Res = float(self.t_RES.text())                 # search grid resolution
        self.weed = int(self.sp_Weed.value())               # profile weed factor
        self.FlD = float(self.t_Fl.text())                  # inner flag distance from TOP
        self.FlP = float(self.t_FlPt.text())                # inner flag patch (from flag distance)
        self.FoDist = float(self.t_FoDist.text())           # outer flag distance from TOP
        self.FoPers = int(self.t_FoPers.text())             # outer flag persentage from TOP
        self.AntiSpoof = float(self.t_AntiSpoof.text())     # antisppofing pillow for adaptive flags - min distance to pipe wall
        self.AdPad = float(self.t_AdPad.text())             # center pad (left blank) for adaptive flags
        self.PtGap = float(self.t_PtGap.text())             # Min gap in PT data for smoothing
        self.CamOffset = float(self.t_CamOffset.text())     # camera offset relative to profile
        self.Tzone = self.spb_Timezone.value()              # time zone (diff DV - timestamps)

        self.ProfileFlag = False                            # Profile loaded flag
        self.ChunkSelected = False                          # Chunk selected flag
        self.ManualPipe = False                             # Manual pipe placement flag
        self.DoPipe = False                                 # Autorun flag
        self.Interpflag = False                             # Running interpolation flag
        self.DVflag = False                                 # DV loaded flag
        self.Pausedflag = True                              # DV pause on / off flag
        self.Ptflag = False                                 # Pipetracker loaded flag
        self.Tideflag = False                               # Tide loaded flag
        self.Appliedflag = False                            # Tide applied flag
        self.ShowPipe = False                               # Pipe dig assistant flag

        self.xini = 0                                       # initial TOP search position
        self.chunk = [-1, -1]                               # empty chunk (first & last profile nos)
        self.profName = ''                                  # empty profiles file name

        self.extlist = ['.xpa', '.XPA', '.cr2', '.CR2',     # file extensions list
                        '.pip', '.PIP', '.fug', '.FUG', '.spt', '.SPT',
                        '.tid', '.TID', '.tif', '.TIF', '.tiff', '.TIFF', '.png', '.PNG',
                        '.wrk', '.WRK', '.bin', '.BIN', '.pll', '.PLL']

        # connect widgets
        self.actionLoad_profiles.triggered.connect(self.menu_select)
        self.actionLoad_GeoTiff.triggered.connect(self.menu_select)
        self.actionLoad_tide.triggered.connect(self.menu_select)
        self.actionLoad_pipetracker.triggered.connect(self.menu_select)
        self.actionLoad_saved_work.triggered.connect(self.menu_select)
        self.actionLoad_layout.triggered.connect(self.menu_select)
        self.actionSave_work.triggered.connect(self.menu_select)
        self.actionSave_layout.triggered.connect(self.menu_select)
        self.actionExport_EIVA.triggered.connect(self.menu_select)
        self.actionExport_SFX.triggered.connect(self.menu_select)
        self.actionBuild_Playlist.triggered.connect(self.menu_select)
        self.actionLoad_playlist.triggered.connect(self.menu_select)
        for widget in [self.actionXView, self.actionPView, self.actionLView, self.actionSettings, self.actionDV_Control]:
            widget.triggered.connect(self.menu_view_win)
        self.actionManual.triggered.connect(self.open_manual)

        self.b_Pause.clicked.connect(self.dvPause)
        self.t_D.textEdited.connect(self.set_goAutoPipe)  # textEdited only when typed / textChanged if changed (by programm)
        self.t_IW.textEdited.connect(self.set_goAutoPipe)
        self.t_OW.textEdited.connect(self.set_goAutoPipe)
        self.t_HW.textEdited.connect(self.set_goAutoPipe)
        self.t_VW.textEdited.connect(self.set_goAutoPipe)
        self.t_RES.textEdited.connect(self.set_goAutoPipe)
        self.sp_Weed.valueChanged.connect(self.set_goAutoPipe)
        self.t_Fl.textEdited.connect(self.set_goAutoFlags)
        self.t_FlPt.textEdited.connect(self.set_goAutoFlags)
        self.t_FoDist.textEdited.connect(self.set_goAutoFlags)
        self.t_FoPers.textEdited.connect(self.set_goAutoFlags)
        self.t_AntiSpoof.textEdited.connect(self.set_goAutoFlags)
        self.t_AdPad.textEdited.connect(self.set_goAutoFlags)
        self.t_CamOffset.textEdited.connect(self.set_goAutoFlags)
        self.spb_Timezone.valueChanged.connect(self.set_goAutoFlags)
        self.ch_FiSnap.stateChanged.connect(self.set_goAutoFlags)
        self.rb_Fmin.clicked.connect(self.set_goAutoFlags)
        self.rb_Fmax.clicked.connect(self.set_goAutoFlags)
        self.rb_Fmean.clicked.connect(self.set_goAutoFlags)
        self.rb_Fadapt.clicked.connect(self.set_goAutoFlags)
        self.rb_FoDist.clicked.connect(self.set_goAutoFlags)
        self.rb_FoPers.clicked.connect(self.set_goAutoFlags)
        self.ch_FoSnap.stateChanged.connect(self.set_goAutoFlags)
        self.ch_FoShow.stateChanged.connect(self.set_goAutoFlags)
        self.ch_ApplyTide.stateChanged.connect(self.set_goUpdatePT)
        self.rb_Pt.clicked.connect(self.set_editmode)
        self.rb_Pr.clicked.connect(self.set_editmode)

        # colors
        self.cProfile = pg.mkColor(0, 255, 128, 255)
        self.cPipe = pg.mkColor(255, 228, 181, 255)
        self.cLeftM = pg.mkColor(255, 0, 0, 255)
        self.cRightM = pg.mkColor(0, 255, 0, 255)
        self.cNotVis = pg.mkColor(204, 0, 0, 255)
        self.cVis = pg.mkColor(0, 204, 0, 255)
        self.cMADJ = pg.mkColor(255, 0, 255, 255)
        self.cMSBL = pg.mkColor(0, 255, 255, 255)
        self.cPipetracker = pg.mkColor(255, 128, 0, 255)
        self.cCurrentProf = pg.mkColor(255, 0, 0, 255)
        self.cBackground = pg.mkColor(0, 0, 0, 255)

    def open_manual(self):
        # open application manual
        appfolder = os.path.dirname(os.path.realpath(sys.argv[0]))
        helpfile = os.path.join(appfolder, '_internal', 'justPipe.pdf')

        platf = platform.system()
        if platf == 'Linux':
            subprocess.call(['xdg-open', helpfile]) #, check=True)
        if platf == 'Windows':
            os.startfile(helpfile)

    def showwarn(self, warn):
        # pop up message with 'warn' text
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Warning!')
        dlg.setWindowIcon(ic_app)
        dlg.setText(warn)
        dlg.show()

    def keyPressEvent(self, e):
        # focus to XView
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            xv.xview.setFocus()
            xv.xview.activateWindow()

    def closeEvent(self, e):
        # catch close event
        #  save workspace
        parentfold = os.path.dirname(sys.argv[0])
        configfile = os.path.join(parentfold, 'config', 'config.bin')

        views_geometry = []
        for view in [mc, xv, pv, lv]:
            views_geometry.append([view.rect(), view.pos()])

        with open(configfile, 'wb') as dumpfile:
            dump = [views_geometry,
                    self.pipeD, self.pipeR, self.inWall, self.outWall,
                    self.HWin, self.VWin, self.Res,
                    self.FlD, self.FlP, self.AntiSpoof,
                    self.FoDist, self.FoPers,
                    self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
                    self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground]
            pickle.dump(dump, dumpfile)


        if self.DVflag:
            for player in self.players:
                player.close()
        xv.close()
        pv.close()
        lv.close()
        opt.close()
        fv.close()

    def set_editmode(self):
        if self.Ptflag and not(self.rb_Pt.isChecked()):  # remove last selector circle disable widgets
            try:
                pv.pview.removeItem(pv.selector_p)
                lv.lview.removeItem(lv.selector_l)
            except:
                pass
        if self.rb_Pr.isChecked():
            self.PT.setDisabled(True)
            pv.b_smoothPT_p.setDisabled(True)
            pv.t_EdSpot.setDisabled(True)
            pv.t_smW.setDisabled(True)
            pv.ch_Center.setChecked(True)
            lv.b_smoothPT_l.setDisabled(True)
            lv.b_levelPT.setDisabled(True)
            lv.t_EdSpot.setDisabled(True)
            lv.t_smW.setDisabled(True)
            lv.t_Lev.setDisabled(True)
            lv.ch_Center.setChecked(True)
        else:
            self.PT.setDisabled(False)
            pv.b_smoothPT_p.setDisabled(False)
            pv.t_EdSpot.setDisabled(False)
            pv.t_smW.setDisabled(False)
            pv.ch_Center.setChecked(False)
            lv.b_smoothPT_l.setDisabled(False)
            lv.b_levelPT.setDisabled(False)
            lv.t_EdSpot.setDisabled(False)
            lv.t_smW.setDisabled(False)
            lv.t_Lev.setDisabled(False)
            lv.ch_Center.setChecked(False)

        Update_PT()

    def set_goAutoPipe(self):
        self.pipeD = float(self.t_D.text())
        self.pipeR = self.pipeD / 2
        self.inWall = float(self.t_IW.text())
        self.outWall = float(self.t_OW.text())
        self.HWin = float(self.t_HW.text())
        self.VWin = float(self.t_VW.text())
        self.Res = float(self.t_RES.text())
        self.weed = int(self.sp_Weed.value())
        self.flush[self.prno, 11] = 0
        AutoPipe()

    def set_goUpdatePT(self):
        if self.ch_ApplyTide.isChecked():
            xv.l_Tide.setText('TIDE LOADED - APPLIED')
            xv.l_Tide.setStyleSheet('color: forestgreen')
            self.Appliedflag = True
        else:
            xv.l_Tide.setText('TIDE LOADED - NOT APPLIED')
            xv.l_Tide.setStyleSheet('color: darkorange')
            self.Appliedflag = False
        Update_PT()

    def set_goAutoFlags(self):
        sender = self.sender().text()

        for mode in [self.rb_Fmin, self.rb_Fmax, self.rb_Fmean]:
            if mode.isChecked():
                self.t_AntiSpoof.setDisabled(True)
                self.t_AdPad.setDisabled(True)
        if self.rb_Fadapt.isChecked():
            self.t_AntiSpoof.setDisabled(False)
            self.t_AdPad.setDisabled(False)

        self.FlD = float(self.t_Fl.text())
        self.FlP = float(self.t_FlPt.text())
        self.AntiSpoof = float(self.t_AntiSpoof.text())
        self.AdPad = float(self.t_AdPad.text())
        self.FoDist = float(self.t_FoDist.text())
        self.FoPers = int(self.t_FoPers.text())
        self.CamOffset = float(self.t_CamOffset.text())
        self.Tzone =self.spb_Timezone.value()

        mc.flush[mc.prno, 11] = 1 if sender == 'Show flags' else 0

        AutoFlags()

    def menu_select(self):
        options = QFileDialog.Options()

        menus_LoadFile = ['Load profiles', 'Load geoimage', 'Load tide', 'Load pipetracker', 'Load saved work', 'Load workspace', 'Load playlist']
        menus_SaveFile = ['Save workspace', 'Export EIVA', 'Export SFX']
        menus_LoadFolder = ['Build playlist']
        menus_SaveFolder = ['Save work']

        loadfile_exts = ['SITRAS profiles (*.cr2);;XPA profiles (*.xpa);;All Files (*)',
                         'GeoTiff files (*.tif);;GeoTiff files (*.tiff);;PNG files (*.png);;All Files (*)',
                         'Tide files (*.tid);;All Files (*)',
                         'justPipe Pipetracker files (*.spt);;EIVA Pipetracker files (*.pip);;SFX Pipetracker files (*.fug);;All Files (*)',
                         'Work files (*.wrk);;All Files (*)',
                         'Workspace files (*.bin);;All Files (*)',
                         'Palylists (*.pll);;All files (*)']
        savefile_exts = ['Workspace files (*.bin);;All Files (*)',
                         'EIVA line files (*.dig);;All Files (*)',
                         'SFX files (*.csv);;All Files (*)']
        loadfile_funcs = ['self.loadprof', 'self.loadtif', 'self.loadtide', 'self.loadpt', 'self.loadwork', 'self.loadlayout', 'self.loadDV']
        savefile_funcs = ['self.savelayout', 'self.exporteiva', 'self.exportsfx']
        loadfold_funcs = ['self.buildDVplaylist']
        savefold_funcs = ['self.savework']

        sender = self.sender().text()
        if sender in menus_LoadFile:
            ix = menus_LoadFile.index(sender)
            fName, _ = QFileDialog.getOpenFileName(self, menus_LoadFile[ix], '',
                                                      loadfile_exts[ix], options=options)
            exec(f'{loadfile_funcs[ix]}(fName)')
        elif sender in menus_SaveFile:
            ix = menus_SaveFile.index(sender)
            fName, _ = QFileDialog.getSaveFileName(self, menus_SaveFile[ix], '',
                                                      savefile_exts[ix], options=options)
            exec(f'{savefile_funcs[ix]}(fName)')
        elif sender in menus_LoadFolder:
            ix = menus_LoadFolder.index(sender)
            foldName = QFileDialog.getExistingDirectory(self, options=options)
            exec(f'{loadfold_funcs[ix]}(foldName)')
        elif sender in menus_SaveFolder:
            ix = menus_SaveFolder.index(sender)
            foldName = QFileDialog.getExistingDirectory(self, options=options)
            opt = '\'\''
            exec(f'{savefold_funcs[ix]}(foldName,{opt})')

    def menu_view_win(self):
        sender = self.sender().objectName()
        if sender == 'actionXView':
            xv.show()
        elif sender == 'actionPView':
            pv.show()
        elif sender == 'actionLView':
            lv.show()
        elif sender == 'actionSettings':
            opt.show()
        elif sender == 'actionDV_Control':
            if self.DVflag:
                for player in mc.players:
                    player.show()

    def buildDVplaylist(self, foldName):
        options = QFileDialog.Options()
        fName, _ = QFileDialog.getSaveFileName(self, 'Save playlist', '',
                                               'Palylists (*.pll);;All files (*)', options=options)


        self.thread = BuildDVPlaylistThread(foldName, self.spb_Convention.value(), (fName))
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.showwarn('Playlist built'))
        self.thread.start()

        self.showwarn('Building playlist\nIt may take a while\nApplication is fully functional during building\nMessage will pop once playlist has been built')
       
    def dvPause(self):
        if self.Pausedflag:
            # set to Playing
            self.Pausedflag = False
            self.b_Pause.setText('Playing')
            self.b_Pause.setStyleSheet('background-color:rgb(204,255,204)')
        else:
            # set to Paused
            self.Pausedflag = True
            self.b_Pause.setText('Paused')
            self.b_Pause.setStyleSheet('background-color:rgb(255,255,153)')

        xv.xview.setFocus()
        xv.xview.activateWindow()    

    def savelayout(self, fName):
        views_geometry = []
        for view in [mc, xv, pv, lv]:
            views_geometry.append([view.rect(), view.pos()])

        if fName:
            dumpfilename = fName

            with open(dumpfilename, 'wb') as dumpfile:
                dump = [views_geometry,
                        self.pipeD, self.pipeR, self.inWall, self.outWall,
                        self.HWin, self.VWin, self.Res,
                        self.FlD, self.FlP, self.AntiSpoof,
                        self.FoDist, self.FoPers,
                        self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
                        self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground]
                pickle.dump(dump, dumpfile)

    def savework(self, foldName, saveopt):
        views_geometry = []
        for view in [mc, xv, pv, lv]:
            views_geometry.append([view.rect(), view.pos()])

        if foldName:
            saving_time = str(datetime.now().strftime('%Y%m%d%H%M%S'))
            wrk_dumpfilename = os.path.join(foldName, Path(os.path.basename(self.profName)).stem) + '_' + saving_time + '.wrk'

            with open(wrk_dumpfilename, 'wb') as dumpfile:
                dump = [views_geometry, self.prno,
                        self.profName, self.no_of_prof, self.profiles, self.flush,
                        self.pipeD, self.pipeR, self.inWall, self.outWall,
                        self.HWin, self.VWin, self.Res,
                        self.FlD, self.FlP, self.AntiSpoof,
                        self.FoDist, self.FoPers,
                        self.Tideflag, self.Appliedflag,
                        self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
                        self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground]
                pickle.dump(dump, dumpfile)
                self.l_Saved.setText(f'LAST SAVED: {saving_time}{saveopt}')

            if self.Ptflag:
                pt_dumpfilename = os.path.join(foldName, Path(os.path.basename(self.profName)).stem) + '_PT_' + saving_time + '.spt'

                with open(pt_dumpfilename, 'wb') as dumpfile:
                    dump = self.pipetracker
                    pickle.dump(dump, dumpfile)

    def loadprof(self, fName):
        if fName:
            self.profiles = []  # empty array of classes Pofile()
            self.profName = fName
            proftype = Path(self.profName).suffix.strip().lower()

            corrupted = 0
            i = 0

            # xpa - from EIVA NM
            if proftype == '.xpa':
                with open(fName, 'r') as infile:
                    profiles_from_file = infile.readlines()

                self.no_of_prof = len(profiles_from_file)
                # initial flush array for TOP/LI/RI - '0' timestamps will be removed in final
                self.flush = np.zeros((self.no_of_prof, 31))

                for line in profiles_from_file:
                    try:
                        # single profile read from file
                        oneprofile = line.split(',')

                        # check if point not duplicated en[i] != en[i-1]
                        if i > 0 and (oneprofile[1] == self.flush[i - 1, 0] and oneprofile[2] == self.flush[i - 1, 1]):
                            corrupted += 1
                        else:
                            self.flush[i, 14] = datetime.strptime(oneprofile[0], '%Y%m%d%H%M%S.%f').replace(tzinfo=timezone.utc).timestamp() # time
                            self.flush[i, 0] = oneprofile[1]                    # easting
                            self.flush[i, 9] = oneprofile[1]                    # easting
                            self.flush[i, 1] = oneprofile[2]                    # northing
                            self.flush[i, 10] = oneprofile[2]                   # northing
                            self.flush[i, 2] = oneprofile[3]                    # heading
                            self.flush[i, 28] = oneprofile[4]                   # pipe direction
                            self.flush[i, 12] = float(oneprofile[5]) * 1000     # kp (in m)
                            self.flush[i, 13] = i

                            # profile to add to profiles array size = (num_of_points, 2)
                            writeprofile = np.zeros((int(len(oneprofile[6:]) / 2), 2), dtype=float)
                            writeprofile[:, 0] = oneprofile[6::2]
                            writeprofile[:, 1] = oneprofile[7::2]
                            writeprofile = writeprofile[writeprofile[:, 0].argsort()]   # sorting by dx
                            writeprofile[:, 1] = -writeprofile[:, 1]                    # height to depth

                            # flip heading and dX if ROV runs decsending
                            if 120 < abs(self.flush[i, 28] - self.flush[i, 2]) < 240:
                                self.flush[i, 2] += 180
                                writeprofile[:, 0] = -writeprofile[:, 0]

                            # add to profiles array
                            self.profiles.append(writeprofile)

                            i += 1

                    except:
                        corrupted += 1


            # SITRAS format, may be exported via export in SFX DataIO
            if proftype == '.cr2':
                with open(fName, 'r') as infile:
                    # read profiles from profile file
                    profiles_from_file = infile.readlines()[3:]

                self.no_of_prof = len(profiles_from_file)
                # initial flush array for TOP/LI/RI - '0' timestamps will be removed in final
                self.flush = np.zeros((self.no_of_prof, 31))

                for line in profiles_from_file:
                    try:
                        oneprofile = line.replace(';;', ';').split(';')   # replace ';;' at string end in EIVA exported cr2

                        # check if point not duplicated en[i] != en[i-1]
                        if i > 0 and (float(oneprofile[6]) == self.flush[i - 1, 0] and float(oneprofile[7]) == self.flush[i - 1, 1]):
                            corrupted += 1
                        else:
                            # combine date & time and remove fraction from seconds (3 last digits)
                            self.flush[i, 14] = datetime.strptime('.'.join(oneprofile[1:3])[:-3], '%d.%m.%Y.%H%M%S').replace(tzinfo=timezone.utc).timestamp()
                            self.flush[i, 0] = float(oneprofile[6])                 # easting
                            self.flush[i, 9] = float(oneprofile[6])                 # easting
                            self.flush[i, 1] = float(oneprofile[7])                 # northing
                            self.flush[i, 10] = float(oneprofile[7])                # northing
                            self.flush[i, 2] = float(oneprofile[13])                # heading
                            self.flush[i, 28] = float(oneprofile[13])               # pipe direction = heading
                            self.flush[i, 12] = float(oneprofile[3]) * 1000         # KP (in m)
                            self.flush[i, 13] = i

                            # profile to add to profiles array size = (num_of_points, 2)
                            writeprofile = np.zeros((int((len(oneprofile) - 44) / 2), 2), dtype=float)
                            writeprofile[:, 0] = oneprofile[43:-1:2]
                            writeprofile[:, 1] = oneprofile[44::2]
                            writeprofile = writeprofile[writeprofile[:, 0].argsort()]           # sorting by dx
                            writeprofile[:, 1] = writeprofile[:, 1] - float(oneprofile[9])      # reference depth

                            # add to profiles array
                            self.profiles.append(writeprofile)

                            i += 1

                    except:
                        corrupted += 1

            self.no_of_prof -= corrupted
            if corrupted != 0:
                self.showwarn(f'{corrupted} corrupted profile(s) were not loaded')
        
            # remove '0' timestamps (corrupted records) from initial array
            self.flush = self.flush[self.flush[:, 14] != 0]
            self.ProfileFlag = True
            self.prno = 0

            self.setWindowTitle(f'v.2.1 Control - {os.path.basename(self.profName)}')
            AutoPipe()

    def loadtif(self, fName):
        if fName:
            available_geodata = False                                   # georef data available flag
            filetype = Path(fName).suffix.strip().lower()               # only TIF presently!!!

            self.geodata = []  # georef data list
            # open image, read metadata
            img = Image.open(fName)
            self.geoimage = np.swapaxes(np.array(img), 0, 1)

            if filetype in ['.tif', '.tiff']:
                refName = fName[: -len(filetype)] + '.tfw'              # world file name
            elif filetype in ['.png']:
                refName = fName[: -len(filetype)] + '.pgw'              # world file name

            try:
                with img:
                    meta_dict = {TAGS[key]: img.tag[key] for key in img.tag_v2}

                # reading georef data from tif metadata or ref world file
                # if 'ModelTiepointTag' in meta_dict.keys() and 'ModelPixelScaleTag' in meta_dict.keys():
                self.geodata.append(float(meta_dict['ModelPixelScaleTag'][0]))
                self.geodata.append(0)
                self.geodata.append(0)
                self.geodata.append(0)
                self.geodata.append(float(meta_dict['ModelTiepointTag'][3]))
                self.geodata.append(float(meta_dict['ModelTiepointTag'][4]))
                available_geodata = True
            except (AttributeError, KeyError):
                if os.path.isfile(refName):
                    with open(refName, 'r') as refFile:
                        refString = refFile.readlines()
                    for line in refString:
                        self.geodata.append(float(line.replace('\n', '')))
                    available_geodata = True
                else:
                    self.showwarn('No geodata available\ngeoimage not loaded')

            if available_geodata:
                # load image to plan view
                cellsize = mc.geodata[0]
                o_left, o_top = mc.geodata[4], mc.geodata[5]
                pv.pview.setImage(mc.geoimage, scale=(cellsize, -cellsize), pos=(o_left - cellsize, o_top + cellsize))
                pv.UpdateP()

    def loadtide(self, fName):
        if not self.ProfileFlag:
            self.showwarn('Load profiles first')
        else:
            if fName:
                tidedata = np.loadtxt(fName, skiprows=0, delimiter=',',
                                      converters={0: lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S.%f').replace(tzinfo=timezone.utc).timestamp(),
                                                  1: float})

                if tidedata[-1, 0] < mc.flush[-1, 14] or tidedata[0, 0] > mc.flush[0, 14]:
                    self.showwarn('Tide file does not cover profiles')
                else:
                    # interpolating tide to flush
                    mc.flush[:, 15] = np.interp(mc.flush[:, 14], tidedata[:, 0], tidedata[:, 1])
                    self.Tideflag = True
                    self.ch_ApplyTide.setDisabled(False)

                    xv.l_Tide.setText('TIDE LOADED - APPLIED')
                    xv.l_Tide.setStyleSheet('color: forestgreen')

                if self.Ptflag:
                    # interpolating tide from flush to pipetracker filed 7
                    self.pipetracker[:, 7] = np.interp(self.pipetracker[:, 0], self.flush[:, 14],
                                                       self.flush[:, 15])

                Update_PT()

    def loadpt(self, fName):
        if not self.ProfileFlag:
            self.showwarn('Load profiles first')
        else:
            if fName:
                if not self.Ptflag:
                    ptfiletype = Path(fName).suffix.strip().lower()

                    if ptfiletype == '.pip':
                        pipetracker_file = np.loadtxt(fName, skiprows=0, delimiter='\t',
                                                      converters={0: lambda x: datetime.strptime(x,
                                                                                                 '%Y:%m:%d:%H:%M:%S.%f').replace(
                                                          tzinfo=timezone.utc).timestamp(),
                                                                  1: float, 2: float, 3: float, 4: float, 5:float})
                        self.pipetracker = np.concatenate((pipetracker_file, np.zeros((len(pipetracker_file), 8))), axis=1)

                        # depth to field 3 from field 4 (and negating Z)
                        self.pipetracker[:, 3] = -self.pipetracker[:, 4]
                        # populating 'smoothed' fields from 'raw'
                        self.pipetracker[:, 4:7] = self.pipetracker[:, 1:4]


                    if ptfiletype == '.fug':
                        pipetracker_file = np.loadtxt(fName, skiprows=1, delimiter=',',
                                                      converters={0: lambda x: datetime.strptime(x,
                                                                                                 '%d/%m/%Y %H:%M:%S.%f').replace(
                                                          tzinfo=timezone.utc).timestamp(),
                                                                  1: float, 2: float, 3: float})
                        self.pipetracker = np.concatenate((pipetracker_file, np.zeros((len(pipetracker_file), 10))), axis=1)

                        # negating Z
                        self.pipetracker[:, 3] *= -1
                        # populating 'smoothed' fields from 'raw'
                        self.pipetracker[:, 4:7] = self.pipetracker[:, 1:4]

                    if ptfiletype == '.spt':
                        with open(fName, 'rb') as loadfile:
                            self.pipetracker = pickle.load(loadfile)

                        # fill level textbox if loaded PT is aready levelled
                        lv.t_Lev.setText(str(self.pipetracker[0, 11]))
                        lv.Lev = self.pipetracker[0, 11]

                    # FOR ALL PT TYPES
                    # interpolating tide from flush to pipetracker filed 7
                    if self.Tideflag:
                        self.pipetracker[:, 7] = np.interp(self.pipetracker[:, 0], self.flush[:, 14],
                                                           self.flush[:, 15])

                    self.rb_Pt.setDisabled(False)
                    pv.ch_ShowPT.setDisabled(False)
                    lv.ch_ShowPT.setDisabled(False)
                    pv.b_snap_h.setDisabled(False)
                    lv.b_snap_v.setDisabled(False)

                    self.Ptflag = True
                    ReChain()
                Update_PT()

    def loadwork(self, fName):
        with open(fName, 'rb') as loadfile:
            [views_geometry, self.prno,
             self.profName, self.no_of_prof, self.profiles, self.flush,
             self.pipeD, self.pipeR, self.inWall, self.outWall,
             self.HWin, self.VWin, self.Res,
             self.FlD, self.FlP, self.AntiSpoof,
             self.FoDist, self.FoPers,
             self.Tideflag, self.Appliedflag,
             self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
             self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground] = pickle.load(loadfile)

        pg.GraphicsView.setBackground(xv.xview, mc.cBackground)
        pg.GraphicsView.setBackground(lv.lview, mc.cBackground)
        pv.pview.getView().setBackgroundColor(mc.cBackground)

        for i, view in enumerate([mc, xv, pv, lv]):
            view.resize(views_geometry[i][0].width(), views_geometry[i][0].height())
            view.move(views_geometry[i][1].x(), views_geometry[i][1].y())

        self.setWindowTitle(f'v.2.1 Control - {os.path.basename(self.profName)[:-4]}')

        self.t_D.setText(str(self.pipeD))
        self.t_IW.setText(str(self.inWall))
        self.t_OW.setText(str(self.outWall))
        self.t_HW.setText(str(self.HWin))
        self.t_VW.setText(str(self.VWin))
        self.t_RES.setText(str(self.Res))
        self.t_Fl.setText(str(self.FlD))
        self.t_FlPt.setText(str(self.FlP))
        self.t_AntiSpoof.setText(str(self.AntiSpoof))
        self.t_FoDist.setText(str(self.FoDist))
        self.t_FoPers.setText(str(self.FoPers))
        if not self.Tideflag:
            self.ch_ApplyTide.setDisabled(True)
            self.ch_ApplyTide.setChecked(True)
            xv.l_Tide.setText('TIDE NOT LOADED')
            xv.l_Tide.setStyleSheet('color: red')
        if self.Tideflag and not self.Appliedflag:
            self.ch_ApplyTide.setDisabled(False)
            self.ch_ApplyTide.setChecked(False)
            xv.l_Tide.setText('TIDE LOADED - NOT APPLIED')
            xv.l_Tide.setStyleSheet('color: darkorange')
        if self.Tideflag and self.Appliedflag:
            self.ch_ApplyTide.setDisabled(False)
            self.ch_ApplyTide.setChecked(True)
            xv.l_Tide.setText('TIDE LOADED - APPLIED')
            xv.l_Tide.setStyleSheet('color: forestgreen')

        self.ProfileFlag = True
        AutoPipe()

    def loadlayout(self, fName):
        with open(fName, 'rb') as loadfile:
            [views_geometry,
             self.pipeD, self.pipeR, self.inWall, self.outWall,
             self.HWin, self.VWin, self.Res,
             self.FlD, self.FlP, self.AntiSpoof,
             self.FoDist, self.FoPers,
             self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
             self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker, self.cCurrentProf, self.cBackground] = pickle.load(loadfile)

        pg.GraphicsView.setBackground(xv.xview, mc.cBackground)
        pg.GraphicsView.setBackground(lv.lview, mc.cBackground)
        pv.pview.getView().setBackgroundColor(mc.cBackground)

        for i, view in enumerate([mc, xv, pv, lv]):
            view.resize(views_geometry[i][0].width(), views_geometry[i][0].height())
            view.move(views_geometry[i][1].x(), views_geometry[i][1].y())

        self.t_D.setText(str(self.pipeD))
        self.t_IW.setText(str(self.inWall))
        self.t_OW.setText(str(self.outWall))
        self.t_HW.setText(str(self.HWin))
        self.t_VW.setText(str(self.VWin))
        self.t_RES.setText(str(self.Res))
        self.t_Fl.setText(str(self.FlD))
        self.t_FlPt.setText(str(self.FlP))
        self.t_AntiSpoof.setText(str(self.AntiSpoof))

        Update_PT()

    def loadDV(self, fName):
        # read built playlist
        with open(fName, 'rb') as loadfile:
            # data[0]
            # [full filename (with path)
            # duration (sec)
            # start timestamp
            # end timestamp
            # channel name]
            # data[1]
            # [channellist]
            data = pickle.load(loadfile)

        channellist = data[1]

        self.playlists = []
        self.DVstarts = []
        self.DVends = []
        self.currentDVs = []
        self.players = []
        for i, channel in enumerate(channellist):          
            playlist = [file for file in data[0] if file[4] == channel]
            self.playlists.append(playlist)
            self.DVstarts.append([ix[2] for ix in playlist])
            self.DVends.append([ix[3] for ix in playlist])
            self.currentDVs.append(0)
            player = _QtPl.Player(channel, i)
            self.players.append(player)

        self.DVflag = True

        self.b_Pause.setDisabled(False)
        self.b_Pause.setText('Playing')
        self.Pausedflag = False
        self.b_Pause.setStyleSheet('background-color:rgb(204,255,204)')

        for i, player in enumerate(self.players):
            player.show()
            player.setWindowIcon(ic_app)
            # load video
            player.loadmedia(self.playlists[i][0][0])

    def exporteiva(self, fName):
        if fName:
            out_top = out_li = out_ri = out_lo = out_ro = '#unit=m\n'
            out_top += '#Type=Pipe\n'
            for point in mc.flush:
                appliedtide = mc.Tideflag * mc.Appliedflag * point[15]
                if point[11] == 1:
                    ref_east = point[0]
                    ref_north = point[1]
                    hdg = point[2]
                    top_x = point[3]
                    top_y = point[4]
                    li_x = point[5]
                    li_y = point[6]
                    ri_x = point[7]
                    ri_y = point[8]
                    lo_x = point[16]
                    lo_y = point[17]
                    ro_x = point[18]
                    ro_y = point[19]

                    # TOP
                    top_e, top_n = round(point[9], 3), round(point[10], 3)
                    out_top += str(top_e) + ' ' + str(top_n) + ' ' + str(-(round(top_y, 3) + appliedtide)) + '\n'
                    # Left inner flag
                    li_en = _F_funcs.Rotation2D(li_x, ref_east, ref_north, hdg)
                    li_e, li_n = round(li_en[0], 3), round(li_en[1], 3)
                    out_li += str(li_e) + ' ' + str(li_n) + ' ' + str(-(round(li_y, 3) + appliedtide)) + '\n'
                    # Right inner flag
                    ri_en = _F_funcs.Rotation2D(ri_x, ref_east, ref_north, hdg)
                    ri_e, ri_n = round(ri_en[0], 3), round(ri_en[1], 3)
                    out_ri += str(ri_e) + ' ' + str(ri_n) + ' ' + str(-(round(ri_y, 3) + appliedtide)) + '\n'
                    # Left outer flag
                    lo_en = _F_funcs.Rotation2D(lo_x, ref_east, ref_north, hdg)
                    lo_e, lo_n = round(lo_en[0], 3), round(lo_en[1], 3)
                    out_lo += str(lo_e) + ' ' + str(lo_n) + ' ' + str(-(round(lo_y, 3) + appliedtide)) + '\n'
                    # Right inner flag
                    ro_en = _F_funcs.Rotation2D(ro_x, ref_east, ref_north, hdg)
                    ro_e, ro_n = round(ro_en[0], 3), round(ro_en[1], 3)
                    out_ro += str(ro_e) + ' ' + str(ro_n) + ' ' + str(-(round(ro_y, 3) + appliedtide)) + '\n'

            li_file_name = fName[:-4] + '_LeftInner.dig'
            ri_file_name = fName[:-4] + '_RightInner.dig'
            lo_file_name = fName[:-4] + '_LeftOuter.dig'
            ro_file_name = fName[:-4] + '_RightOuter.dig'

            with open(fName, 'w') as top_file:
                top_file.write(out_top[:-1])
            with open(li_file_name, 'w') as li_file:
                li_file.write(out_li[:-1])
            with open(ri_file_name, 'w') as ri_file:
                ri_file.write(out_ri[:-1])
            with open(lo_file_name, 'w') as lo_file:
                lo_file.write(out_lo[:-1])
            with open(ro_file_name, 'w') as ro_file:
                ro_file.write(out_ro[:-1])

    def exportsfx(self, fName):
        if fName:
            out_top = out_li = out_ri = out_lo = out_ro = '' #'timedate,edited_easting,edited_northing,edited_height\n'
            c = 50001
            for point in mc.flush:
                appliedtide = mc.Tideflag * mc.Appliedflag * point[15]
                if point[11] == 1:
                    ref_east = point[0]
                    ref_north = point[1]
                    hdg = point[2]
                    top_x = point[3]
                    top_y = point[4]
                    li_x = point[5]
                    li_y = point[6]
                    ri_x = point[7]
                    ri_y = point[8]
                    lo_x = point[16]
                    lo_y = point[17]
                    ro_x = point[18]
                    ro_y = point[19]

                    # TOP
                    top_e, top_n = round(point[9], 3), round(point[10], 3)
                    out_top += str(c) + ',' + str(top_e) + ',' + str(top_n) + ',' + str(round(top_y, 3) + appliedtide) + '\n'
                    # Left inner flag
                    li_en = _F_funcs.Rotation2D(li_x, ref_east, ref_north, hdg)
                    li_e, li_n = round(li_en[0], 3), round(li_en[1], 3)
                    out_li += str(c) + ',' + str(li_e) + ',' + str(li_n) + ',' + str(round(li_y, 3) + appliedtide) + '\n'
                    # Right inner flag
                    ri_en = _F_funcs.Rotation2D(ri_x, ref_east, ref_north, hdg)
                    ri_e, ri_n = round(ri_en[0], 3), round(ri_en[1], 3)
                    out_ri += str(c) + ',' + str(ri_e) + ',' + str(ri_n) + ',' + str(round(ri_y, 3) + appliedtide) + '\n'
                    # Left outer flag
                    lo_en = _F_funcs.Rotation2D(lo_x, ref_east, ref_north, hdg)
                    lo_e, lo_n = round(lo_en[0], 3), round(lo_en[1], 3)
                    out_lo += str(c) + ',' + str(lo_e) + ',' + str(lo_n) + ',' + str(round(lo_y, 3) + appliedtide) + '\n'
                    # Right outer flag
                    ro_en = _F_funcs.Rotation2D(ro_x, ref_east, ref_north, hdg)
                    ro_e, ro_n = round(ro_en[0], 3), round(ro_en[1], 3)
                    out_ro += str(c) + ',' + str(ro_e) + ',' + str(ro_n) + ',' + str(round(ro_y, 3) + appliedtide) + '\n'

                    c += 1

            li_file_name = fName[:-4] + '_LI.csv'
            ri_file_name = fName[:-4] + '_RI.csv'
            lo_file_name = fName[:-4] + '_LO.csv'
            ro_file_name = fName[:-4] + '_RO.csv'

            with open(fName[:-4] + '_T.csv', 'w') as top_file:
                top_file.write(out_top[:-1])
            with open(li_file_name, 'w') as li_file:
                li_file.write(out_li[:-1])
            with open(ri_file_name, 'w') as ri_file:
                ri_file.write(out_ri[:-1])
            with open(lo_file_name, 'w') as lo_file:
                lo_file.write(out_lo[:-1])
            with open(ro_file_name, 'w') as ro_file:
                ro_file.write(out_ro[:-1])


class XV(QtWidgets.QMainWindow, _UI_Xview.Ui_XVIEW):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        # set form
        self.xview.setMenuEnabled(False)
        self.move(425, 0)

        self.l_Tide.setStyleSheet('color: red')
        self.l_Progress.setStyleSheet('color: red')
        self.l_KP.setStyleSheet('color: red')
        self.l_Time.setStyleSheet('color: red')

        # lock scale 1:1
        self.xview.setAspectLocked()
        #self.xview.getViewBox().invertY(True)   # invert Y (depth)
        self.vb_xview = self.xview.plotItem.vb  # for correct mouse tracking !!!!!

        # connecting signals
        self.xview.scene().sigMouseMoved.connect(self.mouse_moved)
        self.xview.scene().sigMouseClicked.connect(self.mouse_clicked)
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.clicked.connect(self.but_pressed)
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_fbwd.setText('\u25C0\u25C0')
        self.b_fbwd.clicked.connect(self.but_pressed)
        self.b_fbwd.setToolTip('To start (Home)')
        self.b_fbwd.setToolTipDuration(2000)
        self.b_bwd.setText('\u25C0')
        self.b_bwd.clicked.connect(self.but_pressed)
        self.b_bwd.setToolTip('One profile back (Z)')
        self.b_bwd.setToolTipDuration(2000)
        self.b_fwd.setText('\u25B6')
        self.b_fwd.clicked.connect(self.but_pressed)
        self.b_fwd.setToolTip('One profile forward (X)')
        self.b_fwd.setToolTipDuration(2000)
        self.b_ffwd.setText('\u25B6\u25B6')
        self.b_ffwd.clicked.connect(self.but_pressed)
        self.b_ffwd.setToolTip('To end (End)')
        self.b_ffwd.setToolTipDuration(2000)
        self.b_endvisit.setText('\u279F')
        self.b_endvisit.clicked.connect(self.but_pressed)
        self.b_endvisit.setToolTip('To last visited (E)')
        self.b_endvisit.setToolTipDuration(2000)
        self.b_resetfwd.setText('\u2326')
        self.b_resetfwd.clicked.connect(self.but_pressed)
        self.b_resetfwd.setToolTip('Reset flags to end (0)')
        self.b_resetfwd.setToolTipDuration(2000)
        self.b_assist.setText('\u2742')
        self.b_assist.setStyleSheet('color: red')
        self.b_assist.clicked.connect(self.but_pressed)
        self.b_assist.setToolTip('Show pipe (C)')
        self.b_assist.setToolTipDuration(2000)
        self.b_hwm.clicked.connect(self.but_pressed)
        self.b_hwm.setToolTip('Decrease horisontal window')
        self.b_hwm.setToolTipDuration(2000)
        self.b_hwp.clicked.connect(self.but_pressed)
        self.b_hwp.setToolTip('Increase horisontal window')
        self.b_hwp.setToolTipDuration(2000)
        self.b_vwm.clicked.connect(self.but_pressed)
        self.b_vwm.setToolTip('Decrease vertical window')
        self.b_vwm.setToolTipDuration(2000)
        self.b_vwp.clicked.connect(self.but_pressed)
        self.b_vwp.setToolTip('Increase vertical window')
        self.b_vwp.setToolTipDuration(2000)
        self.b_Auto.clicked.connect(self.but_pressed)
        self.b_Auto.setToolTip('Auto')
        self.b_Auto.setToolTipDuration(2000)
        self.ch_Center.stateChanged.connect(self.UpdateX)
        self.ch_ShowPatch.stateChanged.connect(self.UpdateX)
        self.ch_ShowAntiSpoof.stateChanged.connect(self.UpdateX)

        # set pipe shape
        self.l_io = np.linspace(0, 2 * np.pi, 50)  # spaced points array for plotting pipe (360 deg / 50 pts)
        # set flags shapes
        self.lifl = pg.ArrowItem(angle=-90, headLen=30, headWidth=4, tailLen=30, tailWidth=2)
        self.rifl = pg.ArrowItem(angle=-90, headLen=30, headWidth=4, tailLen=30, tailWidth=2)
        self.lofl = pg.ArrowItem(angle=-90, headLen=15, headWidth=4, tailLen=15, tailWidth=2)
        self.rofl = pg.ArrowItem(angle=-90, headLen=15, headWidth=4, tailLen=15, tailWidth=2)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText() and (Path(e.mimeData().text()).suffix.strip() in mc.extlist):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        fName = e.mimeData().text().strip().replace('file:///', '')
        dropToViewEvent(e, fName)

    def but_pressed(self):
        sender = self.sender().objectName()

        if sender in ['b_hwm', 'b_hwp', 'b_vwm', 'b_vwp',
                      'b_SectDecr', 'b_SectIncr', 'b_SectLeft', 'b_SectRight']:
            if sender == 'b_hwm':
                mc.t_HW.setText(str(round(mc.HWin - 0.05, 2)))
                mc.HWin = float(mc.t_HW.text())
            elif sender == 'b_hwp':
                mc.t_HW.setText(str(round(mc.HWin + 0.05, 2)))
                mc.HWin = float(mc.t_HW.text())
            elif sender == 'b_vwm':
                if mc.VWin > 0.05:
                    mc.t_VW.setText(str(round(mc.VWin - 0.05, 2)))
                    mc.VWin = float(mc.t_VW.text())
            elif sender == 'b_vwp':
                mc.t_VW.setText(str(round(mc.VWin + 0.05, 2)))
                mc.VWin = float(mc.t_VW.text())

            mc.flush[mc.prno, 11] = 0

        else:
            if sender == 'b_POI':
                mc.flush[mc.prno, 29] = 1 if mc.flush[mc.prno, 29] == 0 else 0
            elif sender == 'b_Auto':
                AutoRun()
            elif sender == 'b_fwd':
                if mc.prno < mc.no_of_prof - 1:
                    mc.prno += 1
            elif sender == 'b_bwd':
                if mc.prno > 0:
                    mc.prno -= 1
            elif sender == 'b_ffwd':
                mc.prno = mc.no_of_prof - 1
            elif sender == 'b_fbwd':
                mc.prno = 0
            elif sender == 'b_endvisit':
                for i in range(mc.prno, mc.no_of_prof):
                    if mc.flush[i, 11] == 0:
                        mc.prno = i - 1
                        break
            elif sender == 'b_resetfwd':
                if mc.ChunkSelected:
                    chs, che = mc.chunk[0], mc.chunk[1]
                else:
                    chs, che = mc.prno + 1, mc.no_of_prof

                mc.flush[chs:che + 1:, 11] = 0
                mc.flush[chs:che + 1:, 9] = mc.flush[chs:che + 1:, 0]
                mc.flush[chs:che + 1:, 10] = mc.flush[chs:che + 1:, 1]

                if mc.ChunkSelected:
                    mc.chunk = [-1, -1]
                    mc.ChunkSelected = False
                    Update_Chunk('action_completed')
                else:
                    xv.UpdateX()
            elif sender == 'b_assist':
                mc.ShowPipe = True if mc.ShowPipe == False else False
                if mc.ShowPipe == False:
                    self.b_assist.setStyleSheet('color: red')
                else:
                    self.b_assist.setStyleSheet('color: green')

        AutoPipe()

    def keyPressEvent(self, e):
        key_pressed(e)

    def keyReleaseEvent(self, e):
        key_pressed(e)

    def mouse_moved(self, e):
        self.cursor = self.vb_xview.mapSceneToView(e)
        mc.l_Coord.setText(f'dX:{round(self.cursor.x(), 1)}, Z:{round(self.cursor.y(), 1)}')

        # pipe assistant ROI
        if mc.ShowPipe:
            try:
                self.xview.removeItem(self.pipeassist)
            except:
                pass

            # pipetracker selector
            pen = pg.mkPen(color='g', width=2)

            self.pipeassist = [np.cos(self.l_io) * mc.pipeR, np.sin(self.l_io) * mc.pipeR]
            self.pipeassist = pg.PlotCurveItem(self.pipeassist[0], self.pipeassist[1])
            self.pipeassist.setPos(self.cursor.x(), self.cursor.y() - mc.pipeR)
            self.pipeassist.setPen(pen)
            self.xview.addItem(self.pipeassist)

    def mouse_clicked(self, e):
        # tide for profile
        T = mc.ch_ApplyTide.isChecked() * mc.flush[mc.prno, 15]
        if e.button() == QtCore.Qt.MouseButton.LeftButton:     # Left mouse button
            # force TOP
            self.min_cx, self.min_cz = self.cursor.x(), self.cursor.y() - mc.pipeR - T
            # write flag 'unvisited' for AutoFlags
            mc.flush[mc.prno, 11] = 0
            mc.flush[mc.prno, 3] = self.min_cx
            mc.flush[mc.prno, 4] = mc.flush[mc.prno:, 4][mc.flush[mc.prno:, 11] == 0] = self.min_cz + mc.pipeR #+ T
            # write to flush top_, top_n
            ref_east, ref_north, hdg = mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], mc.flush[mc.prno, 2]
            # top
            top = _F_funcs.Rotation2D(self.min_cx, mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], hdg)
            mc.flush[mc.prno, 9] = top[0]
            mc.flush[mc.prno, 10] = top[1]

            mc.ManualPipe = True
            AutoPipe()

        if e.button() == QtCore.Qt.MouseButton.RightButton:     # Right mouse button
            pipe_x = mc.flush[mc.prno, 3]
            # force inner Flag
            if e.modifiers() != Qt.ControlModifier:     # RMB
                a, b, c, d = 5, 6, 7, 8
                whatflag = 'Inner'
            # force outer Flag
            if e.modifiers() == Qt.ControlModifier:  # RMB + Ctrl
                a, b, c, d = 16, 17, 18, 19
                whatflag = 'Outer'

            lfl_x, lfl_z = mc.flush[mc.prno, a], mc.flush[mc.prno, b]
            rfl_x, rfl_z = mc.flush[mc.prno, c], mc.flush[mc.prno, d]

            if self.cursor.x() < pipe_x:
                lfl_x, lfl_z = self.cursor.x(), self.cursor.y() - T
            else:
                rfl_x, rfl_z = self.cursor.x(), self.cursor.y() - T

            ManualFlags(lfl_x, lfl_z, rfl_x, rfl_z, whatflag)

    def UpdateX(self):
        if mc.ProfileFlag:
            for but in [self.b_POI, pv.b_POI, lv.b_POI]:
                if mc.flush[mc.prno, 29]:
                        but.setText('\u2717')
                        but.setStyleSheet('color: red')
                else:
                    but.setText('\u2714')
                    but.setStyleSheet('color: green')

            tstamp = mc.flush[mc.prno, 14] + mc.Tzone * 3600
            # DV player
            if mc.DVflag:
                if not mc.Pausedflag:
                    for i, player in enumerate(mc.players):
                        for j, s in enumerate(mc.DVstarts[i]):
                            if s <= tstamp <= mc.DVends[i][j]:
                                if j == mc.currentDVs[i]:
                                    goto_time = 1000 * int(tstamp - s)
                                    player.gototime(goto_time)
                                else:
                                    mc.currentDVs[i] = j
                                    goto_time = 1000 * int(tstamp - s)
                                    player.loadmedia(mc.playlists[i][mc.currentDVs[i]][0])
                                    player.gototime(goto_time)

            # Xview update
            self.xview.clear() 
            self.l_Progress.setText(f'PROFILE {mc.prno + 1} OF {mc.no_of_prof}')
            self.l_KP.setText(f'KP {mc.flush[mc.prno, 12]:.2f}')
            self.l_Time.setText(f'{datetime.fromtimestamp(mc.flush[mc.prno, 14], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}')
            p_coord = [mc.flush[mc.prno, 3], mc.flush[mc.prno, 4] - mc.pipeR]
            lifl_coord = [mc.flush[mc.prno, 5], mc.flush[mc.prno, 6]]
            rifl_coord = [mc.flush[mc.prno, 7], mc.flush[mc.prno, 8]]
            lofl_coord = [mc.flush[mc.prno, 16], mc.flush[mc.prno, 17]]
            rofl_coord = [mc.flush[mc.prno, 18], mc.flush[mc.prno, 19]]

            # tide for profile
            TC = mc.ch_ApplyTide.isChecked() * mc.flush[mc.prno, 15]
            # profile
            self.xview.plot(mc.profile[:, 0], mc.profile[:, 1] + TC,
                            pen=None, symbol='o', symbolPen=None, symbolSize=2.5, symbolBrush=mc.cProfile)
            # flag patches
            if self.ch_ShowPatch.isChecked():
                try:
                    self.xview.plot(mc.profile[mc.li_spot[0], 0], mc.profile[mc.li_spot[0], 1] + TC,
                                    pen=None, symbol='o', symbolPen=None, symbolSize=2.5, symbolBrush='deepskyblue')
                    self.xview.plot(mc.profile[mc.ri_spot[0], 0], mc.profile[mc.ri_spot[0], 1] + TC,
                                    pen=None, symbol='o', symbolPen=None, symbolSize=2.5, symbolBrush='deepskyblue')
                except:
                    pass

            # pipe
            p_P_pts = [mc.pipeR * np.cos(self.l_io), mc.pipeR * np.sin(self.l_io)]
            p_P = pg.PlotCurveItem(p_P_pts[0], p_P_pts[1])
            p_P.setPos(p_coord[0], p_coord[1] + TC)
            p_P.setPen(color=mc.cPipe.getRgb(), width=1.5)
            self.xview.addItem(p_P)
            # inWall
            inWall_pts = [mc.inWall * mc.pipeR * np.cos(self.l_io), mc.inWall * mc.pipeR * np.sin(self.l_io)]
            p_in = pg.PlotCurveItem(inWall_pts[0], inWall_pts[1])
            p_in.setPos(p_coord[0], p_coord[1] + TC)
            p_in.setPen(color=mc.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
            self.xview.addItem(p_in)
            # outWall
            outWall_pts = [mc.outWall * mc.pipeR * np.cos(self.l_io), mc.outWall * mc.pipeR * np.sin(self.l_io)]
            p_out = pg.PlotCurveItem(outWall_pts[0], outWall_pts[1])
            p_out.setPos(p_coord[0], p_coord[1] + TC)
            p_out.setPen(color=mc.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
            self.xview.addItem(p_out)
            # AntiSpoof
            if self.ch_ShowAntiSpoof.isChecked():
                AntiSpoof_pts = [(mc.pipeR + mc.AntiSpoof) * np.cos(self.l_io), (mc.pipeR + mc.AntiSpoof) * np.sin(self.l_io)]
                p_as = pg.PlotCurveItem(AntiSpoof_pts[0], AntiSpoof_pts[1])
                p_as.setPos(p_coord[0], p_coord[1] + TC)
                p_as.setPen(color='red', width=0.5) #, style=QtCore.Qt.DotLine)
                self.xview.addItem(p_as)
            # inner flags
            self.lifl.setPos(lifl_coord[0], lifl_coord[1] + TC)
            self.rifl.setPos(rifl_coord[0], rifl_coord[1] + TC)
            self.lifl.setBrush(mc.cLeftM)
            self.rifl.setBrush(mc.cRightM)
            self.xview.addItem(self.lifl)
            self.xview.addItem(self.rifl)
            # outer flags
            if mc.ch_FoShow.isChecked():
                self.lofl.setPos(lofl_coord[0], lofl_coord[1] + TC)
                self.rofl.setPos(rofl_coord[0], rofl_coord[1] + TC)
                self.lofl.setBrush(mc.cLeftM)
                self.rofl.setBrush(mc.cRightM)
                self.xview.addItem(self.lofl)
                self.xview.addItem(self.rofl)
            # top - bottom & CL
            p_top = pg.InfiniteLine(p_coord[1] + mc.pipeR + TC, angle=0, movable=False,
                                     pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            p_bot = pg.InfiniteLine(p_coord[1] - mc.pipeR + TC, angle=0, movable=False,
                                     pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            cl = pg.InfiniteLine(mc.min_cx, angle=90, movable=False,
                                 pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            self.xview.addItem(p_top)
            self.xview.addItem(p_bot)
            self.xview.addItem(cl)

            # profile_window
            if mc.port != mc.stbd:
                port_p_win = pg.InfiniteLine(mc.port - mc.pipeR, angle=90, movable=False,
                                     pen=pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                stbd_p_win = pg.InfiniteLine(mc.stbd + mc.pipeR, angle=90, movable=False,
                                     pen=pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                self.xview.addItem(port_p_win)
                self.xview.addItem(stbd_p_win)
                # TOP search window
                c_win = [[mc.port, mc.port, mc.stbd, mc.stbd, mc.port],
                              [mc.low, mc.high, mc.high, mc.low, mc.low]]
                c_win = pg.PlotCurveItem(c_win[0], c_win[1])
                c_win.setPos(0, mc.pipeR + TC)
                c_win.setPen(pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                self.xview.addItem(c_win)
            else:
                done = pg.PlotDataItem(x=[p_coord[0]], y=[p_coord[1]] + TC,
                                       pen=None, symbol='x', symbolSize=10, symbolBrush='yellow')
                self.xview.addItem(done)

            # center plot
            if self.ch_Center.isChecked():
                rect = self.xview.visibleRange()
                self.xview.setRange(xRange=[(mc.min_cx - rect.width() / 2), (mc.min_cx + rect.width() / 2)],
                                    yRange=[(mc.min_cz - rect.height() / 2 + TC), (mc.min_cz + rect.height() / 2) + TC], padding=0) # if padding != 0 it will change viewRect

            # starts/ends of visited parts to plot on Pview & Lview
            visited = mc.flush[mc.flush[:, 11] == 1]
            visited_ixs = (visited[:, 13]).astype('int')

            vis_start, vis_end = visited_ixs[0], visited_ixs[-1]

            visited[1:, 30] = np.diff(visited[:, 13])  # ping No's differences forward
            self.vis_starts_ix = np.insert((visited[:, 13][visited[:, 30] > 1]).astype('int'), 0, vis_start)

            visited[-2::-1, 30] = np.diff(visited[::-1, 13]) # ping No's differences backward
            self.vis_ends_ix = np.append((visited[:, 13][visited[:, 30] < -1]).astype('int'), vis_end)

            pv.UpdateP()


class PV(QtWidgets.QMainWindow, _UI_Pview.Ui_PVIEW):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        # set form
        self.pview.ui.roiBtn.hide()
        self.pview.ui.menuBtn.hide()
        self.pview.ui.roiPlot.hide()
        self.pview.ui.histogram.hide()
        self.pview.getView().setMenuEnabled(False)
        self.pview.getView().invertX(False)
        self.pview.getView().invertY(False)
        # set variables
        self.EdSpot = float(self.t_EdSpot.text())
        self.SmWin = int(self.t_smW.text())

        # set pipetracker selector shape
        self.l_io = np.linspace(0, 2 * np.pi, 50)  # spaced points array for plotting pipe (360 deg / 50 pts)

        # connecting signals
        self.pview.scene.sigMouseMoved.connect(self.mouse_moved)
        self.pview.scene.sigMouseClicked.connect(self.mouse_clicked)
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.clicked.connect(self.POI)
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_Interpolate.clicked.connect(Interpolate)
        self.b_Interpolate.setToolTip('Interpolate TOP 3D (I)')
        self.b_Interpolate.setToolTipDuration(2000)
        self.b_Interpolate.setText('I\u02E3\u02B8\u1DBB')
        self.t_EdSpot.textEdited.connect(self.set_vals)
        self.t_smW.textEdited.connect(self.set_vals)
        self.ch_ShowPT.stateChanged.connect(Update_PT)
        # map 'Smooth PT button sync
        self.b_smoothPT_p.clicked.connect(lambda: Smooth_PT('smoothplan'))
        self.b_smoothPT_p.setToolTip('Smooth pipetracker XY')
        self.b_smoothPT_p.setToolTipDuration(2000)
        self.b_smoothPT_p.setText('S\u02E3\u02B8')
        # map 'Snap XY' button sync
        self.b_snap_h.clicked.connect(lambda: Snap_TOP('snapplan'))
        self.b_snap_h.setText('\u21F2\u02E3\u02B8')
        self.b_snap_h.setToolTip('Snap TOP XY to pipetracker')
        self.b_snap_h.setToolTipDuration(2000)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText() and (Path(e.mimeData().text()).suffix.strip() in mc.extlist):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        fName = e.mimeData().text().strip().replace('file:///', '')
        dropToViewEvent(e, fName)

    def set_vals(self):
        self.EdSpot = float(self.t_EdSpot.text())
        self.SmWin = float(self.t_smW.text())

    def POI(self):
        mc.flush[mc.prno, 29] = 1 if mc.flush[mc.prno, 29] == 0 else 0
        AutoPipe()

    def keyPressEvent(self, e):
        key_pressed(e)

    def keyReleaseEvent(self, e):
        key_pressed(e)

    def mouse_moved(self, e):
        self.cursor = self.pview.view.mapSceneToView(e)
        mc.l_Coord.setText(f'E:{round(self.cursor.x(), 1)}, N:{round(self.cursor.y(), 1)}')
        # pipetracker ROI
        if mc.rb_Pt.isChecked() and mc.Ptflag:
            try:
                self.pview.removeItem(self.selector_p)
            except:
                pass

            # pipetracker selector
            if mc.rb_RejectPT.isChecked():
                pen = pg.mkPen(color='r', width=2)
            else:
                pen = pg.mkPen(color='g', width=2)

            self.selector_p = [[-self.EdSpot / 2, -self.EdSpot / 2, self.EdSpot / 2, self.EdSpot / 2, -self.EdSpot / 2],
                               [-self.EdSpot / 2, self.EdSpot / 2, self.EdSpot / 2, -self.EdSpot / 2, -self.EdSpot / 2]]
            self.selector_p = pg.PlotCurveItem(self.selector_p[0], self.selector_p[1])
            self.selector_p.setPos(self.cursor.x(), self.cursor.y())
            self.selector_p.setPen(pen)
            self.pview.addItem(self.selector_p)

    def mouse_clicked(self, e):
        mc.selpt = np.argmin(((mc.flush[:, 9] - self.cursor.x()) ** 2 + (mc.flush[:, 10] - self.cursor.y()) ** 2) ** 0.5)
        if mc.rb_Pr.isChecked():
            # go to clicked profile
            if e.button() == QtCore.Qt.MouseButton.LeftButton and e.double():
                jump_to_profile()
            # select chunk
            if e.button() == QtCore.Qt.MouseButton.RightButton:
                Select_Chunk()

        # accept/reject pipetracker
        elif mc.rb_Pt.isChecked() and mc.Ptflag:
            ix = np.where((((self.cursor.x() - self.EdSpot / 2) < mc.pipetracker[:, 1]) & (mc.pipetracker[:, 1] < (self.cursor.x() + self.EdSpot / 2))) &
                          (((self.cursor.y() - self.EdSpot / 2) < mc.pipetracker[:, 2]) & (mc.pipetracker[:, 2] < (self.cursor.y() + self.EdSpot / 2))))
            mc.pipetracker[ix, 9] = mc.rb_RejectPT.isChecked()      # reject / accept

            Update_PT()

    def UpdateP(self):
        if mc.ProfileFlag:
            try:         # clear tracks only (tiff still loaded)
                for item in [self.visited, self.li, self.ri, self.lo, self.ro]:
                    for line in item:
                        self.pview.removeItem(line)
                for item in [self.notvisited, self.here, self.POI]:
                    self.pview.removeItem(item)
                for item in [self.cam_in, self.cam_out]:
                    self.pview.removeItem(item)
            except:
                pass

            # current position
            self.here = pg.PlotDataItem(x=[mc.flush[mc.prno, 9]],
                                        y=[mc.flush[mc.prno, 10]],
                                        pen=pg.mkPen(mc.cCurrentProf, width=1), symbol='x', symbolSize=15, symbolBrush=mc.cCurrentProf)

            # camera position
            if mc.ch_ShowCamOffset.isChecked():
                symbsize_0 = int(mc.spb_CamSize.value())
                symbsize_1 = int(symbsize_0 / 2)
                cam_e, cam_n = _F_funcs.Rotation2D(mc.CamOffset, mc.flush[mc.prno, 9], mc.flush[mc.prno, 10], mc.flush[mc.prno, 2] - 90)
                self.cam_in = pg.PlotDataItem(x=[cam_e],
                                              y=[cam_n],
                                              pen=pg.mkPen(mc.cCurrentProf, width=0.1), symbol='o', symbolSize=symbsize_0, symbolBrush=mc.cCurrentProf)
                self.cam_out = pg.PlotDataItem(x=[cam_e],
                                               y=[cam_n],
                                               pen=pg.mkPen(mc.cCurrentProf, width=0.1), symbol='s', symbolSize=symbsize_1)

                for item in [self.cam_in, self.cam_out]:
                    self.pview.addItem(item)

            # POI
            self.POI = pg.PlotDataItem(x=mc.flush[:, 9][mc.flush[:, 29] == 1],
                                       y=mc.flush[:, 10][mc.flush[:, 29] == 1],
                                       pen=None, symbol='x', symbolSize=20, symbolBrush='red')

            # pipe not visited
            self.notvisited = pg.PlotDataItem(x=mc.flush[:, 0][mc.flush[:, 11] == 0],
                                              y=mc.flush[:, 1][mc.flush[:, 11] == 0],
                                              pen=None, symbol='o', symbolSize=4, symbolBrush=mc.cNotVis)

            # pipe visited parts
            self.visited = []
            self.li, self.ri = [], []
            self.lo, self.ro = [], []
            for s, e in zip(xv.vis_starts_ix, xv.vis_ends_ix + 1):
                # top
                self.visited.append(pg.PlotDataItem(x=mc.flush[s:e, 9],
                                                    y=mc.flush[s:e, 10],
                                                    pen=pg.mkPen(mc.cVis, width=2.5), symbol='o', symbolSize=5, symbolBrush=mc.cVis))

                # flags
                if self.ch_ShowFlagL.isChecked():
                    self.li.append(pg.PlotDataItem(x=mc.flush[s:e, 20],
                                                   y=mc.flush[s:e, 21],
                                                   pen=pg.mkPen(mc.cLeftM, width=0.75), symbol='o', symbolSize=2,
                                                   symbolBrush=mc.cLeftM))
                    self.ri.append(pg.PlotDataItem(x=mc.flush[s:e, 22],
                                                   y=mc.flush[s:e, 23],
                                                   pen=pg.mkPen(mc.cRightM, width=0.75), symbol='o', symbolSize=2,
                                                   symbolBrush=mc.cRightM))
                    # outer flags
                    if mc.ch_FoShow.isChecked():
                        self.lo.append(pg.PlotDataItem(x=mc.flush[s:e, 24],
                                                       y=mc.flush[s:e, 25],
                                                       pen=pg.mkPen(mc.cLeftM, width=0.75), symbol='o', symbolSize=2,
                                                       symbolBrush=mc.cLeftM))
                        self.ro.append(pg.PlotDataItem(x=mc.flush[s:e, 26],
                                                       y=mc.flush[s:e, 27],
                                                       pen=pg.mkPen(mc.cRightM, width=0.75), symbol='o', symbolSize=2,
                                                       symbolBrush=mc.cRightM))

            # add items
            for item in [self.visited, self.li, self.ri, self.lo, self.ro]:
                for line in item:
                    self.pview.addItem(line)
            for item in [self.notvisited, self.here, self.POI]:
                self.pview.addItem(item)

            # center plot
            if self.ch_Center.isChecked():
                rect = self.pview.view.viewRect()
                x, y = mc.flush[mc.prno, 9], mc.flush[mc.prno, 10]
                self.pview.view.setRange(
                    xRange=[(x - rect.width() / 2), (x + rect.width() / 2)],
                    yRange=[(y - rect.height() / 2), (y + rect.height() / 2)],
                    padding=0) # if padding != 0 it will change viewRect

            lv.UpdateL()


class LV(QtWidgets.QMainWindow, _UI_Lview.Ui_LVIEW):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        # set form
        self.lview.setMenuEnabled(False)
        #self.move(2200, 0)
        # lock scale 1:1 / determine aspect
        self.lview.setAspectLocked(False)
        self.aspect = self.lview.getViewBox().getAspectRatio()
        self.vb_lview = self.lview.plotItem.vb              # for correct mouse tracking
        self.lview.viewport().installEventFilter(self)      # eventFilter for tracking mouse wheel scroll
        # set variables
        self.EdSpot = float(self.t_EdSpot.text())
        self.SmWin = int(self.t_smW.text())
        self.Lev = float(self.t_Lev.text())
        self.aspect_change_flag = False                     # True if 'Ctrl' key held down / False if released
        self.aspect = 1
        self.winrange = [0, 1]                              # init lview xRange
        # set pipetracker selector shape
        self.l_io = np.linspace(0, 2 * np.pi, 50)  # spaced points array for plotting pipe (360 deg / 50 pts)
        # connecting signals
        self.lview.scene().sigMouseMoved.connect(self.mouse_moved)
        self.lview.scene().sigMouseClicked.connect(self.mouse_clicked)
        self.ch_Aspect.stateChanged.connect(self.chbtns)
        self.ch_Time_Chn.stateChanged.connect(self.chbtns)
        self.b_POI.setText('\u2714')
        self.b_POI.setStyleSheet('color: green')
        self.b_POI.clicked.connect(self.POI)
        self.b_POI.setToolTip('Mark POI')
        self.b_POI.setToolTipDuration(2000)
        self.b_Interpolate.setText('I\u02E3\u02B8\u1DBB')
        self.b_Interpolate.setToolTip('Interpolate TOP 3D (I)')
        self.b_Interpolate.clicked.connect(Interpolate)
        self.b_Interpolate.setToolTipDuration(2000)
        self.t_EdSpot.textEdited.connect(self.set_vals)
        self.t_smW.textEdited.connect(self.set_vals)
        self.t_Lev.textEdited.connect(self.set_vals)
        self.b_levelPT.clicked.connect(Level_PT)
        self.b_levelPT.setText('\u21F3')
        self.b_levelPT.setToolTip('Level pipetracker')
        self.b_levelPT.setToolTipDuration(2000)
        self.ch_ShowPT.stateChanged.connect(Update_PT)
        self.l_scale.setStyleSheet('color: red')
        self.l_scale.setText(f'SCALE 1:{1 / self.aspect:.2f}')
        # map 'Smooth PT Z button sync
        self.b_smoothPT_l.clicked.connect(lambda: Smooth_PT('smoothlong'))
        self.b_smoothPT_l.setText('S\u1DBB')
        self.b_smoothPT_l.setToolTip('Smooth pipetracker Z')
        self.b_smoothPT_l.setToolTipDuration(2000)
        # map 'Snap Z' button sync
        self.b_snap_v.clicked.connect(lambda: Snap_TOP('snaplong'))
        self.b_snap_v.setText('\u21F2\u1DBB')
        self.b_snap_v.setToolTip('Snap TOP Z to pipetracker')
        self.b_snap_v.setToolTipDuration(2000)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText() and (Path(e.mimeData().text()).suffix.strip() in mc.extlist):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        fName = e.mimeData().text().strip().replace('file:///', '')
        dropToViewEvent(e, fName)

    def set_vals(self):
        self.EdSpot = float(self.t_EdSpot.text())
        self.SmWin = float(self.t_smW.text())
        self.Lev = float(self.t_Lev.text())

    def POI(self):
        mc.flush[mc.prno, 29] = 1 if mc.flush[mc.prno, 29] == 0 else 0
        AutoPipe()

    def keyPressEvent(self, e):
        key_pressed(e)

    def keyReleaseEvent(self, e):
        key_pressed(e)

    def eventFilter(self, source, e):
        # set event filter for changing Lview aspect
        if e.type() == QtCore.QEvent.Wheel and self.aspect_change_flag:
            self.ch_Aspect.setChecked(False)
            if e.angleDelta().y() > 0:
                self.aspect *= 1.5
            else:
                self.aspect /= 1.5
            self.lview.setAspectLocked(True, ratio=self.aspect)
            self.lview.setRange(xRange=self.winrange)
            self.l_scale.setText(f'SCALE 1:{1 / self.aspect:.2f}')

        return False

    def mouse_moved(self, e):
        self.cursor = self.vb_lview.mapSceneToView(e)
        mc.l_Coord.setText(f'Ch/T:{round(self.cursor.x(), 1)}, Z:{round(self.cursor.y(), 1)}')
        #self.aspect = self.lview.getViewBox().getAspectRatio()
        # pipetracker ROI
        if mc.rb_Pt.isChecked() and mc.Ptflag: # and not self.ch_Time_Chn.isChecked():
            try:
                self.lview.removeItem(self.selector_l)
            except:
                pass

            # pipetracker selector
            if mc.rb_RejectPT.isChecked():
                pen = pg.mkPen(color='r', width=2)
            else:
                pen = pg.mkPen(color='g', width=2)
            self.selector_l = [[-self.EdSpot / 2, -self.EdSpot / 2, self.EdSpot / 2, self.EdSpot / 2, -self.EdSpot / 2],
                               [-self.EdSpot / (2 / self.aspect), self.EdSpot / (2 / self.aspect), self.EdSpot / (2 / self.aspect), -self.EdSpot / (2 / self.aspect), -self.EdSpot / (2 / self.aspect)]]
            self.selector_l = pg.PlotCurveItem(self.selector_l[0], self.selector_l[1])
            self.selector_l.setPos(self.cursor.x(), self.cursor.y())
            self.selector_l.setPen(pen)
            self.lview.addItem(self.selector_l)

    def mouse_clicked(self, e):
        mc.selpt = np.argmin(np.abs(mc.flush[:, 12] - self.cursor.x()))
        if mc.rb_Pr.isChecked():
            # go to clicked profile
            if e.button() == QtCore.Qt.MouseButton.LeftButton and e.double():
                jump_to_profile()
            # select chunk
            if e.button() == QtCore.Qt.MouseButton.RightButton:
                Select_Chunk()

        # accept/reject pipetracker
        elif mc.rb_Pt.isChecked() and mc.Ptflag: # and not self.ch_Time_Chn.isChecked():
            ax = 0 if self.ch_Time_Chn.isChecked() else 8 # change time/ chainage on Lview
            TP = mc.ch_ApplyTide.isChecked() * mc.pipetracker[:, 7]

            ix = np.where((((self.cursor.x() - self.EdSpot / 2) < mc.pipetracker[:, ax]) & (mc.pipetracker[:, ax] < (self.cursor.x() + self.EdSpot / 2))) &
                          (((self.cursor.y() - self.EdSpot / (2 / self.aspect)) < (mc.pipetracker[:, 3] + mc.pipetracker[:, 11] + TP)) & ((mc.pipetracker[:, 3] + mc.pipetracker[:, 11] + TP) < (self.cursor.y() + self.EdSpot / (2 / self.aspect)))))

            mc.pipetracker[ix, 9] = mc.rb_RejectPT.isChecked()      # reject / accept
            Update_PT()

    def chbtns(self):
        if self.ch_Aspect.isChecked():
            self.lview.setAspectLocked(True)
            lv.l_scale.setText(f'SCALE 1:1')
            self.aspect = 1
        else:
            self.lview.setAspectLocked(False)
            self.aspect = 1

        # Update_PT()

    def UpdateL(self):
        if mc.ProfileFlag:
            ix = 14 if self.ch_Time_Chn.isChecked() else 12 # change time/ KP on Lview
            try:    # clear tracks only (tiff and pipetracker (until changed) still loaded)
                for item in [self.visited_top, self.visited_bop,
                             self.visited_inner, self.visited_outer]:
                    for line in item:
                        self.lview.removeItem(line)
                for item in [self.notvisited_top, self.notvisited_bop, self.here, self.POI]:
                    self.lview.removeItem(item)

            except:
                pass

            # tide for long
            TN = mc.ch_ApplyTide.isChecked() * mc.flush[:, 15][mc.flush[:, 11] == 0]            # not visited
            TC = mc.ch_ApplyTide.isChecked() * mc.flush[mc.prno, 15]                            # current profile
            TP = mc.ch_ApplyTide.isChecked() * mc.flush[:, 15][mc.flush[:, 29] == 1]            # POI

            # current position
            self.here = pg.PlotDataItem(x=[mc.flush[mc.prno, ix]],
                                        y=[mc.flush[mc.prno, 4] + TC],
                                        pen=pg.mkPen(mc.cCurrentProf, width=1), symbol='x', symbolSize=15, symbolBrush=mc.cCurrentProf)

            # POI
            self.POI = pg.PlotDataItem(x=mc.flush[:, ix][mc.flush[:, 29] == 1],
                                       y=mc.flush[:, 4][mc.flush[:, 29] == 1] + TP,
                                       pen=None, symbol='x', symbolSize=20, symbolBrush='red')

            # pipe not visited
            # TOP
            self.notvisited_top = pg.PlotDataItem(x=mc.flush[:, ix][mc.flush[:, 11] == 0],
                                                  y=mc.flush[:, 4][mc.flush[:, 11] == 0] + TN,
                                                  pen=None, symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cNotVis)
            # BOP
            self.notvisited_bop = pg.PlotDataItem(x=mc.flush[:, ix][mc.flush[:, 11] == 0],
                                                  y=mc.flush[:, 4][mc.flush[:, 11] == 0] - mc.pipeD + TN,
                                                  pen=None, symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cNotVis)
            # pipe visited parts
            self.visited_top = []
            self.visited_bop = []
            self.visited_inner = []
            self.visited_outer = []
            for s, e in zip(xv.vis_starts_ix, xv.vis_ends_ix + 1):
                TV = mc.ch_ApplyTide.isChecked() * mc.flush[s:e, 15]  # visited parts
                # TOP
                self.visited_top.append(pg.PlotDataItem(x=mc.flush[s:e, ix],
                                                        y=mc.flush[s:e, 4] + TV,
                                                        pen=pg.mkPen(mc.cVis, width=2), symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cVis))
                # BOP
                self.visited_bop.append(pg.PlotDataItem(x=mc.flush[s:e, ix],
                                                        y=mc.flush[s:e, 4] - mc.pipeD + TV,
                                                        pen=pg.mkPen(mc.cVis, width=2), symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cVis))
                # MADJ
                self.visited_inner.append(pg.PlotDataItem(x=mc.flush[s:e, ix],
                                                          y=np.mean(mc.flush[s:e, [6, 8]], axis=1) + TV,
                                                          pen=pg.mkPen(mc.cMADJ, width=2), symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cMADJ))
                # MSBL
                if mc.ch_FoShow.isChecked():
                    self.visited_outer.append(pg.PlotDataItem(x=mc.flush[s:e, ix],
                                                              y=np.mean(mc.flush[s:e, [17, 19]], axis=1) + TV,
                                                              pen=pg.mkPen(mc.cMSBL, width=2), symbol='o', symbolPen=None, symbolSize=4, symbolBrush=mc.cMSBL))

            # add items
            for item in [self.visited_top, self.visited_bop,
                         self.visited_inner, self.visited_outer]:
                for line in item:
                    self.lview.addItem(line)
            for item in [self.notvisited_top, self.notvisited_bop, self.here, self.POI]:
                self.lview.addItem(item)

            # center plot
            if self.ch_Center.isChecked():
                rect = self.lview.viewRect()
                x, y = mc.flush[mc.prno, ix], mc.flush[mc.prno, 4] + TC
                self.lview.setRange(
                    xRange=[(x - rect.width() / 2), (x + rect.width() / 2)],
                    yRange=[(y - rect.height() / 2), (y + rect.height() / 2)],
                    padding=0)  # if padding != 0 it will change viewRect

            self.winrange = self.lview.viewRange()[0]

'''
class FV(QtWidgets.QMainWindow):
    # evf function widget
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TOP Function')
        self.setWindowIcon(ic_app)
        self.setGeometry(100, 100, 600, 500)
        self.UiComponents()

    def UiComponents(self):
        widget = QWidget()
        self.imv = pg.ImageView()
        self.imv.ui.roiBtn.hide()
        self.imv.ui.menuBtn.hide()
        self.imv.ui.roiPlot.hide()
        self.imv.ui.histogram.hide()
        self.imv.getView().setMenuEnabled(False)
        self.imv.getView().invertX(False)
        self.imv.getView().invertY(False)

        layout = QGridLayout()
        widget.setLayout(layout)
        layout.addWidget(self.imv, 0, 1, 3, 1)
        self.setCentralWidget(widget)
'''

def key_pressed(e):
    if e.type() == 6:
        if e.modifiers() & Qt.ControlModifier:  # 'Ctrl + S' -----MODIFIER
            # save work
            if e.key() == Qt.Key_S:
                foldName = os.path.dirname(mc.profName)
                mc.savework(foldName, '(Fastsave)')
            # autodigiize
            if e.key() == Qt.Key_A:
                AutoRun()

        # step back
        if e.key() == Qt.Key_Z:
            if mc.prno > 0:
                mc.prno -= 1
            AutoPipe()
        # step fwd
        if e.key() == Qt.Key_X:
            if mc.prno < mc.no_of_prof - 1:
                mc.prno += 1
            AutoPipe()
        # to end
        if e.key() == Qt.Key_End:
            mc.prno = mc.no_of_prof - 1
            AutoPipe()
        # to start
        if e.key() == Qt.Key_Home:
            mc.prno = 0
            AutoPipe()
        # to last visited
        if e.key() == Qt.Key_E:
            for i in range(mc.prno, mc.no_of_prof):
                if mc.flush[i, 11] == 0:
                    mc.prno = i - 1
                    break
            AutoPipe()
        # reset fwd
        if e.key() == Qt.Key_0:
            if mc.ChunkSelected:
                chs, che = mc.chunk[0], mc.chunk[1]
            else:
                chs, che = mc.prno + 1, mc.no_of_prof

            mc.flush[chs:che + 1, 11] = 0
            mc.flush[chs:che + 1, 9] = mc.flush[chs:che + 1, 0]
            mc.flush[chs:che + 1, 10] = mc.flush[chs:che + 1, 1]
            mc.flush[chs:che + 1, 4] = mc.flush[chs, 4]

            if mc.ChunkSelected:
                mc.chunk = [-1, -1]
                mc.ChunkSelected = False
                Update_Chunk('action_completed')
            else:
                xv.UpdateX()

        # snap TOP
        if e.key() == Qt.Key_Space:
            mc.xini = xv.cursor.x()
            mc.flush[mc.prno][11] = 0  # flag profile 'not visited' for manual edit
            AutoPipe()
        # show pipe assistant
        if e.key() == Qt.Key_C:
            mc.ShowPipe = True if mc.ShowPipe == False else False
            if mc.ShowPipe == False:
                xv.b_assist.setStyleSheet('color: red')
            else:
                xv.b_assist.setStyleSheet('color: green')
            xv.UpdateX()
        # interpolte
        if e.key() == Qt.Key_I:
            Interpolate()
        # switch PT edit accept / reject
        if e.key() == Qt.Key_Alt and mc.rb_Pt.isChecked():
            mc.rb_RejectPT.setChecked(True) if not mc.rb_RejectPT.isChecked() else mc.rb_AcceptPT.setChecked(True)

    # LView aspect change flag Ctrl+mouse wheel
    if e.key() == Qt.Key_Control and e.type() == 6:         # Ctrl pressed
        lv.aspect_change_flag = True
    if e.key() == Qt.Key_Control and e.type() == 7:         # Ctrl released
        lv.aspect_change_flag = False


def dropToViewEvent(e, fName):
    if Path(fName).suffix.strip().lower() in ['.xpa', '.cr2']:
        mc.loadprof(fName)
    elif Path(fName).suffix.strip().lower() in ['.tid']:
        mc.loadtide(fName)
    elif Path(fName).suffix.strip().lower() in ['.wrk']:
        mc.loadwork(fName)
    elif Path(fName).suffix.strip().lower() in ['.bin']:
        mc.loadlayout(fName)
    elif Path(fName).suffix.strip().lower() in ['.pip', '.fug', '.spt']:
        mc.loadpt(fName)
    elif Path(fName).suffix.strip().lower() in ['.tif', '.tiff','.png']:
        mc.loadtif(fName)
    elif Path(fName).suffix.strip().lower() in ['.pll']:
        mc.loadDV(fName)


def AutoPipe():
    if mc.ProfileFlag:
        # read profile array (for AutoPipe and AutoFlag)
        mc.profile = mc.profiles[mc.prno][::(mc.weed)]

        # reset xini to centre of profile if profile is far from xini (wrong profile export)
        if not(np.min(mc.profile[:, 0]) < mc.xini < np.max(mc.profile[:, 0])):
            mc.xini = np.mean(mc.profile[:, 0])

        # if already visited (or when opening wrk file) - search window is not plotted on Xview
        # this works if no AutoPipe is running and port/stbd/high/low not computed but needed
        mc.port = mc.stbd = mc.min_cx = mc.flush[mc.prno, 3]
        mc.high = mc.low = mc.min_cz = mc.flush[mc.prno, 4]

        # AutoPipe only runs if: profile not visited AND no ManualPipe selected
        # or DoPipe - autopipe
        if (not mc.flush[mc.prno, 11] and not mc.ManualPipe) or mc.DoPipe:
            # profile window (part of profile used for TOP search = xini +- HWin/2 +- pipeR)
            prof_win = np.where((mc.xini - mc.HWin / 2 - mc.pipeR <= mc.profile[:, 0]) &
                                (mc.profile[:, 0] <= mc.xini + mc.HWin / 2 + mc.pipeR))[0]
            # TOP search window (profile_window +- pipeR; minZ (in window) + VWin = maxZ)
            mc.port = mc.xini - mc.HWin / 2
            mc.stbd = mc.xini + mc.HWin / 2
            cent_win = np.where((mc.port <= mc.profile[:, 0]) & (mc.profile[:, 0] <= mc.stbd))[0]
            mc.high = max(mc.profile[cent_win, 1] - mc.pipeR)
            mc.low = mc.high - mc.VWin

            # evenly spaced h/v centre search spots - search grid
            x_grid = np.arange(mc.port, mc.stbd, mc.Res)
            z_grid = np.arange(mc.low, mc.high, mc.Res)

            # evaluation function array
            # used points = points within 'wall'(in-wall->out-wall) & 'segment'
            # 0: no of used points - accumulated for grid node
            # 1: d**2 of profile points to pipe wall - accumulated for grid node
            # 2: d**2 of profile points to centre - accumulated for grid node
            # 3: eval factor = (d_sq_wall * d_sq_centre / in_wall) ** in_wall - minimum used
            evf = np.zeros((len(x_grid) * len(z_grid), 4))
            evf.astype(Decimal)

            col = 0
            for cx in x_grid:          # pipe centre dx
                row = 0
                for cz in z_grid:      # pipe centre z
                    # No of ix in evf array
                    cell = col * len(z_grid) + row
                    # distances profile points to pipe C where profile points are higher than pipe C (to reject lower semicircle)
                    point_to_c = ((cx - mc.profile[prof_win, 0][mc.profile[prof_win, 1] >= cz]) ** 2 +
                                  (cz - mc.profile[prof_win, 1][mc.profile[prof_win, 1] >= cz]) ** 2) ** 0.5
                    # distances array where points are within wall
                    point_to_c_within_wall = point_to_c[(mc.inWall * mc.pipeR <= point_to_c) &
                                                               (point_to_c <= mc.outWall * mc.pipeR)]
                    # filling evf array
                    evf[cell, 0] = len(point_to_c_within_wall)
                    evf[cell, 1] = Decimal(np.sum((point_to_c_within_wall - mc.inWall * mc.pipeR) ** 2))
                    evf[cell, 2] = Decimal(np.sum(point_to_c_within_wall ** 2))

                    row += 1
                col += 1

            # +++++++  E V A L  F U N C T I O N
            evf[:, 1][evf[:, 1] == 0] = 10000
            evf[:, 2][evf[:, 2] == 0] = 10000

            evf[:, 3] = ((evf[:, 1] * evf[:, 2]) / evf[:, 0]) ** evf[:, 0]
            min_evf = np.argmin(evf[:, 3])

            '''
            ###################### this is for function widget
            # evf function widget
            evf_3 = np.log10(evf[:, 3]).reshape(len(x_grid), len(z_grid))
            cmap = pg.colormap.get('CET-L17')
            fv.imv.setImage(evf_3)
            fv.imv.setColorMap(cmap)
            ######################
            '''

            # calc min cx/cz node (pipe C)
            min_col = math.floor(min_evf / len(z_grid))
            min_row = min_evf - min_col * len(z_grid)

            mc.min_cx = round(x_grid[min_col], 4)
            mc.min_cz = round(z_grid[min_row], 4)

            # write to flush: top_e, top_n
            ref_east, ref_north, hdg = mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], mc.flush[mc.prno, 2]
            # top
            top = _F_funcs.Rotation2D(mc.min_cx, mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], hdg)
            mc.flush[mc.prno, 9] = top[0]
            mc.flush[mc.prno, 10] = top[1]

            # xini for next profile
            mc.xini = mc.min_cx

            # write to flush: top_x, top_z
            mc.flush[mc.prno, 3] = mc.min_cx
            mc.flush[mc.prno, 4] = mc.flush[mc.prno:, 4][mc.flush[mc.prno:, 11] == 0] = mc.min_cz + mc.pipeR

        mc.ManualPipe = False       # reset flag if manual pipe placement was done

        AutoFlags()


def AutoFlags():
    # AutoFlags only runs if: profile unvisited OR running [interpolation / snap to PT] OR AutoRun
    if not mc.flush[mc.prno, 11] or mc.Interpflag or mc.DoPipe:
        mc.min_cx = mc.flush[mc.prno, 3]
        mc.min_cz = mc.flush[mc.prno, 4] - mc.pipeR
        # inner flags - initial position
        mc.li_x, mc.ri_x = mc.min_cx - mc.FlD, mc.min_cx + mc.FlD
        mc.li_z = mc.ri_z = mc.min_cz
        # outer flags - initial position
        mc.lo_x, mc.ro_x = mc.min_cx - mc.FlD, mc.min_cx + mc.FlD
        mc.lo_z = mc.ro_z = mc.min_cz


        try:
            # set extended / narrow spot
            if mc.rb_Fadapt.isChecked():
                # extended spot -+ AdPadli_x(ri_x) +-inflag_patch to -+inflag_patch - for adaptive mode
                mc.li_spot = np.where((mc.min_cx - mc.FlD - mc.FlP <= mc.profile[:, 0]) & (mc.profile[:, 0] <= mc.min_cx - mc.AdPad))
                mc.ri_spot = np.where((mc.min_cx + mc.AdPad <= mc.profile[:, 0]) & (mc.profile[:, 0] <= mc.min_cx + mc.FlD + mc.FlP))
            else:
                # narrow spot li_x(ri_x)+-inflag_patch to inflag - for other modes
                mc.li_spot = np.where((mc.min_cx - mc.FlD - mc.FlP <= mc.profile[:, 0]) & (mc.profile[:, 0] <= mc.min_cx - mc.FlD))
                mc.ri_spot = np.where((mc.min_cx + mc.FlD <= mc.profile[:, 0]) & (mc.profile[:, 0] <= mc.min_cx + mc.FlD + mc.FlP))

            if len(mc.li_spot[0]) != 0 and len(mc.ri_spot[0]) != 0:
                # if in bad profile low number of datapoints (not hitting flag patch)
                if mc.rb_Fmean.isChecked():
                    # no point snapping for 'mean'
                    mc.li_x, mc.ri_x = mc.min_cx - mc.FlD, mc.min_cx + mc.FlD
                    mc.li_z, mc.ri_z = np.mean(mc.profile[mc.li_spot][:, 1]), np.mean(mc.profile[mc.ri_spot][:, 1])

                elif mc.rb_Fmin.isChecked():
                    if not mc.ch_FiSnap.isChecked():
                        mc.li_x, mc.ri_x = mc.min_cx - mc.FlD, mc.min_cx + mc.FlD
                        mc.li_z, mc.ri_z = np.max(mc.profile[mc.li_spot][:, 1]), np.max(mc.profile[mc.ri_spot][:, 1])
                    else:
                        mc.li_ix, mc.ri_ix = np.argmax(mc.profile[mc.li_spot][:, 1]), np.argmax(mc.profile[mc.ri_spot][:, 1])
                        mc.li_x, mc.ri_x = mc.profile[mc.li_spot][mc.li_ix, 0], mc.profile[mc.ri_spot][mc.ri_ix, 0]
                        mc.li_z, mc.ri_z = mc.profile[mc.li_spot][mc.li_ix, 1], mc.profile[mc.ri_spot][mc.ri_ix, 1]

                elif mc.rb_Fmax.isChecked():
                    if not mc.ch_FiSnap.isChecked():
                        mc.li_x, mc.ri_x = mc.min_cx - mc.FlD, mc.min_cx + mc.FlD
                        mc.li_z, mc.ri_z = np.min(mc.profile[mc.li_spot][:, 1]), np.min(mc.profile[mc.ri_spot][:, 1])
                    else:
                        mc.li_ix, mc.ri_ix = np.argmin(mc.profile[mc.li_spot][:, 1]), np.argmin(mc.profile[mc.ri_spot][:, 1])
                        mc.li_x, mc.ri_x = mc.profile[mc.li_spot][mc.li_ix, 0], mc.profile[mc.ri_spot][mc.ri_ix, 0]
                        mc.li_z, mc.ri_z = mc.profile[mc.li_spot][mc.li_ix, 1], mc.profile[mc.ri_spot][mc.ri_ix, 1]

                elif mc.rb_Fadapt.isChecked():
                    # distances from point to pipe centre
                    li_d = ((mc.profile[mc.li_spot][:, 0] - mc.min_cx) ** 2 + (mc.profile[mc.li_spot][:, 1] - mc.min_cz) ** 2) ** 0.5
                    ri_d = ((mc.profile[mc.ri_spot][:, 0] - mc.min_cx) ** 2 + (mc.profile[mc.ri_spot][:, 1] - mc.min_cz) ** 2) ** 0.5
                    # set d == 1000 if within pipe + anti-spoof (to reject from min dist)
                    li_d[:][li_d[:] < mc.AntiSpoof + mc.pipeR] = 1000
                    ri_d[:][ri_d[:] < mc.AntiSpoof + mc.pipeR] = 1000

                    flagdetected = False        # !!! True if adaptive algo works; False otherwise
                    for dist, flagspot, side in zip([li_d, ri_d],
                                                    [mc.profile[mc.li_spot], mc.profile[mc.ri_spot]],
                                                    ['l', 'r']):
                        # closest point to pipe (outside wall+antispoof)
                        closest_ix = np.argmin(dist)
                        closest_dx, closest_z = flagspot[closest_ix, 0], flagspot[closest_ix, 1]

                        if mc.min_cz - mc.pipeR - mc.AntiSpoof <= closest_z < mc.min_cz + mc.pipeR + mc.AntiSpoof:
                            # if closest point z is within pipe centre z +- R (& AntiSpoof)
                            # takes closest point
                            fl_x, fl_z = closest_dx, closest_z
                            flagdetected = True
                        else:
                            if closest_z > mc.min_cz + mc.pipeR + mc.AntiSpoof:
                                # if closest profile point z is higher than pipe (& AntiSpoof)
                                # takes point closest to min_cx
                                if len(flagspot[:, 0]) != 0:
                                    fl_ix = np.argmin(np.abs(flagspot[:, 0] - mc.min_cx))
                                    fl_x, fl_z = flagspot[fl_ix, 0], flagspot[fl_ix, 1]
                                    flagdetected = True
                            else:
                                # if closest profile point z is lower than pipe (& AntiSpoof)
                                # takes closest point ot min_cx where z < lower than pipe wall (& antispoof)
                                if len(flagspot[:, 0][flagspot[:, 1] < mc.min_cz - mc.pipeR]) != 0:
                                    fl_ix = np.argmin(np.abs(flagspot[:, 0][flagspot[:, 1] < mc.min_cz - mc.pipeR] - mc.min_cx))
                                    fl_x = (flagspot[:][flagspot[:, 1] < mc.min_cz - mc.pipeR])[fl_ix, 0]
                                    fl_z = (flagspot[:][flagspot[:, 1] < mc.min_cz - mc.pipeR])[fl_ix, 1]
                                    flagdetected = True

                        if side == 'l' and flagdetected:
                            mc.li_x, mc.li_z = fl_x, fl_z
                        if side == 'r' and flagdetected:
                            mc.ri_x, mc.ri_z = fl_x, fl_z

            # outer flags
            # define D of outer flag
            l_end, r_end = mc.profile[0, 0], mc.profile[-1, 0]
            if mc.rb_FoDist.isChecked():
                l_Dist = r_Dist = mc.FoDist
            if mc.rb_FoPers.isChecked():
                l_Dist, r_Dist = (mc.FoPers * (mc.min_cx - l_end) / 100,
                                  mc.FoPers * (r_end - mc.min_cx) / 100)

            mc.lo_ix = np.argmin(np.abs(mc.profile[:, 0] - (mc.min_cx - l_Dist)))
            mc.ro_ix = np.argmin(np.abs(mc.profile[:, 0] - (mc.min_cx + r_Dist)))
            mc.lo_z, mc.ro_z = mc.profile[mc.lo_ix, 1], mc.profile[mc.ro_ix, 1]

            if not mc.ch_FoSnap.isChecked():
                mc.lo_x, mc.ro_x = mc.min_cx - l_Dist, mc.min_cx + r_Dist
            else:
                mc.lo_x, mc.ro_x = mc.profile[mc.lo_ix, 0], mc.profile[mc.ro_ix, 0]

        except:
            pass

        # write to flush flags x & z
        mc.flush[mc.prno, 5] = mc.flush[mc.prno:, 5][mc.flush[mc.prno:, 11] == 0] = mc.li_x
        mc.flush[mc.prno, 6] = mc.flush[mc.prno:, 6][mc.flush[mc.prno:, 11] == 0] = mc.li_z
        mc.flush[mc.prno, 7] = mc.flush[mc.prno:, 7][mc.flush[mc.prno:, 11] == 0] = mc.ri_x
        mc.flush[mc.prno, 8] = mc.flush[mc.prno:, 8][mc.flush[mc.prno:, 11] == 0] = mc.ri_z
        mc.flush[mc.prno, 16] = mc.flush[mc.prno:, 16][mc.flush[mc.prno:, 11] == 0] = mc.lo_x
        mc.flush[mc.prno, 17] = mc.flush[mc.prno:, 17][mc.flush[mc.prno:, 11] == 0] = mc.lo_z
        mc.flush[mc.prno, 18] = mc.flush[mc.prno:, 18][mc.flush[mc.prno:, 11] == 0] = mc.ro_x
        mc.flush[mc.prno, 19] = mc.flush[mc.prno:, 19][mc.flush[mc.prno:, 11] == 0] = mc.ro_z

        # flags en
        ref_east, ref_north, hdg = mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], mc.flush[mc.prno, 2]
        # left inner flag
        li_en = _F_funcs.Rotation2D(mc.li_x, ref_east, ref_north, hdg)
        li_e, li_n = round(li_en[0], 3), round(li_en[1], 3)
        # right inner flag
        ri_en = _F_funcs.Rotation2D(mc.ri_x, ref_east, ref_north, hdg)
        ri_e, ri_n = round(ri_en[0], 3), round(ri_en[1], 3)
        # left outer flag
        lo_en = _F_funcs.Rotation2D(mc.lo_x, ref_east, ref_north, hdg)
        lo_e, lo_n = round(lo_en[0], 3), round(lo_en[1], 3)
        # right inner flag
        ro_en = _F_funcs.Rotation2D(mc.ro_x, ref_east, ref_north, hdg)
        ro_e, ro_n = round(ro_en[0], 3), round(ro_en[1], 3)

        # write to flash flags e & n
        mc.flush[mc.prno, 20] = li_e
        mc.flush[mc.prno, 21] = li_n
        mc.flush[mc.prno, 22] = ri_e
        mc.flush[mc.prno, 23] = ri_n
        mc.flush[mc.prno, 24] = lo_e
        mc.flush[mc.prno, 25] = lo_n
        mc.flush[mc.prno, 26] = ro_e
        mc.flush[mc.prno, 27] = ro_n

        # write to flash flag = 'visited'
        mc.flush[mc.prno, 11] = 1

    if not mc.Interpflag and not mc.DoPipe:
        xv.UpdateX()


def ManualFlags(lfl_x, lfl_z, rfl_x, rfl_z, ToEdit):
    # flags en
    ref_east, ref_north, hdg = mc.flush[mc.prno, 0], mc.flush[mc.prno, 1], mc.flush[mc.prno, 2]
    # left inner flag
    lfl_en = _F_funcs.Rotation2D(lfl_x, ref_east, ref_north, hdg)
    lfl_e, lfl_n = round(lfl_en[0], 3), round(lfl_en[1], 3)
    # right inner flag
    rfl_en = _F_funcs.Rotation2D(rfl_x, ref_east, ref_north, hdg)
    rfl_e, rfl_n = round(rfl_en[0], 3), round(rfl_en[1], 3)

    if ToEdit == 'Inner':
        a, b, c, d, e, f, g, h = 5, 6, 7, 8, 20, 21, 22, 23
    if ToEdit == 'Outer':
        a, b, c, d, e, f, g, h = 16, 17, 18, 19, 24, 25, 26, 27

    mc.flush[mc.prno, a] = mc.flush[mc.prno:, a][mc.flush[mc.prno:, 11] == 0] = lfl_x
    mc.flush[mc.prno, b] = mc.flush[mc.prno:, b][mc.flush[mc.prno:, 11] == 0] = lfl_z
    mc.flush[mc.prno, c] = mc.flush[mc.prno:, c][mc.flush[mc.prno:, 11] == 0] = rfl_x
    mc.flush[mc.prno, d] = mc.flush[mc.prno:, d][mc.flush[mc.prno:, 11] == 0] = rfl_z
    mc.flush[mc.prno, e] = mc.flush[mc.prno:, e][mc.flush[mc.prno:, 11] == 0] = lfl_e
    mc.flush[mc.prno, f] = mc.flush[mc.prno:, f][mc.flush[mc.prno:, 11] == 0] = lfl_n
    mc.flush[mc.prno, g] = mc.flush[mc.prno:, g][mc.flush[mc.prno:, 11] == 0] = rfl_e
    mc.flush[mc.prno, h] = mc.flush[mc.prno:, h][mc.flush[mc.prno:, 11] == 0] = rfl_n

    xv.UpdateX()


def jump_to_profile():
    mc.ChunkSelected = False  # chunk not selected
    mc.chunk = [-1, -1]
    mc.prno = mc.selpt
    del mc.selpt
    AutoPipe()


def Interpolate():
    # interplote chunk top e, n, z
    if mc.ChunkSelected:
        chs, che = mc.chunk[0], mc.chunk[1]
        chs_e, che_e = mc.flush[chs, 9], mc.flush[che, 9]
        chs_n, che_n = mc.flush[chs, 10], mc.flush[che, 10]
        chs_z, che_z = mc.flush[chs, 4], mc.flush[che, 4]
        chs_ch, che_ch = mc.flush[chs, 12], mc.flush[che, 12]
        mc.flush[chs:che + 1, 9] = np.interp(mc.flush[chs:che + 1, 13],
                                             [chs, che], [chs_e, che_e])
        mc.flush[chs:che + 1, 10] = np.interp(mc.flush[chs:che + 1, 13],
                                              [chs, che], [chs_n, che_n])
        mc.flush[chs:che + 1, 4] = np.interp(mc.flush[chs:che + 1, 13],
                                             [chs, che], [chs_z, che_z])

        UpdateMinCX_Flags(chs, che)


def UpdateMinCX_Flags(s, e):
    if mc.ProfileFlag:
        # new min_cx distance
        new_dist = ((mc.flush[s:e + 1, 0] - mc.flush[s:e + 1, 9]) ** 2 +
                    (mc.flush[s:e + 1, 1] - mc.flush[s:e + 1, 10]) ** 2) ** 0.5

        # new min_cx (min_cx distance projected to profile)
        brg = _F_funcs.Bearing((mc.flush[s:e + 1, 9] - mc.flush[s:e + 1, 0]), (mc.flush[s:e + 1, 10] - mc.flush[s:e + 1, 1]))
        mc.flush[s:e + 1, 3] = new_dist * np.sin(brg - np.deg2rad(mc.flush[s:e + 1, 2]))

        # set visited (prevents changing TOP in AutoPipe() but re-sets flags based on Interpolation flag)
        mc.flush[s:e + 1, 11] = 1

        mc.Interpflag = True
        for i in range(s, e + 1):
            mc.prno = i  # set profile_no and min_cx for re-placing flags
            AutoPipe()
        mc.Interpflag = False

        mc.chunk[0], mc.chunk[1] = -1, -1
        mc.ChunkSelected = False

        Update_Chunk('action_completed')


def AutoRun():
    if mc.ChunkSelected:
        s, e = mc.chunk[0], mc.chunk[1]
    else:
        s, e = mc.prno, mc.no_of_prof - 1

    mc.DoPipe = True
    for mc.prno in range(s, e + 1):
        AutoPipe()
    mc.DoPipe = False

    mc.showwarn('Autorun completed')
    Update_Chunk('action_completed')


def FindPtGaps():
    # search starts/ends of accepted parts based on min Pt gap criteria
    mc.PtGap = float(mc.t_PtGap.text())

    accepted = mc.pipetracker[mc.pipetracker[:, 9] == 0]
    accepted_ixs = (accepted[:, 10]).astype('int')

    acc_start, acc_end = accepted_ixs[0], accepted_ixs[-1]

    accepted[1:, 13] = np.diff(accepted[:, 12])         # chainage differences forward
    acc_starts_ix = np.insert((accepted[:, 10][accepted[:, 13] > mc.PtGap]).astype('int'), 0, acc_start)

    accepted[-2::-1, 13] = np.diff(accepted[::-1, 12])  # chainage differences backward
    acc_ends_ix = np.append((accepted[:, 10][accepted[:, 13] < -mc.PtGap]).astype('int'), acc_end)

    return(acc_starts_ix, acc_ends_ix)


def Smooth_PT(smooth):
    if mc.Ptflag and mc.rb_Pt.isChecked():
        sm_win = int(pv.SmWin) if smooth == 'smoothplan' else int(lv.SmWin)
        filt = np.ones(sm_win)
        mov = sm_win // 2

        acc_starts_ix, acc_ends_ix = FindPtGaps()

        for s, e in zip(acc_starts_ix, acc_ends_ix):
            _for_smooth = mc.pipetracker[s + 1: e + 1][mc.pipetracker[s + 1: e + 1, 9] == 0]
            if len(_for_smooth) > 2 * sm_win:       #!!!! only smoothing if section > window +- margin (window/2)
                if smooth == 'smoothplan':                         # smoothing plan
                    if sm_win != 0:                 # smooth
                        _for_smooth[:, 4][mov:-mov] = (np.convolve(_for_smooth[:, 1], filt, 'same') / sm_win)[mov:-mov]
                        _for_smooth[:, 5][mov:-mov] = (np.convolve(_for_smooth[:, 2], filt, 'same') / sm_win)[mov:-mov]
                        mc.pipetracker[s + 1: e + 1, 4][mc.pipetracker[s + 1: e + 1, 9] == 0] = _for_smooth[:, 4]
                        mc.pipetracker[s + 1: e + 1, 5][mc.pipetracker[s + 1: e + 1, 9] == 0] = _for_smooth[:, 5]
                elif smooth == 'smoothlong':                       # smoothing depth
                    if sm_win != 0:                 # smooth
                        _for_smooth[:, 6][mov:-mov] = (np.convolve(_for_smooth[:, 3], filt, 'same') / sm_win)[mov:-mov]
                        mc.pipetracker[s + 1: e + 1, 6][mc.pipetracker[s + 1: e + 1, 9] == 0] = _for_smooth[:, 6]

        if sm_win == 0:  # reset all but rejected
            mc.pipetracker[:, 4] = mc.pipetracker[:, 1]
            mc.pipetracker[:, 5] = mc.pipetracker[:, 2]
            mc.pipetracker[:, 6] = mc.pipetracker[:, 3]
            mc.pipetracker[:, 11] = 0

        lv.t_Lev.setText('0.0')
        lv.Lev = 0

        ReChain()
        Update_PT()


def Level_PT():
    mc.pipetracker[:, 11] = lv.Lev
    Update_PT()


def Snap_TOP(snap):
    # snap top e, n, z to pt by KP
    if mc.Ptflag:
        acc_starts_ix, acc_ends_ix = FindPtGaps()

        if mc.ChunkSelected:
            chs, che = mc.chunk[0], mc.chunk[1]
        else:
            chs, che = 0, mc.no_of_prof - 1

        for s, e in zip(acc_starts_ix, acc_ends_ix):
            if (s <= che) & (chs <= e):
                _p_part = (mc.flush[chs:che + 1, 13][(s <= mc.flush[chs:che + 1, 13]) & (mc.flush[chs:che + 1, 13] <= e)]).astype('int')

                if snap == 'snapplan':
                    mc.flush[_p_part, 9] = np.interp(mc.flush[_p_part, 12],                                 # flush KP
                                                     mc.pipetracker[:, 8][mc.pipetracker[:, 9] == 0],       # pt KP
                                                     mc.pipetracker[:, 4][mc.pipetracker[:, 9] == 0])       # pt E
                    mc.flush[_p_part, 10] = np.interp(mc.flush[_p_part, 12],                                # flush KP
                                                      mc.pipetracker[:, 8][mc.pipetracker[:, 9] == 0],      # pt KP
                                                      mc.pipetracker[:, 5][mc.pipetracker[:, 9] == 0])      # pt N

                if snap == 'snaplong':
                    mc.flush[_p_part, 4] = np.interp(mc.flush[_p_part, 12],                                 # flush KP
                                                     mc.pipetracker[:, 8][mc.pipetracker[:, 9] == 0],       # pt KP
                                                     mc.pipetracker[:, 6][mc.pipetracker[:, 9] == 0] +      # pt smoothed Z
                                                     mc.pipetracker[:, 11][mc.pipetracker[:, 9] == 0])      # pt v shift

                UpdateMinCX_Flags(_p_part[0], _p_part[-1])


def ReChain():
    if mc.Ptflag:
        mc.pipetracker[:, 8] = _F_kp_to_point.go(mc.flush[:, [9, 10, 12]], mc.pipetracker[:, [4, 5]])[:, 2]
        # sorting by KP
        mc.pipetracker = mc.pipetracker[mc.pipetracker[:, 8].argsort()]
        # filling sequential point no to pipetracker filed 10
        mc.pipetracker[:, 10] = np.arange(len(mc.pipetracker))
        # re-compute chainage
        mc.pipetracker[1:, 12] = np.cumsum((np.diff(mc.pipetracker[:, 1]) ** 2 +
                                            np.diff(mc.pipetracker[:, 2]) ** 2) ** 0.5)


def Select_Chunk():
    if mc.ProfileFlag:
        if mc.ChunkSelected or mc.chunk[0] == -1:
            # selecting first point
            mc.chunk[0] = int(mc.flush[mc.selpt, 13])
            mc.ChunkSelected = False
            Update_Chunk('deselected')
            Update_Chunk('point_selected')
        elif not mc.ChunkSelected and mc.chunk[0] != -1:
            # selecting second point
            if mc.selpt != mc.chunk[0]:
                mc.chunk[1] = int(mc.flush[mc.selpt, 13])
            mc.chunk.sort()
            mc.ChunkSelected = True
            Update_Chunk('chunk_selected')


def Update_Chunk(action):
    ix = 14 if lv.ch_Time_Chn.isChecked() else 12  # select time/ KP on Lview

    if action == 'deselected':
        try:
            pv.pview.removeItem(pv.chunk)
            lv.lview.removeItem(lv.chunk)
        except:
            pass
    
    if action == 'point_selected':
        TP = mc.ch_ApplyTide.isChecked() * mc.flush[mc.selpt, 15]  # current profile
        pv.selected = pg.PlotDataItem(x=[mc.flush[mc.selpt, 9]], y=[mc.flush[mc.selpt, 10]],
                                      pen=pg.mkPen('b', width=1), symbol='o', symbolSize=10, symbolBrush='yellow')
        lv.selected = pg.PlotDataItem(x=[mc.flush[mc.selpt, ix]], y=[mc.flush[mc.selpt, 4]] + TP,
                                      pen=pg.mkPen('b', width=1), symbol='o', symbolSize=10, symbolBrush='yellow')
        pv.pview.addItem(pv.selected)
        lv.lview.addItem(lv.selected)

    if action == 'chunk_selected':
        pv.pview.removeItem(pv.selected)
        lv.lview.removeItem(lv.selected)

        chs, che = mc.chunk[0], mc.chunk[1]
        TH = mc.ch_ApplyTide.isChecked() * mc.flush[chs:che + 1, 15]
        pv.chunk = pg.PlotDataItem(x=mc.flush[chs:che + 1, 9], y=mc.flush[chs:che + 1, 10],
                                   pen=pg.mkPen('yellow', width=5), symbol=None)
        lv.chunk = pg.PlotDataItem(x=mc.flush[chs:che + 1, ix], y=mc.flush[chs:che + 1, 4] + TH,
                                   pen=pg.mkPen('yellow', width=5), symbol=None)
        pv.pview.addItem(pv.chunk)
        lv.lview.addItem(lv.chunk)

    if action == 'action_completed':
        try:
            pv.pview.removeItem(pv.chunk)
            lv.lview.removeItem(lv.chunk)
        except:
            pass

        xv.UpdateX()


def Update_PT():
    # update PT view (accepted / rejected / levelled)
    if mc.Ptflag:
        ix = 0 if lv.ch_Time_Chn.isChecked() else 8  # change time/ chainage on Lview
        TP_all = mc.ch_ApplyTide.isChecked() * mc.pipetracker[:, 7]
        TP_acc = mc.ch_ApplyTide.isChecked() * mc.pipetracker[:, 7][mc.pipetracker[:, 9] == 0]
        TP_rej = mc.ch_ApplyTide.isChecked() * mc.pipetracker[:, 7][mc.pipetracker[:, 9] == 1]

        try:
            pv.pview.removeItem(pv.pview.pt_all)
            pv.pview.removeItem(pv.pview.pt_rej)
            pv.pview.removeItem(pv.pview.pt_acc)
            lv.lview.removeItem(lv.lview.pt_all)
            lv.lview.removeItem(lv.lview.pt_rej)
            lv.lview.removeItem(lv.lview.pt_acc)
        except:
            pass

        if pv.ch_ShowPT.isChecked():
            # plan view
            pv.pview.pt_acc = pg.PlotDataItem(x=mc.pipetracker[:, 4][mc.pipetracker[:, 9] == 0],
                                              y=mc.pipetracker[:, 5][mc.pipetracker[:, 9] == 0],
                                              pen=pg.mkPen(mc.cPipetracker, width=2), symbol='o', symbolSize=4, symbolBrush=mc.cPipetracker)
            pv.pview.pt_rej = pg.PlotDataItem(x=mc.pipetracker[:, 4][mc.pipetracker[:, 9] == 1],
                                              y=mc.pipetracker[:, 5][mc.pipetracker[:, 9] == 1],
                                              pen=None, symbol='o', symbolSize=4, symbolBrush=(255, 0, 0, 255))
            pv.pview.pt_all = pg.PlotDataItem(x=mc.pipetracker[:, 4],
                                              y=mc.pipetracker[:, 5],
                                              pen=None, symbol='o', symbolSize=1, symbolBrush=(100, 100, 100, 255))
            pv.pview.addItem(pv.pview.pt_all)
            pv.pview.addItem(pv.pview.pt_rej)
            pv.pview.addItem(pv.pview.pt_acc)

        if lv.ch_ShowPT.isChecked():
            # long view
            lv.lview.pt_acc = pg.PlotDataItem(x=mc.pipetracker[:, ix][mc.pipetracker[:, 9] == 0],
                                              y=mc.pipetracker[:, 6][mc.pipetracker[:, 9] == 0] +
                                                mc.pipetracker[:, 11][mc.pipetracker[:, 9] == 0] + TP_acc,
                                              pen=pg.mkPen(mc.cPipetracker, width=2), symbol='o', symbolSize=4, symbolBrush=mc.cPipetracker)
            lv.lview.pt_rej = pg.PlotDataItem(x=mc.pipetracker[:, ix][mc.pipetracker[:, 9] == 1],
                                              y=mc.pipetracker[:, 6][mc.pipetracker[:, 9] == 1] +
                                                mc.pipetracker[:, 11][mc.pipetracker[:, 9] == 1] + TP_rej,
                                              pen=None, symbol='o', symbolSize=4, symbolBrush=(255, 0, 0, 255))
            lv.lview.pt_all = pg.PlotDataItem(x=mc.pipetracker[:, ix],
                                              y=mc.pipetracker[:, 6] + TP_all,
                                              pen=None, symbol='o', symbolSize=1, symbolBrush=(100, 100, 100, 255))
            lv.lview.addItem(lv.lview.pt_all)
            lv.lview.addItem(lv.lview.pt_rej)
            lv.lview.addItem(lv.lview.pt_acc)

    xv.UpdateX()


def iconFromBase64():
    # convert base64 icon to Qt icon
    base64 = b'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XltJc53WMOJYQgJJiJBRQxkVWIjSrpFiIkXnMQ//kONPkksmVxmMHAuoQoXk+MH/4PdszcLUpJsUigHdL7b9MQIEdoFm3ba/j227eQL4n4Erre2vNoDZT9LrbS1yBPRtAxfXbU3eAy53gMEnXTIkR/LTEgoF4P2MvikH9N8CwTV3bq1znD4AGZrV8g1wcAiMFil73ePdPZ1z+7enNb8f4E1y0yigt2sAAA0YaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjc0NmM2Y2I0LWM5YTctNDY3Ni05OWFkLWQzMWJjNDdjNWVjOCIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1MWM1Y2IzNi1hYWQ4LTQ4YTktOThiMi1lMjNmNTk1ZmZiYzUiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDphNzk3MDY2Mi0zNDMzLTRhN2QtYTlhZS0wOTQxZjU1N2MyMzIiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTcwNjAwNjc2NTExNDE5NyIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjI0IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjk2ZTNkZmZlLWE5YTEtNDRlOC1iOGExLTEwYjEyYzQ0MjAyOCIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNC0wMS0yM1QxMzo0NjowNSIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4VZYgnAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH6AEXCi4FsJcNrAAAIABJREFUeNrt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'
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon


def main():
    global mc
    global xv
    global pv
    global lv
    global opt
    global fv
    global ic_app

    # executable parent folder and path to config.bin
    parentfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(parentfold, 'config')
    configfile = os.path.join(configfold, 'config.bin')

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    # icon
    ic_app = iconFromBase64()

    mc = MainWindow()
    opt = Colors()
    xv = XV()
    pv = PV()
    lv = LV()

    for win in [opt, mc, xv, pv, lv]:
        win.setWindowIcon(ic_app)

    # check if config folder and config file exist / read config if exists
    if not os.path.isdir(configfold):
        os.makedirs(configfold)
    elif not os.path.isfile(configfile):
        pass
    else:
        with open(configfile, 'rb') as loadfile:
            [views_geometry,
             mc.pipeD, mc.pipeR, mc.inWall, mc.outWall,
             mc.HWin, mc.VWin, mc.Res,
             mc.FlD, mc.FlP, mc.AntiSpoof,
             mc.FoDist, mc.FoPers,
             mc.cProfile, mc.cPipe, mc.cLeftM, mc.cRightM,
             mc.cNotVis, mc.cVis, mc.cMADJ, mc.cMSBL, mc.cPipetracker, mc.cCurrentProf,
             mc.cBackground] = pickle.load(loadfile)

        pg.GraphicsView.setBackground(xv.xview, mc.cBackground)
        pg.GraphicsView.setBackground(lv.lview, mc.cBackground)
        pv.pview.getView().setBackgroundColor(mc.cBackground)

        for i, view in enumerate([mc, xv, pv, lv]):
            view.resize(views_geometry[i][0].width(), views_geometry[i][0].height())
            view.move(views_geometry[i][1].x(), views_geometry[i][1].y())

        mc.t_D.setText(str(mc.pipeD))
        mc.t_IW.setText(str(mc.inWall))
        mc.t_OW.setText(str(mc.outWall))
        mc.t_HW.setText(str(mc.HWin))
        mc.t_VW.setText(str(mc.VWin))
        mc.t_RES.setText(str(mc.Res))
        mc.t_Fl.setText(str(mc.FlD))
        mc.t_FlPt.setText(str(mc.FlP))
        mc.t_AntiSpoof.setText(str(mc.AntiSpoof))

    mc.show()
    lv.show()
    pv.show()
    xv.show()

    '''
    # evf function widget
    fv = FV()
    fv.show()
    '''

    sys.exit(app.exec())


if __name__ == '__main__':
    main()