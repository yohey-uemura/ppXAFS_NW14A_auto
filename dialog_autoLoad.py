# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_autoLoad.ui',
# licensing of 'dialog_autoLoad.ui' applies.
#
# Created: Sat Mar 20 23:15:00 2021
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(843, 322)
        self.pB_cp_from = QtWidgets.QPushButton(Dialog)
        self.pB_cp_from.setGeometry(QtCore.QRect(40, 65, 121, 41))
        self.pB_cp_from.setObjectName("pB_cp_from")
        self.tB_DatDir = QtWidgets.QTextBrowser(Dialog)
        self.tB_DatDir.setGeometry(QtCore.QRect(180, 65, 581, 41))
        self.tB_DatDir.setObjectName("tB_DatDir")
        self.tB_cp_direction = QtWidgets.QTextBrowser(Dialog)
        self.tB_cp_direction.setGeometry(QtCore.QRect(180, 120, 581, 41))
        self.tB_cp_direction.setObjectName("tB_cp_direction")
        self.pB_cp_direction = QtWidgets.QPushButton(Dialog)
        self.pB_cp_direction.setGeometry(QtCore.QRect(40, 121, 121, 41))
        self.pB_cp_direction.setObjectName("pB_cp_direction")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(650, 195, 111, 27))
        self.spinBox.setMaximum(1800)
        self.spinBox.setProperty("value", 1200)
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(570, 200, 71, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pB_exec = QtWidgets.QPushButton(Dialog)
        self.pB_exec.setGeometry(QtCore.QRect(50, 250, 121, 41))
        self.pB_exec.setAutoDefault(True)
        self.pB_exec.setObjectName("pB_exec")
        self.pB_close = QtWidgets.QPushButton(Dialog)
        self.pB_close.setGeometry(QtCore.QRect(650, 250, 121, 41))
        self.pB_close.setObjectName("pB_close")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(200, 258, 431, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 200, 51, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(200, 195, 113, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(420, 195, 113, 27))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(350, 200, 61, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(470, 20, 291, 35))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(40, 10, 71, 18))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(150, 10, 97, 18))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.pB_cp_from.setText(QtWidgets.QApplication.translate("Dialog", "Open Data Dir.", None, -1))
        self.pB_cp_direction.setText(QtWidgets.QApplication.translate("Dialog", "Copy Direction", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Wait for [s]", None, -1))
        self.pB_exec.setText(QtWidgets.QApplication.translate("Dialog", "exec auto Load", None, -1))
        self.pB_close.setText(QtWidgets.QApplication.translate("Dialog", "close", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "header:", None, -1))
        self.lineEdit.setToolTip(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p>write a common part of data files (ex. a_001_0001.dat, a_001_0002.dat, =&gt; \'ax\')</p></body></html>", None, -1))
        self.lineEdit_2.setToolTip(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p>write a common extention (ex. a_001_0001.dat, a_001_0002.dat, =&gt; \'dat\')</p></body></html>", None, -1))
        self.lineEdit_2.setText(QtWidgets.QApplication.translate("Dialog", "dat", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "extention:", None, -1))
        self.radioButton.setText(QtWidgets.QApplication.translate("Dialog", "XANES", None, -1))
        self.radioButton_2.setText(QtWidgets.QApplication.translate("Dialog", "Time Scan", None, -1))

