from PySide6.QtWidgets  import QApplication
import sys

app = QApplication(sys.argv)
screen_resolution = app.primaryScreen().size()
print(screen_resolution)