# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_Control.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_CONTROL(object):
    def setupUi(self, CONTROL):
        if not CONTROL.objectName():
            CONTROL.setObjectName(u"CONTROL")
        CONTROL.resize(544, 510)
        CONTROL.setMinimumSize(QSize(0, 0))
        CONTROL.setMaximumSize(QSize(545, 510))
        font = QFont()
        font.setPointSize(10)
        CONTROL.setFont(font)
        CONTROL.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.actionLoad_profiles = QAction(CONTROL)
        self.actionLoad_profiles.setObjectName(u"actionLoad_profiles")
        self.actionLoad_profiles.setFont(font)
        self.actionLoad_GeoTiff = QAction(CONTROL)
        self.actionLoad_GeoTiff.setObjectName(u"actionLoad_GeoTiff")
        self.actionLoad_GeoTiff.setFont(font)
        self.actionLoad_tide = QAction(CONTROL)
        self.actionLoad_tide.setObjectName(u"actionLoad_tide")
        self.actionLoad_tide.setFont(font)
        self.actionSave_work = QAction(CONTROL)
        self.actionSave_work.setObjectName(u"actionSave_work")
        self.actionSave_work.setFont(font)
        self.actionLoad_saved_work = QAction(CONTROL)
        self.actionLoad_saved_work.setObjectName(u"actionLoad_saved_work")
        self.actionLoad_saved_work.setFont(font)
        self.actionExport_EIVA = QAction(CONTROL)
        self.actionExport_EIVA.setObjectName(u"actionExport_EIVA")
        self.actionExport_EIVA.setFont(font)
        self.actionLoad_pipetracker = QAction(CONTROL)
        self.actionLoad_pipetracker.setObjectName(u"actionLoad_pipetracker")
        self.actionLoad_pipetracker.setFont(font)
        self.actionSave_layout = QAction(CONTROL)
        self.actionSave_layout.setObjectName(u"actionSave_layout")
        self.actionSave_layout.setFont(font)
        self.actionLoad_layout = QAction(CONTROL)
        self.actionLoad_layout.setObjectName(u"actionLoad_layout")
        self.actionLoad_layout.setFont(font)
        self.actionExport_SFX = QAction(CONTROL)
        self.actionExport_SFX.setObjectName(u"actionExport_SFX")
        self.actionExport_SFX.setFont(font)
        self.actionBuild_Playlist = QAction(CONTROL)
        self.actionBuild_Playlist.setObjectName(u"actionBuild_Playlist")
        self.actionBuild_Playlist.setFont(font)
        self.actionLoad_playlist = QAction(CONTROL)
        self.actionLoad_playlist.setObjectName(u"actionLoad_playlist")
        self.actionLoad_playlist.setFont(font)
        self.actionXView = QAction(CONTROL)
        self.actionXView.setObjectName(u"actionXView")
        self.actionXView.setFont(font)
        self.actionPView = QAction(CONTROL)
        self.actionPView.setObjectName(u"actionPView")
        self.actionPView.setFont(font)
        self.actionLView = QAction(CONTROL)
        self.actionLView.setObjectName(u"actionLView")
        self.actionLView.setFont(font)
        self.actionSettings = QAction(CONTROL)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setFont(font)
        self.actionLoad_colors = QAction(CONTROL)
        self.actionLoad_colors.setObjectName(u"actionLoad_colors")
        self.actionLoad_colors.setFont(font)
        self.actionDV_Control = QAction(CONTROL)
        self.actionDV_Control.setObjectName(u"actionDV_Control")
        self.actionDV_Control.setFont(font)
        self.actionInfo = QAction(CONTROL)
        self.actionInfo.setObjectName(u"actionInfo")
        self.actionInfo.setEnabled(False)
        self.actionInfo.setFont(font)
        self.actionVersion = QAction(CONTROL)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionVersion.setCheckable(False)
        self.actionVersion.setEnabled(False)
        self.actionVersion.setFont(font)
        self.actionManual = QAction(CONTROL)
        self.actionManual.setObjectName(u"actionManual")
        self.actionManual.setFont(font)
        self.actionLoad_events = QAction(CONTROL)
        self.actionLoad_events.setObjectName(u"actionLoad_events")
        self.actionLoad_events.setFont(font)
        self.actionEvents = QAction(CONTROL)
        self.actionEvents.setObjectName(u"actionEvents")
        self.actionEvents.setFont(font)
        self.centralwidget = QWidget(CONTROL)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabPipe = QWidget()
        self.tabPipe.setObjectName(u"tabPipe")
        self.tabPipe.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_4 = QVBoxLayout(self.tabPipe)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout0 = QGridLayout()
        self.gridLayout0.setSpacing(10)
        self.gridLayout0.setObjectName(u"gridLayout0")
        self.gridLayout0.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout0.setContentsMargins(5, 5, 5, 5)
        self.l7 = QLabel(self.tabPipe)
        self.l7.setObjectName(u"l7")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l7.sizePolicy().hasHeightForWidth())
        self.l7.setSizePolicy(sizePolicy)
        self.l7.setMinimumSize(QSize(0, 0))
        self.l7.setMaximumSize(QSize(140, 20))
        self.l7.setBaseSize(QSize(0, 0))
        self.l7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l7, 3, 3, 1, 1)

        self.l2 = QLabel(self.tabPipe)
        self.l2.setObjectName(u"l2")
        sizePolicy.setHeightForWidth(self.l2.sizePolicy().hasHeightForWidth())
        self.l2.setSizePolicy(sizePolicy)
        self.l2.setMinimumSize(QSize(0, 0))
        self.l2.setMaximumSize(QSize(140, 35))
        self.l2.setBaseSize(QSize(0, 0))
        self.l2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l2, 1, 0, 1, 1)

        self.t_RES = QLineEdit(self.tabPipe)
        self.t_RES.setObjectName(u"t_RES")
        sizePolicy.setHeightForWidth(self.t_RES.sizePolicy().hasHeightForWidth())
        self.t_RES.setSizePolicy(sizePolicy)
        self.t_RES.setMinimumSize(QSize(80, 25))
        self.t_RES.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_RES, 3, 4, 1, 1)

        self.l5 = QLabel(self.tabPipe)
        self.l5.setObjectName(u"l5")
        sizePolicy.setHeightForWidth(self.l5.sizePolicy().hasHeightForWidth())
        self.l5.setSizePolicy(sizePolicy)
        self.l5.setMinimumSize(QSize(0, 0))
        self.l5.setMaximumSize(QSize(140, 20))
        self.l5.setBaseSize(QSize(0, 0))
        self.l5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l5, 0, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout0.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.l3 = QLabel(self.tabPipe)
        self.l3.setObjectName(u"l3")
        sizePolicy.setHeightForWidth(self.l3.sizePolicy().hasHeightForWidth())
        self.l3.setSizePolicy(sizePolicy)
        self.l3.setMinimumSize(QSize(0, 0))
        self.l3.setMaximumSize(QSize(140, 35))
        self.l3.setBaseSize(QSize(0, 0))
        self.l3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l3, 3, 0, 1, 1)

        self.t_D = QLineEdit(self.tabPipe)
        self.t_D.setObjectName(u"t_D")
        sizePolicy.setHeightForWidth(self.t_D.sizePolicy().hasHeightForWidth())
        self.t_D.setSizePolicy(sizePolicy)
        self.t_D.setMinimumSize(QSize(80, 25))
        self.t_D.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_D, 0, 1, 1, 1)

        self.l1 = QLabel(self.tabPipe)
        self.l1.setObjectName(u"l1")
        sizePolicy.setHeightForWidth(self.l1.sizePolicy().hasHeightForWidth())
        self.l1.setSizePolicy(sizePolicy)
        self.l1.setMinimumSize(QSize(0, 0))
        self.l1.setMaximumSize(QSize(140, 35))
        self.l1.setBaseSize(QSize(0, 0))
        self.l1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l1, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout0.addItem(self.horizontalSpacer, 3, 2, 1, 1)

        self.l6 = QLabel(self.tabPipe)
        self.l6.setObjectName(u"l6")
        sizePolicy.setHeightForWidth(self.l6.sizePolicy().hasHeightForWidth())
        self.l6.setSizePolicy(sizePolicy)
        self.l6.setMinimumSize(QSize(0, 0))
        self.l6.setMaximumSize(QSize(140, 20))
        self.l6.setBaseSize(QSize(0, 0))
        self.l6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l6, 1, 3, 1, 1)

        self.t_VW = QLineEdit(self.tabPipe)
        self.t_VW.setObjectName(u"t_VW")
        sizePolicy.setHeightForWidth(self.t_VW.sizePolicy().hasHeightForWidth())
        self.t_VW.setSizePolicy(sizePolicy)
        self.t_VW.setMinimumSize(QSize(80, 25))
        self.t_VW.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_VW, 1, 4, 1, 1)

        self.t_HW = QLineEdit(self.tabPipe)
        self.t_HW.setObjectName(u"t_HW")
        sizePolicy.setHeightForWidth(self.t_HW.sizePolicy().hasHeightForWidth())
        self.t_HW.setSizePolicy(sizePolicy)
        self.t_HW.setMinimumSize(QSize(80, 25))
        self.t_HW.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_HW, 0, 4, 1, 1)

        self.t_IW = QLineEdit(self.tabPipe)
        self.t_IW.setObjectName(u"t_IW")
        sizePolicy.setHeightForWidth(self.t_IW.sizePolicy().hasHeightForWidth())
        self.t_IW.setSizePolicy(sizePolicy)
        self.t_IW.setMinimumSize(QSize(80, 25))
        self.t_IW.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_IW, 1, 1, 1, 1)

        self.t_OW = QLineEdit(self.tabPipe)
        self.t_OW.setObjectName(u"t_OW")
        sizePolicy.setHeightForWidth(self.t_OW.sizePolicy().hasHeightForWidth())
        self.t_OW.setSizePolicy(sizePolicy)
        self.t_OW.setMinimumSize(QSize(80, 25))
        self.t_OW.setMaximumSize(QSize(80, 25))

        self.gridLayout0.addWidget(self.t_OW, 3, 1, 1, 1)

        self.l12 = QLabel(self.tabPipe)
        self.l12.setObjectName(u"l12")
        self.l12.setMaximumSize(QSize(140, 35))
        self.l12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout0.addWidget(self.l12, 4, 0, 1, 1)

        self.sp_Weed = QSpinBox(self.tabPipe)
        self.sp_Weed.setObjectName(u"sp_Weed")
        sizePolicy.setHeightForWidth(self.sp_Weed.sizePolicy().hasHeightForWidth())
        self.sp_Weed.setSizePolicy(sizePolicy)
        self.sp_Weed.setMinimumSize(QSize(80, 25))
        self.sp_Weed.setMaximumSize(QSize(80, 25))
        self.sp_Weed.setMinimum(1)
        self.sp_Weed.setMaximum(10)

        self.gridLayout0.addWidget(self.sp_Weed, 4, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout0)

        self.ch_ApplyTide = QCheckBox(self.tabPipe)
        self.ch_ApplyTide.setObjectName(u"ch_ApplyTide")
        self.ch_ApplyTide.setEnabled(False)
        sizePolicy.setHeightForWidth(self.ch_ApplyTide.sizePolicy().hasHeightForWidth())
        self.ch_ApplyTide.setSizePolicy(sizePolicy)
        self.ch_ApplyTide.setMaximumSize(QSize(180, 35))
        self.ch_ApplyTide.setChecked(True)

        self.verticalLayout_4.addWidget(self.ch_ApplyTide)

        self.tabWidget.addTab(self.tabPipe, "")
        self.tabFlags = QWidget()
        self.tabFlags.setObjectName(u"tabFlags")
        self.verticalLayout_5 = QVBoxLayout(self.tabFlags)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox = QGroupBox(self.tabFlags)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout1 = QGridLayout()
        self.gridLayout1.setSpacing(10)
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.gridLayout1.setContentsMargins(5, 5, 5, 5)
        self.l9 = QLabel(self.groupBox)
        self.l9.setObjectName(u"l9")
        sizePolicy.setHeightForWidth(self.l9.sizePolicy().hasHeightForWidth())
        self.l9.setSizePolicy(sizePolicy)
        self.l9.setMaximumSize(QSize(160, 35))
        self.l9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout1.addWidget(self.l9, 1, 0, 1, 1)

        self.l10 = QLabel(self.groupBox)
        self.l10.setObjectName(u"l10")
        sizePolicy.setHeightForWidth(self.l10.sizePolicy().hasHeightForWidth())
        self.l10.setSizePolicy(sizePolicy)
        self.l10.setMaximumSize(QSize(160, 35))
        self.l10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout1.addWidget(self.l10, 2, 0, 1, 1)

        self.t_AntiSpoof = QLineEdit(self.groupBox)
        self.t_AntiSpoof.setObjectName(u"t_AntiSpoof")
        sizePolicy.setHeightForWidth(self.t_AntiSpoof.sizePolicy().hasHeightForWidth())
        self.t_AntiSpoof.setSizePolicy(sizePolicy)
        self.t_AntiSpoof.setMinimumSize(QSize(80, 25))
        self.t_AntiSpoof.setMaximumSize(QSize(80, 25))

        self.gridLayout1.addWidget(self.t_AntiSpoof, 2, 1, 1, 1)

        self.t_Fl = QLineEdit(self.groupBox)
        self.t_Fl.setObjectName(u"t_Fl")
        sizePolicy.setHeightForWidth(self.t_Fl.sizePolicy().hasHeightForWidth())
        self.t_Fl.setSizePolicy(sizePolicy)
        self.t_Fl.setMinimumSize(QSize(80, 25))
        self.t_Fl.setMaximumSize(QSize(80, 25))

        self.gridLayout1.addWidget(self.t_Fl, 0, 1, 1, 1)

        self.l8 = QLabel(self.groupBox)
        self.l8.setObjectName(u"l8")
        sizePolicy.setHeightForWidth(self.l8.sizePolicy().hasHeightForWidth())
        self.l8.setSizePolicy(sizePolicy)
        self.l8.setMaximumSize(QSize(160, 35))
        self.l8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout1.addWidget(self.l8, 0, 0, 1, 1)

        self.t_FlPt = QLineEdit(self.groupBox)
        self.t_FlPt.setObjectName(u"t_FlPt")
        sizePolicy.setHeightForWidth(self.t_FlPt.sizePolicy().hasHeightForWidth())
        self.t_FlPt.setSizePolicy(sizePolicy)
        self.t_FlPt.setMinimumSize(QSize(80, 25))
        self.t_FlPt.setMaximumSize(QSize(80, 25))

        self.gridLayout1.addWidget(self.t_FlPt, 1, 1, 1, 1)

        self.l13 = QLabel(self.groupBox)
        self.l13.setObjectName(u"l13")
        self.l13.setMaximumSize(QSize(160, 35))
        self.l13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout1.addWidget(self.l13, 3, 0, 1, 1)

        self.t_AdPad = QLineEdit(self.groupBox)
        self.t_AdPad.setObjectName(u"t_AdPad")
        sizePolicy.setHeightForWidth(self.t_AdPad.sizePolicy().hasHeightForWidth())
        self.t_AdPad.setSizePolicy(sizePolicy)
        self.t_AdPad.setMinimumSize(QSize(80, 25))
        self.t_AdPad.setMaximumSize(QSize(80, 25))

        self.gridLayout1.addWidget(self.t_AdPad, 3, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout1)

        self.gB1 = QGroupBox(self.groupBox)
        self.gB1.setObjectName(u"gB1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gB1.sizePolicy().hasHeightForWidth())
        self.gB1.setSizePolicy(sizePolicy1)
        self.gB1.setMaximumSize(QSize(280, 200))
        self.gridLayout = QGridLayout(self.gB1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rb_Fmean = QRadioButton(self.gB1)
        self.rb_Fmean.setObjectName(u"rb_Fmean")
        sizePolicy.setHeightForWidth(self.rb_Fmean.sizePolicy().hasHeightForWidth())
        self.rb_Fmean.setSizePolicy(sizePolicy)
        self.rb_Fmean.setMaximumSize(QSize(160, 35))

        self.gridLayout.addWidget(self.rb_Fmean, 0, 1, 1, 1)

        self.rb_Fmin = QRadioButton(self.gB1)
        self.rb_Fmin.setObjectName(u"rb_Fmin")
        sizePolicy.setHeightForWidth(self.rb_Fmin.sizePolicy().hasHeightForWidth())
        self.rb_Fmin.setSizePolicy(sizePolicy)
        self.rb_Fmin.setMaximumSize(QSize(160, 35))

        self.gridLayout.addWidget(self.rb_Fmin, 0, 0, 1, 1)

        self.rb_Fmax = QRadioButton(self.gB1)
        self.rb_Fmax.setObjectName(u"rb_Fmax")
        sizePolicy.setHeightForWidth(self.rb_Fmax.sizePolicy().hasHeightForWidth())
        self.rb_Fmax.setSizePolicy(sizePolicy)
        self.rb_Fmax.setMaximumSize(QSize(160, 35))

        self.gridLayout.addWidget(self.rb_Fmax, 1, 0, 1, 1)

        self.rb_Fadapt = QRadioButton(self.gB1)
        self.rb_Fadapt.setObjectName(u"rb_Fadapt")
        sizePolicy.setHeightForWidth(self.rb_Fadapt.sizePolicy().hasHeightForWidth())
        self.rb_Fadapt.setSizePolicy(sizePolicy)
        self.rb_Fadapt.setMaximumSize(QSize(160, 35))
        self.rb_Fadapt.setChecked(True)

        self.gridLayout.addWidget(self.rb_Fadapt, 1, 1, 1, 1)

        self.line = QFrame(self.gB1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)

        self.ch_FiSnap = QCheckBox(self.gB1)
        self.ch_FiSnap.setObjectName(u"ch_FiSnap")
        sizePolicy.setHeightForWidth(self.ch_FiSnap.sizePolicy().hasHeightForWidth())
        self.ch_FiSnap.setSizePolicy(sizePolicy)
        self.ch_FiSnap.setMinimumSize(QSize(200, 0))
        self.ch_FiSnap.setMaximumSize(QSize(200, 35))
        self.ch_FiSnap.setChecked(True)

        self.gridLayout.addWidget(self.ch_FiSnap, 5, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.horizontalLayout.addWidget(self.gB1)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tabFlags)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.rb_FoDist = QRadioButton(self.groupBox_2)
        self.rb_FoDist.setObjectName(u"rb_FoDist")
        self.rb_FoDist.setMinimumSize(QSize(180, 0))
        self.rb_FoDist.setMaximumSize(QSize(180, 35))
        self.rb_FoDist.setChecked(True)

        self.gridLayout_2.addWidget(self.rb_FoDist, 0, 0, 1, 1)

        self.t_FoPers = QLineEdit(self.groupBox_2)
        self.t_FoPers.setObjectName(u"t_FoPers")
        self.t_FoPers.setMinimumSize(QSize(80, 25))
        self.t_FoPers.setMaximumSize(QSize(80, 25))

        self.gridLayout_2.addWidget(self.t_FoPers, 1, 1, 1, 1)

        self.t_FoDist = QLineEdit(self.groupBox_2)
        self.t_FoDist.setObjectName(u"t_FoDist")
        self.t_FoDist.setMinimumSize(QSize(80, 25))
        self.t_FoDist.setMaximumSize(QSize(80, 25))

        self.gridLayout_2.addWidget(self.t_FoDist, 0, 1, 1, 1)

        self.rb_FoPers = QRadioButton(self.groupBox_2)
        self.rb_FoPers.setObjectName(u"rb_FoPers")
        self.rb_FoPers.setMinimumSize(QSize(180, 0))
        self.rb_FoPers.setMaximumSize(QSize(180, 35))

        self.gridLayout_2.addWidget(self.rb_FoPers, 1, 0, 1, 1)

        self.ch_FoSnap = QCheckBox(self.groupBox_2)
        self.ch_FoSnap.setObjectName(u"ch_FoSnap")
        self.ch_FoSnap.setMaximumSize(QSize(180, 35))
        self.ch_FoSnap.setChecked(True)

        self.gridLayout_2.addWidget(self.ch_FoSnap, 2, 0, 1, 2)

        self.ch_FoShow = QCheckBox(self.groupBox_2)
        self.ch_FoShow.setObjectName(u"ch_FoShow")
        self.ch_FoShow.setMaximumSize(QSize(180, 35))

        self.gridLayout_2.addWidget(self.ch_FoShow, 3, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tabFlags, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Edit = QGroupBox(self.tab)
        self.Edit.setObjectName(u"Edit")
        self.verticalLayout_2 = QVBoxLayout(self.Edit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rb_Pr = QRadioButton(self.Edit)
        self.rb_Pr.setObjectName(u"rb_Pr")
        self.rb_Pr.setChecked(True)

        self.verticalLayout_2.addWidget(self.rb_Pr)

        self.rb_Pt = QRadioButton(self.Edit)
        self.rb_Pt.setObjectName(u"rb_Pt")
        self.rb_Pt.setEnabled(False)

        self.verticalLayout_2.addWidget(self.rb_Pt)

        self.PT = QGroupBox(self.Edit)
        self.PT.setObjectName(u"PT")
        self.PT.setEnabled(False)
        self.verticalLayout_3 = QVBoxLayout(self.PT)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.rb_RejectPT = QRadioButton(self.PT)
        self.rb_RejectPT.setObjectName(u"rb_RejectPT")
        self.rb_RejectPT.setChecked(True)

        self.verticalLayout_3.addWidget(self.rb_RejectPT)

        self.rb_AcceptPT = QRadioButton(self.PT)
        self.rb_AcceptPT.setObjectName(u"rb_AcceptPT")

        self.verticalLayout_3.addWidget(self.rb_AcceptPT)


        self.verticalLayout_2.addWidget(self.PT)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.l14 = QLabel(self.Edit)
        self.l14.setObjectName(u"l14")
        self.l14.setMaximumSize(QSize(140, 35))
        self.l14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.l14)

        self.t_PtGap = QLineEdit(self.Edit)
        self.t_PtGap.setObjectName(u"t_PtGap")
        sizePolicy.setHeightForWidth(self.t_PtGap.sizePolicy().hasHeightForWidth())
        self.t_PtGap.setSizePolicy(sizePolicy)
        self.t_PtGap.setMinimumSize(QSize(80, 25))
        self.t_PtGap.setMaximumSize(QSize(80, 25))

        self.horizontalLayout_4.addWidget(self.t_PtGap)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.verticalLayout_6.addWidget(self.Edit)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.l11 = QLabel(self.tab_2)
        self.l11.setObjectName(u"l11")
        self.l11.setEnabled(True)
        self.l11.setMinimumSize(QSize(80, 25))
        self.l11.setMaximumSize(QSize(80, 25))
        self.l11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.l11, 3, 0, 1, 1)

        self.l15 = QLabel(self.tab_2)
        self.l15.setObjectName(u"l15")
        self.l15.setMinimumSize(QSize(80, 25))
        self.l15.setMaximumSize(QSize(80, 25))
        self.l15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.l15, 1, 0, 1, 1)

        self.spb_Convention = QSpinBox(self.tab_2)
        self.spb_Convention.setObjectName(u"spb_Convention")
        self.spb_Convention.setMinimumSize(QSize(80, 25))
        self.spb_Convention.setMaximumSize(QSize(80, 25))
        self.spb_Convention.setMinimum(14)
        self.spb_Convention.setMaximum(20)

        self.gridLayout_3.addWidget(self.spb_Convention, 0, 1, 1, 1)

        self.l16 = QLabel(self.tab_2)
        self.l16.setObjectName(u"l16")
        self.l16.setMinimumSize(QSize(80, 25))
        self.l16.setMaximumSize(QSize(80, 25))

        self.gridLayout_3.addWidget(self.l16, 2, 0, 1, 1)

        self.ch_ShowCamOffset = QCheckBox(self.tab_2)
        self.ch_ShowCamOffset.setObjectName(u"ch_ShowCamOffset")
        self.ch_ShowCamOffset.setMinimumSize(QSize(200, 25))
        self.ch_ShowCamOffset.setMaximumSize(QSize(200, 25))

        self.gridLayout_3.addWidget(self.ch_ShowCamOffset, 3, 2, 1, 1)

        self.spb_Timezone = QDoubleSpinBox(self.tab_2)
        self.spb_Timezone.setObjectName(u"spb_Timezone")
        self.spb_Timezone.setMinimumSize(QSize(80, 25))
        self.spb_Timezone.setMaximumSize(QSize(80, 25))
        self.spb_Timezone.setDecimals(1)
        self.spb_Timezone.setMinimum(-12.000000000000000)
        self.spb_Timezone.setMaximum(12.000000000000000)
        self.spb_Timezone.setSingleStep(0.500000000000000)

        self.gridLayout_3.addWidget(self.spb_Timezone, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 0, 2, 1, 1)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 25))
        self.label_2.setMaximumSize(QSize(80, 25))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.t_CamOffset = QLineEdit(self.tab_2)
        self.t_CamOffset.setObjectName(u"t_CamOffset")
        self.t_CamOffset.setEnabled(True)
        self.t_CamOffset.setMinimumSize(QSize(80, 25))
        self.t_CamOffset.setMaximumSize(QSize(80, 25))

        self.gridLayout_3.addWidget(self.t_CamOffset, 3, 1, 1, 1)

        self.l17 = QLabel(self.tab_2)
        self.l17.setObjectName(u"l17")
        self.l17.setMinimumSize(QSize(80, 25))
        self.l17.setMaximumSize(QSize(80, 25))
        self.l17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.l17, 4, 0, 1, 1)

        self.spb_CamSize = QSpinBox(self.tab_2)
        self.spb_CamSize.setObjectName(u"spb_CamSize")
        self.spb_CamSize.setMinimumSize(QSize(80, 25))
        self.spb_CamSize.setMaximumSize(QSize(80, 25))
        self.spb_CamSize.setMinimum(4)
        self.spb_CamSize.setMaximum(50)
        self.spb_CamSize.setValue(15)

        self.gridLayout_3.addWidget(self.spb_CamSize, 4, 1, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.b_Pause = QPushButton(self.tab_2)
        self.b_Pause.setObjectName(u"b_Pause")
        self.b_Pause.setEnabled(False)
        sizePolicy.setHeightForWidth(self.b_Pause.sizePolicy().hasHeightForWidth())
        self.b_Pause.setSizePolicy(sizePolicy)
        self.b_Pause.setMinimumSize(QSize(150, 150))
        self.b_Pause.setMaximumSize(QSize(150, 150))

        self.horizontalLayout_3.addWidget(self.b_Pause)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_8.addWidget(self.tabWidget)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_3)

        self.l_Coord = QLabel(self.centralwidget)
        self.l_Coord.setObjectName(u"l_Coord")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.l_Coord.setFont(font1)

        self.verticalLayout_8.addWidget(self.l_Coord)

        self.l_Saved = QLabel(self.centralwidget)
        self.l_Saved.setObjectName(u"l_Saved")
        self.l_Saved.setFont(font1)

        self.verticalLayout_8.addWidget(self.l_Saved)

        CONTROL.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CONTROL)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 544, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuSave = QMenu(self.menubar)
        self.menuSave.setObjectName(u"menuSave")
        self.menuSave.setFont(font)
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        self.menuVideo = QMenu(self.menubar)
        self.menuVideo.setObjectName(u"menuVideo")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        CONTROL.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuVideo.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionLoad_profiles)
        self.menuFile.addAction(self.actionLoad_GeoTiff)
        self.menuFile.addAction(self.actionLoad_tide)
        self.menuFile.addAction(self.actionLoad_pipetracker)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_saved_work)
        self.menuSave.addAction(self.actionSave_work)
        self.menuExport.addAction(self.actionExport_EIVA)
        self.menuExport.addAction(self.actionExport_SFX)
        self.menuVideo.addAction(self.actionBuild_Playlist)
        self.menuVideo.addAction(self.actionLoad_playlist)
        self.menuView.addAction(self.actionXView)
        self.menuView.addAction(self.actionPView)
        self.menuView.addAction(self.actionLView)
        self.menuView.addAction(self.actionDV_Control)
        self.menuSettings.addAction(self.actionSettings)
        self.menuSettings.addAction(self.actionSave_layout)
        self.menuSettings.addAction(self.actionLoad_layout)
        self.menuAbout.addAction(self.actionManual)
        self.menuAbout.addAction(self.actionVersion)
        self.menuAbout.addAction(self.actionInfo)

        self.retranslateUi(CONTROL)
        self.t_D.editingFinished.connect(CONTROL.setFocus)
        self.t_IW.editingFinished.connect(CONTROL.setFocus)
        self.t_OW.editingFinished.connect(CONTROL.setFocus)
        self.t_HW.editingFinished.connect(CONTROL.setFocus)
        self.t_VW.editingFinished.connect(CONTROL.setFocus)
        self.t_RES.editingFinished.connect(CONTROL.setFocus)
        self.ch_ApplyTide.stateChanged.connect(CONTROL.setFocus)
        self.t_Fl.editingFinished.connect(CONTROL.setFocus)
        self.t_FlPt.editingFinished.connect(CONTROL.setFocus)
        self.t_AntiSpoof.editingFinished.connect(CONTROL.setFocus)
        self.gB1.toggled.connect(CONTROL.setFocus)
        self.t_FoDist.editingFinished.connect(CONTROL.setFocus)
        self.t_FoPers.editingFinished.connect(CONTROL.setFocus)
        self.ch_FiSnap.stateChanged.connect(CONTROL.setFocus)
        self.rb_FoDist.toggled.connect(CONTROL.setFocus)
        self.rb_FoPers.toggled.connect(CONTROL.setFocus)
        self.ch_FoSnap.stateChanged.connect(CONTROL.setFocus)
        self.t_AdPad.editingFinished.connect(CONTROL.setFocus)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CONTROL)
    # setupUi

    def retranslateUi(self, CONTROL):
        CONTROL.setWindowTitle(QCoreApplication.translate("CONTROL", u"Control", None))
        self.actionLoad_profiles.setText(QCoreApplication.translate("CONTROL", u"Load profiles", None))
        self.actionLoad_GeoTiff.setText(QCoreApplication.translate("CONTROL", u"Load geoimage", None))
#if QT_CONFIG(tooltip)
        self.actionLoad_GeoTiff.setToolTip(QCoreApplication.translate("CONTROL", u"Load Georeferenced Image", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoad_tide.setText(QCoreApplication.translate("CONTROL", u"Load tide", None))
        self.actionSave_work.setText(QCoreApplication.translate("CONTROL", u"Save work", None))
        self.actionLoad_saved_work.setText(QCoreApplication.translate("CONTROL", u"Load saved work", None))
        self.actionExport_EIVA.setText(QCoreApplication.translate("CONTROL", u"Export EIVA", None))
        self.actionLoad_pipetracker.setText(QCoreApplication.translate("CONTROL", u"Load pipetracker", None))
        self.actionSave_layout.setText(QCoreApplication.translate("CONTROL", u"Save workspace", None))
        self.actionLoad_layout.setText(QCoreApplication.translate("CONTROL", u"Load workspace", None))
        self.actionExport_SFX.setText(QCoreApplication.translate("CONTROL", u"Export SFX", None))
        self.actionBuild_Playlist.setText(QCoreApplication.translate("CONTROL", u"Build playlist", None))
        self.actionLoad_playlist.setText(QCoreApplication.translate("CONTROL", u"Load playlist", None))
        self.actionXView.setText(QCoreApplication.translate("CONTROL", u"XView", None))
        self.actionPView.setText(QCoreApplication.translate("CONTROL", u"PView", None))
        self.actionLView.setText(QCoreApplication.translate("CONTROL", u"LView", None))
        self.actionSettings.setText(QCoreApplication.translate("CONTROL", u"Edit palette", None))
        self.actionLoad_colors.setText(QCoreApplication.translate("CONTROL", u"Load palette", None))
        self.actionDV_Control.setText(QCoreApplication.translate("CONTROL", u"DV Control", None))
        self.actionInfo.setText(QCoreApplication.translate("CONTROL", u"Copyright (c) 2025 Aleksandr Kaiurin (akayurin@gmail.com)", None))
        self.actionInfo.setIconText(QCoreApplication.translate("CONTROL", u"Copyright (c) 2025 Aleksandr Kaiurin (akayurin@gmail.com)", None))
        self.actionVersion.setText(QCoreApplication.translate("CONTROL", u"Version 7.1", None))
        self.actionManual.setText(QCoreApplication.translate("CONTROL", u"Manual", None))
        self.actionLoad_events.setText(QCoreApplication.translate("CONTROL", u"Load VW events", None))
        self.actionEvents.setText(QCoreApplication.translate("CONTROL", u"Events", None))
        self.l7.setText(QCoreApplication.translate("CONTROL", u"Resolution (m):", None))
        self.l2.setText(QCoreApplication.translate("CONTROL", u"In wall (*D):", None))
        self.t_RES.setText(QCoreApplication.translate("CONTROL", u"0.01", None))
        self.l5.setText(QCoreApplication.translate("CONTROL", u"H window (m):", None))
        self.l3.setText(QCoreApplication.translate("CONTROL", u"Out wall (*D):", None))
        self.t_D.setText(QCoreApplication.translate("CONTROL", u"0.2", None))
        self.l1.setText(QCoreApplication.translate("CONTROL", u"Diameter (m):", None))
        self.l6.setText(QCoreApplication.translate("CONTROL", u"V window (m):", None))
        self.t_VW.setText(QCoreApplication.translate("CONTROL", u"0.1", None))
        self.t_HW.setText(QCoreApplication.translate("CONTROL", u"1.0", None))
        self.t_IW.setText(QCoreApplication.translate("CONTROL", u"0.98", None))
        self.t_OW.setText(QCoreApplication.translate("CONTROL", u"1.05", None))
        self.l12.setText(QCoreApplication.translate("CONTROL", u"Weed:", None))
        self.ch_ApplyTide.setText(QCoreApplication.translate("CONTROL", u"Apply tide", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPipe), QCoreApplication.translate("CONTROL", u"Pipe", None))
        self.groupBox.setTitle(QCoreApplication.translate("CONTROL", u"Inner flags", None))
        self.l9.setText(QCoreApplication.translate("CONTROL", u"Flag patch (m):", None))
        self.l10.setText(QCoreApplication.translate("CONTROL", u"AntiSpoof (m):", None))
        self.t_AntiSpoof.setText(QCoreApplication.translate("CONTROL", u"0.01", None))
        self.t_Fl.setText(QCoreApplication.translate("CONTROL", u"0.26", None))
        self.l8.setText(QCoreApplication.translate("CONTROL", u"TOP to Flag (m):", None))
        self.t_FlPt.setText(QCoreApplication.translate("CONTROL", u"0.1", None))
        self.l13.setText(QCoreApplication.translate("CONTROL", u"Pad (m):", None))
        self.t_AdPad.setText(QCoreApplication.translate("CONTROL", u"0.0", None))
        self.gB1.setTitle(QCoreApplication.translate("CONTROL", u"Place flags", None))
        self.rb_Fmean.setText(QCoreApplication.translate("CONTROL", u"Mean", None))
        self.rb_Fmin.setText(QCoreApplication.translate("CONTROL", u"Minimum", None))
        self.rb_Fmax.setText(QCoreApplication.translate("CONTROL", u"Maximum", None))
        self.rb_Fadapt.setText(QCoreApplication.translate("CONTROL", u"Adaptive", None))
        self.ch_FiSnap.setText(QCoreApplication.translate("CONTROL", u"Snap to data", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("CONTROL", u"Outer flags", None))
        self.rb_FoDist.setText(QCoreApplication.translate("CONTROL", u"TOP to Flag (m):", None))
        self.t_FoPers.setText(QCoreApplication.translate("CONTROL", u"100", None))
        self.t_FoDist.setText(QCoreApplication.translate("CONTROL", u"1", None))
        self.rb_FoPers.setText(QCoreApplication.translate("CONTROL", u"TOP to Flag (%):", None))
        self.ch_FoSnap.setText(QCoreApplication.translate("CONTROL", u"Snap to data", None))
        self.ch_FoShow.setText(QCoreApplication.translate("CONTROL", u"Show flags", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFlags), QCoreApplication.translate("CONTROL", u"Flags", None))
        self.Edit.setTitle(QCoreApplication.translate("CONTROL", u"Edit", None))
        self.rb_Pr.setText(QCoreApplication.translate("CONTROL", u"Pipe", None))
        self.rb_Pt.setText(QCoreApplication.translate("CONTROL", u"Pipetracker", None))
        self.PT.setTitle("")
        self.rb_RejectPT.setText(QCoreApplication.translate("CONTROL", u"Reject (ALT key)", None))
        self.rb_AcceptPT.setText(QCoreApplication.translate("CONTROL", u"Accept (ALT key)", None))
        self.l14.setText(QCoreApplication.translate("CONTROL", u"Max PT gap (m):", None))
        self.t_PtGap.setText(QCoreApplication.translate("CONTROL", u"5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("CONTROL", u"Edit", None))
        self.l11.setText(QCoreApplication.translate("CONTROL", u"Cam offset:", None))
        self.l15.setText(QCoreApplication.translate("CONTROL", u"Time zone:", None))
        self.l16.setText("")
        self.ch_ShowCamOffset.setText(QCoreApplication.translate("CONTROL", u"Show camera offset", None))
        self.label_2.setText(QCoreApplication.translate("CONTROL", u"Time digits:", None))
        self.t_CamOffset.setText(QCoreApplication.translate("CONTROL", u"0.0", None))
        self.l17.setText(QCoreApplication.translate("CONTROL", u"Symb. size:", None))
        self.b_Pause.setText(QCoreApplication.translate("CONTROL", u"No DV loaded", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("CONTROL", u"Video", None))
        self.l_Coord.setText(QCoreApplication.translate("CONTROL", u"C:", None))
        self.l_Saved.setText(QCoreApplication.translate("CONTROL", u"LAST SAVED:", None))
        self.menuFile.setTitle(QCoreApplication.translate("CONTROL", u"File", None))
        self.menuSave.setTitle(QCoreApplication.translate("CONTROL", u"Save", None))
        self.menuExport.setTitle(QCoreApplication.translate("CONTROL", u"Export", None))
        self.menuVideo.setTitle(QCoreApplication.translate("CONTROL", u"Video", None))
        self.menuView.setTitle(QCoreApplication.translate("CONTROL", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("CONTROL", u"Workspace", None))
        self.menuAbout.setTitle(QCoreApplication.translate("CONTROL", u"About", None))
    # retranslateUi

