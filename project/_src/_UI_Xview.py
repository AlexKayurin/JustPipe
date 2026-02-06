# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_Xview.ui'
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
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_XVIEW(object):
    def setupUi(self, XVIEW):
        if not XVIEW.objectName():
            XVIEW.setObjectName(u"XVIEW")
        XVIEW.resize(870, 857)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(XVIEW.sizePolicy().hasHeightForWidth())
        XVIEW.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        XVIEW.setFont(font)
        XVIEW.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(XVIEW)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.Layout0 = QHBoxLayout()
        self.Layout0.setSpacing(10)
        self.Layout0.setObjectName(u"Layout0")
        self.Layout0.setSizeConstraint(QLayout.SetMinimumSize)
        self.Layout0.setContentsMargins(0, 0, 0, 0)
        self.b_POI = QPushButton(self.centralwidget)
        self.b_POI.setObjectName(u"b_POI")
        self.b_POI.setMinimumSize(QSize(40, 40))
        self.b_POI.setMaximumSize(QSize(40, 40))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.b_POI.setFont(font1)

        self.Layout0.addWidget(self.b_POI)

        self.b_fbwd = QPushButton(self.centralwidget)
        self.b_fbwd.setObjectName(u"b_fbwd")
        self.b_fbwd.setMinimumSize(QSize(40, 40))
        self.b_fbwd.setMaximumSize(QSize(40, 40))
        self.b_fbwd.setFont(font1)

        self.Layout0.addWidget(self.b_fbwd)

        self.b_bwd = QPushButton(self.centralwidget)
        self.b_bwd.setObjectName(u"b_bwd")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.b_bwd.sizePolicy().hasHeightForWidth())
        self.b_bwd.setSizePolicy(sizePolicy1)
        self.b_bwd.setMinimumSize(QSize(40, 40))
        self.b_bwd.setMaximumSize(QSize(40, 40))
        self.b_bwd.setFont(font1)
        self.b_bwd.setToolTipDuration(-1)

        self.Layout0.addWidget(self.b_bwd)

        self.b_fwd = QPushButton(self.centralwidget)
        self.b_fwd.setObjectName(u"b_fwd")
        sizePolicy1.setHeightForWidth(self.b_fwd.sizePolicy().hasHeightForWidth())
        self.b_fwd.setSizePolicy(sizePolicy1)
        self.b_fwd.setMinimumSize(QSize(40, 40))
        self.b_fwd.setMaximumSize(QSize(40, 40))
        self.b_fwd.setFont(font1)

        self.Layout0.addWidget(self.b_fwd)

        self.b_ffwd = QPushButton(self.centralwidget)
        self.b_ffwd.setObjectName(u"b_ffwd")
        self.b_ffwd.setMinimumSize(QSize(40, 40))
        self.b_ffwd.setMaximumSize(QSize(40, 40))
        self.b_ffwd.setFont(font1)

        self.Layout0.addWidget(self.b_ffwd)

        self.b_endvisit = QPushButton(self.centralwidget)
        self.b_endvisit.setObjectName(u"b_endvisit")
        self.b_endvisit.setMinimumSize(QSize(40, 40))
        self.b_endvisit.setMaximumSize(QSize(40, 40))
        self.b_endvisit.setFont(font1)

        self.Layout0.addWidget(self.b_endvisit)

        self.b_resetfwd = QPushButton(self.centralwidget)
        self.b_resetfwd.setObjectName(u"b_resetfwd")
        self.b_resetfwd.setMinimumSize(QSize(40, 40))
        self.b_resetfwd.setMaximumSize(QSize(40, 40))
        self.b_resetfwd.setFont(font1)

        self.Layout0.addWidget(self.b_resetfwd)

        self.b_assist = QPushButton(self.centralwidget)
        self.b_assist.setObjectName(u"b_assist")
        self.b_assist.setMinimumSize(QSize(40, 40))
        self.b_assist.setMaximumSize(QSize(40, 40))
        self.b_assist.setFont(font1)

        self.Layout0.addWidget(self.b_assist)

        self.b_hwm = QPushButton(self.centralwidget)
        self.b_hwm.setObjectName(u"b_hwm")
        self.b_hwm.setMinimumSize(QSize(40, 40))
        self.b_hwm.setMaximumSize(QSize(40, 40))
        self.b_hwm.setFont(font1)

        self.Layout0.addWidget(self.b_hwm)

        self.b_hwp = QPushButton(self.centralwidget)
        self.b_hwp.setObjectName(u"b_hwp")
        self.b_hwp.setMinimumSize(QSize(40, 40))
        self.b_hwp.setMaximumSize(QSize(40, 40))
        self.b_hwp.setFont(font1)

        self.Layout0.addWidget(self.b_hwp)

        self.b_vwm = QPushButton(self.centralwidget)
        self.b_vwm.setObjectName(u"b_vwm")
        self.b_vwm.setMinimumSize(QSize(40, 40))
        self.b_vwm.setMaximumSize(QSize(40, 40))
        self.b_vwm.setFont(font1)

        self.Layout0.addWidget(self.b_vwm)

        self.b_vwp = QPushButton(self.centralwidget)
        self.b_vwp.setObjectName(u"b_vwp")
        self.b_vwp.setMinimumSize(QSize(40, 40))
        self.b_vwp.setMaximumSize(QSize(40, 40))
        self.b_vwp.setFont(font1)

        self.Layout0.addWidget(self.b_vwp)

        self.b_Auto = QPushButton(self.centralwidget)
        self.b_Auto.setObjectName(u"b_Auto")
        self.b_Auto.setMinimumSize(QSize(40, 40))
        self.b_Auto.setMaximumSize(QSize(40, 40))
        self.b_Auto.setFont(font1)

        self.Layout0.addWidget(self.b_Auto)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout0.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.Layout0)

        self.Layout1 = QGridLayout()
        self.Layout1.setSpacing(10)
        self.Layout1.setObjectName(u"Layout1")
        self.Layout1.setSizeConstraint(QLayout.SetMaximumSize)
        self.Layout1.setContentsMargins(5, 5, 5, 5)
        self.xview = PlotWidget(self.centralwidget)
        self.xview.setObjectName(u"xview")
        self.l_Tide = QLabel(self.xview)
        self.l_Tide.setObjectName(u"l_Tide")
        self.l_Tide.setGeometry(QRect(60, 0, 600, 20))
        self.l_Tide.setMinimumSize(QSize(600, 20))
        self.l_Tide.setMaximumSize(QSize(600, 20))
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        self.l_Tide.setFont(font2)
        self.l_Progress = QLabel(self.xview)
        self.l_Progress.setObjectName(u"l_Progress")
        self.l_Progress.setGeometry(QRect(60, 20, 600, 20))
        self.l_Progress.setMinimumSize(QSize(600, 20))
        self.l_Progress.setMaximumSize(QSize(600, 20))
        self.l_Progress.setFont(font2)
        self.l_KP = QLabel(self.xview)
        self.l_KP.setObjectName(u"l_KP")
        self.l_KP.setGeometry(QRect(60, 40, 600, 20))
        self.l_KP.setMinimumSize(QSize(600, 20))
        self.l_KP.setMaximumSize(QSize(600, 20))
        font3 = QFont()
        font3.setPointSize(8)
        self.l_KP.setFont(font3)
        self.l_Time = QLabel(self.xview)
        self.l_Time.setObjectName(u"l_Time")
        self.l_Time.setGeometry(QRect(60, 60, 600, 20))
        self.l_Time.setMinimumSize(QSize(600, 20))
        self.l_Time.setMaximumSize(QSize(600, 20))
        self.l_Time.setFont(font3)

        self.Layout1.addWidget(self.xview, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.Layout1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ch_Center = QCheckBox(self.centralwidget)
        self.ch_Center.setObjectName(u"ch_Center")
        self.ch_Center.setMinimumSize(QSize(150, 20))
        self.ch_Center.setMaximumSize(QSize(150, 20))
        self.ch_Center.setFont(font3)
        self.ch_Center.setChecked(True)

        self.horizontalLayout.addWidget(self.ch_Center)

        self.ch_ShowPatch = QCheckBox(self.centralwidget)
        self.ch_ShowPatch.setObjectName(u"ch_ShowPatch")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ch_ShowPatch.sizePolicy().hasHeightForWidth())
        self.ch_ShowPatch.setSizePolicy(sizePolicy2)
        self.ch_ShowPatch.setMinimumSize(QSize(150, 20))
        self.ch_ShowPatch.setMaximumSize(QSize(150, 20))
        self.ch_ShowPatch.setFont(font3)
        self.ch_ShowPatch.setChecked(False)

        self.horizontalLayout.addWidget(self.ch_ShowPatch)

        self.ch_ShowAntiSpoof = QCheckBox(self.centralwidget)
        self.ch_ShowAntiSpoof.setObjectName(u"ch_ShowAntiSpoof")
        self.ch_ShowAntiSpoof.setMinimumSize(QSize(150, 20))
        self.ch_ShowAntiSpoof.setMaximumSize(QSize(150, 20))
        self.ch_ShowAntiSpoof.setFont(font3)

        self.horizontalLayout.addWidget(self.ch_ShowAntiSpoof)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        XVIEW.setCentralWidget(self.centralwidget)

        self.retranslateUi(XVIEW)
        self.b_hwm.clicked.connect(self.xview.setFocus)
        self.b_hwp.clicked.connect(self.xview.setFocus)
        self.b_vwm.clicked.connect(self.xview.setFocus)
        self.b_vwp.clicked.connect(self.xview.setFocus)
        self.b_fbwd.clicked.connect(self.xview.setFocus)
        self.b_bwd.clicked.connect(self.xview.setFocus)
        self.b_fwd.clicked.connect(self.xview.setFocus)
        self.b_ffwd.clicked.connect(self.xview.setFocus)
        self.b_endvisit.clicked.connect(self.xview.setFocus)
        self.b_resetfwd.clicked.connect(self.xview.setFocus)
        self.b_assist.clicked.connect(self.xview.setFocus)

        QMetaObject.connectSlotsByName(XVIEW)
    # setupUi

    def retranslateUi(self, XVIEW):
        XVIEW.setWindowTitle(QCoreApplication.translate("XVIEW", u"XVIEW", None))
        self.b_POI.setText(QCoreApplication.translate("XVIEW", u"POI", None))
        self.b_fbwd.setText(QCoreApplication.translate("XVIEW", u"FB", None))
#if QT_CONFIG(tooltip)
        self.b_bwd.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.b_bwd.setText(QCoreApplication.translate("XVIEW", u"B", None))
        self.b_fwd.setText(QCoreApplication.translate("XVIEW", u"F", None))
        self.b_ffwd.setText(QCoreApplication.translate("XVIEW", u"FF", None))
        self.b_endvisit.setText(QCoreApplication.translate("XVIEW", u"E", None))
        self.b_resetfwd.setText(QCoreApplication.translate("XVIEW", u"'0'", None))
        self.b_assist.setText(QCoreApplication.translate("XVIEW", u"C", None))
        self.b_hwm.setText(QCoreApplication.translate("XVIEW", u"H-", None))
        self.b_hwp.setText(QCoreApplication.translate("XVIEW", u"H+", None))
        self.b_vwm.setText(QCoreApplication.translate("XVIEW", u"V-", None))
        self.b_vwp.setText(QCoreApplication.translate("XVIEW", u"V+", None))
        self.b_Auto.setText(QCoreApplication.translate("XVIEW", u"A", None))
        self.l_Tide.setText(QCoreApplication.translate("XVIEW", u"TIDE NOT LOADED", None))
        self.l_Progress.setText(QCoreApplication.translate("XVIEW", u"PROGRESS", None))
        self.l_KP.setText(QCoreApplication.translate("XVIEW", u"KP", None))
        self.l_Time.setText(QCoreApplication.translate("XVIEW", u"T", None))
        self.ch_Center.setText(QCoreApplication.translate("XVIEW", u"Follow", None))
        self.ch_ShowPatch.setText(QCoreApplication.translate("XVIEW", u"Show Patch", None))
        self.ch_ShowAntiSpoof.setText(QCoreApplication.translate("XVIEW", u"Show AntiSpoof", None))
    # retranslateUi

