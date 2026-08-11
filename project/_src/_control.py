import os
import sys
import platform
import subprocess
import logging
import pickle
from datetime import datetime, timezone
import platform
import subprocess
from pathlib import Path
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import pyqtgraph as pg


class Controller:
    def __init__(self, model, mainWin, xv, pv, lv, config, appfolder):
        self._model = model
        self._mainWin = mainWin
        self._xv = xv
        self._pv = pv
        self._lv = lv
        self._config = config

        # subscribe views to controller
        self._model.subscribe_controller(self)
        self._mainWin.subscribe_controller(self)
        self._xv.subscribe_controller(self)
        self._pv.subscribe_controller(self)
        self._lv.subscribe_controller(self)
        self._config.subscribe_controller(self)

        # init files
        self._appfolder = appfolder
        self._configfold = os.path.join(self._appfolder, '_internal', 'config')
        self._configfile = os.path.join(self._configfold, 'config.bin')
        self._icon = QtGui.QIcon(os.path.join(self._configfold, 'icon.ico'))
        self._logfile = os.path.join(self._configfold, 'error.log')
        self._manualfile = os.path.join(self._configfold, 'justPipe.pdf')
        self._licensefile = os.path.join(self._configfold, 'license.pdf')

        # Set up the basic configuration for logging
        if os.path.isfile(self._logfile):
            os.remove(self._logfile)
        logging.basicConfig(filename=self._logfile, level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.debug('App started')

        # check if config file exist and read config if exists, else set up default
        if not os.path.isfile(self._configfile):
            # default colors
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
        else:
            with open(self._configfile, 'rb') as loadfile:
                [self.views_geometry,
                 self._model.pipeD, self._model.pipeR, self._model.inWall, self._model.outWall,
                 self._model.HWin, self._model.VWin, self._model.Res,
                 self._model.FlD, self._model.FlP, self._model.AntiSpoof, self._model.AntiSpoof_A,
                 self._model.FoDist,
                 self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
                 self.cNotVis, self.cVis, self.cMADJ, self.cMSBL,
                 self.cPipetracker, self.cCurrentProf,
                 self.cBackground] = pickle.load(loadfile)
            self.load_saved_config()

        # set up default variables
        self.ProfileFlag = False        # Profile loaded flag
        self.ChunkSelCounter = 0        # click counter/flag for chunk selection (0-not selected; 1-start selected;2-sterat&end (chunk) selected
        self.ManualPipe = False         # Manual pipe placement flag
        self.DoPipe = False             # Autorun flag
        self.Interpflag = False         # Running interpolation flag
        self.DVflag = False             # DV loaded flag
        self.Pausedflag = True          # DV pause on / off flag
        self.Ptflag = False             # Pipetracker loaded flag
        self.EditMode = True            # Pipe(True)/Pipetracker(False) edit flag
        self.Tideflag = False           # Tide loaded flag
        self.Appliedflag = False        # Tide applied flag
        self.ShowPipe = False           # Pipe dig assistant flag


        # set up ui
        for _w in [self._mainWin, self._xv, self._pv, self._lv, self._config]:
            _w.setWindowIcon(self._icon)
        # set up mainWin
        self._mainWin.setWindowTitle(f'jP')
        # set up xView------------------------------------------------------------------------------------------
        self._xv.setWindowTitle(f'Profile View')
        self._xv.xview.setAspectLocked()
        self._xv.x_prof.setSymbolBrush(self.cProfile)
        self._xv.pipe_P.setPen(color=self.cPipe.getRgb(), width=1.5)
        self._xv.pipe_I.setPen(color=self.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
        self._xv.pipe_O.setPen(color=self.cPipe.getRgb(), width=0.5, style=QtCore.Qt.DotLine)
        self._xv.pipe_A.setPen(color='red', width=0.5)
        self._xv.pipeassist.setPen(color='g', width=2)
        self._xv.pipe_top.setPen(color='white', width=0.3, style=QtCore.Qt.DotLine)
        self._xv.pipe_bot.setPen(color='white', width=0.3, style=QtCore.Qt.DotLine)
        self._xv.pipe_cl.setPen(color='white', width=0.3, style=QtCore.Qt.DotLine)
        self._xv.x_l_inner.setBrush(self.cLeftM)
        self._xv.x_r_inner.setBrush(self.cRightM)
        self._xv.x_l_outer.setBrush(self.cLeftM)
        self._xv.x_r_outer.setBrush(self.cRightM)
        self._xv.port_p_win.setPen(color='orange', width=1.0, style=QtCore.Qt.DotLine)
        self._xv.stbd_p_win.setPen(color='orange', width=1.0, style=QtCore.Qt.DotLine)
        self._xv.c_win.setPen(color='orange', width=1.0,style=QtCore.Qt.DotLine)
        self._xv.c_win.setPen(color='orange', width=1.0, style=QtCore.Qt.DotLine)
        # set up pView------------------------------------------------------------------------------------------
        self._pv.setWindowTitle(f'Plan View')
        self._pv.here.setPen(self.cCurrentProf, width=1)
        self._pv.here.setSymbolBrush(self.cCurrentProf)
        self._pv.visited.setPen(self.cVis.getRgb(), width=2.5)
        self._pv.visited.setSymbolBrush(self.cVis)
        self._pv.li.setPen(self.cLeftM.getRgb(), width=0.75, style=QtCore.Qt.DotLine)
        self._pv.li.setSymbolBrush(self.cLeftM)
        self._pv.ri.setPen(self.cRightM.getRgb(), width=0.75, style=QtCore.Qt.DotLine)
        self._pv.ri.setSymbolBrush(self.cRightM)
        self._pv.lo.setPen(self.cLeftM.getRgb(), width=0.75, style=QtCore.Qt.DotLine)
        self._pv.lo.setSymbolBrush(self.cLeftM)
        self._pv.ro.setPen(self.cRightM.getRgb(), width=0.75, style=QtCore.Qt.DotLine)
        self._pv.ro.setSymbolBrush(self.cRightM)
        self._pv.pt_acc.setPen(self.cPipetracker.getRgb(), width=2)
        self._pv.pt_acc.setSymbolBrush(self.cPipetracker)
        # set up lView------------------------------------------------------------------------------------------
        self._lv.setWindowTitle(f'Long View')
        self._lv.here.setPen(self.cCurrentProf.getRgb(), width=1)
        self._lv.here.setSymbolBrush(self.cCurrentProf)
        self._lv.visited_top.setPen(self.cVis.getRgb(), width = 2.5)
        self._lv.visited_top.setSymbolBrush(self.cVis)
        self._lv.visited_bot.setPen(self.cVis.getRgb(), width = 2.5)
        self._lv.madj.setPen(self.cMADJ.getRgb(), width=1.5, style=QtCore.Qt.DotLine)
        self._lv.msbl.setPen(self.cMSBL.getRgb(), width=1.5, style=QtCore.Qt.DotLine)
        self._lv.pt_acc.setPen(self.cPipetracker.getRgb(), width=2)
        self._lv.pt_acc.setSymbolBrush(self.cPipetracker)
        # set up colors------------------------------------------------------------------------------------------
        self._config.w_Profile.setStyleSheet(f'background-color: rgba{self.cProfile.getRgb()}')
        self._config.w_Pipe.setStyleSheet(f'background-color: rgba{self.cPipe.getRgb()}')
        self._config.w_LeftM.setStyleSheet(f'background-color: rgba{self.cLeftM.getRgb()}')
        self._config.w_RightM.setStyleSheet(f'background-color: rgba{self.cRightM.getRgb()}')
        self._config.w_NotVis.setStyleSheet(f'background-color: rgba{self.cNotVis.getRgb()}')
        self._config.w_Vis.setStyleSheet(f'background-color: rgba{self.cVis.getRgb()}')
        self._config.w_MADJ.setStyleSheet(f'background-color: rgba{self.cMADJ.getRgb()}')
        self._config.w_MSBL.setStyleSheet(f'background-color: rgba{self.cMSBL.getRgb()}')
        self._config.w_Pipetracker.setStyleSheet(f'background-color: rgba{self.cPipetracker.getRgb()}')
        self._config.w_CurrentProf.setStyleSheet(f'background-color: rgba{self.cCurrentProf.getRgb()}')
        self._config.w_Background.setStyleSheet(f'background-color: rgba{self.cBackground.getRgb()}')


        self.get_vals()


    def load_saved_config(self):
        pg.GraphicsView.setBackground(self._xv.xview, self.cBackground)
        pg.GraphicsView.setBackground(self._lv.lview, self.cBackground)
        self._pv.pview.getView().setBackgroundColor(self.cBackground)

        for i, view in enumerate([self._mainWin,
                                  self._xv,
                                  self._pv,
                                  self._lv, ]):
            view.resize(self.views_geometry[i][0].width(), self.views_geometry[i][0].height())
            view.move(self.views_geometry[i][1].x(), self.views_geometry[i][1].y())

        self._mainWin.t_D.setText(str(self._model.pipeD))
        self._mainWin.t_IW.setText(str(self._model.inWall))
        self._mainWin.t_OW.setText(str(self._model.outWall))
        self._mainWin.t_HW.setText(str(self._model.HWin))
        self._mainWin.t_VW.setText(str(self._model.VWin))
        self._mainWin.t_RES.setText(str(self._model.Res))
        self._mainWin.t_Fl.setText(str(self._model.FlD))
        self._mainWin.t_FlPt.setText(str(self._model.FlP))
        self._mainWin.t_AntiSpoof.setText(str(self._model.AntiSpoof))
        self._mainWin.t_AntiSpoof_A.setText(str(self._model.AntiSpoof_A))
        self._mainWin.t_FoDist.setText(str(self._model.FoDist))


    def get_vals(self):
        self._model.pipeD = float(self._mainWin.t_D.text())                 # pipe D
        self._model.pipeR = self._model.pipeD / 2                           # pipe R
        self._model.inWall = float(self._mainWin.t_IW.text())               # in wall
        self._model.outWall = float(self._mainWin.t_OW.text())              # out wall
        self._model.HWin = float(self._mainWin.t_HW.text())                 # horizontal search window
        self._model.VWin = float(self._mainWin.t_VW.text())                 # vertical search window (from the highest sounding in H window)
        self._model.Res = float(self._mainWin.t_RES.text())                 # search grid resolution
        self._model.weed_prof_val = int(self._mainWin.sp_Weed.value())               # profile weed factor
        self._model.FlD = float(self._mainWin.t_Fl.text())                  # inner flag distance from TOP
        self._model.FlP = float(self._mainWin.t_FlPt.text())                # inner flag patch (from flag distance)
        self._model.FoDist = float(self._mainWin.t_FoDist.text())           # outer flag distance from TOP
        self._model.AntiSpoof = float(self._mainWin.t_AntiSpoof.text())     # antisppofing pillow for adaptive flags - min distance to pipe wall
        self._model.AntiSpoof_A = float(self._mainWin.t_AntiSpoof_A.text()) # antisppofing sector angle
        self._model.AdPad = float(self._mainWin.t_AdPad.text())             # center pad (left blank) for adaptive flags
        self._model.CamOffset = float(self._mainWin.t_CamOffset.text())     # camera offset relative to profile
        self._model.Tzone = self._mainWin.spb_Timezone.value()              # time zone (diff DV - timestamps)
        self._model.weed_pt_val = int(self._mainWin.sp_Pt_Weed.value())         # pipetracker weed factor
        self._model.PtGap = float(self._mainWin.t_PtGap.text())             # Min gap in PT data for smoothing
        self._model.EditSpot = float(self._mainWin.t_EdSpot.text())         # plan/long view PT edit rectangle size
        self._model.SmoothWin = int(self._mainWin.t_smW.text())             # plan/long view PT smooth window
        self._model.SmoothWin_A = float(self._mainWin.sp_smW_A.value())
        self._model.SmoothWin_B = float(self._mainWin.sp_smW_B.value())
        self._model.pt_Level = float(self._mainWin.t_Lev.text())            # long view PT levelling value

        # tide apply/unapply text
        if not self.Tideflag:
            self._xv.l_Tide.setText('TIDE NOT LOADED')
            self._xv.l_Tide.setStyleSheet('color: red')
        elif self.Tideflag and self._mainWin.ch_ApplyTide.isChecked():
            self._xv.l_Tide.setText('TIDE LOADED - APPLIED')
            self._xv.l_Tide.setStyleSheet('color: forestgreen')
            self.Appliedflag = True
        else:
            self._xv.l_Tide.setText('TIDE LOADED - NOT APPLIED')
            self._xv.l_Tide.setStyleSheet('color: darkorange')
            self.Appliedflag = False

        # show/hide flags antispoof on xView
        if self._xv.ch_ShowAntiSpoof.isChecked():
            self._xv.pipe_A.setVisible(True)
        else:
            self._xv.pipe_A.setVisible(False)

        # show/hide flags patches on xView
        if self._xv.ch_ShowPatch.isChecked():
            self._xv.x_patch_l.setVisible(True)
            self._xv.x_patch_r.setVisible(True)
        else:
            self._xv.x_patch_l.setVisible(False)
            self._xv.x_patch_r.setVisible(False)

        # show/hide pipetracker on pView
        if self._pv.ch_ShowPT.isChecked():
            self._pv.pt_acc.setVisible(True)
        else:
            self._pv.pt_acc.setVisible(False)

        # show/hide pipetracker selector on pView
        if not self.EditMode and self.Ptflag:
            self._pv.gb_PT_Rej_Acc.setDisabled(False)
            self._pv.pt_selector.setVisible(True)
            if self._pv.rb_RejectPT.isChecked():
                self._pv.pt_selector.setPen(color='red', width=2)
            elif self._pv.rb_AcceptPT.isChecked():
                self._pv.pt_selector.setPen(color='green', width=2)
        else:
            self._pv.gb_PT_Rej_Acc.setDisabled(True)
            self._pv.pt_selector.setVisible(False)

        # show/hide pipetracker on lView
        if self._lv.ch_ShowPT.isChecked():
            self._lv.pt_acc.setVisible(True)
        else:
            self._lv.pt_acc.setVisible(False)

        # show/hide pipetracker selector on lView
        if not self.EditMode and self.Ptflag:
            self._pv.gb_PT_Rej_Acc.setDisabled(False)
            self._lv.pt_selector.setVisible(True)
            if self._pv.rb_RejectPT.isChecked():
                self._lv.pt_selector.setPen(color='red', width=2)
            elif self._pv.rb_AcceptPT.isChecked():
                self._lv.pt_selector.setPen(color='green', width=2)
        else:
            self._pv.gb_PT_Rej_Acc.setDisabled(True)
            self._lv.pt_selector.setVisible(False)

        # lView 1:1 on/off
        if self._lv.ch_Aspect.isChecked():
            self._lv.lview.setAspectLocked(True)
            self._lv.l_scale.setText(f'SCALE 1:1')
            self._lv.aspect = 1
        else:
            self._lv.lview.setAspectLocked(False)
            self._lv.aspect = 1

        # chunk pView/lView on/off
        if self.ChunkSelCounter == 0:
            self._pv.chunk_point.setVisible(False)
            self._pv.chunk.setVisible(False)
            self._lv.chunk_point.setVisible(False)
            self._lv.chunk.setVisible(False)
        elif self.ChunkSelCounter == 1:
            self._pv.chunk_point.setVisible(True)
            self._lv.chunk_point.setVisible(True)
        elif self.ChunkSelCounter == 2:
            self._pv.chunk.setVisible(True)
            self._lv.chunk.setVisible(True)


    def handle_close_ui(self):
        #  save workspace config
        views_geometry = []
        for view in [self._mainWin,
                     self._xv,
                     self._pv,
                     self._lv, ]:
            views_geometry.append([view.rect(), view.pos()])

        with open(self._configfile, 'wb') as dumpfile:
            dump = [views_geometry,
                    self._model.pipeD, self._model.pipeR,
                    self._model.inWall, self._model.outWall,
                    self._model.HWin, self._model.VWin, self._model.Res,
                    self._model.FlD, self._model.FlP, self._model.AntiSpoof, self._model.AntiSpoof_A,
                    self._model.FoDist,
                    self.cProfile, self.cPipe,
                    self.cLeftM, self.cRightM,
                    self.cNotVis, self.cVis,
                    self.cMADJ, self.cMSBL, self.cPipetracker,
                    self.cCurrentProf, self.cBackground]
            pickle.dump(dump, dumpfile)

        self._mainWin.close()
        self._xv.close()
        self._pv.close()
        self._lv.close()


    def handle_key_pressed(self, e, view):
        # xView pipe
        if e.type() == 6 and view == 'x':
            # snap TOP
            if e.key() == Qt.Key_Space:
                self._model.xini = self.cursor.x()
                self._model.flush[self._model.prno][11] = 0  # flag profile 'not visited' for manual edit
                self._model.make_profile()
                self.update_views()
            # show pipe assistant
            if e.key() == Qt.Key_C:
                self.ShowPipe = True if self.ShowPipe == False else False
                if self.ShowPipe == False:
                    self._xv.pipeassist.setVisible(False)
                    self._xv.b_assist.setStyleSheet('color: red')
                else:
                    self._xv.pipeassist.setVisible(True)
                    self._xv.b_assist.setStyleSheet('color: green')

        # lView aspect change flag Ctrl+mouse wheel
        if e.key() == Qt.Key_Control and e.type() == 6 and view == 'l':  # Ctrl pressed on lView
            self._lv.ch_Aspect.setChecked(False)
            self._lv.aspect_change_flag = True
        if e.key() == Qt.Key_Control and e.type() == 7 and view == 'l':  # Ctrl released on lView
            self._lv.aspect_change_flag = False
            self._model.make_shapes()


        if e.type() == 6:
            # focus to XView
            if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self._xv.xview.activateWindow()

            # reset chunk
            if e.key() == Qt.Key_Escape:
                self.ChunkSelCounter = 0
                self._model.chunk = [-1, -1]
                self.get_vals()
                self.update_views()

            if e.modifiers() & Qt.ControlModifier:  # 'Ctrl + S' -----MODIFIER
                # save work
                if e.key() == Qt.Key_S:
                    saving_time = self._model.save_work(os.path.dirname(self._model.profName))
                    self._mainWin.l_Saved.setText(f'SAVED: {saving_time}')
            # autodigiize
            if e.key() == Qt.Key_A:
                self._model.auto_run()
                self.get_vals()
                self.update_views()
                self.messagepop('Autorun completed')
            # step back
            if e.key() == Qt.Key_Z:
                if self._model.prno > 0:
                    self._model.prno -= 1
                self._model.make_profile()
                self.update_views()
            # step fwd
            if e.key() == Qt.Key_X:
                if self._model.prno < self._model.no_of_prof - 1:
                    self._model.prno += 1
                self._model.make_profile()
                self.update_views()
            # to end
            if e.key() == Qt.Key_End:
                self._model.prno = self._model.no_of_prof - 1
                self._model.make_profile()
                self.update_views()
            # to start
            if e.key() == Qt.Key_Home:
                self._model.prno = 0
                self._model.make_profile()
                self.update_views()
            # to last visited
            if e.key() == Qt.Key_E:
                for i in range(self._model.prno, self._model.no_of_prof):
                    if self._model.flush[i, 11] == 0:
                        self._model.prno = i - 1
                        break
                self._model.make_profile()
                self.update_views()
            # interpolate chunk
            if e.key() == Qt.Key_I:
                if self.ChunkSelCounter == 2:
                    self._model.interpolate_chunk()
                    self.get_vals()
                    self.update_views()
            # reset fwd
            if e.key() == Qt.Key_0:
                if self.ChunkSelCounter == 2:
                    chs, che = self._model.chunk[0], self._model.chunk[1]
                else:
                    chs, che = self._model.prno + 1, self._model.no_of_prof

                self._model.flush[chs:che + 1, 11] = 0
                self._model.flush[chs:che + 1, 9] = self._model.flush[chs:che + 1, 0]
                self._model.flush[chs:che + 1, 10] = self._model.flush[chs:che + 1, 1]
                self._model.flush[chs:che + 1, 4] = self._model.flush[chs, 4]

                self._model.chunk = [-1, -1]
                self.ChunkSelCounter = 0
                self.get_vals()
                self.update_views()

            # switch PT edit accept / reject
            if e.key() == Qt.Key_Alt and not self.EditMode:
                self._pv.rb_RejectPT.setChecked(True) if not self._pv.rb_RejectPT.isChecked()\
                    else self._pv.rb_AcceptPT.setChecked(True)
                if self._pv.rb_RejectPT.isChecked():
                    self._pv.pt_selector.setPen(color='red', width=2)
                    self._lv.pt_selector.setPen(color='red', width=2)
                else:
                    self._pv.pt_selector.setPen(color='green', width=2)
                    self._lv.pt_selector.setPen(color='green', width=2)


    def handle_button_pressed(self, sender, view):
        # this emulates QKeyEvent and passes to self.handle_key_pressed
        match sender:
            case 'b_POI':
                self._model.flush[self._model.prno, 29] = 1 if self._model.flush[self._model.prno, 29] == 0 else 0
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_Y, Qt.KeyboardModifier.NoModifier, 'y') # nothing
            case 'b_fbwd':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_Home, Qt.KeyboardModifier.NoModifier, '')
            case 'b_bwd':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier, 'z')
            case 'b_fwd':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_X, Qt.KeyboardModifier.NoModifier, 'x')
            case 'b_ffwd':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_End, Qt.KeyboardModifier.NoModifier, '')
            case 'b_endvisit':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_E, Qt.KeyboardModifier.NoModifier, 'e')
            case 'b_resetfwd':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_0, Qt.KeyboardModifier.NoModifier, '0')
            case 'b_assist':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.NoModifier, 'c')
            case 'b_Interpolate':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_I, Qt.KeyboardModifier.NoModifier, 'i')
            case 'b_Auto':
                e = QtGui.QKeyEvent(QtCore.QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier, 'a')

        self.handle_key_pressed(e, view)


    def handle_mouse_moved(self, cursor, view):
        self.cursor = cursor
        # cursor coords
        self._mainWin.l_Coord.setText(f'dX:{round(self.cursor.x(), 1)}, Z:{round(self.cursor.y(), 1)}')

        if view == 'x':
            # pipe assistant
            if self.ShowPipe:
                self._xv.pipeassist.setPos(self.cursor.x(), self.cursor.y() - self._model.pipeR)
            else:
                pass
        elif view == 'p':
            if not self.EditMode and self.Ptflag:
                self._pv.pt_selector.setPos(self.cursor.x(), self.cursor.y())
            else:
                pass
        elif view == 'l':
            if not self.EditMode and self.Ptflag:
                self._lv.pt_selector.setPos(self.cursor.x(), self.cursor.y())
            else:
                pass


    def handle_mouse_pressed(self, e, view):
        if view == 'x':
            # tide for profile
            T = self._mainWin.ch_ApplyTide.isChecked() * self._model.flush[self._model.prno, 15]
            # force TOP
            if e.button() == QtCore.Qt.MouseButton.LeftButton:
                self._model.min_cx, self._model.min_cz = self.cursor.x(), self.cursor.y() - self._model.pipeR - T

                self._model.manual_pipe()
                self.update_views()

            # force flags
            if e.button() == QtCore.Qt.MouseButton.RightButton:
                pipe_x = self._model.flush[self._model.prno, 3]
                # force inner Flag
                if e.modifiers() != Qt.ControlModifier:     # RMB
                    a, b, c, d = 5, 6, 7, 8
                    flag = 'Inner'
                # force outer Flag
                if e.modifiers() == Qt.ControlModifier:  # RMB + Ctrl
                    a, b, c, d = 16, 17, 18, 19
                    flag = 'Outer'

                lfl_x, lfl_z = self._model.flush[self._model.prno, a], self._model.flush[self._model.prno, b]
                rfl_x, rfl_z = self._model.flush[self._model.prno, c], self._model.flush[self._model.prno, d]

                if self.cursor.x() < pipe_x:
                    lfl_x, lfl_z = self.cursor.x(), self.cursor.y() - T
                else:
                    rfl_x, rfl_z = self.cursor.x(), self.cursor.y() - T

                self._model.manual_flags(lfl_x, lfl_z, rfl_x, rfl_z, flag)
                self.update_views()


        elif view == 'p' or view == 'l':
            if view == 'p':
                selected_pt = np.argmin(
                    ((self._model.flush[:, 9] - self.cursor.x()) ** 2 +
                     (self._model.flush[:, 10] - self.cursor.y()) ** 2) ** 0.5)
            elif view == 'l':
                ixf = 14 if self._lv.ch_Time_Chn.isChecked() else 12  # flush np field index time/ KP on Lview
                selected_pt = np.argmin(
                    ((self._model.flush[:, ixf] - self.cursor.x()) ** 2 +
                     (self._model.flush[:, 4] - self.cursor.y()) ** 2) ** 0.5)

            # jump to profile (double-click) / select chunk (right-click)
            if self.EditMode:
                # go to clicked profile
                if e.button() == QtCore.Qt.MouseButton.LeftButton and e.double():
                    self.ChunkSelCounter = 0
                    self._model.chunk = [-1, -1]
                    self._model.prno = selected_pt
                    self.get_vals()
                    self._model.make_profile()
                    self.update_views()
                # select chunk
                if e.button() == QtCore.Qt.MouseButton.RightButton:
                    if self.ChunkSelCounter == 0:
                        # selecting first point
                        self._model.chunk[0] = int(self._model.flush[selected_pt, 13])
                        self.ChunkSelCounter += 1
                        self._model.prno = selected_pt
                        self.get_vals()
                    elif self.ChunkSelCounter == 1:
                        # selecting second point
                        if selected_pt != self._model.chunk[0]:
                            self._model.chunk[1] = int(self._model.flush[selected_pt, 13])
                        self._model.chunk.sort()
                        self.ChunkSelCounter += 1
                        self._model.prno = selected_pt
                        self.get_vals()
                    self.update_views()


            # accept/reject pipetracker
            elif not self.EditMode and self.Ptflag:
                if view == 'p':
                    spot_p = self._model.EditSpot / 2
                    ix = np.where((((self.cursor.x() - spot_p) < self._model.pipetracker[:, 1]) &
                                   (self._model.pipetracker[:, 1] < (self.cursor.x() + spot_p))) &
                                  (((self.cursor.y() - spot_p) < self._model.pipetracker[:, 2]) &
                                   (self._model.pipetracker[:, 2] < (self.cursor.y() + spot_p))))
                    ixw = np.where((((self.cursor.x() - spot_p) < self._model.pipetracker_W[:, 1]) &
                                     (self._model.pipetracker_W[:, 1] < (self.cursor.x() + spot_p))) &
                                    (((self.cursor.y() - spot_p) < self._model.pipetracker_W[:, 2]) &
                                     (self._model.pipetracker_W[:, 2] < (self.cursor.y() + spot_p))))

                elif view == 'l':
                    spot_h = self._model.EditSpot / 2
                    spot_v = self._model.EditSpot / (2 / self._lv.aspect)
                    ax = 0 if self._lv.ch_Time_Chn.isChecked() else 8  # change time/ chainage on Lview
                    TP = self._mainWin.ch_ApplyTide.isChecked() * self._model.pipetracker[:, 7]
                    TPW = self._mainWin.ch_ApplyTide.isChecked() * self._model.pipetracker_W[:, 7]

                    ix = np.where((((self.cursor.x() - spot_h) < self._model.pipetracker[:, ax]) &
                                   (self._model.pipetracker[:, ax] < (self.cursor.x() + spot_h))) &
                                  (((self.cursor.y() - spot_v) <
                                    (self._model.pipetracker[:, 3] + self._model.pipetracker[:, 11] + TP)) &
                                   ((self._model.pipetracker[:, 3] + self._model.pipetracker[:, 11] + TP) <
                                    (self.cursor.y() + spot_v))))
                    ixw = np.where((((self.cursor.x() - spot_h) < self._model.pipetracker_W[:, ax]) &
                                    (self._model.pipetracker_W[:, ax] < (self.cursor.x() + spot_h))) &
                                   (((self.cursor.y() - spot_v) <
                                     (self._model.pipetracker_W[:, 3] + self._model.pipetracker_W[:, 11] + TPW)) &
                                    ((self._model.pipetracker_W[:, 3] + self._model.pipetracker_W[:, 11] + TPW) <
                                     (self.cursor.y() + spot_v))))

                self._model.pipetracker[ix, 9] = self._pv.rb_RejectPT.isChecked()      # reject / accept
                self._model.pipetracker_W[ixw, 9] = self._pv.rb_RejectPT.isChecked()

                self.update_pipetracker()


    def handle_load_data(self, fName):
        _ext = Path(fName).suffix.strip().lower()
        # profiles
        if _ext in ['.xpa', '.cr2']:
            self.profName, self._model.prno, self._model.no_of_prof = self._model.loadprof(_ext, fName)
            self.ProfileFlag = True

        # tide
        elif _ext in ['.tid']:
            self._model.loadtide(_ext, fName)
            self._xv.l_Tide.setText('TIDE LOADED - APPLIED')
            self._xv.l_Tide.setStyleSheet('color: forestgreen')

            self.update_pipetracker()
            self.update_views()

        # work
        elif _ext in ['.wrk']:
            self._model.loadwork(_ext, fName)
            self.load_saved_config()
            if not self.Tideflag:
                self._mainWin.ch_ApplyTide.setDisabled(True)
                self._mainWin.ch_ApplyTide.setChecked(True)
                self._xv.l_Tide.setText('TIDE NOT LOADED')
                self._xv.l_Tide.setStyleSheet('color: red')
            if self.Tideflag and not self.Appliedflag:
                self._mainWin.ch_ApplyTide.setDisabled(False)
                self._mainWin.ch_ApplyTide.setChecked(False)
                self._xv.l_Tide.setText('TIDE LOADED - NOT APPLIED')
                self._xv.l_Tide.setStyleSheet('color: darkorange')
            if self.Tideflag and self.Appliedflag:
                self._mainWin.ch_ApplyTide.setDisabled(False)
                self._mainWin.ch_ApplyTide.setChecked(True)
                self._xv.l_Tide.setText('TIDE LOADED - APPLIED')
                self._xv.l_Tide.setStyleSheet('color: forestgreen')
            self.ProfileFlag = True
            self._model.make_shapes()

        # pipetracker
        elif _ext in ['.pip', '.fug', '.ptr']:
            self._mainWin.sp_Pt_Weed.setValue(1)
            self._model.weed_pt_val = 1
            self._model.loadpt(_ext, fName)

            self._pv.ch_ShowPT.setDisabled(False)
            self._pv.b_snap_h.setDisabled(False)
            self._pv.b_EditMode.setDisabled(False)

            self._lv.ch_ShowPT.setDisabled(False)
            self._lv.b_snap_v.setDisabled(False)

            self._mainWin.sp_Pt_Weed.setDisabled(False)
            self._mainWin.b_savePT.setDisabled(False)
            self._mainWin.b_analysePtShift.setDisabled(False)
            self._mainWin.t_PtGap.setDisabled(False)
            self._mainWin.t_EdSpot.setDisabled(False)
            self._mainWin.t_smW.setDisabled(False)
            self._mainWin.sp_smW_A.setDisabled(False)
            self._mainWin.sp_smW_B.setDisabled(False)
            self._mainWin.b_smoothPT_p_MA.setDisabled(False)
            self._mainWin.b_smoothPT_p_AB.setDisabled(False)
            self._mainWin.b_smoothPT_l_MA.setDisabled(False)
            self._mainWin.b_smoothPT_l_AB.setDisabled(False)
            self._mainWin.t_Lev.setDisabled(False)
            self._mainWin.b_levelPT.setDisabled(False)
            self._mainWin.t_Lev.setText(str(self._model.pipetracker_W[0, 11]))
            self._model.pt_Level = self._model.pipetracker_W[0, 11]

            self.update_pipetracker()

        # image
        elif _ext in ['.tif', '.tiff', '.png']:
            geoimage, cellsize, o_left, o_top = self._model.loadtif(_ext, fName)
            self._pv.pview.setImage(geoimage, scale=(cellsize, -cellsize), pos=(o_left - cellsize, o_top + cellsize))
            self.update_views()

        # playlist
        elif _ext in ['.pll']:
            self._model.loadplaylist(_ext, fName)

        self._xv.xview.activateWindow()

        self._model.make_shapes()
        self._model.make_profile()
        self.update_views()


    def handle_save_data(self, function, fNname):
        if function == 'savework':
            saving_time = self._model.save_work(fNname)
            self._mainWin.l_Saved.setText(f'SAVED: {saving_time}')
        if function in ['exporteiva', 'exportsfx']:
            self._model.save_result(function, fNname)
            self.messagepop('Files saved')


    def handle_val_changed(self, sender):
        self.get_vals()
        # change Pipe/Pt edit mode
        if sender == 'b_EditMode' and self.Ptflag:
            self.EditMode = False if self.EditMode else True
            self._pv.b_EditMode.setText('\U0001F3A5') if self.EditMode else self._pv.b_EditMode.setText('\U0001F9F2')
            self._pv.gb_PT_Rej_Acc.setDisabled(True) if self.EditMode else self._pv.gb_PT_Rej_Acc.setDisabled(False)
            self.get_vals()
        # weed pipetracker
        if sender == 'sp_Pt_Weed':
            if self.Ptflag:
                self._model.weed_pipetracker()
                self.update_pipetracker()
        # weed pipetracker / end of pipetracker editing / apply loaded tide
        if sender == 'ch_ApplyTide':
            if self.Ptflag:
                self.update_pipetracker()
            self.update_views()
        # level pipetracker
        if sender == 'b_levelPT':
            if self.Ptflag:
                self._model.level_pipetracker()
                self.update_pipetracker()
        # smooth pipetracker Moving Average
        if sender == 'b_smoothPT_p_MA' or sender  == 'b_smoothPT_l_MA':
            if self.Ptflag: # and self._mainWin.rb_Pt.isChecked():
                self._model.smooth_pipetracker_MA(sender)
                self.update_pipetracker()
        # smooth pipetracker AB
        if sender == 'b_smoothPT_p_AB' or sender  == 'b_smoothPT_l_AB':
            if self.Ptflag: # and self._mainWin.rb_Pt.isChecked():
                self._model.smooth_pipetracker_AB(sender)
                self.update_pipetracker()
        # analyse PT to Pipe shifts
        if sender == 'b_analysePtShift':
            if self.Ptflag: # and self._mainWin.rb_Pt.isChecked():
                self._model.analyse_pypetracker()
                self._mainWin.t_Lev.setText(str(self._model.pipetracker_W[0, 11]))
                self._model.pt_Level = self._model.pipetracker_W[0, 11]
                self.update_pipetracker()
        # save pipetracker
        if sender == 'b_savePT':
            if self.Ptflag:
                saving_time = str(datetime.now().strftime('%Y%m%d%H%M%S'))
                self._model.save_pipetracker(saving_time, os.path.dirname(self._model.profName))
                self._mainWin.l_Saved.setText(f'SAVED: {saving_time}')
        # snap top to pipetracker
        if sender == 'b_snap_h' or sender == 'b_snap_v':
            self._model.snap_top_to_pipetracker(sender)
            self.get_vals()
            self.update_pipetracker()
            self.update_views()
        # change search window
        if sender == 'b_hwm':
            if self._model.HWin > 0.15:
                self._mainWin.t_HW.setText(str(round(self._model.HWin - 0.05, 2)))
                self._model.HWin = float(self._mainWin.t_HW.text())
        elif sender == 'b_hwp':
            self._mainWin.t_HW.setText(str(round(self._model.HWin + 0.05, 2)))
            self._model.HWin = float(self._mainWin.t_HW.text())
        elif sender == 'b_vwm':
            if self._model.VWin > 0.05:
                self._mainWin.t_VW.setText(str(round(self._model.VWin - 0.05, 2)))
                self._model.VWin = float(self._mainWin.t_VW.text())
        elif sender == 'b_vwp':
            self._mainWin.t_VW.setText(str(round(self._model.VWin + 0.05, 2)))
            self._model.VWin = float(self._mainWin.t_VW.text())
        # change AS mask sector
        if sender == 'b_asam':
            if self._model.AntiSpoof_A > 5:
                self._mainWin.t_AntiSpoof_A.setText(str(int(self._model.AntiSpoof_A - 5)))
                self._model.AntiSpoof_A = float(self._mainWin.t_AntiSpoof_A.text())
        elif sender == 'b_asap':
            self._mainWin.t_AntiSpoof_A.setText(str(int(self._model.AntiSpoof_A + 5)))
            self._model.AntiSpoof_A = float(self._mainWin.t_AntiSpoof_A.text())

        if sender not in ['b_EditMode', 'sp_Pt_Weed', 'rb_Pr', 'ch_ApplyTide',
                          'b_levelPT', 'b_smoothPT_p_MA', 'b_smoothPT_p_AB',
                          'b_smoothPT_l_MA', 'b_smoothPT_l_AB',
                          'b_snap_h', 'b_snap_v',
                          'b_savePT', 'b_analysePtShift', 't_PtGap', 't_EdSpot', 't_smW', 'sp_smW_A', 'sp_smW_B', 't_Lev',
                          'gb_PT_Rej_Acc', 'rb_RejectPT', 'rb_AcceptPT']:
            self._model.flush[self._model.prno, 11] = 0
            self._model.make_profile()
        else:
            pass
        self._model.make_shapes()
        self.update_views()


    def update_views(self):
        for but in [self._xv.b_POI , self._pv.b_POI, self._lv.b_POI]:
            if self._model.flush[self._model.prno, 29]:
                    but.setText('\u2717')
                    but.setStyleSheet('color: red')
            else:
                but.setText('\u2714')
                but.setStyleSheet('color: green')

        # profile timestamp (for DV)
        tstamp = self._model.flush[self._model.prno, 14] + self._model.Tzone * 3600
        # pipe & flags coordinates
        pipe_coord = [self._model.flush[self._model.prno, 3], self._model.flush[self._model.prno, 4] - self._model.pipeR]
        l_inner_coord = [self._model.flush[self._model.prno, 5], self._model.flush[self._model.prno, 6]]
        r_inner_coord = [self._model.flush[self._model.prno, 7], self._model.flush[self._model.prno, 8]]
        l_outer_coord = [self._model.flush[self._model.prno, 16], self._model.flush[self._model.prno, 17]]
        r_outer_coord = [self._model.flush[self._model.prno, 18], self._model.flush[self._model.prno, 19]]


        # # DV player
        # if mc.DVflag:
        #     if not mc.Pausedflag:
        #         for i, player in enumerate(mc.players):
        #             for j, s in enumerate(mc.DVstarts[i]):
        #                 if s <= tstamp <= mc.DVends[i][j]:
        #                     if j == mc.currentDVs[i]:
        #                         goto_time = 1000 * int(tstamp - s)
        #                         player.gototime(goto_time)
        #                     else:
        #                         mc.currentDVs[i] = j
        #                         goto_time = 1000 * int(tstamp - s)
        #                         player.loadmedia(mc.playlists[i][mc.currentDVs[i]][0])
        #                         player.gototime(goto_time)

        # update xView------------------------------------------------------------------------------------------
        # tide for X profile
        TXC = self._mainWin.ch_ApplyTide.isChecked() * self._model.flush[self._model.prno, 15]
        self._xv.l_Progress.setText(f'PROFILE {self._model.prno + 1} OF {self._model.no_of_prof}')
        self._xv.l_KP.setText(f'KP {self._model.flush[self._model.prno, 12]:.2f}')
        self._xv.l_Time.setText(f'{datetime.fromtimestamp(self._model.flush[self._model.prno, 14],
                                                          tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}')

        # profile
        self._xv.x_prof.setData(self._model.profile[:, 0], self._model.profile[:, 1] + TXC)
        # pipe/walls/antispoof
        self._xv.pipe_P.setPos(pipe_coord[0], pipe_coord[1] + TXC)
        self._xv.pipe_I.setPos(pipe_coord[0], pipe_coord[1] + TXC)
        self._xv.pipe_O.setPos(pipe_coord[0], pipe_coord[1] + TXC)
        if self._xv.ch_ShowAntiSpoof.isChecked():
            self._xv.pipe_A.setPos(pipe_coord[0], pipe_coord[1] + TXC)
        else:
            pass
        # pipe top/bottom/CL
        self._xv.pipe_top.setPos(pipe_coord[1] + self._model.pipeR + TXC)
        self._xv.pipe_bot.setPos(pipe_coord[1] - self._model.pipeR + TXC)
        self._xv.pipe_cl.setPos(self._model.min_cx)
        # flags
        self._xv.x_l_inner.setPos(l_inner_coord[0], l_inner_coord[1] + TXC)
        self._xv.x_r_inner.setPos(r_inner_coord[0], r_inner_coord[1] + TXC)
        self._xv.x_l_outer.setPos(l_outer_coord[0], l_outer_coord[1] + TXC)
        self._xv.x_r_outer.setPos(r_outer_coord[0], r_outer_coord[1] + TXC)
        # flag patches
        if self._xv.ch_ShowPatch.isChecked():
            try:
                self._xv.x_patch_l.setData(self._model.profile[self._model.li_spot[0], 0],
                                            self._model.profile[self._model.li_spot[0], 1] + TXC)
                self._xv.x_patch_r.setData(self._model.profile[self._model.ri_spot[0], 0],
                                            self._model.profile[self._model.ri_spot[0], 1] + TXC)
            except:
                pass
        else:
            pass
        # profile_window
        if self._model.port != self._model.stbd:
            self._xv.done.setVisible(False)
            self._xv.port_p_win.setVisible(True)
            self._xv.stbd_p_win.setVisible(True)
            self._xv.c_win.setVisible(True)
            self._xv.port_p_win.setPos(self._model.port - self._model.pipeR)
            self._xv.stbd_p_win.setPos(self._model.stbd + self._model.pipeR)
            # TOP search window
            c_win_coord = [[self._model.port, self._model.port, self._model.stbd, self._model.stbd, self._model.port],
                           [self._model.low, self._model.high, self._model.high, self._model.low, self._model.low]]
            self._xv.c_win.setData(c_win_coord[0], c_win_coord[1])
            self._xv.c_win.setPos(0, self._model.pipeR + TXC)
        else:
            self._xv.done.setVisible(True)
            self._xv.port_p_win.setVisible(False)
            self._xv.stbd_p_win.setVisible(False)
            self._xv.c_win.setVisible(False)
            self._xv.done.setData([pipe_coord[0]], [pipe_coord[1]] + TXC)

        # center xView
        if self._xv.ch_Center.isChecked():
            rect = self._xv.xview.visibleRange()
            self._xv.xview.setRange(xRange=[(self._model.min_cx - rect.width() / 2),
                                            (self._model.min_cx + rect.width() / 2)],
                                yRange=[(self._model.min_cz - rect.height() / 2 + TXC),
                                        (self._model.min_cz + rect.height() / 2) + TXC],
                                    padding=0) # if padding != 0 it will change viewRect

        # update pView------------------------------------------------------------------------------------------
        visited_mask = np.hstack((self._model.flush[1:, 11], np.zeros((1))))
        # current profile
        self._pv.here.setData([self._model.flush[self._model.prno, 9]],
                              [self._model.flush[self._model.prno, 10]])
        # top visited/not visited
        self._pv.visited.setData(self._model.flush[:, 9],
                                 self._model.flush[:, 10], connect=visited_mask)
        # flags
        self._pv.li.setData(self._model.flush[:, 20],
                            self._model.flush[:, 21], connect=visited_mask)
        self._pv.ri.setData(self._model.flush[:, 22],
                            self._model.flush[:, 23], connect=visited_mask)
        self._pv.lo.setData(self._model.flush[:, 24],
                            self._model.flush[:, 25], connect=visited_mask)
        self._pv.ro.setData(self._model.flush[:, 26],
                            self._model.flush[:, 27], connect=visited_mask)
        # POI
        self._pv.POI.setData(self._model.flush[:, 9][self._model.flush[:, 29] == 1],
                         self._model.flush[:, 10][self._model.flush[:, 29] == 1])

        # chunk
        if self.ChunkSelCounter == 1:
            self._pv.chunk_point.setData([self._model.flush[self._model.chunk[0], 9]],
                                         [self._model.flush[self._model.chunk[0], 10]])
        if self.ChunkSelCounter == 2:
            self._pv.chunk_point.setData([self._model.flush[self._model.chunk[1], 9]],
                                         [self._model.flush[self._model.chunk[1], 10]])
            self._pv.chunk.setData(self._model.flush[self._model.chunk[0]:self._model.chunk[1] + 1, 9],
                                   self._model.flush[self._model.chunk[0]:self._model.chunk[1] + 1, 10])

        # center pView
        if self._pv.ch_Center.isChecked():
            rect = self._pv.pview.view.viewRect()
            x, y = self._model.flush[self._model.prno, 9], self._model.flush[self._model.prno, 10]
            self._pv.pview.view.setRange(
                xRange=[(x - rect.width() / 2), (x + rect.width() / 2)],
                yRange=[(y - rect.height() / 2), (y + rect.height() / 2)],
                padding=0)  # if padding != 0 it will change viewRect

        # update lView------------------------------------------------------------------------------------------
        ixf = 14 if self._lv.ch_Time_Chn.isChecked() else 12    # flush np field index time/ KP on Lview
        # tide for long
        TLV = self._mainWin.ch_ApplyTide.isChecked() * self._model.flush[:, 15]                                 # visited
        TLC = self._mainWin.ch_ApplyTide.isChecked() * self._model.flush[self._model.prno, 15]                  # current profile
        TLP = self._mainWin.ch_ApplyTide.isChecked() * self._model.flush[:, 15][self._model.flush[:, 29] == 1]  # POI

        # current position
        self._lv.here.setData([self._model.flush[self._model.prno, ixf]],
                              [self._model.flush[self._model.prno, 4]
                               + TLC])
        # top visited/not visited
        self._lv.visited_top.setData(self._model.flush[:, ixf],
                                     self._model.flush[:, 4]
                                     + TLV, connect=visited_mask)
        # bop visited/not visited
        self._lv.visited_bot.setData(self._model.flush[:, ixf],
                                     self._model.flush[:, 4] -
                                        self._model.pipeD + TLV, connect=visited_mask)
        # madj/msbl
        self._lv.madj.setData(self._model.flush[:, ixf],
                              np.mean(self._model.flush[:, [6, 8]], axis=1)
                              + TLV, connect=visited_mask)
        self._lv.msbl.setData(self._model.flush[:, ixf],
                              np.mean(self._model.flush[:, [17, 19]], axis=1)
                              + TLV, connect=visited_mask)
        # POI
        self._lv.POI.setData(self._model.flush[:, ixf][self._model.flush[:, 29] == 1],
                             self._model.flush[:, 4][self._model.flush[:, 29] == 1] + TLP)

        # chunk
        TP = (self._mainWin.ch_ApplyTide.isChecked() *
              self._model.flush[self._model.chunk[0], 15])                              # tide for chunk point
        TH = (self._mainWin.ch_ApplyTide.isChecked() *
              self._model.flush[self._model.chunk[0]:self._model.chunk[1] + 1, 15])     # tide for chunk line
        if self.ChunkSelCounter == 1:
            self._lv.chunk_point.setData([self._model.flush[self._model.chunk[0], ixf]],
                                         [self._model.flush[self._model.chunk[0], 4]] + TP)
        if self.ChunkSelCounter == 2:
            self._lv.chunk_point.setData([self._model.flush[self._model.chunk[1], ixf]],
                                         [self._model.flush[self._model.chunk[1], 4]] + TP)
            self._lv.chunk.setData(self._model.flush[self._model.chunk[0]:self._model.chunk[1] + 1, ixf],
                                   self._model.flush[self._model.chunk[0]:self._model.chunk[1] + 1, 4] + TH)

        # center plot
        if self._lv.ch_Center.isChecked():
            rect = self._lv.lview.viewRect()
            x, y = self._model.flush[self._model.prno, ixf], self._model.flush[self._model.prno, 4] + TLC
            self._lv.lview.setRange(
                xRange=[(x - rect.width() / 2), (x + rect.width() / 2)],
                yRange=[(y - rect.height() / 2), (y + rect.height() / 2)],
                padding=0)  # if padding != 0 it will change viewRect

        self._lv.winrange = self._lv.lview.viewRange()[0]


    def update_pipetracker(self):
        if self._pv.ch_ShowPT.isChecked() and self.Ptflag:
            accepted_mask = np.logical_not(np.hstack((self._model.pipetracker_W[1:, 9], np.zeros((1)))))
            # pView
            self._pv.pt_acc.setData(self._model.pipetracker_W[:, 14],
                                    self._model.pipetracker_W[:, 15],
                                    connect=accepted_mask)
            # lView
            ixp = 0 if self._lv.ch_Time_Chn.isChecked() else 8  # pipetracker np field index time/ KP on Lview
            # tide for pipetracker on long
            TP_acc = self._mainWin.ch_ApplyTide.isChecked() * self._model.pipetracker_W[:, 7]
            self._lv.pt_acc.setData(self._model.pipetracker_W[:, ixp],
                                    self._model.pipetracker_W[:, 6] +
                                    self._model.pipetracker_W[:, 11]
                                    + TP_acc,
                                    connect=accepted_mask)

        else:
            pass


    def handle_show_view(self, sender):
        if sender == 'actionXView':
            self._xv.show()

        if sender == 'actionPView':
            self._pv.show()

        if sender == 'actionLView':
            self._lv.show()

        if sender == 'actionDV_Control':
            pass

        if sender == 'actionSettings':
            self._config.show()

        if sender == 'actionManual':
            # open application manual
            platf = platform.system()
            if platf == 'Linux':
                subprocess.call(['xdg-open', self._manualfile])  # , check=True)
            if platf == 'Windows':
                os.startfile(self._manualfile)


    def handle_config(self, sender, ix, selectedcolor):
        _objcolors= [self.cProfile, self.cPipe, self.cLeftM, self.cRightM,
                     self.cNotVis, self.cVis, self.cMADJ, self.cMSBL, self.cPipetracker,
                     self.cCurrentProf, self.cBackground]

        _objcolors[ix].setRgb(*selectedcolor)
        pg.GraphicsView.setBackground(self._xv.xview, self.cBackground)
        pg.GraphicsView.setBackground(self._lv.lview, self.cBackground)
        self._pv.pview.getView().setBackgroundColor(self.cBackground)

        self.update_views()


    def messagepop(self, message):
        _msg = QMessageBox()
        _msg.setWindowTitle('Warning')
        _msg.setText(message)
        _msg.setWindowIcon(self._icon)
        _msg.show()
        _msg.exec()