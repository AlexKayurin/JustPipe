import os
import sys
import re
import pickle
from datetime import datetime, timezone
from pathlib import Path

from PySide6 import QtGui
from PySide6.QtCore import QUrl, QTimer, QSize
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
    QMessageBox,
)
from PySide6.QtMultimedia import QMediaPlayer


VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.wmv',
    '.flv', '.asf', '.m4v', '.mpeg', '.mpg'
}

TIMEPATTERN = '%Y%m%d%H%M%S'

class DvIndexBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 500)

        self.channel_set = set()    # set for channel names
        self.dvindex = []           # full filename (with path), duration, s_tstamp, e_tstamp (s_timestamp+duration), channel_name

        self.files = []             # list of dv files in folder
        self.current_index = 0      # ix in files list

        # Media player used to read duration
        self.player = QMediaPlayer(self)

        # QMediaPlayer emits durationChanged when duration is known
        self.player.durationChanged.connect(self.duration_changed)

        # If media fails to load
        self.player.errorOccurred.connect(self.media_error)

        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Folder selection
        folder_layout = QHBoxLayout()

        self.folder_label = QLabel("No folder selected")

        self.select_button = QPushButton("Select Folder")
        self.select_button.setFixedSize(QSize(120, 40))
        self.select_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.select_button)
        folder_layout.addWidget(self.folder_label, 1)

        layout.addLayout(folder_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([
            'File',
            'Duration',
            'Status'
        ])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            0, self.table.horizontalHeader().ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Progress
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.status_label = QLabel('Select DV folder')
        layout.addWidget(self.status_label)


    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            'Select DV folder'
        )

        if not folder:
            return

        self.folder_label.setText(folder)

        self.index_fName, _ = QFileDialog.getSaveFileName(self, 'Select as dv index file',
                                                          '',
                                                          'DV index files (*.dvi);;All Files (*)')

        if not self.index_fName:
            return

        self.find_videos(Path(folder))


    def find_videos(self, folder: Path):
        self.files = []

        for root, dirs, files in  os.walk(folder, topdown=False):
            for name in files:
                if Path(os.path.join(root, name)).suffix.lower() in VIDEO_EXTENSIONS:
                    timestring = re.search(r'\d{14}', name)         # contains 14 digits time (yyyymmddhhmmss)
                    if timestring:
                        self.files.append((Path(os.path.join(root, name))))

        self.files.sort()

        if not self.files:
            QMessageBox.information(
                self,
                'No Videos',
                'No supported video files were found.'
            )
            return

        self.table.setRowCount(0)

        for path in self.files:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(path.name)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem('Reading...')
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem('Waiting')
            )

        self.table.resizeColumnsToContents()

        self.current_index = 0
        self.progress.setMaximum(len(self.files))
        self.progress.setValue(0)

        self.read_next_video()


    def read_next_video(self):
        if self.current_index >= len(self.files):
            with open(self.index_fName, 'wb') as dumpfile:
                pickle.dump([self.dvindex, sorted(self.channel_set)], dumpfile)

            self.status_label.setText(f'Finished. {len(self.files)} videos scanned. DV index saved.')

            return

        path = self.files[self.current_index]

        row = self.current_index

        self.table.item(row, 2).setText('Loading')
        self.status_label.setText(
            f'Reading: {path.name}'
        )

        # Reset player before loading another file
        self.player.stop()

        # Load video
        self.player.setSource(
            QUrl.fromLocalFile(str(path))
        )


    def duration_changed(self, duration_ms):
        # duration can initially be 0 while the media is loading
        if duration_ms <= 0:
            return

        if self.current_index >= len(self.files):
            return

        _dvname = self.files[self.current_index]
        _timestring = re.search(r'\d{14}', str(_dvname))
        _filetstart = datetime.strptime(_timestring[0], TIMEPATTERN)
        _tstamp = _filetstart.replace(tzinfo=timezone.utc).timestamp()
        _parsed_fname = re.split(r'_|\.|\@', str(_dvname))

        self.dvindex.append([_dvname, duration_ms / 1000, _tstamp, _tstamp + (duration_ms / 1000), _parsed_fname[-2]])
        self.channel_set.add(_parsed_fname[-2])

        duration_to_show = self.format_duration(duration_ms)
        row = self.current_index
        self.table.item(row, 1).setText(duration_to_show)
        self.table.item(row, 2).setText('OK')

        self.progress.setValue(self.current_index + 1)

        self.current_index += 1

        # Give QMediaPlayer time to release/change media
        QTimer.singleShot(50, self.read_next_video)


    def media_error(self, error, error_string):
        if self.current_index >= len(self.files):
            return

        row = self.current_index

        self.table.item(row, 1).setText('Unknown')
        self.table.item(row, 2).setText(
            f'Error: {error_string or 'Unable to read'}'
        )

        self.progress.setValue(self.current_index + 1)

        self.current_index += 1

        QTimer.singleShot(50, self.read_next_video)


    @staticmethod
    def format_duration(milliseconds):
        total_seconds = milliseconds // 1000

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return f'{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    appfold = os.path.dirname(sys.argv[0])
    configfold = os.path.join(appfold, '_internal', 'config')
    icon_logo = QtGui.QIcon(os.path.join(configfold, 'icon_pipe_256.ico'))

    control = DvIndexBuilder()
    control.setWindowIcon(icon_logo)
    control.setWindowTitle("DV index builder")

    control.show()

    sys.exit(app.exec())