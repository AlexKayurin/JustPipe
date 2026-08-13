# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_UI_Lview.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_LVIEW(object):
    def setupUi(self, LVIEW):
        if not LVIEW.objectName():
            LVIEW.setObjectName(u"LVIEW")
        LVIEW.resize(1035, 424)
        font = QFont()
        font.setPointSize(10)
        LVIEW.setFont(font)
        self.centralwidget = QWidget(LVIEW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.Layout1 = QHBoxLayout()
        self.Layout1.setSpacing(5)
        self.Layout1.setObjectName(u"Layout1")
        self.Layout1.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.Layout1.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(140, 50))
        self.groupBox.setMaximumSize(QSize(140, 50))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.b_POI = QPushButton(self.groupBox)
        self.b_POI.setObjectName(u"b_POI")
        self.b_POI.setMinimumSize(QSize(40, 40))
        self.b_POI.setMaximumSize(QSize(40, 40))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.b_POI.setFont(font1)

        self.horizontalLayout.addWidget(self.b_POI)

        self.b_Interpolate = QPushButton(self.groupBox)
        self.b_Interpolate.setObjectName(u"b_Interpolate")
        self.b_Interpolate.setMinimumSize(QSize(40, 40))
        self.b_Interpolate.setMaximumSize(QSize(40, 40))
        self.b_Interpolate.setFont(font1)

        self.horizontalLayout.addWidget(self.b_Interpolate)

        self.b_snap_v = QPushButton(self.groupBox)
        self.b_snap_v.setObjectName(u"b_snap_v")
        self.b_snap_v.setEnabled(False)
        self.b_snap_v.setMinimumSize(QSize(40, 40))
        self.b_snap_v.setMaximumSize(QSize(40, 40))
        self.b_snap_v.setFont(font1)

        self.horizontalLayout.addWidget(self.b_snap_v)


        self.Layout1.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout1.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.Layout1)

        self.Layout0 = QGridLayout()
        self.Layout0.setObjectName(u"Layout0")
        self.Layout0.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.Layout0.setHorizontalSpacing(0)
        self.Layout0.setVerticalSpacing(5)
        self.lview = PlotWidget(self.centralwidget)
        self.lview.setObjectName(u"lview")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lview.sizePolicy().hasHeightForWidth())
        self.lview.setSizePolicy(sizePolicy)
        self.l_scale = QLabel(self.lview)
        self.l_scale.setObjectName(u"l_scale")
        self.l_scale.setGeometry(QRect(60, 0, 600, 20))
        self.l_scale.setMinimumSize(QSize(600, 20))
        self.l_scale.setMaximumSize(QSize(600, 20))
        font2 = QFont()
        font2.setPointSize(8)
        self.l_scale.setFont(font2)

        self.Layout0.addWidget(self.lview, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.Layout0)

        self.Layout3 = QHBoxLayout()
        self.Layout3.setSpacing(5)
        self.Layout3.setObjectName(u"Layout3")
        self.Layout3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.Layout3.setContentsMargins(0, 0, 0, 0)
        self.ch_Center = QCheckBox(self.centralwidget)
        self.ch_Center.setObjectName(u"ch_Center")
        self.ch_Center.setMinimumSize(QSize(120, 20))
        self.ch_Center.setMaximumSize(QSize(120, 20))
        self.ch_Center.setFont(font)
        self.ch_Center.setChecked(True)

        self.Layout3.addWidget(self.ch_Center)

        self.ch_Aspect = QCheckBox(self.centralwidget)
        self.ch_Aspect.setObjectName(u"ch_Aspect")
        self.ch_Aspect.setMinimumSize(QSize(120, 20))
        self.ch_Aspect.setMaximumSize(QSize(120, 20))
        self.ch_Aspect.setFont(font)

        self.Layout3.addWidget(self.ch_Aspect)

        self.ch_Time_Chn = QCheckBox(self.centralwidget)
        self.ch_Time_Chn.setObjectName(u"ch_Time_Chn")
        self.ch_Time_Chn.setMinimumSize(QSize(120, 20))
        self.ch_Time_Chn.setMaximumSize(QSize(120, 20))
        self.ch_Time_Chn.setFont(font)

        self.Layout3.addWidget(self.ch_Time_Chn)

        self.ch_ShowTOP = QCheckBox(self.centralwidget)
        self.ch_ShowTOP.setObjectName(u"ch_ShowTOP")
        self.ch_ShowTOP.setMinimumSize(QSize(120, 20))
        self.ch_ShowTOP.setMaximumSize(QSize(120, 20))
        self.ch_ShowTOP.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowTOP)

        self.ch_ShowFlags = QCheckBox(self.centralwidget)
        self.ch_ShowFlags.setObjectName(u"ch_ShowFlags")
        self.ch_ShowFlags.setMinimumSize(QSize(120, 20))
        self.ch_ShowFlags.setMaximumSize(QSize(120, 20))
        self.ch_ShowFlags.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowFlags)

        self.ch_ShowPT = QCheckBox(self.centralwidget)
        self.ch_ShowPT.setObjectName(u"ch_ShowPT")
        self.ch_ShowPT.setEnabled(False)
        self.ch_ShowPT.setMinimumSize(QSize(120, 20))
        self.ch_ShowPT.setMaximumSize(QSize(120, 20))
        self.ch_ShowPT.setFont(font)
        self.ch_ShowPT.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowPT)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.Layout3)

        LVIEW.setCentralWidget(self.centralwidget)

        self.retranslateUi(LVIEW)

        QMetaObject.connectSlotsByName(LVIEW)
    # setupUi

    def retranslateUi(self, LVIEW):
        LVIEW.setWindowTitle(QCoreApplication.translate("LVIEW", u"LVIEW", None))
        self.groupBox.setTitle("")
        self.b_POI.setText(QCoreApplication.translate("LVIEW", u"POI", None))
        self.b_Interpolate.setText(QCoreApplication.translate("LVIEW", u"I", None))
        self.b_snap_v.setText(QCoreApplication.translate("LVIEW", u"SnZ", None))
        self.l_scale.setText(QCoreApplication.translate("LVIEW", u"SCALE 1:", None))
        self.ch_Center.setText(QCoreApplication.translate("LVIEW", u"Follow", None))
        self.ch_Aspect.setText(QCoreApplication.translate("LVIEW", u"Scale 1:1", None))
        self.ch_Time_Chn.setText(QCoreApplication.translate("LVIEW", u"Time", None))
        self.ch_ShowTOP.setText(QCoreApplication.translate("LVIEW", u"Show Pipe", None))
        self.ch_ShowFlags.setText(QCoreApplication.translate("LVIEW", u"Show Levels", None))
        self.ch_ShowPT.setText(QCoreApplication.translate("LVIEW", u"Show PT", None))
    # retranslateUi

