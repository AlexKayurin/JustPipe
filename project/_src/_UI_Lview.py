# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_Lview.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QMainWindow,
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
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Layout1 = QHBoxLayout()
        self.Layout1.setSpacing(10)
        self.Layout1.setObjectName(u"Layout1")
        self.Layout1.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.Layout1.setContentsMargins(0, 0, 0, 0)
        self.b_POI = QPushButton(self.centralwidget)
        self.b_POI.setObjectName(u"b_POI")
        self.b_POI.setMinimumSize(QSize(40, 40))
        self.b_POI.setMaximumSize(QSize(40, 40))

        self.Layout1.addWidget(self.b_POI)

        self.b_Interpolate = QPushButton(self.centralwidget)
        self.b_Interpolate.setObjectName(u"b_Interpolate")
        self.b_Interpolate.setMinimumSize(QSize(40, 40))
        self.b_Interpolate.setMaximumSize(QSize(40, 40))

        self.Layout1.addWidget(self.b_Interpolate)

        self.b_smoothPT_l = QPushButton(self.centralwidget)
        self.b_smoothPT_l.setObjectName(u"b_smoothPT_l")
        self.b_smoothPT_l.setEnabled(False)
        self.b_smoothPT_l.setMinimumSize(QSize(40, 40))
        self.b_smoothPT_l.setMaximumSize(QSize(40, 40))

        self.Layout1.addWidget(self.b_smoothPT_l)

        self.b_levelPT = QPushButton(self.centralwidget)
        self.b_levelPT.setObjectName(u"b_levelPT")
        self.b_levelPT.setEnabled(False)
        self.b_levelPT.setMinimumSize(QSize(40, 40))
        self.b_levelPT.setMaximumSize(QSize(40, 40))

        self.Layout1.addWidget(self.b_levelPT)

        self.b_snap_v = QPushButton(self.centralwidget)
        self.b_snap_v.setObjectName(u"b_snap_v")
        self.b_snap_v.setEnabled(False)
        self.b_snap_v.setMinimumSize(QSize(40, 40))
        self.b_snap_v.setMaximumSize(QSize(40, 40))

        self.Layout1.addWidget(self.b_snap_v)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout1.addItem(self.horizontalSpacer)

        self.l1 = QLabel(self.centralwidget)
        self.l1.setObjectName(u"l1")
        self.l1.setMinimumSize(QSize(140, 20))
        self.l1.setMaximumSize(QSize(140, 20))
        font1 = QFont()
        font1.setPointSize(8)
        self.l1.setFont(font1)
        self.l1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Layout1.addWidget(self.l1)

        self.t_EdSpot = QLineEdit(self.centralwidget)
        self.t_EdSpot.setObjectName(u"t_EdSpot")
        self.t_EdSpot.setEnabled(False)
        self.t_EdSpot.setMinimumSize(QSize(60, 25))
        self.t_EdSpot.setMaximumSize(QSize(60, 25))
        self.t_EdSpot.setFont(font1)

        self.Layout1.addWidget(self.t_EdSpot)

        self.l0 = QLabel(self.centralwidget)
        self.l0.setObjectName(u"l0")
        self.l0.setMinimumSize(QSize(140, 20))
        self.l0.setMaximumSize(QSize(140, 20))
        self.l0.setFont(font1)
        self.l0.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Layout1.addWidget(self.l0)

        self.t_smW = QLineEdit(self.centralwidget)
        self.t_smW.setObjectName(u"t_smW")
        self.t_smW.setEnabled(False)
        self.t_smW.setMinimumSize(QSize(60, 25))
        self.t_smW.setMaximumSize(QSize(60, 25))
        self.t_smW.setFont(font1)

        self.Layout1.addWidget(self.t_smW)

        self.l2 = QLabel(self.centralwidget)
        self.l2.setObjectName(u"l2")
        self.l2.setMinimumSize(QSize(140, 20))
        self.l2.setMaximumSize(QSize(140, 20))
        self.l2.setFont(font1)
        self.l2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.Layout1.addWidget(self.l2)

        self.t_Lev = QLineEdit(self.centralwidget)
        self.t_Lev.setObjectName(u"t_Lev")
        self.t_Lev.setEnabled(False)
        self.t_Lev.setMinimumSize(QSize(60, 25))
        self.t_Lev.setMaximumSize(QSize(60, 25))
        self.t_Lev.setFont(font1)

        self.Layout1.addWidget(self.t_Lev)


        self.verticalLayout.addLayout(self.Layout1)

        self.Layout0 = QGridLayout()
        self.Layout0.setObjectName(u"Layout0")
        self.Layout0.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
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
        self.l_scale.setFont(font1)

        self.Layout0.addWidget(self.lview, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.Layout0)

        self.LAyout3 = QHBoxLayout()
        self.LAyout3.setSpacing(10)
        self.LAyout3.setObjectName(u"LAyout3")
        self.LAyout3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.LAyout3.setContentsMargins(0, 0, 0, 0)
        self.ch_Center = QCheckBox(self.centralwidget)
        self.ch_Center.setObjectName(u"ch_Center")
        self.ch_Center.setMinimumSize(QSize(140, 20))
        self.ch_Center.setMaximumSize(QSize(140, 20))
        self.ch_Center.setFont(font1)
        self.ch_Center.setChecked(True)

        self.LAyout3.addWidget(self.ch_Center)

        self.ch_Time_Chn = QCheckBox(self.centralwidget)
        self.ch_Time_Chn.setObjectName(u"ch_Time_Chn")
        self.ch_Time_Chn.setMinimumSize(QSize(140, 20))
        self.ch_Time_Chn.setMaximumSize(QSize(140, 20))
        self.ch_Time_Chn.setFont(font1)

        self.LAyout3.addWidget(self.ch_Time_Chn)

        self.ch_ShowPT = QCheckBox(self.centralwidget)
        self.ch_ShowPT.setObjectName(u"ch_ShowPT")
        self.ch_ShowPT.setEnabled(False)
        self.ch_ShowPT.setMinimumSize(QSize(140, 20))
        self.ch_ShowPT.setMaximumSize(QSize(140, 20))
        self.ch_ShowPT.setFont(font1)
        self.ch_ShowPT.setChecked(True)

        self.LAyout3.addWidget(self.ch_ShowPT)

        self.ch_Aspect = QCheckBox(self.centralwidget)
        self.ch_Aspect.setObjectName(u"ch_Aspect")
        self.ch_Aspect.setMinimumSize(QSize(140, 20))
        self.ch_Aspect.setMaximumSize(QSize(140, 20))
        self.ch_Aspect.setFont(font1)

        self.LAyout3.addWidget(self.ch_Aspect)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.LAyout3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.LAyout3)

        LVIEW.setCentralWidget(self.centralwidget)

        self.retranslateUi(LVIEW)

        QMetaObject.connectSlotsByName(LVIEW)
    # setupUi

    def retranslateUi(self, LVIEW):
        LVIEW.setWindowTitle(QCoreApplication.translate("LVIEW", u"LVIEW", None))
        self.b_POI.setText("")
        self.b_Interpolate.setText("")
        self.b_smoothPT_l.setText("")
        self.b_levelPT.setText("")
        self.b_snap_v.setText("")
        self.l1.setText(QCoreApplication.translate("LVIEW", u"Edit spot:", None))
        self.t_EdSpot.setText(QCoreApplication.translate("LVIEW", u"0.5", None))
        self.l0.setText(QCoreApplication.translate("LVIEW", u"Sm. pts:", None))
        self.t_smW.setText(QCoreApplication.translate("LVIEW", u"10", None))
        self.l2.setText(QCoreApplication.translate("LVIEW", u"Level:", None))
        self.t_Lev.setText(QCoreApplication.translate("LVIEW", u"0.0", None))
        self.l_scale.setText(QCoreApplication.translate("LVIEW", u"SCALE 1:", None))
        self.ch_Center.setText(QCoreApplication.translate("LVIEW", u"Follow", None))
        self.ch_Time_Chn.setText(QCoreApplication.translate("LVIEW", u"Time", None))
        self.ch_ShowPT.setText(QCoreApplication.translate("LVIEW", u"Show PT", None))
        self.ch_Aspect.setText(QCoreApplication.translate("LVIEW", u"Scale 1:1", None))
    # retranslateUi

