# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_RawBk_win.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(754, 724)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 30, 671, 501))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(560, 635, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(40, 570, 241, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.dsb_pos_bk_start = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.dsb_pos_bk_start.setGeometry(QtCore.QRect(80, 30, 141, 27))
        self.dsb_pos_bk_start.setObjectName("dsb_pos_bk_start")
        self.dsb_pos_bk_end = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.dsb_pos_bk_end.setGeometry(QtCore.QRect(80, 70, 141, 27))
        self.dsb_pos_bk_end.setObjectName("dsb_pos_bk_end")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 35, 61, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 75, 51, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 570, 241, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.dsb_neg_bk_start = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.dsb_neg_bk_start.setGeometry(QtCore.QRect(80, 30, 141, 27))
        self.dsb_neg_bk_start.setObjectName("dsb_neg_bk_start")
        self.dsb_neg_bk_end = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.dsb_neg_bk_end.setGeometry(QtCore.QRect(80, 70, 141, 27))
        self.dsb_neg_bk_end.setObjectName("dsb_neg_bk_end")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 35, 61, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 75, 51, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "close"))
        self.groupBox.setTitle(_translate("Dialog", "Pos: background"))
        self.label.setText(_translate("Dialog", "start:"))
        self.label_2.setText(_translate("Dialog", "end:"))
        self.groupBox_2.setTitle(_translate("Dialog", "Neg: background"))
        self.label_3.setText(_translate("Dialog", "start:"))
        self.label_4.setText(_translate("Dialog", "end:"))

