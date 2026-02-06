# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_Options.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(390, 610)
        Dialog.setMinimumSize(QSize(390, 610))
        Dialog.setMaximumSize(QSize(390, 610))
        font = QFont()
        font.setPointSize(8)
        Dialog.setFont(font)
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(5, 5, 376, 600))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.b_NotVis = QPushButton(self.gridLayoutWidget)
        self.b_NotVis.setObjectName(u"b_NotVis")
        self.b_NotVis.setMinimumSize(QSize(150, 40))
        self.b_NotVis.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_NotVis, 4, 0, 1, 1)

        self.w_Background = QWidget(self.gridLayoutWidget)
        self.w_Background.setObjectName(u"w_Background")
        self.w_Background.setMinimumSize(QSize(120, 30))
        self.w_Background.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_Background, 10, 1, 1, 1)

        self.w_MADJ = QWidget(self.gridLayoutWidget)
        self.w_MADJ.setObjectName(u"w_MADJ")
        self.w_MADJ.setMinimumSize(QSize(120, 30))
        self.w_MADJ.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_MADJ, 6, 1, 1, 1)

        self.b_LeftM = QPushButton(self.gridLayoutWidget)
        self.b_LeftM.setObjectName(u"b_LeftM")
        self.b_LeftM.setMinimumSize(QSize(150, 40))
        self.b_LeftM.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_LeftM, 2, 0, 1, 1)

        self.w_Pipe = QWidget(self.gridLayoutWidget)
        self.w_Pipe.setObjectName(u"w_Pipe")
        self.w_Pipe.setMinimumSize(QSize(120, 30))
        self.w_Pipe.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_Pipe, 1, 1, 1, 1)

        self.w_Vis = QWidget(self.gridLayoutWidget)
        self.w_Vis.setObjectName(u"w_Vis")
        self.w_Vis.setMinimumSize(QSize(120, 30))
        self.w_Vis.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_Vis, 5, 1, 1, 1)

        self.b_Vis = QPushButton(self.gridLayoutWidget)
        self.b_Vis.setObjectName(u"b_Vis")
        self.b_Vis.setMinimumSize(QSize(150, 40))
        self.b_Vis.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_Vis, 5, 0, 1, 1)

        self.b_Pipetracker = QPushButton(self.gridLayoutWidget)
        self.b_Pipetracker.setObjectName(u"b_Pipetracker")
        self.b_Pipetracker.setMinimumSize(QSize(150, 40))
        self.b_Pipetracker.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_Pipetracker, 8, 0, 1, 1)

        self.b_Background = QPushButton(self.gridLayoutWidget)
        self.b_Background.setObjectName(u"b_Background")
        self.b_Background.setMinimumSize(QSize(150, 40))
        self.b_Background.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_Background, 10, 0, 1, 1)

        self.b_MADJ = QPushButton(self.gridLayoutWidget)
        self.b_MADJ.setObjectName(u"b_MADJ")
        self.b_MADJ.setMinimumSize(QSize(150, 40))
        self.b_MADJ.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_MADJ, 6, 0, 1, 1)

        self.b_RightM = QPushButton(self.gridLayoutWidget)
        self.b_RightM.setObjectName(u"b_RightM")
        self.b_RightM.setMinimumSize(QSize(150, 40))
        self.b_RightM.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_RightM, 3, 0, 1, 1)

        self.b_Profile = QPushButton(self.gridLayoutWidget)
        self.b_Profile.setObjectName(u"b_Profile")
        self.b_Profile.setMinimumSize(QSize(150, 40))
        self.b_Profile.setMaximumSize(QSize(150, 40))
        self.b_Profile.setFont(font)

        self.gridLayout.addWidget(self.b_Profile, 0, 0, 1, 1)

        self.b_CurrentProf = QPushButton(self.gridLayoutWidget)
        self.b_CurrentProf.setObjectName(u"b_CurrentProf")
        self.b_CurrentProf.setMinimumSize(QSize(150, 40))
        self.b_CurrentProf.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_CurrentProf, 9, 0, 1, 1)

        self.w_CurrentProf = QWidget(self.gridLayoutWidget)
        self.w_CurrentProf.setObjectName(u"w_CurrentProf")
        self.w_CurrentProf.setMinimumSize(QSize(120, 30))
        self.w_CurrentProf.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_CurrentProf, 9, 1, 1, 1)

        self.b_MSBL = QPushButton(self.gridLayoutWidget)
        self.b_MSBL.setObjectName(u"b_MSBL")
        self.b_MSBL.setMinimumSize(QSize(150, 40))
        self.b_MSBL.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_MSBL, 7, 0, 1, 1)

        self.b_Pipe = QPushButton(self.gridLayoutWidget)
        self.b_Pipe.setObjectName(u"b_Pipe")
        self.b_Pipe.setMinimumSize(QSize(150, 40))
        self.b_Pipe.setMaximumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.b_Pipe, 1, 0, 1, 1)

        self.w_NotVis = QWidget(self.gridLayoutWidget)
        self.w_NotVis.setObjectName(u"w_NotVis")
        self.w_NotVis.setMinimumSize(QSize(120, 30))
        self.w_NotVis.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_NotVis, 4, 1, 1, 1)

        self.w_LeftM = QWidget(self.gridLayoutWidget)
        self.w_LeftM.setObjectName(u"w_LeftM")
        self.w_LeftM.setMinimumSize(QSize(120, 30))
        self.w_LeftM.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_LeftM, 2, 1, 1, 1)

        self.w_Pipetracker = QWidget(self.gridLayoutWidget)
        self.w_Pipetracker.setObjectName(u"w_Pipetracker")
        self.w_Pipetracker.setMinimumSize(QSize(120, 30))
        self.w_Pipetracker.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_Pipetracker, 8, 1, 1, 1)

        self.w_Profile = QWidget(self.gridLayoutWidget)
        self.w_Profile.setObjectName(u"w_Profile")
        self.w_Profile.setMinimumSize(QSize(120, 30))
        self.w_Profile.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_Profile, 0, 1, 1, 1)

        self.w_RightM = QWidget(self.gridLayoutWidget)
        self.w_RightM.setObjectName(u"w_RightM")
        self.w_RightM.setMinimumSize(QSize(120, 30))
        self.w_RightM.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_RightM, 3, 1, 1, 1)

        self.w_MSBL = QWidget(self.gridLayoutWidget)
        self.w_MSBL.setObjectName(u"w_MSBL")
        self.w_MSBL.setMinimumSize(QSize(120, 30))
        self.w_MSBL.setMaximumSize(QSize(120, 30))

        self.gridLayout.addWidget(self.w_MSBL, 7, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Select colors", None))
        self.b_NotVis.setText(QCoreApplication.translate("Dialog", u"Not visited", None))
        self.b_LeftM.setText(QCoreApplication.translate("Dialog", u"Left flag", None))
        self.b_Vis.setText(QCoreApplication.translate("Dialog", u"Visited", None))
        self.b_Pipetracker.setText(QCoreApplication.translate("Dialog", u"Pipetracker", None))
        self.b_Background.setText(QCoreApplication.translate("Dialog", u"Background", None))
        self.b_MADJ.setText(QCoreApplication.translate("Dialog", u"Mean adjacent", None))
        self.b_RightM.setText(QCoreApplication.translate("Dialog", u"Right flag", None))
        self.b_Profile.setText(QCoreApplication.translate("Dialog", u"Profile", None))
        self.b_CurrentProf.setText(QCoreApplication.translate("Dialog", u"Current position", None))
        self.b_MSBL.setText(QCoreApplication.translate("Dialog", u"Mean seabed", None))
        self.b_Pipe.setText(QCoreApplication.translate("Dialog", u"Pipe", None))
    # retranslateUi

