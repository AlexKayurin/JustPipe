# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_UI_Playpause.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_PLAYPAUSE(object):
    def setupUi(self, PLAYPAUSE):
        if not PLAYPAUSE.objectName():
            PLAYPAUSE.setObjectName(u"PLAYPAUSE")
        PLAYPAUSE.resize(168, 150)
        PLAYPAUSE.setMinimumSize(QSize(150, 150))
        PLAYPAUSE.setMaximumSize(QSize(168, 150))
        self.centralwidget = QWidget(PLAYPAUSE)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.b_Pause = QPushButton(self.centralwidget)
        self.b_Pause.setObjectName(u"b_Pause")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.b_Pause.sizePolicy().hasHeightForWidth())
        self.b_Pause.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(56)
        font.setBold(True)
        self.b_Pause.setFont(font)

        self.verticalLayout.addWidget(self.b_Pause)

        PLAYPAUSE.setCentralWidget(self.centralwidget)

        self.retranslateUi(PLAYPAUSE)

        QMetaObject.connectSlotsByName(PLAYPAUSE)
    # setupUi

    def retranslateUi(self, PLAYPAUSE):
        PLAYPAUSE.setWindowTitle(QCoreApplication.translate("PLAYPAUSE", u"Play/Pause", None))
        self.b_Pause.setText(QCoreApplication.translate("PLAYPAUSE", u"PP", None))
    # retranslateUi

