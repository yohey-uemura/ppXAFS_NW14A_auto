# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_ppXAFS_win.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1201, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1181, 641))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(940, 10, 181, 41))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab)
        self.pushButton_12.setGeometry(QtCore.QRect(1040, 500, 121, 41))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab)
        self.pushButton_9.setGeometry(QtCore.QRect(910, 560, 251, 41))
        self.pushButton_9.setObjectName("pushButton_9")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(910, 60, 241, 421))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 239, 419))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.widget_3 = QtWidgets.QWidget(self.tab)
        self.widget_3.setGeometry(QtCore.QRect(20, 29, 851, 571))
        self.widget_3.setObjectName("widget_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(910, 500, 121, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.widget = QtWidgets.QWidget(self.tab_2)
        self.widget.setGeometry(QtCore.QRect(20, 10, 441, 401))
        self.widget.setObjectName("widget")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(910, 560, 111, 32))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(1040, 0, 111, 32))
        self.pushButton.setObjectName("pushButton")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setGeometry(QtCore.QRect(910, 40, 251, 511))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 249, 509))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 460, 451, 71))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setGeometry(QtCore.QRect(290, 30, 131, 25))
        self.spinBox_2.setProperty("value", 10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(230, 34, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 34, 51, 16))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(70, 30, 131, 25))
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 530, 451, 71))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.spinBox_4 = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_4.setGeometry(QtCore.QRect(290, 30, 131, 25))
        self.spinBox_4.setProperty("value", 10)
        self.spinBox_4.setObjectName("spinBox_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(230, 34, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 34, 51, 16))
        self.label_4.setObjectName("label_4")
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_3.setGeometry(QtCore.QRect(70, 30, 131, 25))
        self.spinBox_3.setProperty("value", 5)
        self.spinBox_3.setObjectName("spinBox_3")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_11.setGeometry(QtCore.QRect(1050, 560, 111, 32))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_13.setGeometry(QtCore.QRect(370, 420, 111, 32))
        self.pushButton_13.setObjectName("pushButton_13")
        self.widget_I0 = QtWidgets.QWidget(self.tab_2)
        self.widget_I0.setGeometry(QtCore.QRect(510, 20, 371, 181))
        self.widget_I0.setObjectName("widget_I0")
        self.widget_I1 = QtWidgets.QWidget(self.tab_2)
        self.widget_I1.setGeometry(QtCore.QRect(510, 220, 371, 181))
        self.widget_I1.setObjectName("widget_I1")
        self.widget_I2 = QtWidgets.QWidget(self.tab_2)
        self.widget_I2.setGeometry(QtCore.QRect(510, 420, 371, 181))
        self.widget_I2.setObjectName("widget_I2")
        self.pushButton_14 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_14.setGeometry(QtCore.QRect(20, 420, 111, 32))
        self.pushButton_14.setObjectName("pushButton_14")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1201, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_7.setText(_translate("MainWindow", "Open"))
        self.pushButton_12.setText(_translate("MainWindow", "Check"))
        self.pushButton_9.setText(_translate("MainWindow", "Save Sum"))
        self.pushButton_2.setText(_translate("MainWindow", "Select/Release All"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "TimeScan"))
        self.pushButton_10.setText(_translate("MainWindow", "Select All"))
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.groupBox.setTitle(_translate("MainWindow", "Lower"))
        self.label_2.setText(_translate("MainWindow", "End"))
        self.label.setText(_translate("MainWindow", "Start:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Upper"))
        self.label_3.setText(_translate("MainWindow", "End"))
        self.label_4.setText(_translate("MainWindow", "Start"))
        self.pushButton_11.setText(_translate("MainWindow", "Caclulate"))
        self.pushButton_13.setText(_translate("MainWindow", "Save"))
        self.pushButton_14.setText(_translate("MainWindow", "Caclulate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "XANES"))
