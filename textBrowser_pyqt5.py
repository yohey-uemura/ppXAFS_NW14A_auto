# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'textBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(670, 646)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(50, 150, 571, 421))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(280, 591, 110, 41))
        self.pushButton.setObjectName("pushButton")
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setGeometry(QtCore.QRect(470, 30, 121, 24))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(9999)
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(380, 33, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_2.setGeometry(QtCore.QRect(150, 60, 471, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(190, 110, 431, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 115, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.spinBox, self.textBrowser_2)
        Form.setTabOrder(self.textBrowser_2, self.lineEdit)
        Form.setTabOrder(self.lineEdit, self.textBrowser)
        Form.setTabOrder(self.textBrowser, self.pushButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "OK"))
        self.label.setText(_translate("Form", "Read from:"))
        self.label_2.setText(_translate("Form", "File Name:"))
        self.lineEdit.setText(_translate("Form", "k, chi_pos, chi_neg"))
        self.label_3.setText(_translate("Form", "Columns:"))

