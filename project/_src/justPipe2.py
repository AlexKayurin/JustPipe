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
from PySide6.QtWidgets import QFileDialog, QMessageBox, QColorDialog #, QWidget, QGridLayout
from PySide6.QtCore import Qt, QThread #, QObject, QEvent
# from PySide6.QtGui import QWheelEvent
import pyqtgraph as pg
# from pyqtgraph import Vector
import _UI_Control
import _UI_Xview
import _UI_Pview
import _UI_Lview
import _UI_Options
import _F_icon
import _F_funcs
import _F_kp_to_point
import _F_makePlayList
import _QtPl


PIL.Image.MAX_IMAGE_PIXELS = 10000000000
# OPTIONS = QFileDialog.Options()


class BuildDVPlaylistThread(QThread):
    def __init__(self, foldName, convention, fName):
        super().__init__()
        self.foldName = foldName
        self.convention = convention
        self.fName = fName

    def run(self):
        _F_makePlayList.run(self.foldName, self.convention, self.fName)


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
                        '.wrk', '.WRK', '.pll', '.PLL']

        # connect widgets
        self.actionLoad_profiles.triggered.connect(self.menu_select)
        self.actionLoad_GeoTiff.triggered.connect(self.menu_select)
        self.actionLoad_tide.triggered.connect(self.menu_select)
        self.actionLoad_pipetracker.triggered.connect(self.menu_select)
        self.actionLoad_saved_work.triggered.connect(self.menu_select)
        self.actionSave_work.triggered.connect(self.menu_select)
        self.actionExport_EIVA.triggered.connect(self.menu_select)
        self.actionExport_SFX.triggered.connect(self.menu_select)
        self.actionBuild_Playlist.triggered.connect(self.menu_select)
        self.actionLoad_playlist.triggered.connect(self.menu_select)

        self.actionXView.triggered.connect(self.menu_view_win)
        self.actionPView.triggered.connect(self.menu_view_win)
        self.actionLView.triggered.connect(self.menu_view_win)
        self.actionSettings.triggered.connect(self.menu_view_win)
        self.actionDV_Control.triggered.connect(self.menu_view_win)
        
        self.actionManual.triggered.connect(self.open_manual)

        self.b_Pause.clicked.connect(self.dvPause)
        self.t_D.textEdited.connect(self.set_goAutoPipe)
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
        # fv.close()

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

    def menu_select(self):
        menus = ['Load profiles',
                 'Load geoimage',
                 'Load tide',
                 'Load pipetracker',
                 'Load saved work',
                 'Load playlist',
                 'Export EIVA',
                 'Export SFX',
                 'Build playlist',
                 'Save work']

        funcs = ['self.loadprof',
                 'self.loadtif',
                 'self.loadtide',
                 'self.loadpt',
                 'self.loadwork',
                 'self.loadplaylist',
                 'self.exporteiva',
                 'self.exportsfx',
                 'self.buildDVplaylistfile',
                 'self.savework']

        exts = ['SITRAS profiles (*.cr2);;XPA profiles (*.xpa);;All Files (*)',
                'GeoTiff files (*.tif);;GeoTiff files (*.tiff);;PNG files (*.png);;All Files (*)',
                'Tide files (*.tid);;All Files (*)',
                'justPipe Pipetracker files (*.spt);;EIVA Pipetracker files (*.pip);;SFX Pipetracker files (*.fug);;All Files (*)',
                'Work files (*.wrk);;All Files (*)',
                'Palylists (*.pll);;All files (*)',
                'EIVA line files (*.dig);;All Files (*)',
                'SFX files (*.csv);;All Files (*)']

        sender = self.sender().text()
        ix = menus.index(sender)
        # selct option
        if ix < 6:              # open files
            Name, _ = QFileDialog.getOpenFileName(self, menus[ix], '', exts[ix]) #, options=OPTIONS)
        if 5 < ix < 8:          # save files
            Name, _ = QFileDialog.getSaveFileName(self, menus[ix], '', exts[ix]) #, options=OPTIONS)
        if 7 < ix:              # select folder
            Name = QFileDialog.getExistingDirectory(self) #, options=OPTIONS)
        # execute function
        exec(f'{funcs[ix]}(\'{Name}\')')

    def buildDVplaylistfile(self, foldName):
        fName, _ = QFileDialog.getSaveFileName(self, 'Save playlist', '',
                                               'Palylists (*.pll);;All files (*)') #, options=OPTIONS)
        if fName:
            self.thread = BuildDVPlaylistThread(foldName, self.spb_Convention.value(), fName)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(lambda: self.showwarn('Playlist built'))
            self.thread.start()

            self.showwarn('Building playlist\n'
                          'It may take a while\n'
                          'Application is fully functional during building\n'
                          'Message will pop once playlist has been built')

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

    def savework(self, foldName):
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
                self.l_Saved.setText(f'LAST SAVED: {saving_time}')

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

    def loadplaylist(self, fName):
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

            pipeassist_coord = [np.cos(self.l_io) * mc.pipeR, np.sin(self.l_io) * mc.pipeR]
            self.pipeassist = pg.PlotCurveItem(pipeassist_coord[0], pipeassist_coord[1])
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
            PARENT = pg.PlotDataItem()

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
            x_prof = pg.PlotDataItem(mc.profile[:, 0], mc.profile[:, 1] + TC,
                                     pen=None, symbol='o', symbolPen=None, symbolSize=2.5, symbolBrush=mc.cProfile)
            x_prof.setParentItem(PARENT)
            # flag patches
            if self.ch_ShowPatch.isChecked():
                try:
                    x_patch_l = pg.PlotDataItem(mc.profile[mc.li_spot[0], 0],
                                                mc.profile[mc.li_spot[0], 1] + TC,
                                                pen=None, symbol='o', symbolPen=None,
                                                symbolSize=2.5, symbolBrush='deepskyblue')
                    x_patch_r = pg.PlotDataItem(mc.profile[mc.ri_spot[0], 0],
                                                mc.profile[mc.ri_spot[0], 1] + TC,
                                                pen=None, symbol='o', symbolPen=None,
                                                symbolSize=2.5, symbolBrush='deepskyblue')
                    x_patch_l.setParentItem(PARENT)
                    x_patch_l.setParentItem(PARENT)
                except:
                    pass

            # pipe
            p_P_pts = [mc.pipeR * np.cos(self.l_io), mc.pipeR * np.sin(self.l_io)]
            p_P = pg.PlotCurveItem(p_P_pts[0], p_P_pts[1])
            p_P.setPos(p_coord[0], p_coord[1] + TC)
            p_P.setPen(color=mc.cPipe.getRgb(), width=1.5)
            p_P.setParentItem(PARENT)
            # inWall
            inWall_pts = [mc.inWall * mc.pipeR * np.cos(self.l_io), mc.inWall * mc.pipeR * np.sin(self.l_io)]
            p_in = pg.PlotCurveItem(inWall_pts[0], inWall_pts[1])
            p_in.setPos(p_coord[0], p_coord[1] + TC)
            p_in.setPen(color=mc.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
            p_in.setParentItem(PARENT)
            # outWall
            outWall_pts = [mc.outWall * mc.pipeR * np.cos(self.l_io), mc.outWall * mc.pipeR * np.sin(self.l_io)]
            p_out = pg.PlotCurveItem(outWall_pts[0], outWall_pts[1])
            p_out.setPos(p_coord[0], p_coord[1] + TC)
            p_out.setPen(color=mc.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
            p_out.setParentItem(PARENT)
            # AntiSpoof
            if self.ch_ShowAntiSpoof.isChecked():
                AntiSpoof_pts = [(mc.pipeR + mc.AntiSpoof) * np.cos(self.l_io), (mc.pipeR + mc.AntiSpoof) * np.sin(self.l_io)]
                p_as = pg.PlotCurveItem(AntiSpoof_pts[0], AntiSpoof_pts[1])
                p_as.setPos(p_coord[0], p_coord[1] + TC)
                p_as.setPen(color='red', width=0.5) #, style=QtCore.Qt.DotLine)
                p_as.setParentItem(PARENT)
            # inner flags
            x_lifl = pg.ArrowItem(angle=-120, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
            x_rifl = pg.ArrowItem(angle=-60, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
            x_lifl.setPos(lifl_coord[0], lifl_coord[1] + TC)
            x_rifl.setPos(rifl_coord[0], rifl_coord[1] + TC)
            x_lifl.setBrush(mc.cLeftM)
            x_rifl.setBrush(mc.cRightM)
            x_lifl.setParentItem(PARENT)
            x_rifl.setParentItem(PARENT)
            # outer flags
            if mc.ch_FoShow.isChecked():
                x_lofl = pg.ArrowItem(angle=-90, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
                x_rofl = pg.ArrowItem(angle=-90, headLen=20, headWidth=4, tailLen=30, tailWidth=2)
                x_lofl.setPos(lofl_coord[0], lofl_coord[1] + TC)
                x_rofl.setPos(rofl_coord[0], rofl_coord[1] + TC)
                x_lofl.setBrush(mc.cLeftM)
                x_rofl.setBrush(mc.cRightM)
                x_lofl.setParentItem(PARENT)
                x_rofl.setParentItem(PARENT)
            # top - bottom & CL
            p_top = pg.InfiniteLine(p_coord[1] + mc.pipeR + TC, angle=0, movable=False,
                                     pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            p_bot = pg.InfiniteLine(p_coord[1] - mc.pipeR + TC, angle=0, movable=False,
                                     pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            cl = pg.InfiniteLine(mc.min_cx, angle=90, movable=False,
                                 pen=pg.mkPen('white', width=0.3, style=QtCore.Qt.DotLine))
            p_top.setParentItem(PARENT)
            p_bot.setParentItem(PARENT)
            cl.setParentItem(PARENT)

            # profile_window
            if mc.port != mc.stbd:
                port_p_win = pg.InfiniteLine(mc.port - mc.pipeR, angle=90, movable=False,
                                     pen=pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                stbd_p_win = pg.InfiniteLine(mc.stbd + mc.pipeR, angle=90, movable=False,
                                     pen=pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                port_p_win.setParentItem(PARENT)
                stbd_p_win.setParentItem(PARENT)
                # TOP search window
                c_win = [[mc.port, mc.port, mc.stbd, mc.stbd, mc.port],
                              [mc.low, mc.high, mc.high, mc.low, mc.low]]
                c_win = pg.PlotCurveItem(c_win[0], c_win[1])
                c_win.setPos(0, mc.pipeR + TC)
                c_win.setPen(pg.mkPen('orange', width=1.0, style=QtCore.Qt.DotLine))
                c_win.setParentItem(PARENT)
            else:
                done = pg.PlotDataItem(x=[p_coord[0]], y=[p_coord[1]] + TC,
                                       pen=None, symbol='x', symbolSize=10, symbolBrush='yellow')
                done.setParentItem(PARENT)

            self.xview.addItem(PARENT)

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
        sender = self.sender().objectName()

        if sender == 'ch_Aspect':
            if self.ch_Aspect.isChecked():
                self.lview.setAspectLocked(True)
                lv.l_scale.setText(f'SCALE 1:1')
                self.aspect = 1
            else:
                self.lview.setAspectLocked(False)
                self.aspect = 1

        if sender == 'ch_Time_Chn':
            Update_PT()

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
                mc.savework(foldName)
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
    elif Path(fName).suffix.strip().lower() in ['.pip', '.fug', '.spt']:
        mc.loadpt(fName)
    elif Path(fName).suffix.strip().lower() in ['.tif', '.tiff','.png']:
        mc.loadtif(fName)
    elif Path(fName).suffix.strip().lower() in ['.pll']:
        mc.loadplaylist(fName)


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

        # AutoPipe only runs if: profile not visited AND no ManualPipe selected OR Autorun
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

            # calc min cx/cz node (pipe C)
            min_col = math.floor(min_evf / len(z_grid))
            min_row = min_evf - min_col * len(z_grid)

            mc.min_cx = round(x_grid[min_col], 4)
            mc.min_cz = round(z_grid[min_row], 4)

            '''
            ###################### this is for function widget
            # evf function widget
            evf_3 = np.log10(evf[:, 3]).reshape(len(x_grid), len(z_grid))
            cmap = pg.colormap.get('CET-L17')
            fv.imv.setImage(evf_3)
            fv.imv.setColorMap(cmap)
            ######################
            '''


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
                                # takes closest point to min_cx where z < lower than pipe wall (& antispoof)
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

        UpdateMinCX_and_Flags(chs, che)


def UpdateMinCX_and_Flags(s, e):
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

                UpdateMinCX_and_Flags(_p_part[0], _p_part[-1])


def ReChain():
    if mc.Ptflag:
        mc.pipetracker[:, 8] = _F_kp_to_point.go(mc.flush[:, [9, 10, 12]], mc.pipetracker[:, [4, 5]])[:, 2]

        # # sorting by KP
        # mc.pipetracker = mc.pipetracker[mc.pipetracker[:, 8].argsort()]

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


def main():
    global mc
    global xv
    global pv
    global lv
    global opt
    global fv
    global ic_app

    # executable parent folder and path to config.bin
    appfolder = os.path.dirname(sys.argv[0])
    configfold = os.path.join(appfolder, 'config')
    configfile = os.path.join(configfold, 'config', 'config.bin')

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    # icon
    ic_app = _F_icon.iconFromBase64()

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