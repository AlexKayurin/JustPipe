import os
import pathlib
import re
from datetime import datetime, timezone
from moviepy.video.io.VideoFileClip import VideoFileClip


def buildplaylist(foldName, convention):
    # pattern to search file start time in filename
    timepattern = '%Y%m%d%H%M%S'  
    
    chset = set()       # set for channel names
    playlist = []       # full filename, fps, total frames, duration, s_tstamp, e_tstamp, chname
    for root, dirs, files in os.walk(foldName, topdown=False):
        for fname in files:
            ext = pathlib.Path(fname).suffix
            filetimestring = re.search(r'\d{14}', fname)

            if filetimestring and ext in ['.mp4', '.asf', '.mkv']:
                # get video metadata
                video = VideoFileClip(os.path.join(root, fname))
                duration       = video.duration
                # print(duration)
                #fps            = video.fps
                #width, height  = video.size

                if convention != 14:
                    backindent = 14 - convention
                    filetstart = datetime.strptime(filetimestring[0][:backindent], timepattern)
                else:
                    filetstart = datetime.strptime(filetimestring[0], timepattern)

                tstamp = filetstart.replace(tzinfo=timezone.utc).timestamp()

                parsed_fname = re.split(r'_|\.|\@', fname)
                
                # [full filename (with path)
                # duration (sec)
                # start timestamp
                # end timestamp
                # channel name]
                playlist.append([os.path.join(root, fname), duration, tstamp, tstamp + duration, parsed_fname[-2]])
                # [cannellist]
                chset.add(parsed_fname[-2])

    return [playlist, sorted(chset)]
