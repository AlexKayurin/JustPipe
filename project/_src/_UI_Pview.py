# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_Pview.ui'
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

from pyqtgraph import ImageView

class Ui_PVIEW(object):
    def setupUi(self, PVIEW):
        if not PVIEW.objectName():
            PVIEW.setObjectName(u"PVIEW")
        PVIEW.resize(953, 862)
        font = QFont()
        font.setPointSize(10)
        PVIEW.setFont(font)
        self.centralwidget = QWidget(PVIEW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Layout0 = QHBoxLayout()
        self.Layout0.setSpacing(10)
        self.Layout0.setObjectName(u"Layout0")
        self.Layout0.setSizeConstraint(QLayout.SetMinimumSize)
        self.Layout0.setContentsMargins(0, 0, 0, 0)
        self.b_POI = QPushButton(self.centralwidget)
        self.b_POI.setObjectName(u"b_POI")
        self.b_POI.setMinimumSize(QSize(40, 40))
        self.b_POI.setMaximumSize(QSize(40, 40))

        self.Layout0.addWidget(self.b_POI)

        self.b_Interpolate = QPushButton(self.centralwidget)
        self.b_Interpolate.setObjectName(u"b_Interpolate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_Interpolate.sizePolicy().hasHeightForWidth())
        self.b_Interpolate.setSizePolicy(sizePolicy)
        self.b_Interpolate.setMinimumSize(QSize(40, 40))
        self.b_Interpolate.setMaximumSize(QSize(40, 40))
        self.b_Interpolate.setToolTipDuration(-1)
        self.b_Interpolate.setFlat(False)

        self.Layout0.addWidget(self.b_Interpolate)

        self.b_smoothPT_p = QPushButton(self.centralwidget)
        self.b_smoothPT_p.setObjectName(u"b_smoothPT_p")
        self.b_smoothPT_p.setEnabled(False)
        sizePolicy.setHeightForWidth(self.b_smoothPT_p.sizePolicy().hasHeightForWidth())
        self.b_smoothPT_p.setSizePolicy(sizePolicy)
        self.b_smoothPT_p.setMinimumSize(QSize(40, 40))
        self.b_smoothPT_p.setMaximumSize(QSize(40, 40))
        self.b_smoothPT_p.setFlat(False)

        self.Layout0.addWidget(self.b_smoothPT_p)

        self.b_snap_h = QPushButton(self.centralwidget)
        self.b_snap_h.setObjectName(u"b_snap_h")
        self.b_snap_h.setEnabled(False)
        self.b_snap_h.setMinimumSize(QSize(40, 40))
        self.b_snap_h.setMaximumSize(QSize(40, 40))

        self.Layout0.addWidget(self.b_snap_h)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout0.addItem(self.horizontalSpacer)

        self.l1 = QLabel(self.centralwidget)
        self.l1.setObjectName(u"l1")
        self.l1.setMinimumSize(QSize(140, 20))
        self.l1.setMaximumSize(QSize(140, 20))
        font1 = QFont()
        font1.setPointSize(8)
        self.l1.setFont(font1)
        self.l1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.Layout0.addWidget(self.l1)

        self.t_EdSpot = QLineEdit(self.centralwidget)
        self.t_EdSpot.setObjectName(u"t_EdSpot")
        self.t_EdSpot.setEnabled(False)
        self.t_EdSpot.setMinimumSize(QSize(60, 25))
        self.t_EdSpot.setMaximumSize(QSize(60, 25))
        self.t_EdSpot.setFont(font1)

        self.Layout0.addWidget(self.t_EdSpot)

        self.l0 = QLabel(self.centralwidget)
        self.l0.setObjectName(u"l0")
        self.l0.setMinimumSize(QSize(140, 20))
        self.l0.setMaximumSize(QSize(140, 20))
        self.l0.setFont(font1)
        self.l0.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.Layout0.addWidget(self.l0)

        self.t_smW = QLineEdit(self.centralwidget)
        self.t_smW.setObjectName(u"t_smW")
        self.t_smW.setEnabled(False)
        self.t_smW.setMinimumSize(QSize(60, 25))
        self.t_smW.setMaximumSize(QSize(60, 25))
        self.t_smW.setFont(font1)

        self.Layout0.addWidget(self.t_smW)


        self.verticalLayout.addLayout(self.Layout0)

        self.Layout2 = QGridLayout()
        self.Layout2.setObjectName(u"Layout2")
        self.Layout2.setSizeConstraint(QLayout.SetMaximumSize)
        self.pview = ImageView(self.centralwidget)
        self.pview.setObjectName(u"pview")

        self.Layout2.addWidget(self.pview, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.Layout2)

        self.Layout3 = QHBoxLayout()
        self.Layout3.setSpacing(10)
        self.Layout3.setObjectName(u"Layout3")
        self.Layout3.setSizeConstraint(QLayout.SetMinimumSize)
        self.Layout3.setContentsMargins(0, 0, 0, 0)
        self.ch_Center = QCheckBox(self.centralwidget)
        self.ch_Center.setObjectName(u"ch_Center")
        self.ch_Center.setMinimumSize(QSize(150, 20))
        self.ch_Center.setMaximumSize(QSize(150, 20))
        self.ch_Center.setFont(font1)
        self.ch_Center.setChecked(True)

        self.Layout3.addWidget(self.ch_Center)

        self.ch_ShowPT = QCheckBox(self.centralwidget)
        self.ch_ShowPT.setObjectName(u"ch_ShowPT")
        self.ch_ShowPT.setEnabled(False)
        self.ch_ShowPT.setMinimumSize(QSize(150, 20))
        self.ch_ShowPT.setMaximumSize(QSize(150, 20))
        self.ch_ShowPT.setFont(font1)
        self.ch_ShowPT.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowPT)

        self.ch_ShowFlagL = QCheckBox(self.centralwidget)
        self.ch_ShowFlagL.setObjectName(u"ch_ShowFlagL")
        self.ch_ShowFlagL.setMinimumSize(QSize(150, 20))
        self.ch_ShowFlagL.setMaximumSize(QSize(150, 20))
        self.ch_ShowFlagL.setFont(font1)
        self.ch_ShowFlagL.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowFlagL)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.Layout3)

        PVIEW.setCentralWidget(self.centralwidget)

        self.retranslateUi(PVIEW)

        QMetaObject.connectSlotsByName(PVIEW)
    # setupUi

    def retranslateUi(self, PVIEW):
        PVIEW.setWindowTitle(QCoreApplication.translate("PVIEW", u"PVIEW", None))
        self.b_POI.setText("")
#if QT_CONFIG(tooltip)
        self.b_Interpolate.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.b_Interpolate.setStatusTip(QCoreApplication.translate("PVIEW", u"Interpolate TOP 3D", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.b_Interpolate.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.b_Interpolate.setText("")
        self.b_smoothPT_p.setText("")
        self.b_snap_h.setText("")
        self.l1.setText(QCoreApplication.translate("PVIEW", u"Edit spot:", None))
        self.t_EdSpot.setText(QCoreApplication.translate("PVIEW", u"0.5", None))
        self.l0.setText(QCoreApplication.translate("PVIEW", u"Sm. pts:", None))
        self.t_smW.setText(QCoreApplication.translate("PVIEW", u"10", None))
        self.ch_Center.setText(QCoreApplication.translate("PVIEW", u"Follow", None))
        self.ch_ShowPT.setText(QCoreApplication.translate("PVIEW", u"Show PT", None))
        self.ch_ShowFlagL.setText(QCoreApplication.translate("PVIEW", u"Show Flags", None))
    # retranslateUi

