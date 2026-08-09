import os
import math
import pickle
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from decimal import Decimal
import _F_funcs
import _F_kp_to_point
from PIL import Image
from PIL.TiffTags import TAGS

Image.MAX_IMAGE_PIXELS = 10000000000

class Model:
    def __init__(self):
        self.prno = 0
        self.xini = 0

        # empty selection chunk (first & last profile nos)
        self.chunk = [-1, -1]
        # set pipe shape - spaced points array for plotting pipe (360 deg / 50 pts)
        pipeshape = np.linspace(-0.5 * np.pi, -2.5 * np.pi, 360)
        self.pipeshape_cos = np.cos(pipeshape)
        self.pipeshape_sin = np.sin(pipeshape)


    def subscribe_controller(self, controller) -> None:
        self._controller = controller


    def loadprof(self, proftype, fName):
        self.profiles = []  # empty array of classes Pofile()
        self.profName = fName

        corrupted = 0
        i = 0

        # xpa - from EIVA NM
        if proftype == '.xpa':
            with open(fName, 'r') as infile:
                self.profiles_from_file = infile.readlines()

            self.no_of_prof = len(self.profiles_from_file)
            # initial self.flush array for TOP/LI/RI - '0' timestamps will be removed in final
            self.flush = np.zeros((self.no_of_prof, 31))

            for line in self.profiles_from_file:
                try:
                    # single profile read from file
                    oneprofile = line.split(',')

                    # check if point not duplicated en[i] != en[i-1]
                    if i > 0 and (oneprofile[1] == self.flush[i - 1, 0] and oneprofile[2] == self.flush[i - 1, 1]):
                        corrupted += 1
                    else:
                        self.flush[i, 14] = datetime.strptime(oneprofile[0], '%Y%m%d%H%M%S.%f').replace(
                            tzinfo=timezone.utc).timestamp()  # time
                        self.flush[i, 0] = oneprofile[1]  # easting
                        self.flush[i, 9] = oneprofile[1]  # easting
                        self.flush[i, 1] = oneprofile[2]  # northing
                        self.flush[i, 10] = oneprofile[2]  # northing
                        self.flush[i, 2] = oneprofile[3]  # heading
                        self.flush[i, 28] = oneprofile[4]  # pipe direction
                        self.flush[i, 12] = float(oneprofile[5]) * 1000  # kp (in m)
                        self.flush[i, 13] = i

                        # profile to add to self.profiles array size = (num_of_points, 2)
                        writeprofile = np.zeros((int(len(oneprofile[6:]) / 2), 2), dtype=float)
                        writeprofile[:, 0] = oneprofile[6::2]
                        writeprofile[:, 1] = oneprofile[7::2]
                        writeprofile = writeprofile[writeprofile[:, 0].argsort()]  # sorting by dx
                        writeprofile[:, 1] = -writeprofile[:, 1]  # height to depth

                        # flip heading and dX if ROV runs decsending
                        if 120 < abs(self.flush[i, 28] - self.flush[i, 2]) < 240:
                            self.flush[i, 2] += 180
                            writeprofile[:, 0] = -writeprofile[:, 0]

                        # add to self.profiles array
                        self.profiles.append(writeprofile)

                        i += 1

                except:
                    corrupted += 1

            # set flag coords as ref coords (for plotting)
            self.flush[:, 20] = self.flush[:, 9]
            self.flush[:, 22] = self.flush[:, 9]
            self.flush[:, 24] = self.flush[:, 9]
            self.flush[:, 26] = self.flush[:, 9]
            self.flush[:, 21] = self.flush[:, 10]
            self.flush[:, 23] = self.flush[:, 10]
            self.flush[:, 25] = self.flush[:, 10]
            self.flush[:, 27] = self.flush[:, 10]


        # SITRAS format, may be exported via export in SFX DataIO
        if proftype == '.cr2':
            with open(fName, 'r') as infile:
                # read self.profiles from profile file
                self.profiles_from_file = infile.readlines()[3:]

            self.no_of_prof = len(self.profiles_from_file)
            # initial self.flush array for TOP/LI/RI - '0' timestamps will be removed in final
            self.flush = np.zeros((self.no_of_prof, 31))

            for line in self.profiles_from_file:
                try:
                    oneprofile = line.replace(';;', ';').split(';')  # replace ';;' at string end in EIVA exported cr2

                    # check if point not duplicated en[i] != en[i-1]
                    if i > 0 and (float(oneprofile[6]) == self.flush[i - 1, 0] and float(oneprofile[7]) == self.flush[
                        i - 1, 1]):
                        corrupted += 1
                    else:
                        # combine date & time and remove fraction from seconds (3 last digits)
                        self.flush[i, 14] = datetime.strptime('.'.join(oneprofile[1:3])[:-3],
                                                         '%d.%m.%Y.%H%M%S').replace(
                            tzinfo=timezone.utc).timestamp()
                        self.flush[i, 0] = float(oneprofile[6])  # easting
                        self.flush[i, 9] = float(oneprofile[6])  # easting
                        self.flush[i, 1] = float(oneprofile[7])  # northing
                        self.flush[i, 10] = float(oneprofile[7])  # northing
                        self.flush[i, 2] = float(oneprofile[13])  # heading
                        self.flush[i, 28] = float(oneprofile[13])  # pipe direction = heading
                        self.flush[i, 12] = float(oneprofile[3]) * 1000  # KP (in m)
                        self.flush[i, 13] = i

                        # profile to add to self.profiles array size = (num_of_points, 2)
                        writeprofile = np.zeros((int((len(oneprofile) - 44) / 2), 2), dtype=float)
                        writeprofile[:, 0] = oneprofile[43:-1:2]
                        writeprofile[:, 1] = oneprofile[44::2]
                        writeprofile = writeprofile[writeprofile[:, 0].argsort()]  # sorting by dx
                        writeprofile[:, 1] = writeprofile[:, 1] - float(oneprofile[9])  # reference depth

                        # add to self.profiles array
                        self.profiles.append(writeprofile)

                        i += 1

                except:
                    corrupted += 1

            # set flag coords as ref coords (for plotting)
            self.flush[:, 20] = self.flush[:, 9]
            self.flush[:, 22] = self.flush[:, 9]
            self.flush[:, 24] = self.flush[:, 9]
            self.flush[:, 26] = self.flush[:, 9]
            self.flush[:, 21] = self.flush[:, 10]
            self.flush[:, 23] = self.flush[:, 10]
            self.flush[:, 25] = self.flush[:, 10]
            self.flush[:, 27] = self.flush[:, 10]

        self.no_of_prof -= corrupted
        if corrupted != 0:
            self._controller.messagepop(f'{corrupted} corrupted profile(s) were not loaded')

        # remove '0' timestamps (corrupted records) from initial array
        self.flush = self.flush[self.flush[:, 14] != 0]

        self.prno = 0   # current profile no
        self.xini = 0   # initial TOP search position

        return self.profName, self.prno, self.no_of_prof


    def loadtide(self, _ext, fName):
        pass
        if not self._controller.ProfileFlag:
            self._controller.messagepop('Load profiles first')
        else:
            tidedata = np.loadtxt(fName, skiprows=0, delimiter=',',
                                  converters={0: lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S.%f').replace(tzinfo=timezone.utc).timestamp(),
                                              1: float})

            if tidedata[-1, 0] < self.flush[-1, 14] or tidedata[0, 0] > self.flush[0, 14]:
                self._controller.messagepop('Tide file does not cover profiles range')
            else:
                # interpolating tide to flush
                self.flush[:, 15] = np.interp(self.flush[:, 14], tidedata[:, 0], tidedata[:, 1])
                self._controller.Tideflag = True
                self._controller._mainWin.ch_ApplyTide.setDisabled(False)

            if self._controller.Ptflag:
                # interpolating tide from flush to pipetracker filed 7
                self.pipetracker[:, 7] = np.interp(self.pipetracker[:, 0], self.flush[:, 14],
                                                   self.flush[:, 15])


    def loadwork(self, _ext, fName):
        with open(fName, 'rb') as loadfile:
            [self._controller.views_geometry, self.prno,
             self.profName, self.no_of_prof, self.profiles, self.flush,
             self.pipeD, self.pipeR, self.inWall, self.outWall,
             self.HWin, self.VWin, self.Res,
             self.FlD, self.FlP, self.AntiSpoof, self.AntiSpoof_A,
             self.FoDist,
             self._controller.Tideflag, self._controller.Appliedflag,
             self._controller.cProfile, self._controller.cPipe,
             self._controller.cLeftM, self._controller.cRightM,
             self._controller.cNotVis, self._controller.cVis,
             self._controller.cMADJ, self._controller.cMSBL,
             self._controller.cPipetracker, self._controller.cCurrentProf,
             self._controller.cBackground] = pickle.load(loadfile)


    def loadpt(self, _ext, fName):
        if not self._controller.ProfileFlag:
            self._controller.messagepop('Load profiles first')
        else:
            if not self._controller.Ptflag:
                if _ext == '.pip':
                    pipetracker_file = np.loadtxt(fName, skiprows=0, delimiter='\t',
                                                  converters={0: lambda x: datetime.strptime(x,
                                                                                             '%Y:%m:%d:%H:%M:%S.%f').replace(
                                                      tzinfo=timezone.utc).timestamp(),
                                                              1: float, 2: float, 3: float, 4: float, 5: float})
                    self.pipetracker = np.concatenate((pipetracker_file, np.zeros((len(pipetracker_file), 8))),
                                                      axis=1)

                    # depth to field 3 from field 4 (and negating Z)
                    self.pipetracker[:, 3] = -self.pipetracker[:, 4]
                    # populating 'smoothed' fields from 'raw'
                    self.pipetracker[:, 4:7] = self.pipetracker[:, 1:4]

                    self._rechain_pipetracker(self.pipetracker)

                if _ext == '.fug':
                    pipetracker_file = np.loadtxt(fName, skiprows=1, delimiter=',',
                                                  converters={0: lambda x: datetime.strptime(x,
                                                                                             '%d/%m/%Y %H:%M:%S.%f').replace(
                                                      tzinfo=timezone.utc).timestamp(),
                                                              1: float, 2: float, 3: float})
                    self.pipetracker = np.concatenate((pipetracker_file, np.zeros((len(pipetracker_file), 10))),
                                                      axis=1)

                    # negating Z
                    self.pipetracker[:, 3] *= -1
                    # populating 'smoothed' fields from 'raw'
                    self.pipetracker[:, 4:7] = self.pipetracker[:, 1:4]

                    self._rechain_pipetracker(self.pipetracker)

                if _ext == '.spt':
                    with open(fName, 'rb') as loadfile:
                        self.pipetracker = pickle.load(loadfile)

                # FOR ALL PT TYPES
                # interpolating tide from flush to pipetracker filed 7
                if self._controller.Tideflag:
                    self.pipetracker[:, 7] = np.interp(self.pipetracker[:, 0], self.flush[:, 14],
                                                       self.flush[:, 15])

                self.weed_pipetracker()
                self._controller.Ptflag = True


    def loadtif(self, _ext, fName):
        geodata = []  # georef data list
        # open image, read metadata
        img = Image.open(fName)
        geoimage = np.swapaxes(np.array(img), 0, 1)

        if _ext in ['.tif', '.tiff']:
            refName = fName[: -len(_ext)] + '.tfw'  # world file name
        elif _ext in ['.png']:
            refName = fName[: -len(_ext)] + '.pgw'  # world file name

        try:
            with img:
                meta_dict = {TAGS[key]: img.tag[key] for key in img.tag_v2}

            # reading georef data from tif metadata or ref world file
            # if 'ModelTiepointTag' in meta_dict.keys() and 'ModelPixelScaleTag' in meta_dict.keys():
            geodata.append(float(meta_dict['ModelPixelScaleTag'][0]))
            geodata.append(0)
            geodata.append(0)
            geodata.append(0)
            geodata.append(float(meta_dict['ModelTiepointTag'][3]))
            geodata.append(float(meta_dict['ModelTiepointTag'][4]))
            available_geodata = True
        except (AttributeError, KeyError):
            if os.path.isfile(refName):
                with open(refName, 'r') as refFile:
                    refString = refFile.readlines()
                for line in refString:
                    geodata.append(float(line.replace('\n', '')))
                available_geodata = True
            else:
                self._controller.messagepop('No geodata available\ngeoimage not loaded')

        if available_geodata:
            # load image to plan view
            cellsize = geodata[0]
            o_left, o_top = geodata[4], geodata[5]

            return geoimage, cellsize, o_left, o_top


    def loadplaylist(self, _ext, fName):
        pass


    def save_work(self, foldName):
        views_geometry = []
        for view in [self._controller._mainWin,
                     self._controller._xv,
                     self._controller._pv,
                     self._controller._lv, ]:
            views_geometry.append([view.rect(), view.pos()])

        saving_time = str(datetime.now().strftime('%Y%m%d%H%M%S'))
        wrk_dumpfilename = os.path.join(foldName, Path(os.path.basename(self.profName)).stem) + '_' + saving_time + '.wrk'

        with open(wrk_dumpfilename, 'wb') as dumpfile:
            dump = [views_geometry, self.prno,
                    self.profName, self.no_of_prof, self.profiles, self.flush,
                    self.pipeD, self.pipeR, self.inWall, self.outWall,
                    self.HWin, self.VWin, self.Res,
                    self.FlD, self.FlP, self.AntiSpoof, self.AntiSpoof_A,
                    self.FoDist,
                    self._controller.Tideflag, self._controller.Appliedflag,
                    self._controller.cProfile, self._controller.cPipe,
                    self._controller.cLeftM, self._controller.cRightM,
                    self._controller.cNotVis, self._controller.cVis,
                    self._controller.cMADJ, self._controller.cMSBL,
                    self._controller.cPipetracker, self._controller.cCurrentProf,
                    self._controller.cBackground]
            pickle.dump(dump, dumpfile)

        if self._controller.Ptflag:
            pt_dumpfilename = os.path.join(foldName, Path(os.path.basename(self.profName)).stem) + '_PT_' + saving_time + '.spt'

            with open(pt_dumpfilename, 'wb') as dumpfile:
                dump = self.pipetracker
                pickle.dump(dump, dumpfile)

        return saving_time


    def save_result(self, format, fName):
        if format == 'exporteiva':
            out_top = out_li = out_ri = out_lo = out_ro = '#unit=m\n'
            out_top += '#Type=Pipe\n'
            for point in self.flush:
                appliedtide = self._controller.Tideflag * self._controller.Appliedflag * point[15]
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

        if format == 'exportsfx':
            out_top = out_li = out_ri = out_lo = out_ro = '' #'timedate,edited_easting,edited_northing,edited_height\n'
            c = 50001
            for point in self.flush:
                appliedtide = self._controller.Tideflag * self._controller.Appliedflag * point[15]
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


    def auto_run(self):
        if self._controller.ChunkSelCounter == 2:
            s, e = self.chunk[0], self.chunk[1]
        else:
            s, e = self.prno, self.no_of_prof - 1

        self._controller.DoPipe = True
        for self.prno in range(s, e + 1):
            self.make_profile()
        self._controller.DoPipe = False


    def level_pipetracker(self):
        self.pipetracker[:, 11] = self.pt_Level
        self.pipetracker_W[:, 11] = self.pt_Level


    def smooth_pipetracker(self, sender):
        acc_starts_ix, acc_ends_ix = self._find_gaps_on_pipetracker_W()

        # smoothing window
        sm_win = self.p_SmoothWin if sender == 'b_smoothPT_p'  else self.l_SmoothWin
        filt = np.ones(sm_win)
        mov = sm_win // 2

        # smoothing parts
        for s, e in zip(acc_starts_ix, acc_ends_ix):
            _for_smooth = self.pipetracker_W[s + 1: e + 1][self.pipetracker_W[s + 1: e + 1, 9] == 0]
            if len(_for_smooth) > 2 * sm_win:  # !!!! only smoothing if section > window +- margin (window/2)
                if sender == 'b_smoothPT_p':  # smoothing plan
                    if sm_win != 0:  # smooth
                        _for_smooth[:, 4][mov:-mov] = (np.convolve(_for_smooth[:, 1], filt, 'same') / sm_win)[
                            mov:-mov]
                        _for_smooth[:, 5][mov:-mov] = (np.convolve(_for_smooth[:, 2], filt, 'same') / sm_win)[
                            mov:-mov]
                        self.pipetracker_W[s + 1: e + 1, 4][self.pipetracker_W[s + 1: e + 1, 9] == 0] = _for_smooth[:, 4]
                        self.pipetracker_W[s + 1: e + 1, 5][self.pipetracker_W[s + 1: e + 1, 9] == 0] = _for_smooth[:, 5]
                elif sender == 'b_smoothPT_l':  # smoothing depth
                    if sm_win != 0:  # smooth
                        _for_smooth[:, 6][mov:-mov] = (np.convolve(_for_smooth[:, 3], filt, 'same') / sm_win)[
                            mov:-mov]
                        self.pipetracker_W[s + 1: e + 1, 6][self.pipetracker_W[s + 1: e + 1, 9] == 0] = _for_smooth[:, 6]

        # reset all but rejected
        if sm_win == 0:
            self.pipetracker_W[:, 4] = self.pipetracker_W[:, 1]
            self.pipetracker_W[:, 5] = self.pipetracker_W[:, 2]
            self.pipetracker_W[:, 6] = self.pipetracker_W[:, 3] + self.pipetracker_W[:, 11]
            # self.pipetracker_W[:, 11] = 0

        self._rechain_pipetracker(self.pipetracker_W)


    def snap_top_to_pipetracker(self, sender):
        acc_starts_ix, acc_ends_ix = self._find_gaps_on_pipetracker_W()

        if self._controller.ChunkSelCounter == 2:
            chs, che = self.chunk[0], self.chunk[1]
        else:
            chs, che = 0, self.no_of_prof - 1

        for s, e in zip(acc_starts_ix, acc_ends_ix):
            if (s <= che) & (chs <= e):
                _p_part = (self.flush[chs:che + 1, 13][
                    (s <= self.flush[chs:che + 1, 13]) & (self.flush[chs:che + 1, 13] <= e)]).astype('int')

                if sender == 'b_snap_h':
                    self.flush[_p_part, 9] = np.interp(self.flush[_p_part, 12],
                                                       self.pipetracker_W[:, 8][self.pipetracker_W[:, 9] == 0],
                                                       self.pipetracker_W[:, 4][self.pipetracker_W[:, 9] == 0])
                    self.flush[_p_part, 10] = np.interp(self.flush[_p_part, 12],
                                                        self.pipetracker_W[:, 8][self.pipetracker_W[:, 9] == 0],
                                                        self.pipetracker_W[:, 5][self.pipetracker_W[:, 9] == 0])

                if sender == 'b_snap_v':
                    self.flush[_p_part, 4] = np.interp(self.flush[_p_part, 12],
                                                       self.pipetracker_W[:, 8][self.pipetracker_W[:, 9] == 0],
                                                       self.pipetracker_W[:, 6][self.pipetracker_W[:, 9] == 0] +
                                                       self.pipetracker_W[:, 11][self.pipetracker_W[:, 9] == 0])

        self._upd_mincx_flags(chs, che)


    def _find_gaps_on_pipetracker_W(self):
        # search starts/ends of accepted parts based on min Pt gap criteria
        accepted = self.pipetracker_W[self.pipetracker_W[:, 9] == 0]
        accepted_ixs = (accepted[:, 10]).astype('int')

        acc_start, acc_end = accepted_ixs[0], accepted_ixs[-1]

        accepted[1:, 13] = np.diff(accepted[:, 12])  # chainage differences forward
        acc_starts_ix = np.insert((accepted[:, 10][accepted[:, 13] > self.PtGap]).astype('int'), 0, acc_start)

        accepted[-2::-1, 13] = np.diff(accepted[::-1, 12])  # chainage differences backward
        acc_ends_ix = np.append((accepted[:, 10][accepted[:, 13] < -self.PtGap]).astype('int'), acc_end)

        return acc_starts_ix, acc_ends_ix


    def _rechain_pipetracker(self, pipetracker):
        _pipetracker = pipetracker
        _pipetracker[:, 8] = _F_kp_to_point.go(self.flush[:, [9, 10, 12]], _pipetracker[:, [4, 5]])[:, 2]

        # filling sequential point no to pipetracker filed 10
        _pipetracker[:, 10] = np.arange(len(_pipetracker))
        # re-compute chainage
        _pipetracker[1:, 12] = np.cumsum((np.diff(_pipetracker[:, 1]) ** 2 +
                                          np.diff(_pipetracker[:, 2]) ** 2) ** 0.5)


    def weed_pipetracker(self):
        self.pipetracker_W = self.pipetracker.copy()[::self.weed_pt]


    def interpolate_chunk(self):
        chs, che = self.chunk[0], self.chunk[1]
        chs_e, che_e = self.flush[chs, 9], self.flush[che, 9]
        chs_n, che_n = self.flush[chs, 10], self.flush[che, 10]
        chs_z, che_z = self.flush[chs, 4], self.flush[che, 4]

        self.flush[chs:che + 1, 9] = np.interp(self.flush[chs:che + 1, 13],
                                               [chs, che], [chs_e, che_e])
        self.flush[chs:che + 1, 10] = np.interp(self.flush[chs:che + 1, 13],
                                                [chs, che], [chs_n, che_n])
        self.flush[chs:che + 1, 4] = np.interp(self.flush[chs:che + 1, 13],
                                               [chs, che], [chs_z, che_z])

        self._upd_mincx_flags(chs, che)


    def _upd_mincx_flags(self, s, e):
        # new min_cx distance
        new_dist = ((self.flush[s:e + 1, 0] - self.flush[s:e + 1, 9]) ** 2 +
                    (self.flush[s:e + 1, 1] - self.flush[s:e + 1, 10]) ** 2) ** 0.5

        # new min_cx (min_cx distance projected to profile)
        brg = _F_funcs.Bearing((self.flush[s:e + 1, 9] - self.flush[s:e + 1, 0]),
                               (self.flush[s:e + 1, 10] - self.flush[s:e + 1, 1]))
        self.flush[s:e + 1, 3] = new_dist * np.sin(brg - np.deg2rad(self.flush[s:e + 1, 2]))

        # set visited (prevents changing TOP in AutoPipe() but re-sets flags based on Interpolation flag)
        self.flush[s:e + 1, 11] = 1

        self._controller.Interpflag = True
        for i in range(s, e + 1):
            self.prno = i
            self.make_profile()
        self._controller.Interpflag = False

        self.chunk = [-1, -1]
        self._controller.ChunkSelCounter = 0


    def make_shapes(self):
        # make shapes of view elements (pipe, walls, antispoof)
        pipe_P_pts = [self.pipeR * self.pipeshape_cos,
                      self.pipeR * self.pipeshape_sin]
        pipe_I_pts = [self.inWall * self.pipeR * self.pipeshape_cos,
                      self.inWall * self.pipeR * self.pipeshape_sin]
        pipe_O_pts = [self.outWall * self.pipeR * self.pipeshape_cos,
                      self.outWall * self.pipeR * self.pipeshape_sin]
        # -------------------------antispoof
        ax = ((self.pipeR + self.AntiSpoof) *
              self.pipeshape_cos[(180 - int(self.AntiSpoof_A)):(180 + int(self.AntiSpoof_A))])
        ay = ((self.pipeR + self.AntiSpoof) *
              self.pipeshape_sin[(180 - int(self.AntiSpoof_A)):(180 + int(self.AntiSpoof_A))])
        pipe_A_pts = [np.hstack((np.zeros((1)), ax, np.zeros((1)))),
                      np.hstack((np.zeros((1)), ay, np.zeros((1))))]
        # -------------------------antispoof
        assist_pts = [self.pipeR * self.pipeshape_cos,
                      self.pipeR * self.pipeshape_sin]
        pt_sel_pts_p = [[-self.p_EditSpot / 2, -self.p_EditSpot / 2, self.p_EditSpot / 2,
                       self.p_EditSpot / 2, -self.p_EditSpot / 2],
                      [-self.p_EditSpot / 2, self.p_EditSpot / 2, self.p_EditSpot / 2,
                       -self.p_EditSpot / 2, -self.p_EditSpot / 2]]
        pt_sel_pts_l = [[-self.l_EditSpot / 2,
                       -self.l_EditSpot / 2,
                       self.l_EditSpot / 2,
                       self.l_EditSpot / 2,
                       -self.l_EditSpot / 2],
                      [-self.l_EditSpot / (2 / self._controller._lv.aspect),
                       self.l_EditSpot / (2 / self._controller._lv.aspect),
                       self.l_EditSpot / (2 / self._controller._lv.aspect),
                       -self.l_EditSpot / (2 / self._controller._lv.aspect),
                       -self.l_EditSpot / (2 / self._controller._lv.aspect)]]

        # set shapes of view elements (pipe, walls, antispoof), points are calculate in _model.make_shapes
        self._controller._xv.pipe_P.setData(pipe_P_pts[0], pipe_P_pts[1])
        self._controller._xv.pipe_I.setData(pipe_I_pts[0], pipe_I_pts[1])
        self._controller._xv.pipe_O.setData(pipe_O_pts[0], pipe_O_pts[1])
        self._controller._xv.pipe_A.setData(pipe_A_pts[0], pipe_A_pts[1])
        self._controller._xv.pipeassist.setData(assist_pts[0], assist_pts[1])
        self._controller._pv.pt_selector.setData(pt_sel_pts_p[0], pt_sel_pts_p[1])
        self._controller._lv.pt_selector.setData(pt_sel_pts_l[0], pt_sel_pts_l[1])


    def make_profile(self):
        # read profile array (for AutoPipe and AutoFlag)
        self.profile = self.profiles[self.prno][::(self.weed)]

        # reset xini to centre of profile if profile is far from xini (wrong profile export)
        if not(np.min(self.profile[:, 0]) < self.xini < np.max(self.profile[:, 0])):
            self.xini = np.mean(self.profile[:, 0])

        # if already visited (or when opening wrk file) - search window is not plotted on Xview
        # this works if no AutoPipe is running and port/stbd/high/low not computed but needed
        self.port = self.stbd = self.min_cx = self.flush[self.prno, 3]
        self.high = self.low = self.min_cz = self.flush[self.prno, 4]

        self._autopipe()


    def manual_pipe(self):
        # write flag 'unvisited' for AutoFlags
        self.flush[self.prno, 11] = 0
        self.flush[self.prno, 3] = self.min_cx
        self.flush[self.prno, 4] = self.flush[self.prno:, 4][
            self.flush[self.prno:, 11] == 0] = self.min_cz + self.pipeR  # + T
        # write to flush top_, top_n
        ref_east, ref_north, hdg = (self.flush[self.prno, 0],
                                    self.flush[self.prno, 1],
                                    self.flush[self.prno, 2])
        # top
        top = _F_funcs.Rotation2D(self.min_cx, self.flush[self.prno, 0],
                                  self.flush[self.prno, 1], hdg)
        self.flush[self.prno, 9] = top[0]
        self.flush[self.prno, 10] = top[1]

        self._controller.ManualPipe = True

        self._autopipe()


    def manual_flags(self, lfl_x, lfl_z, rfl_x, rfl_z, flag):
        # flags en
        ref_east, ref_north, hdg = self.flush[self.prno, 0], self.flush[self.prno, 1], self.flush[self.prno, 2]
        # left inner flag
        lfl_en = _F_funcs.Rotation2D(lfl_x, ref_east, ref_north, hdg)
        lfl_e, lfl_n = round(lfl_en[0], 3), round(lfl_en[1], 3)
        # right inner flag
        rfl_en = _F_funcs.Rotation2D(rfl_x, ref_east, ref_north, hdg)
        rfl_e, rfl_n = round(rfl_en[0], 3), round(rfl_en[1], 3)

        if flag == 'Inner':
            a, b, c, d, e, f, g, h = 5, 6, 7, 8, 20, 21, 22, 23
        if flag == 'Outer':
            a, b, c, d, e, f, g, h = 16, 17, 18, 19, 24, 25, 26, 27

        self.flush[self.prno, a] = self.flush[self.prno:, a][self.flush[self.prno:, 11] == 0] = lfl_x
        self.flush[self.prno, b] = self.flush[self.prno:, b][self.flush[self.prno:, 11] == 0] = lfl_z
        self.flush[self.prno, c] = self.flush[self.prno:, c][self.flush[self.prno:, 11] == 0] = rfl_x
        self.flush[self.prno, d] = self.flush[self.prno:, d][self.flush[self.prno:, 11] == 0] = rfl_z
        self.flush[self.prno, e] = self.flush[self.prno:, e][self.flush[self.prno:, 11] == 0] = lfl_e
        self.flush[self.prno, f] = self.flush[self.prno:, f][self.flush[self.prno:, 11] == 0] = lfl_n
        self.flush[self.prno, g] = self.flush[self.prno:, g][self.flush[self.prno:, 11] == 0] = rfl_e
        self.flush[self.prno, h] = self.flush[self.prno:, h][self.flush[self.prno:, 11] == 0] = rfl_n


    def _autopipe(self):
        # AutoPipe only runs if: profile not visited AND no ManualPipe selected OR Autorun
        # or DoPipe - autopipe
        if (not self.flush[self.prno, 11] and not self._controller.ManualPipe) or self._controller.DoPipe:
            # profile window (part of profile used for TOP search = xini +- HWin/2 +- pipeR)
            prof_win = np.where((self.xini - self.HWin / 2 - self.pipeR <= self.profile[:, 0]) &
                                (self.profile[:, 0] <= self.xini + self.HWin / 2 + self.pipeR))[0]
            # TOP search window (profile_window +- pipeR; minZ (in window) + VWin = maxZ)
            self.port = self.xini - self.HWin / 2
            self.stbd = self.xini + self.HWin / 2
            cent_win = np.where((self.port <= self.profile[:, 0]) & (self.profile[:, 0] <= self.stbd))[0]
            self.high = max(self.profile[cent_win, 1] - self.pipeR)
            self.low = self.high - self.VWin

            # evenly spaced h/v centre search spots - search grid
            x_grid = np.arange(self.port, self.stbd, self.Res)
            z_grid = np.arange(self.low, self.high, self.Res)

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
                    point_to_c = ((cx - self.profile[prof_win, 0][self.profile[prof_win, 1] >= cz]) ** 2 +
                                  (cz - self.profile[prof_win, 1][self.profile[prof_win, 1] >= cz]) ** 2) ** 0.5
                    # distances array where points are within wall
                    point_to_c_within_wall = point_to_c[(self.inWall * self.pipeR <= point_to_c) &
                                                               (point_to_c <= self.outWall * self.pipeR)]
                    # filling evf array
                    evf[cell, 0] = len(point_to_c_within_wall)
                    evf[cell, 1] = Decimal(np.sum((point_to_c_within_wall - self.inWall * self.pipeR) ** 2))
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

            self.min_cx = round(x_grid[min_col], 4)
            self.min_cz = round(z_grid[min_row], 4)

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
            ref_east, ref_north, hdg = self.flush[self.prno, 0], self.flush[self.prno, 1], self.flush[self.prno, 2]
            # top
            top = _F_funcs.Rotation2D(self.min_cx, self.flush[self.prno, 0], self.flush[self.prno, 1], hdg)
            self.flush[self.prno, 9] = top[0]
            self.flush[self.prno, 10] = top[1]

            # xini for next profile
            self.xini = self.min_cx

            # write to flush: top_x, top_z
            self.flush[self.prno, 3] = self.min_cx
            self.flush[self.prno, 4] = self.flush[self.prno:, 4][self.flush[self.prno:, 11] == 0] =(
                    self.min_cz + self.pipeR)

        self._controller.ManualPipe = False       # reset flag if manual pipe placement was done

        self._autoflags()


    def _autoflags(self):
        # AutoFlags only runs if: profile unvisited OR running [interpolation / snap to PT] OR AutoRun
        if not self.flush[self.prno, 11] or self._controller.Interpflag or self._controller.DoPipe:
            self.min_cx = self.flush[self.prno, 3]
            self.min_cz = self.flush[self.prno, 4] - self.pipeR
            # inner flags - initial position
            self.li_x, self.ri_x = self.min_cx - self.FlD, self.min_cx + self.FlD
            self.li_z = self.ri_z = self.min_cz
            # outer flags - initial position
            self.lo_x, self.ro_x = self.min_cx - self.FlD, self.min_cx + self.FlD
            self.lo_z = self.ro_z = self.min_cz

            try:
                # set extended / narrow spot
                if self._controller._mainWin.rb_Fadapt.isChecked():
                    # extended spot -+ AdPadli_x(ri_x) +-inflag_patch to -+inflag_patch - for adaptive mode
                    self.li_spot = (
                        np.where((self.min_cx - self.FlD - self.FlP <= self.profile[:, 0]) &
                                 (self.profile[:, 0] <= self.min_cx - self.AdPad)))
                    self.ri_spot =(
                        np.where((self.min_cx + self.AdPad <= self.profile[:, 0]) &
                                 (self.profile[:, 0] <= self.min_cx + self.FlD + self.FlP)))
                else:
                    # narrow spot li_x(ri_x)+-inflag_patch to inflag - for other modes
                    self.li_spot =(
                        np.where((self.min_cx - self.FlD - self.FlP <= self.profile[:, 0]) &
                                 (self.profile[:, 0] <= self.min_cx - self.FlD)))
                    self.ri_spot =(
                        np.where((self.min_cx + self.FlD <= self.profile[:, 0]) &
                                 (self.profile[:, 0] <= self.min_cx + self.FlD + self.FlP)))

                if len(self.li_spot[0]) != 0 and len(self.ri_spot[0]) != 0:
                    # if in bad profile low number of datapoints (not hitting flag patch)
                    if self._controller._mainWin.rb_Fmean.isChecked():
                        # no point snapping for 'mean'
                        self.li_x, self.ri_x = self.min_cx - self.FlD, self.min_cx + self.FlD
                        self.li_z, self.ri_z = np.mean(self.profile[self.li_spot][:, 1]), np.mean(self.profile[self.ri_spot][:, 1])

                    elif self._controller._mainWin.rb_Fmin.isChecked():
                        if not self._controller._mainWin.ch_FiSnap.isChecked():
                            self.li_x, self.ri_x = self.min_cx - self.FlD, self.min_cx + self.FlD
                            self.li_z, self.ri_z = np.max(self.profile[self.li_spot][:, 1]), np.max(
                                self.profile[self.ri_spot][:, 1])
                        else:
                            self.li_ix, self.ri_ix = np.argmax(self.profile[self.li_spot][:, 1]), np.argmax(
                                self.profile[self.ri_spot][:, 1])
                            self.li_x, self.ri_x = (self.profile[self.li_spot][self.li_ix, 0],
                                                    self.profile[self.ri_spot][self.ri_ix, 0])
                            self.li_z, self.ri_z = (self.profile[self.li_spot][self.li_ix, 1],
                                                    self.profile[self.ri_spot][self.ri_ix, 1])

                    elif self._controller._mainWin.rb_Fmax.isChecked():
                        if not self._controller._mainWin.ch_FiSnap.isChecked():
                            self.li_x, self.ri_x = self.min_cx - self.FlD, self.min_cx + self.FlD
                            self.li_z, self.ri_z = np.min(self.profile[self.li_spot][:, 1]), np.min(
                                self.profile[self.ri_spot][:, 1])
                        else:
                            self.li_ix, self.ri_ix = np.argmin(self.profile[self.li_spot][:, 1]), np.argmin(
                                self.profile[self.ri_spot][:, 1])
                            self.li_x, self.ri_x = (self.profile[self.li_spot][self.li_ix, 0],
                                                    self.profile[self.ri_spot][self.ri_ix, 0])
                            self.li_z, self.ri_z = (self.profile[self.li_spot][self.li_ix, 1],
                                                    self.profile[self.ri_spot][self.ri_ix, 1])

                    elif self._controller._mainWin.rb_Fadapt.isChecked():
                        # distances and vertical angles from pipe centre to profile points
                        li_d = ((self.profile[self.li_spot][:, 0] - self.min_cx) ** 2 + (
                                    self.profile[self.li_spot][:, 1] - self.min_cz) ** 2) ** 0.5
                        ri_d = ((self.profile[self.ri_spot][:, 0] - self.min_cx) ** 2 + (
                                    self.profile[self.ri_spot][:, 1] - self.min_cz) ** 2) ** 0.5
                        li_a = np.rad2deg(_F_funcs.Bearing(self.profile[self.li_spot][:, 0] - self.min_cx,
                                                           self.profile[self.li_spot][:, 1] - self.min_cz)) - 360
                        ri_a = np.rad2deg(_F_funcs.Bearing(self.profile[self.ri_spot][:, 0] - self.min_cx,
                                                           self.profile[self.ri_spot][:, 1] - self.min_cz))

                        # set d == 1000 if within pipe + anti-spoof sector (to reject from min dist)
                        li_d[:][li_d[:] <= self.pipeR] = 100000
                        ri_d[:][ri_d[:] <= self.pipeR] = 100000

                        li_d[:][(li_d[:] <= (self.AntiSpoof + self.pipeR)) &
                                (li_a[:] >= -self.AntiSpoof_A)] = 100000
                        ri_d[:][(ri_d[:] <= (self.AntiSpoof + self.pipeR)) &
                                (ri_a[:] <= self.AntiSpoof_A)] = 100000


                        flagdetected = False  # !!! True if adaptive algo works; False otherwise
                        for dist, flagspot, side in zip([li_d, ri_d],
                                                        [self.profile[self.li_spot],
                                                         self.profile[self.ri_spot]],
                                                        ['l', 'r']):
                            # closest point to pipe (outside wall+antispoof)
                            closest_ix = np.argmin(dist)
                            closest_dx, closest_z = flagspot[closest_ix, 0], flagspot[closest_ix, 1]

                            if (self.min_cz - self.pipeR - self.AntiSpoof <= closest_z <
                                    self.min_cz + self.pipeR + self.AntiSpoof):
                                # if closest point z is within pipe centre z +- R (& AntiSpoof)
                                # takes closest point
                                fl_x, fl_z = closest_dx, closest_z
                                flagdetected = True
                            else:
                                if closest_z > self.min_cz + self.pipeR + self.AntiSpoof:
                                    # if closest profile point z is higher than pipe (& AntiSpoof)
                                    # takes point closest to min_cx
                                    if len(flagspot[:, 0]) != 0:
                                        fl_ix = np.argmin(np.abs(flagspot[:, 0] - self.min_cx))
                                        fl_x, fl_z = flagspot[fl_ix, 0], flagspot[fl_ix, 1]
                                        flagdetected = True
                                else:
                                    # if closest profile point z is lower than pipe (& AntiSpoof)
                                    # takes closest point to min_cx where z < lower than pipe wall (& antispoof)
                                    if len(flagspot[:, 0][flagspot[:, 1] < self.min_cz - self.pipeR]) != 0:
                                        fl_ix = np.argmin(
                                            np.abs(flagspot[:, 0][flagspot[:, 1] < self.min_cz - self.pipeR] - self.min_cx))
                                        fl_x = (flagspot[:][flagspot[:, 1] < self.min_cz - self.pipeR])[fl_ix, 0]
                                        fl_z = (flagspot[:][flagspot[:, 1] < self.min_cz - self.pipeR])[fl_ix, 1]
                                        flagdetected = True

                            if side == 'l' and flagdetected:
                                self.li_x, self.li_z = fl_x, fl_z
                            if side == 'r' and flagdetected:
                                self.ri_x, self.ri_z = fl_x, fl_z

                # outer flags
                self.lo_ix = np.argmin(np.abs(self.profile[:, 0] - (self.min_cx - self.FoDist)))
                self.ro_ix = np.argmin(np.abs(self.profile[:, 0] - (self.min_cx + self.FoDist)))
                self.lo_z, self.ro_z = self.profile[self.lo_ix, 1], self.profile[self.ro_ix, 1]

                if not self._controller._mainWin.ch_FoSnap.isChecked():
                    self.lo_x, self.ro_x = self.min_cx - self.FoDist, self.min_cx + self.FoDist
                else:
                    self.lo_x, self.ro_x = self.profile[self.lo_ix, 0], self.profile[self.ro_ix, 0]

            except:
                pass

            # write to flush flags x & z
            self.flush[self.prno, 5] = self.flush[self.prno:, 5][self.flush[self.prno:, 11] == 0] = self.li_x
            self.flush[self.prno, 6] = self.flush[self.prno:, 6][self.flush[self.prno:, 11] == 0] = self.li_z
            self.flush[self.prno, 7] = self.flush[self.prno:, 7][self.flush[self.prno:, 11] == 0] = self.ri_x
            self.flush[self.prno, 8] = self.flush[self.prno:, 8][self.flush[self.prno:, 11] == 0] = self.ri_z
            self.flush[self.prno, 16] = self.flush[self.prno:, 16][self.flush[self.prno:, 11] == 0] = self.lo_x
            self.flush[self.prno, 17] = self.flush[self.prno:, 17][self.flush[self.prno:, 11] == 0] = self.lo_z
            self.flush[self.prno, 18] = self.flush[self.prno:, 18][self.flush[self.prno:, 11] == 0] = self.ro_x
            self.flush[self.prno, 19] = self.flush[self.prno:, 19][self.flush[self.prno:, 11] == 0] = self.ro_z

            # flags en
            ref_east, ref_north, hdg = self.flush[self.prno, 0], self.flush[self.prno, 1], self.flush[self.prno, 2]
            # left inner flag
            li_en = _F_funcs.Rotation2D(self.li_x, ref_east, ref_north, hdg)
            li_e, li_n = round(li_en[0], 3), round(li_en[1], 3)
            # right inner flag
            ri_en = _F_funcs.Rotation2D(self.ri_x, ref_east, ref_north, hdg)
            ri_e, ri_n = round(ri_en[0], 3), round(ri_en[1], 3)
            # left outer flag
            lo_en = _F_funcs.Rotation2D(self.lo_x, ref_east, ref_north, hdg)
            lo_e, lo_n = round(lo_en[0], 3), round(lo_en[1], 3)
            # right inner flag
            ro_en = _F_funcs.Rotation2D(self.ro_x, ref_east, ref_north, hdg)
            ro_e, ro_n = round(ro_en[0], 3), round(ro_en[1], 3)

            # write to flash flags e & n
            self.flush[self.prno, 20] = li_e
            self.flush[self.prno, 21] = li_n
            self.flush[self.prno, 22] = ri_e
            self.flush[self.prno, 23] = ri_n
            self.flush[self.prno, 24] = lo_e
            self.flush[self.prno, 25] = lo_n
            self.flush[self.prno, 26] = ro_e
            self.flush[self.prno, 27] = ro_n

            # write to flash flag = 'visited'
            self.flush[self.prno, 11] = 1


        if not self._controller.Interpflag and not self._controller.DoPipe:
            pass
            # return self.profile


