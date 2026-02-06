# sudo apt purge gstreamer1.0-vaapi (linux) ???????? MAY NOT NEED
# may need LAV filters (win)

from PySide6 import QtGui
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QMainWindow

class Player(QMainWindow):
    def __init__(self, channel, i):
      super().__init__()
      self.setGeometry(100 + i * 10, 100 + i * 10, 800, 500)
      self.setWindowTitle(channel)

      self.mdp = QMediaPlayer()
      self.vd = QVideoWidget(self)
      self.vd.setGeometry(0, 0, 800, 500)
      self.mdp.setVideoOutput(self.vd)

    def loadmedia(self, media):
      self.mdp.setSource(QUrl.fromLocalFile(media))
      self.mdp.play()
      self.mdp.pause()
    
    def gototime(self, pos):
      # self.mdp.play()
      self.mdp.setPosition(pos)
      # self.mdp.pause()

    def resizeEvent(self, e: QtGui.QResizeEvent):
      self.vd.setGeometry(0, 0, self.size().width(), self.size().height())

