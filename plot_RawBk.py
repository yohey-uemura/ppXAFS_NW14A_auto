# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_RawBk.ui',
# licensing of 'plot_RawBk.ui' applies.
#
# Created: Sat Mar 20 23:14:24 2021
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(754, 724)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 30, 671, 501))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(560, 630, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(50, 570, 211, 111))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.dsb_pos_bk_start = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.dsb_pos_bk_start.setGeometry(QtCore.QRect(60, 30, 141, 27))
        self.dsb_pos_bk_start.setObjectName("dsb_pos_bk_start")
        self.dsb_pos_bk_end = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.dsb_pos_bk_end.setGeometry(QtCore.QRect(60, 70, 141, 27))
        self.dsb_pos_bk_end.setObjectName("dsb_pos_bk_end")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 35, 41, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 75, 41, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(320, 570, 211, 111))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.dsb_neg_bk_start = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.dsb_neg_bk_start.setGeometry(QtCore.QRect(60, 30, 141, 27))
        self.dsb_neg_bk_start.setObjectName("dsb_neg_bk_start")
        self.dsb_neg_bk_end = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.dsb_neg_bk_end.setGeometry(QtCore.QRect(60, 70, 141, 27))
        self.dsb_neg_bk_end.setObjectName("dsb_neg_bk_end")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 35, 41, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 75, 41, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "close", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Pos: background", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "start:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "end:", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Dialog", "Neg: background", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "start:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "end:", None, -1))

