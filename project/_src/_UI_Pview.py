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
    QHBoxLayout, QLayout, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
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
        font1.setPointSize(14)
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

        self.b_EditMode = QPushButton(self.centralwidget)
        self.b_EditMode.setObjectName(u"b_EditMode")
        self.b_EditMode.setEnabled(False)
        self.b_EditMode.setMinimumSize(QSize(120, 40))
        self.b_EditMode.setMaximumSize(QSize(120, 40))
        self.b_EditMode.setFont(font1)

        self.Layout0.addWidget(self.b_EditMode)

        self.gb_PT_Rej_Acc = QGroupBox(self.centralwidget)
        self.gb_PT_Rej_Acc.setObjectName(u"gb_PT_Rej_Acc")
        self.gb_PT_Rej_Acc.setEnabled(False)
        self.gb_PT_Rej_Acc.setMinimumSize(QSize(100, 50))
        self.gb_PT_Rej_Acc.setMaximumSize(QSize(100, 50))
        self.verticalLayout_2 = QVBoxLayout(self.gb_PT_Rej_Acc)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.rb_RejectPT = QRadioButton(self.gb_PT_Rej_Acc)
        self.rb_RejectPT.setObjectName(u"rb_RejectPT")
        self.rb_RejectPT.setMinimumSize(QSize(70, 20))
        self.rb_RejectPT.setMaximumSize(QSize(70, 20))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.rb_RejectPT.setFont(font2)
        self.rb_RejectPT.setChecked(True)

        self.verticalLayout_2.addWidget(self.rb_RejectPT)

        self.rb_AcceptPT = QRadioButton(self.gb_PT_Rej_Acc)
        self.rb_AcceptPT.setObjectName(u"rb_AcceptPT")
        self.rb_AcceptPT.setMinimumSize(QSize(70, 20))
        self.rb_AcceptPT.setMaximumSize(QSize(70, 20))
        self.rb_AcceptPT.setFont(font2)

        self.verticalLayout_2.addWidget(self.rb_AcceptPT)


        self.Layout0.addWidget(self.gb_PT_Rej_Acc)

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
        self.b_EditMode.setText(QCoreApplication.translate("PVIEW", u"Pt/P", None))
        self.gb_PT_Rej_Acc.setTitle("")
        self.rb_RejectPT.setText(QCoreApplication.translate("PVIEW", u"Reject", None))
        self.rb_AcceptPT.setText(QCoreApplication.translate("PVIEW", u"Accept", None))
        self.ch_Center.setText(QCoreApplication.translate("PVIEW", u"Follow", None))
        self.ch_ShowPT.setText(QCoreApplication.translate("PVIEW", u"Show PT", None))
    # retranslateUi

