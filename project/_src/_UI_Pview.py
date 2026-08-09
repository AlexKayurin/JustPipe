# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_UI_Pview.ui'
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
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

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
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.Layout0 = QHBoxLayout()
        self.Layout0.setSpacing(5)
        self.Layout0.setObjectName(u"Layout0")
        self.Layout0.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.Layout0.setContentsMargins(0, 0, 0, 0)
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
        font1.setPointSize(10)
        font1.setBold(True)
        self.b_POI.setFont(font1)

        self.horizontalLayout.addWidget(self.b_POI)

        self.b_Interpolate = QPushButton(self.groupBox)
        self.b_Interpolate.setObjectName(u"b_Interpolate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_Interpolate.sizePolicy().hasHeightForWidth())
        self.b_Interpolate.setSizePolicy(sizePolicy)
        self.b_Interpolate.setMinimumSize(QSize(40, 40))
        self.b_Interpolate.setMaximumSize(QSize(40, 40))
        self.b_Interpolate.setFont(font1)
        self.b_Interpolate.setToolTipDuration(-1)
        self.b_Interpolate.setFlat(False)

        self.horizontalLayout.addWidget(self.b_Interpolate)

        self.b_snap_h = QPushButton(self.groupBox)
        self.b_snap_h.setObjectName(u"b_snap_h")
        self.b_snap_h.setEnabled(False)
        self.b_snap_h.setMinimumSize(QSize(40, 40))
        self.b_snap_h.setMaximumSize(QSize(40, 40))
        self.b_snap_h.setFont(font1)

        self.horizontalLayout.addWidget(self.b_snap_h)


        self.Layout0.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(470, 50))
        self.groupBox_2.setMaximumSize(QSize(470, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.b_EditMode = QPushButton(self.groupBox_2)
        self.b_EditMode.setObjectName(u"b_EditMode")
        self.b_EditMode.setEnabled(False)
        self.b_EditMode.setMinimumSize(QSize(40, 40))
        self.b_EditMode.setMaximumSize(QSize(40, 40))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.b_EditMode.setFont(font2)

        self.horizontalLayout_2.addWidget(self.b_EditMode)

        self.gb_PT_Rej_Acc = QGroupBox(self.groupBox_2)
        self.gb_PT_Rej_Acc.setObjectName(u"gb_PT_Rej_Acc")
        self.gb_PT_Rej_Acc.setEnabled(False)
        self.gb_PT_Rej_Acc.setMinimumSize(QSize(70, 40))
        self.gb_PT_Rej_Acc.setMaximumSize(QSize(70, 40))
        self.verticalLayout_2 = QVBoxLayout(self.gb_PT_Rej_Acc)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.rb_RejectPT = QRadioButton(self.gb_PT_Rej_Acc)
        self.rb_RejectPT.setObjectName(u"rb_RejectPT")
        self.rb_RejectPT.setMinimumSize(QSize(70, 15))
        self.rb_RejectPT.setMaximumSize(QSize(70, 15))
        font3 = QFont()
        font3.setPointSize(8)
        self.rb_RejectPT.setFont(font3)
        self.rb_RejectPT.setChecked(True)

        self.verticalLayout_2.addWidget(self.rb_RejectPT)

        self.rb_AcceptPT = QRadioButton(self.gb_PT_Rej_Acc)
        self.rb_AcceptPT.setObjectName(u"rb_AcceptPT")
        self.rb_AcceptPT.setMinimumSize(QSize(70, 15))
        self.rb_AcceptPT.setMaximumSize(QSize(70, 15))
        self.rb_AcceptPT.setFont(font3)

        self.verticalLayout_2.addWidget(self.rb_AcceptPT)


        self.horizontalLayout_2.addWidget(self.gb_PT_Rej_Acc)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 20))
        self.label_2.setMaximumSize(QSize(70, 20))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.sp_Pt_Weed = QSpinBox(self.groupBox_2)
        self.sp_Pt_Weed.setObjectName(u"sp_Pt_Weed")
        self.sp_Pt_Weed.setMinimumSize(QSize(70, 20))
        self.sp_Pt_Weed.setMaximumSize(QSize(70, 20))
        self.sp_Pt_Weed.setFont(font)
        self.sp_Pt_Weed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sp_Pt_Weed.setMinimum(1)
        self.sp_Pt_Weed.setMaximum(1000)
        self.sp_Pt_Weed.setValue(5)

        self.verticalLayout_3.addWidget(self.sp_Pt_Weed)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.l14 = QLabel(self.groupBox_2)
        self.l14.setObjectName(u"l14")
        self.l14.setMinimumSize(QSize(70, 20))
        self.l14.setMaximumSize(QSize(70, 20))
        self.l14.setFont(font)
        self.l14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.l14)

        self.t_PtGap = QLineEdit(self.groupBox_2)
        self.t_PtGap.setObjectName(u"t_PtGap")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.t_PtGap.sizePolicy().hasHeightForWidth())
        self.t_PtGap.setSizePolicy(sizePolicy1)
        self.t_PtGap.setMinimumSize(QSize(70, 20))
        self.t_PtGap.setMaximumSize(QSize(70, 20))
        self.t_PtGap.setFont(font)
        self.t_PtGap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.t_PtGap)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.l1 = QLabel(self.groupBox_2)
        self.l1.setObjectName(u"l1")
        self.l1.setMinimumSize(QSize(70, 20))
        self.l1.setMaximumSize(QSize(70, 20))
        self.l1.setFont(font)
        self.l1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.l1)

        self.t_EdSpot = QLineEdit(self.groupBox_2)
        self.t_EdSpot.setObjectName(u"t_EdSpot")
        self.t_EdSpot.setEnabled(False)
        self.t_EdSpot.setMinimumSize(QSize(70, 20))
        self.t_EdSpot.setMaximumSize(QSize(70, 20))
        self.t_EdSpot.setFont(font)
        self.t_EdSpot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.t_EdSpot)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.l0 = QLabel(self.groupBox_2)
        self.l0.setObjectName(u"l0")
        self.l0.setMinimumSize(QSize(70, 20))
        self.l0.setMaximumSize(QSize(70, 20))
        self.l0.setFont(font)
        self.l0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.l0)

        self.t_smW = QLineEdit(self.groupBox_2)
        self.t_smW.setObjectName(u"t_smW")
        self.t_smW.setEnabled(False)
        self.t_smW.setMinimumSize(QSize(70, 20))
        self.t_smW.setMaximumSize(QSize(70, 20))
        self.t_smW.setFont(font)
        self.t_smW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.t_smW)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.b_smoothPT_p = QPushButton(self.groupBox_2)
        self.b_smoothPT_p.setObjectName(u"b_smoothPT_p")
        self.b_smoothPT_p.setEnabled(False)
        sizePolicy.setHeightForWidth(self.b_smoothPT_p.sizePolicy().hasHeightForWidth())
        self.b_smoothPT_p.setSizePolicy(sizePolicy)
        self.b_smoothPT_p.setMinimumSize(QSize(40, 40))
        self.b_smoothPT_p.setMaximumSize(QSize(40, 40))
        self.b_smoothPT_p.setFont(font1)
        self.b_smoothPT_p.setFlat(False)

        self.horizontalLayout_2.addWidget(self.b_smoothPT_p)


        self.Layout0.addWidget(self.groupBox_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.Layout0.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.Layout0)

        self.Layout2 = QGridLayout()
        self.Layout2.setObjectName(u"Layout2")
        self.Layout2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.Layout2.setHorizontalSpacing(0)
        self.Layout2.setVerticalSpacing(5)
        self.pview = ImageView(self.centralwidget)
        self.pview.setObjectName(u"pview")

        self.Layout2.addWidget(self.pview, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.Layout2)

        self.Layout3 = QHBoxLayout()
        self.Layout3.setSpacing(5)
        self.Layout3.setObjectName(u"Layout3")
        self.Layout3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.Layout3.setContentsMargins(0, 0, 0, 0)
        self.ch_Center = QCheckBox(self.centralwidget)
        self.ch_Center.setObjectName(u"ch_Center")
        self.ch_Center.setMinimumSize(QSize(150, 20))
        self.ch_Center.setMaximumSize(QSize(150, 20))
        self.ch_Center.setFont(font)
        self.ch_Center.setChecked(True)

        self.Layout3.addWidget(self.ch_Center)

        self.ch_ShowPT = QCheckBox(self.centralwidget)
        self.ch_ShowPT.setObjectName(u"ch_ShowPT")
        self.ch_ShowPT.setEnabled(False)
        self.ch_ShowPT.setMinimumSize(QSize(150, 20))
        self.ch_ShowPT.setMaximumSize(QSize(150, 20))
        self.ch_ShowPT.setFont(font)
        self.ch_ShowPT.setChecked(True)

        self.Layout3.addWidget(self.ch_ShowPT)

        self.ch_ShowFlagL = QCheckBox(self.centralwidget)
        self.ch_ShowFlagL.setObjectName(u"ch_ShowFlagL")
        self.ch_ShowFlagL.setMinimumSize(QSize(150, 20))
        self.ch_ShowFlagL.setMaximumSize(QSize(150, 20))
        self.ch_ShowFlagL.setFont(font)
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
        self.groupBox.setTitle("")
        self.b_POI.setText(QCoreApplication.translate("PVIEW", u"POI", None))
#if QT_CONFIG(tooltip)
        self.b_Interpolate.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.b_Interpolate.setStatusTip(QCoreApplication.translate("PVIEW", u"Interpolate TOP 3D", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.b_Interpolate.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.b_Interpolate.setText(QCoreApplication.translate("PVIEW", u"I", None))
        self.b_snap_h.setText(QCoreApplication.translate("PVIEW", u"SnH", None))
        self.groupBox_2.setTitle("")
        self.b_EditMode.setText(QCoreApplication.translate("PVIEW", u"Pt/P", None))
        self.gb_PT_Rej_Acc.setTitle("")
        self.rb_RejectPT.setText(QCoreApplication.translate("PVIEW", u"Reject", None))
        self.rb_AcceptPT.setText(QCoreApplication.translate("PVIEW", u"Accept", None))
        self.label_2.setText(QCoreApplication.translate("PVIEW", u"Weed PT", None))
        self.l14.setText(QCoreApplication.translate("PVIEW", u"Gap", None))
        self.t_PtGap.setText(QCoreApplication.translate("PVIEW", u"5", None))
        self.l1.setText(QCoreApplication.translate("PVIEW", u"Edit spot", None))
        self.t_EdSpot.setText(QCoreApplication.translate("PVIEW", u"0.5", None))
        self.l0.setText(QCoreApplication.translate("PVIEW", u"Smooth pts", None))
        self.t_smW.setText(QCoreApplication.translate("PVIEW", u"10", None))
        self.b_smoothPT_p.setText(QCoreApplication.translate("PVIEW", u"Sm", None))
        self.ch_Center.setText(QCoreApplication.translate("PVIEW", u"Follow", None))
        self.ch_ShowPT.setText(QCoreApplication.translate("PVIEW", u"Show PT", None))
        self.ch_ShowFlagL.setText(QCoreApplication.translate("PVIEW", u"Show Flags", None))
    # retranslateUi

