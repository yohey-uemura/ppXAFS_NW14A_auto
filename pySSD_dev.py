import sys
import os
import string
import glob
import re
import yaml
import math
import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'

#import matplotlib.pyplot
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import numpy.linalg as linalg
import scipy.optimize as optim
import shutil
import pandas as pd
import use_larch

from PySide import QtCore, QtGui
if sys.platform =='win32':
    from UI_pySSD_win_2 import Ui_MainWindow
else:
    from UI_pySSD import Ui_MainWindow

from plot_dialog import Ui_Dialog

home_dir = QtCore.QDir()
text = home_dir.homePath()
cwd = os.getcwd()

#print shaping_t
list = ["no correction", "0.25 us", "0.50 us", "1.00 us", "2.00 us", "3.00 us", "6.00 us"]


class params:
    D = None
    ignore_or_not = []
    angles = []
    i0 = []
    ICR = []
    darray = np.empty([1, 1])
    Energy = []
    dat = []
    which_BL = "BL12C"
    len_eff = None
    sum = np.ndarray([0])
    dir = ""
    current_dfile = ""
    outdir = ""
    current_ofile = ""
    dfiles = []
    d_rbs = []
    dfiles_36XU = []
    d_rbs_36XU = []
    aq_time = []
    shaping_time = ""
    grid = QtGui.QGridLayout()
    grid2 = QtGui.QGridLayout()
    grid3 = QtGui.QGridLayout()
    grid4 = QtGui.QGridLayout()
    grid5 = QtGui.QGridLayout()
    grid6 = QtGui.QGridLayout()
    grid7 = QtGui.QGridLayout()
    grid_dialog = QtGui.QGridLayout()
    cbs = []
    ex3 = []
    E_intp = []
    path_to_ex3 = ""
    colors = ["Red", "Blue", "Green", "DeepPink", "Black", "Orange", "Brown","OrangeRed",
               "DarkRed","Crimson", "DarkBlue", "DarkGreen", "Hotpink","Coral",
              "DarkMagenta",  "FireBrick", "GoldenRod", "Grey",
              "Indigo", "MediumBlue", "MediumVioletRed"]
    rgb_color = ["#FF0000","#0000FF","#00CC00","#FF1493","#000000"]
    if sys.platform == 'win32':
        homedir = os.environ['HOMEPATH']
    else:
        homedir = os.environ['HOME']
    xanes =[]
    exafs = []

    path_to_xanes = ""
    path_to_exafs = ""
    data_length =""
    exafs_rb = QtGui.QButtonGroup()
    data_and_conditions = {}
    current_EXAFS = ''

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        self.u = Ui_MainWindow()
        self.u.setupUi(self)
        self.u.comboBox.addItems(list)
        self.u.comboBox_2.addItems(["K", "L"])
        self.u.comboBox_3.addItems(["K", "L"])
        self.u.comboBox_4.addItems(["PFBL9A", "PFBL12C", "PFNW10A", "SP8_01B1"])
        self.u.comboBox_5.addItems(["K", "L"])
        self.u.comboBox_6.addItems(["Transmission", "Fluorescence", "SSD_wCorrection"])
        self.u.rb_sum.toggle()
        scroll_layout = QtGui.QVBoxLayout()
        scroll_widgets = QtGui.QWidget()
        scroll_widgets.setLayout(scroll_layout)
        self.u.scrollArea.setWidget(scroll_widgets)
        params.cbs = [self.u.ch_1, self.u.ch_2, self.u.ch_3,
                      self.u.ch_4, self.u.ch_5, self.u.ch_6, self.u.ch_7,
                      self.u.ch_8, self.u.ch_9, self.u.ch_10, self.u.ch_11, self.u.ch_12,
                      self.u.ch_13, self.u.ch_14,self.u.ch_15, self.u.ch_16,
                      self.u.ch_17, self.u.ch_18, self.u.ch_19]
        scroll_layout2 = QtGui.QVBoxLayout()
        scroll_widgets2 = QtGui.QWidget()
        scroll_widgets2.setLayout(scroll_layout2)
        self.u.scrollArea_2.setWidget(scroll_widgets2)
        self.u.pushButton_8.setEnabled(False)
        params.rb_REX = [self.u.radioButton, self.u.radioButton_3, self.u.radioButton_5]
        self.u.comboBox_bk.addItems(['average','linear','victoreen'])
        self.dialog = QtGui.QDialog()
        self.plot_dialog = Ui_Dialog()
        self.plot_dialog.setupUi(self.dialog)
        self.plot_dialog.comboBox_Ftype.addItems(['average','linear','victoreen'])

        def toggle_rbs_REX():
            for rb in params.rb_REX:
                rb.toggle()

        for rb in params.rb_REX:
            rb.setObjectName(".ex3")
            rb.toggle()
            rb.clicked.connect(toggle_rbs_REX)
        params.rb_Athena = [self.u.radioButton_2, self.u.radioButton_4, self.u.radioButton_6]

        def toggle_rbs_ATHENA():
            for rb in params.rb_Athena:
                rb.toggle()

        for rb in params.rb_Athena:
            rb.setObjectName(".dat")
            rb.clicked.connect(toggle_rbs_ATHENA)

        scroll_layout3 = QtGui.QVBoxLayout()
        scroll_widgets3 = QtGui.QWidget()
        scroll_widgets3.setLayout(scroll_layout3)
        self.u.scrollArea_3.setWidget(scroll_widgets3)

        scroll_layout4 = QtGui.QVBoxLayout()
        scroll_widgets4 = QtGui.QWidget()
        scroll_widgets4.setLayout(scroll_layout4)
        self.u.scrollArea_4.setWidget(scroll_widgets4)

        for cb in params.cbs:
            cb.setAutoFillBackground(True)
            plt = cb.palette()
            if params.cbs.index(cb) >= 0 and params.cbs.index(cb) <=2:
                plt.setColor(cb.backgroundRole(), params.rgb_color[0])
            elif params.cbs.index(cb) >= 3 and params.cbs.index(cb) <=6:
                plt.setColor(cb.backgroundRole(), params.rgb_color[1])
            elif params.cbs.index(cb) >= 7 and params.cbs.index(cb) <=11:
                plt.setColor(cb.backgroundRole(), params.rgb_color[2])
            elif params.cbs.index(cb) >= 12 and params.cbs.index(cb) <=15:
                plt.setColor(cb.backgroundRole(), params.rgb_color[3])
            elif params.cbs.index(cb) >= 16 and params.cbs.index(cb) <=18:
                plt.setColor(cb.backgroundRole(), params.rgb_color[4])
            plt.setColor(cb.foregroundRole(), "#FFFFFF")
            cb.setPalette(plt)
        palette = self.u.frame.palette()
        palette.setColor(cb.foregroundRole(), "Grey")


        #Figure for Transmission & Fluorescence
        fig4 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax4 = fig4.add_subplot(111)
        ax4.set_xlabel("E / eV")
        ax4.set_ylabel("$\mu$ t")
        canvas4 = FigureCanvas(fig4)
        navibar_4 = NavigationToolbar(canvas4, self.u.widget_4)
        self.u.widget_4.setLayout(params.grid4)
        params.grid4.addWidget(canvas4, 0, 0)
        params.grid4.addWidget(navibar_4)

        #Figure for SSD (left)
        fig = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)
        ax.set_xlabel("E / eV")
        ax.set_ylabel("$\mu$ t")
        canvas = FigureCanvas(fig)
        self.u.widget.setLayout(params.grid)
        navibar_1 = NavigationToolbar(canvas, self.u.widget)
        params.grid.addWidget(canvas, 0, 0)
        params.grid.addWidget(navibar_1)

        #Figure for SSD (right)
        fig2 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax2 = fig2.add_subplot(111)
        ax2.set_xlabel("E / eV")
        ax2.set_ylabel("$\mu$ t")
        canvas2 = FigureCanvas(fig2)
        self.u.widget_2.setLayout(params.grid2)
        navibar_2 = NavigationToolbar(canvas2, self.u.widget_2)
        self.u.widget_2.setLayout(params.grid2)
        params.grid2.addWidget(canvas2, 0, 0)
        params.grid2.addWidget(navibar_2)


        #Figure for XANES Compare
        self.fig5 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax5 = self.fig5.add_subplot(111)
        self.ax5.set_xlabel("E / eV")
        self.ax5.set_ylabel("$\mu$ t")
        self.canvas5 = FigureCanvas(self.fig5)
        self.navibar_5 = NavigationToolbar(self.canvas5, self.u.widget_5)
        self.u.widget_5.setLayout(params.grid5)
        params.grid5.addWidget(self.canvas5, 0, 0)
        params.grid5.addWidget(self.navibar_5)

        #Figure for XANES plot (dialog)
        self.fig_dialog = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_dialog = self.fig_dialog.add_subplot(121)
        self.ax_dialog.set_xlabel("E / eV")
        self.ax_dialog.set_ylabel("$\mu$ t")
        self.ax_dialog_norm = self.fig_dialog.add_subplot(122)
        self.ax_dialog_norm.set_xlabel("E / eV")
        self.ax_dialog_norm.set_ylabel("$\mu$ t")
        self.canvas_dialog = FigureCanvas(self.fig_dialog)
        self.navibar_dialog = NavigationToolbar(self.canvas_dialog, self.plot_dialog.widget)
        self.plot_dialog.widget.setLayout(params.grid_dialog)
        params.grid_dialog.addWidget(self.canvas_dialog, 0, 0)
        params.grid_dialog.addWidget(self.navibar_dialog)

        #Figure for interpolation and summation
        fig3 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax3 = fig3.add_subplot(111)
        ax3.set_xlabel("E / eV")
        ax3.set_ylabel("$\mu$ t")
        canvas3 = FigureCanvas(fig3)
        navibar_3 = NavigationToolbar(canvas3, self.u.widget_3)
        self.u.widget_3.setLayout(params.grid3)
        params.grid3.addWidget(canvas3, 0, 0)
        params.grid3.addWidget(navibar_3)

        def change_CB3():
            self.u.comboBox_3.setCurrentIndex(self.u.comboBox_2.currentIndex())

        def change_lineEdit2():
            self.u.lineEdit_2.clear()
            self.u.lineEdit_2.setText(self.u.lineEdit.text())

        def define_outdir():
            self.u.textBrowser.clear()
            FO_dialog = QtGui.QFileDialog(self)
            params.outdir = FO_dialog.getExistingDirectory(parent=None, dir=params.dir)
            self.u.textBrowser.append(params.outdir)
            if self.u.textBrowser_2.toPlainText() == "":
                self.u.textBrowser_2.append(params.outdir)

        def define_outdir_for_sum():
            self.u.textBrowser_2.clear()
            FO_dialog = QtGui.QFileDialog(self)
            directory = ""
            if params.outdir == "":
                directory = params.outdir
            else:
                directory = home_dir
            params.outdir = FO_dialog.getExistingDirectory(parent=None, dir=directory)
            self.u.textBrowser_2.append(params.outdir)

        def read_dat(Test_Dat):
            params.ignore_or_not = []
            params.angles = []
            params.aq_time = []
            params.i0 = []
            params.dat = []
            params.ICR = []
            params.Energy = []
            params.darray = np.empty([1, 1])
            f = open(Test_Dat, "r")
            i = 0
            for line in f:
                line.rstrip()
                if re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line):
                    if re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "BL9A":
                        self.u.comboBox_4.setCurrentIndex(0)
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "BL12C":
                        self.u.comboBox_4.setCurrentIndex(1)
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "NW10A":
                        self.u.comboBox_4.setCurrentIndex(2)
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "01b1":
                        self.u.comboBox_4.setCurrentIndex(3)
                elif re.match(r".+D=(.+)A.+", line):
                    params.D = float(re.match(r".+D=\s+(.+)\sA.+", line).group(1))
                #print str(params.D)
                elif re.match(r"\s+Angle\(c\).+", line):
                    t_array = line.split()
                #print t_array[0]
                elif re.match(r"\s+Mode", line):
                    t_array = line.split()
                    params.ignore_or_not = t_array[3:23]
                #print params.ignore_or_not
                elif re.match(r"\s+Offset", line):
                    pass
                elif len(line.split()) > 23:
                    t_array = line.split()
                    params.angles.append(t_array[1])
                    params.aq_time.append(float(t_array[2]))
                    params.i0.append(float(t_array[22]))
                    params.dat.append(t_array[3:23])
                    params.ICR.append(t_array[23:])
                #print i
                i += 1
            print params.aq_time
            k = 0
            while k < 19:
                if params.ignore_or_not[k] == "0":
                    params.cbs[k].setCheckState(QtCore.Qt.CheckState.Unchecked)
                    params.cbs[k].setEnabled(False)
                elif params.ignore_or_not[k] != "0":
                    if self.u.cB_keep_condition.isChecked():
                        pass
                    else:
                        params.cbs[k].setCheckState(QtCore.Qt.CheckState.Checked)
                k += 1
            params.darray.resize(19, len(params.dat))
            k = 0
            while k < 19:
                j = 0
                while j < len(params.dat):
                    params.darray[k][j] = float(params.dat[j][k])
                    j += 1
                k += 1
            #print params.darray[1]
            j = 0
            while j < len(params.dat):
                E = 12398.52 / (2 * float(params.D) * np.sin(float(params.angles[j]) / 180 * np.pi))
                params.Energy.append(E)
                j += 1

        def plot_each_ch():
            conf = cwd + "/" + self.u.comboBox_4.currentText() + ".conf"
            str_tconst = open(conf).read()
            DT = yaml.load(str_tconst)
            sum = np.zeros(len(params.Energy))
            params.grid.removeItem(params.grid.itemAt(0))
            params.grid.removeItem(params.grid.itemAt(0))
            fig = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            ax = fig.add_subplot(111)
            ax.set_xlabel("E / eV")
            ax.set_ylabel("$\mu$ t")
            canvas = FigureCanvas(fig)
            navibar_1 = NavigationToolbar(canvas, self.u.widget)

            params.grid2.removeItem(params.grid2.itemAt(0))
            params.grid2.removeItem(params.grid2.itemAt(0))
            fig2 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            ax2 = fig2.add_subplot(111)
            ax2.set_xlabel("E / eV")
            ax2.set_ylabel("$\mu$ t")
            canvas2 = FigureCanvas(fig2)
            navibar_2 = NavigationToolbar(canvas2, self.u.widget_2)
            if self.u.comboBox.currentText() == "no correction":
                for cb in params.cbs:
                    if cb.isChecked():
                        ut = np.divide(np.array(params.darray[params.cbs.index(cb)]), np.array(params.i0))
                        sum = np.add(sum, np.array(params.darray[params.cbs.index(cb)]))
                        if params.cbs.index(cb) >= 0 and params.cbs.index(cb) <=2:
                            ax.plot(params.Energy, ut, color=params.colors[0])
                        elif params.cbs.index(cb) >= 3 and params.cbs.index(cb) <=6:
                            ax.plot(params.Energy, ut, color=params.colors[1])
                        elif params.cbs.index(cb) >= 7 and params.cbs.index(cb) <=11:
                            ax.plot(params.Energy, ut, color=params.colors[2])
                        elif params.cbs.index(cb) >= 12 and params.cbs.index(cb) <=15:
                            ax.plot(params.Energy, ut, color=params.colors[3])
                        elif params.cbs.index(cb) >= 16 and params.cbs.index(cb) <=18:
                            ax.plot(params.Energy, ut, color=params.colors[4])
                        #ax.plot(params.Energy, ut, color=params.colors[params.cbs.index(cb)])
            elif self.u.comboBox.currentText() != "no correction":
                if self.u.comboBox.currentText() == "0.25 us":
                    params.shaping_time = "us025"
                elif self.u.comboBox.currentText() == "0.50 us":
                    params.shaping_time = "us050"
                elif self.u.comboBox.currentText() == "1.00 us":
                    params.shaping_time = "us100"
                elif self.u.comboBox.currentText() == "2.00 us":
                    params.shaping_time = "us200"
                elif self.u.comboBox.currentText() == "3.00 us":
                    params.shaping_time = "us300"
                elif self.u.comboBox.currentText() == "6.00 us":
                    params.shaping_time = "us600"
                micro = math.pow(10, -6)
                k = 0
                while k < 19:
                    if params.cbs[k].isChecked():
                        j = 0
                        ut = np.zeros(len(params.Energy))
                        while j < len(params.Energy):
                            ut[j] = params.darray[k][j] * (
                                1 + micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                    DT["PF"]["individual"]["preamp"][k])) / (
                                        1 - micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                            DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #ut[j] = params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[j])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                            sum[j] += params.darray[k][j] * (
                                1 + micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                    DT["PF"]["individual"]["preamp"][k])) / (
                                          1 - micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                              DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #sum[j] += params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[j])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                            j += 1
                        if k >= 0 and k <=2:
                            ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[0])
                        elif k >= 3 and k <=6:
                            ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[1])
                        elif k >= 7 and k <=11:
                            ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[2])
                        elif k >= 12 and k <=15:
                            ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[3])
                        elif k >= 16 and k <=18:
                            ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[4])
                        #ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[k])
                    k += 1
            params.grid.addWidget(canvas, 0, 0)
            params.grid.addWidget(navibar_1)
            ax2.plot(params.Energy, np.divide(sum, params.i0))
            params.grid2.addWidget(canvas2, 0, 0)
            params.grid2.addWidget(navibar_2)

        def select_or_release_all():
            checked_cb = []
            for cb in params.cbs:
                if cb.isChecked():
                    checked_cb.append(cb)
            if len(checked_cb) > 0:
                self.u.pushButton_5.setText("Select All")
                for cb in checked_cb:
                    cb.setCheckState(QtCore.Qt.CheckState.Unchecked)
            elif len(checked_cb) == 0:
                self.u.pushButton_5.setText("Release All")
                k = 0
                while k < 19:
                    if params.ignore_or_not[k] != "0":
                        params.cbs[k].setCheckState(QtCore.Qt.CheckState.Checked)
                    elif params.ignore_or_not[k] == "0":
                        params.cbs[k].setEnabled(False)
                    k += 1
            plot_each_ch()

        def plot_():
            params.current_dfile = ""
            params.current_ofile = ""
            if self.u.cB_keep_condition.isChecked():
                for cb in params.cbs:
                    cb.setEnabled(True)
            else:
                for cb in params.cbs:
                    cb.setEnabled(True)
                    cb.setCheckState(QtCore.Qt.CheckState.Unchecked)
            for t_rb in params.d_rbs:
                if t_rb.isChecked():
                    params.current_dfile = params.dir + "/" + t_rb.objectName()
                    if re.match(r"(.+)\.\d+", t_rb.objectName()) is None:
                        #params.current_ofile = o_dir + "/" + t_rb.objectName() + "_000" + ".ex3"
                        break
                    elif re.match(r"(.+)\.(\d+)", t_rb.objectName()):
                        t_line = t_rb.objectName().split(".")
                        #params.current_ofile =o_dir + "/" + t_line[0] + "_" + t_line[1]  + ".ex3"
                        break
            read_dat(params.current_dfile)
            plot_each_ch()

        def func_for_rb():
            plot_()
            self.u.pushButton_5.setText("Release all")

        def openFiles():
            print "here"
            while scroll_layout.count() > 0:
                b = scroll_layout.takeAt(len(params.d_rbs) - 1)
                params.dfiles.pop()
                params.d_rbs.pop()
                b.widget().deleteLater()
            self.u.cB_keep_condition.setCheckState(QtCore.Qt.CheckState.Unchecked)
            dat_dir = home_dir.homePath()
            if params.dir == "":
                dat_dir = home_dir.homePath()
            elif params.dir != "":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir)
            finfo = QtCore.QFileInfo(files[0][0])
            params.dir = finfo.path()
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                params.dfiles.append(info.fileName())
            for d_file in params.dfiles:
                rb = QtGui.QRadioButton(d_file)
                rb.setObjectName(d_file)
                params.d_rbs.append(rb)
                scroll_layout.addWidget(rb)
            for t_rb in params.d_rbs:
                t_rb.clicked.connect(func_for_rb)

        def Save():
            conf = cwd + "/" + self.u.comboBox_4.currentText() + ".conf"
            str_tconst = open(conf).read()
            DT = yaml.load(str_tconst)
            sum = np.zeros(len(params.Energy))
            ut = np.zeros(len(params.Energy))
            o_dir = params.dir
            exd = ""
            if self.u.radioButton.isChecked():
                exd = self.u.radioButton.objectName()
            else:
                exd = self.u.radioButton_2.objectName()
            if params.outdir == "":
                o_dir = params.dir
            elif os.path.exists(params.outdir):
                o_dir = params.outdir
            for t_rb in params.d_rbs:
                if t_rb.isChecked():
                    if re.match(r"(.+)\.\d+", t_rb.objectName()) is None:
                        params.current_ofile = o_dir + "/" + t_rb.objectName() + "_000" + exd
                        break
                    elif re.match(r"(.+)\.(\d+)", t_rb.objectName()):
                        t_line = t_rb.objectName().split(".")
                        params.current_ofile = o_dir + "/" + t_line[0] + "_" + t_line[1] + exd
                        break
            out = open(params.current_ofile, "w")
            if self.u.radioButton.isChecked():
                line = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                atom = "*EX_ATOM=" + self.u.lineEdit.text() + "\n"
                edge = "*EX_EDGE=" + self.u.comboBox_2.currentText() + "\n"
                line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                line3 = "\n[EX_BEGIN]\n"
                out.write(line + atom + edge + line2 + line3)
            else:
                out.write("#Energy  ut\n")
            if self.u.comboBox.currentText() == "no correction":
                for cb in params.cbs:
                    if cb.isChecked():
                        sum = np.add(sum, np.array(params.darray[params.cbs.index(cb)]))
            elif self.u.comboBox.currentText() != "no correction":
                if self.u.comboBox.currentText() == "25 us":
                    params.shaping_time = "us025"
                elif self.u.comboBox.currentText() == "50 us":
                    params.shaping_time = "us050"
                elif self.u.comboBox.currentText() == "100 us":
                    params.shaping_time = "us100"
                elif self.u.comboBox.currentText() == "200 us":
                    params.shaping_time = "us200"
                elif self.u.comboBox.currentText() == "300 us":
                    params.shaping_time = "us300"
                elif self.u.comboBox.currentText() == "600 us":
                    params.shaping_time = "us600"
                micro = math.pow(10, -6)
                k = 0
                while k < 19:
                    if params.cbs[k].isChecked():
                        j = 0
                        while j < len(params.Energy):
                            sum[j] += params.darray[k][j] * (
                                1 + micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                    DT["PF"]["individual"]["preamp"][k])) / (
                                          1 - micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                                              DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #sum[j] += params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[k])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                            j += 1
                    k += 1
            ut = np.divide(sum, params.i0)
            k = 0
            while k < len(params.Energy):
                str_ = "%7.3f  %1.8f\n" % (params.Energy[k], ut[k])
                out.write(str_)
                k += 1
            if self.u.radioButton.isChecked():
                out.write("\n[EX_END]\n")
            else:
                pass

        def read_SSD(fname):
            ignore_or_not = []
            angles = []
            aq_time = []
            i0 = []
            dat = []
            ICR = []
            Energy = []
            darray = np.empty([1, 1])
            D = 0.0
            BL = 0.0
            f = open(fname, "r")
            #angles, aq_time, i0, dat, ICR, Energy, darray, D, BL
            i = 0
            for line in f:
                line.rstrip()
                if re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line):
                    if re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "BL9A":
                        BL="BL9A"
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "BL12C":
                        BL="BL12C"
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "NW10A":
                        BL="NW10A"
                    elif re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(2) == "01b1":
                        BL="01b1"
                elif re.match(r".+D=(.+)A.+", line):
                    D = float(re.match(r".+D=\s+(.+)\sA.+", line).group(1))
                #print str(params.D)
                elif re.match(r"\s+Angle\(c\).+", line):
                    t_array = line.split()
                #print t_array[0]
                elif re.match(r"\s+Mode", line):
                    t_array = line.split()
                    ignore_or_not = t_array[3:23]
                #print params.ignore_or_not
                elif re.match(r"\s+Offset", line):
                    pass
                elif len(line.split()) > 23:
                    t_array = line.split()
                    angles.append(t_array[1])
                    aq_time.append(float(t_array[2]))
                    i0.append(float(t_array[22]))
                    dat.append(t_array[3:23])
                    ICR.append(t_array[23:])
                #print i
                i += 1
            darray.resize(19, len(dat))
            k = 0
            while k < 19:
                j = 0
                while j < len(dat):
                    darray[k][j] = float(dat[j][k])
                    j += 1
                k += 1
            j = 0
            while j < len(dat):
                E = 12398.52 / (2 * float(D) * np.sin(float(angles[j]) / 180 * np.pi))
                Energy.append(E)
                j += 1
            return np.array(Energy), np.array(aq_time), np.array(i0), np.array(ICR),  np.array(darray), BL

        def Save_all_as_Current():
            conf = cwd + "/" + self.u.comboBox_4.currentText() + ".conf"
            str_tconst = open(conf).read()
            DT = yaml.load(str_tconst)
            sum = np.zeros(len(params.Energy))
            ut = np.zeros(len(params.Energy))
            o_dir = params.dir
            exd = ""
            current_ofile = ""
            if self.u.radioButton.isChecked():
                exd = self.u.radioButton.objectName()
            else:
                exd = self.u.radioButton_2.objectName()
            if params.outdir == "":
                o_dir = params.dir
            elif os.path.exists(params.outdir):
                o_dir = params.outdir
            for t_rb in params.d_rbs:
                Energy, aq_time, i0, ICR, darray, BL = read_SSD(params.dir + "/"+t_rb.objectName())
                if re.match(r"(.+)\.\d+", t_rb.objectName()) is None:
                    current_ofile = o_dir + "/" + t_rb.objectName() + "_000" + exd
                elif re.match(r"(.+)\.(\d+)", t_rb.objectName()):
                    t_line = t_rb.objectName().split(".")
                    current_ofile = o_dir + "/" + t_line[0] + "_" + t_line[1] + exd
                out = open(current_ofile, "w")
                if self.u.radioButton.isChecked():
                    line = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                    atom = "*EX_ATOM=" + self.u.lineEdit.text() + "\n"
                    edge = "*EX_EDGE=" + self.u.comboBox_2.currentText() + "\n"
                    line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                    line3 = "\n[EX_BEGIN]\n"
                    out.write(line + atom + edge + line2 + line3)
                else:
                    out.write("#Energy  ut\n")
                if self.u.comboBox.currentText() == "no correction":
                    for cb in params.cbs:
                        if cb.isChecked():
                            sum = np.add(sum, np.array(darray[params.cbs.index(cb)]))
                elif self.u.comboBox.currentText() != "no correction":
                    if self.u.comboBox.currentText() == "25 us":
                        params.shaping_time = "us025"
                    elif self.u.comboBox.currentText() == "50 us":
                        params.shaping_time = "us050"
                    elif self.u.comboBox.currentText() == "100 us":
                        params.shaping_time = "us100"
                    elif self.u.comboBox.currentText() == "200 us":
                        params.shaping_time = "us200"
                    elif self.u.comboBox.currentText() == "300 us":
                        params.shaping_time = "us300"
                    elif self.u.comboBox.currentText() == "600 us":
                        params.shaping_time = "us600"
                    micro = math.pow(10, -6)
                    k = 0
                    while k < 19:
                        if params.cbs[k].isChecked():
                            j = 0
                            while j < len(params.Energy):
                                sum[j] += darray[k][j] * (
                                    1 + micro * float(ICR[j][k]) / float(aq_time[j]) * float(
                                        DT["PF"]["individual"]["preamp"][k])) / (
                                            1 - micro * float(ICR[j][k]) / float(aq_time[j]) * float(
                                                DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #sum[j] += params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[k])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                                j += 1
                        k += 1
                ut = np.divide(sum, i0)
                k = 0
                while k < len(Energy):
                    str_ = "%7.3f  %1.8f\n" % (Energy[k], ut[k])
                    out.write(str_)
                    k += 1
                if self.u.radioButton.isChecked():
                    out.write("\n[EX_END]\n")
                else:
                    pass

        def func_pushButton_3():
            while scroll_layout2.count() > 0:
                b = scroll_layout2.takeAt(len(params.ex3) - 1)
                params.ex3.pop()
                b.widget().deleteLater()
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=params.outdir,
                                               filter="xas files(*.ex3 *.dat)")
            finfo = QtCore.QFileInfo(files[0][0])
            params.path_to_ex3 = finfo.path()
            j = 0
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                cb = QtGui.QCheckBox(info.fileName())
                cb.setObjectName(info.fileName())
                params.ex3.append(cb)
                cb.setCheckState(QtCore.Qt.Checked)
                scroll_layout2.addWidget(cb)
                j += 1
            if self.u.textBrowser_2.toPlainText() == "":
                self.u.textBrowser_2.append(finfo.path())
            click_pB4()

        def plot_in_tab2(E, ut):
            params.grid3.removeItem(params.grid3.itemAt(0))
            params.grid3.removeItem(params.grid3.itemAt(0))
            fig3 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            ax3 = fig3.add_subplot(111)
            ax3.set_xlabel("E / eV")
            ax3.set_ylabel("$\mu$ t")
            canvas3 = FigureCanvas(fig3)
            navibar_3 = NavigationToolbar(canvas3, self.u.widget_3)
            ax3.plot(E, ut)
            params.grid3.addWidget(canvas3, 0, 0)
            params.grid3.addWidget(navibar_3)

        def set_interpolation_file():
            self.u.textBrowser_4.clear()
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileName(parent=None, caption="", dir=params.outdir,
                                              filter="xas files(*.ex3 *.dat)")
            finfo = QtCore.QFileInfo(files[0])
            if os.path.exists(finfo.filePath()):
                self.u.textBrowser_4.append(finfo.filePath())
            click_pB4()

        def make_sum():
            if len(params.E_intp) != 0:
                params.E_intp = []
            fname = self.u.textBrowser_4.toPlainText()
            f_ex3 = open(fname, "r")
            for line in f_ex3:
                line.rstrip()
                if re.match(r"^\d+\.\d+\s+\-?\d+\.\d+", line):
                    t_array = line.split()
                    params.E_intp.append(float(t_array[0]))
            #print len(params.E_intp)
            params.sum = np.zeros(len(params.E_intp))
            params.int_checked = 0
            for cb in params.ex3:
                if cb.isChecked():
                    params.int_checked += 1
                    E_ = []
                    ut = []
                    fname = params.path_to_ex3 + "/" + cb.objectName()
                    f = open(fname, "r")
                    for line in f:
                        line.rstrip()
                        if re.match(r"^\d+\.\d+\s+\-?\d+\.\d+", line):
                            t_array = line.split()
                            E_.append(float(t_array[0]))
                            ut.append(float(t_array[1]))
                    ut_intp = np.interp(np.array(params.E_intp), np.array(E_), np.array(ut))
                    #print ut_intp
                    params.sum = np.add(params.sum, ut_intp)
            params.avg = params.sum / params.int_checked
            if self.u.rb_sum.isChecked():
                plot_in_tab2(np.array(params.E_intp), params.sum)
            elif self.u.rb_avg.isChecked():
                plot_in_tab2(np.array(params.E_intp), params.avg)
            self.u.pushButton_8.setEnabled(True)

        def Save_sum_and_avg():
            FO_dialog = QtGui.QFileDialog(self)
            outdir = ""
            exd = ""
            if self.u.radioButton_3.isChecked():
                exd = self.u.radioButton_3.objectName()
            else:
                exd = self.u.radioButton_4.objectName()
            if self.u.textBrowser_2.toPlainText() != "":
                outdir = self.u.textBrowser_2.toPlainText()
            else:
                outdir = home_dir.homePath()
            Ffilter = "xas file (*" + exd + ")"
            files = FO_dialog.getSaveFileName(parent=None, caption="Write a file name like \"******.***\"", dir=outdir,
                                              filter=Ffilter)
            print files
            finfo = QtCore.QFileInfo(files[0])
            arr_fname = finfo.fileName().split(".")
            fname = finfo.path() + "/" + arr_fname[0] + "_sum" + exd
            f_sum = open(fname, "w")
            if self.u.radioButton_3.isChecked():
                line1 = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                atom = "*EX_ATOM=" + self.u.lineEdit_2.text() + "\n"
                edge = "*EX_EDGE=" + self.u.comboBox_3.currentText() + "\n"
                line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                line3 = "\n[EX_BEGIN]\n"
                header_str = line1 + atom + edge + line2 + line3
                f_sum.write(header_str)
            else:
                f_sum.write("#Energy  ut\n")
            for energy in params.E_intp:
                str_ = "%7.3f  %1.8f\n" % (energy, params.sum[params.E_intp.index(energy)])
                f_sum.write(str_)
            if self.u.radioButton_3.isChecked():
                f_sum.write("\n[EX_END]\n")
            else:
                pass
            f_sum.close()

            fname = finfo.path() + "/" + arr_fname[0] + "_avg" + exd
            f_sum = open(fname, "w")
            if self.u.radioButton_3.isChecked():
                line1 = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                atom = "*EX_ATOM=" + self.u.lineEdit_2.text() + "\n"
                edge = "*EX_EDGE=" + self.u.comboBox_3.currentText() + "\n"
                line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                line3 = "\n[EX_BEGIN]\n"
                header_str = line1 + atom + edge + line2 + line3
                f_sum.write(header_str)
            else:
                f_sum.write("#Energy  ut\n")
            for energy in params.E_intp:
                str_ = "%7.3f  %1.8f\n" % (energy, params.avg[params.E_intp.index(energy)])
                f_sum.write(str_)
            if self.u.radioButton_3.isChecked():
                f_sum.write("\n[EX_END]\n")
            else:
                pass
            f_sum.close()
            self.u.pushButton_8.setEnabled(False)

        def plot_sum():
            if len(params.E_intp) != 0:
                plot_in_tab2(np.array(params.E_intp), params.sum)

        def plot_avg():
            if len(params.E_intp) != 0:
                plot_in_tab2(np.array(params.E_intp), params.avg)

        def change_CB4():
            if len(params.d_rbs) != 0:
                for t_rb in params.d_rbs:
                    if t_rb.isChecked():
                        plot_each_ch()
                        break
                    else:
                        pass

        def click_pB4():
            if len(params.ex3) != 0 and os.path.exists(self.u.textBrowser_4.toPlainText()):
                make_sum()

        # Functions for Transmissions and Fluorescense
        def define_outdir9809():
            self.u.textBrowser_3.clear()
            FO_dialog = QtGui.QFileDialog(self)
            dir_ = FO_dialog.getExistingDirectory(parent=None, dir=params.dir)
            self.u.textBrowser_3.append(dir_)

        def open_9809():
            while scroll_layout3.count() > 0:
                b = scroll_layout3.takeAt(len(params.cb9809) - 1)
                params.cb9809.pop()
                params.rb9809.pop()
                b.widget().deleteLater()
            params.dir9809 = ""
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=home_dir.homePath())
            finfo = QtCore.QFileInfo(files[0][0])
            params.dir9809 = finfo.path()
            if self.u.textBrowser_3.toPlainText() == "":
                self.u.textBrowser_3.append(params.dir9809)
            params.d9809 = []
            params.cb9809 = []
            params.rb9809 = []
            params.bg9809 = QtGui.QButtonGroup()
            j = 0
            for fname in files[0]:
                widget = QtGui.QWidget()
                hlayout = QtGui.QHBoxLayout()
                widget.setLayout(hlayout)
                info = QtCore.QFileInfo(fname)
                params.d9809.append(info.fileName())
                cb = QtGui.QCheckBox(info.fileName())
                cb.setObjectName(info.fileName())
                cb.setCheckState(QtCore.Qt.Checked)
                params.cb9809.append(cb)
                rb = QtGui.QRadioButton()
                rb.setObjectName(info.fileName())
                params.rb9809.append(rb)
                params.bg9809.addButton(rb, j)
                hlayout.addWidget(cb)
                hlayout.addWidget(rb)
                scroll_layout3.addWidget(widget)
                j += 1
            for rb in params.rb9809:
                rb.clicked.connect(plot_9809)

        def calc_ut(i0, i, mode):
            if mode == "Transmission":
                return math.log(i0 / i)
            elif mode == "Fluorescence":
                return i / i0

        def calc_ut_wcollection(i0, i, ICR, t_m, t1, t2):
            micro = math.pow(10, -6)
            return i * ((1 + ICR / t_m * micro * t1) / (1 - ICR / t_m * micro * t2)) / i0

        def convert_9809():
            line1 = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
            atom = "*EX_ATOM=" + self.u.lineEdit_3.text() + "\n"
            edge = "*EX_EDGE=" + self.u.comboBox_5.currentText() + "\n"
            line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
            line3 = "\n[EX_BEGIN]\n"
            line4 = "\n[EX_END]\n"
            exd = ""
            t1 = 0.0
            t2 = 0.0
            if self.u.comboBox_6.currentText() == "SSSD_wCorrection" and os.path.exists(
                            params.homedir + "/deadtime.txt"):
                print "deadtime collection"
                f_ = open(params.homedir + "/deadtime.txt")
                t_line = f_.readline().rstrip()
                [t1, t2] = [float(t_line.split(",")[0]), float(t_line.split(",")[1])]
            if self.u.radioButton_5.isChecked():
                exd = self.u.radioButton_5.objectName()
            else:
                exd = self.u.radioButton_6.objectName()
            if len(params.cb9809) != 0:
                for cb in params.cb9809:
                    f_in = ""
                    f_out = ""
                    D = ""
                    BL = ""
                    if cb.isChecked():
                        f_in = params.dir9809 + "/" + cb.objectName()
                        if re.match(r".+\.(\d+|[a-zA-Z]+)", cb.objectName()) is None:
                            f_out = self.u.textBrowser_3.toPlainText() + "/" + cb.objectName() + "_000" + exd
                        elif re.match(r".+\.\d+", cb.objectName()):
                            t_array = cb.objectName().split(".")
                            f_out = self.u.textBrowser_3.toPlainText() + "/" + t_array[0] + "_" + t_array[1] + exd
                        elif re.match(r".+\.[a-zA-Z]+", cb.objectName()):
                            t_array = cb.objectName().split(".")
                            f_out = self.u.textBrowser_3.toPlainText() + "/" + t_array[0] + exd
                        data = open(f_in, "r")
                        ut_out = open(f_out, "w")
                        if self.u.radioButton_5.isChecked():
                            ut_out.write(line1 + atom + edge + line2 + line3)
                        else:
                            ut_out.write("#Energy  ut\n")
                        for line in data:
                            line.rstrip()
                            if re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line):
                                BL = re.match(r"\s+9809\s+(KEK\-PF|SPring\-8)\s+(\w+)", line).group(1)
                                print BL
                            elif re.match(r".+D=(.+)A.+", line):
                                D = float(re.match(r".+D=\s+(.+)\sA.+", line).group(1))
                            elif re.match(r"^\s+\d+\.\d+.+", line):
                                str_ = ""
                                t_array = line.split()
                                Energy = 12398.52 / (2 * D * np.sin(float(t_array[1]) / 180 * np.pi))
                                if self.u.comboBox_6.currentText() == "SSSD_wCorrection":
                                    ut = calc_ut_wcollection(float(t_array[3]), float(t_array[4]), float(t_array[5]),
                                                             float(t_array[2]), t1, t2)
                                    str_ = "%7.3f  %1.8f\n" % (Energy, ut)
                                else:
                                    ut = calc_ut(float(t_array[3]), float(t_array[4]), self.u.comboBox_6.currentText())
                                    str_ = "%7.3f  %1.8f\n" % (Energy, ut)
                                ut_out.write(str_)
                        if self.u.radioButton_5.isChecked():
                            ut_out.write(line4)
                        else:
                            pass
                        #ax4.plot(np.array(Energy),np.array(ut))
                        #params.grid4.addWidget(canvas4,0,0)

        def plot_9809():
            params.grid4.removeItem(params.grid4.itemAt(0))
            params.grid4.removeItem(params.grid4.itemAt(0))
            fig4 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            ax4 = fig4.add_subplot(111)
            ax4.set_xlabel("E / eV")
            ax4.set_ylabel("$\mu$ t")
            canvas4 = FigureCanvas(fig4)
            navibar_4 = NavigationToolbar(canvas4, self.u.widget_4)
            t1 = 0.0
            t2 = 0.0
            if self.u.comboBox_6.currentText() == "SSSD_wCorrection" and os.path.exists(
                            params.homedir + "/deadtime.txt"):
                print "deadtime collection"
                f_ = open(params.homedir + "/deadtime.txt")
                t_line = f_.readline().rstrip()
                [t1, t2] = [float(t_line.split(",")[0]), float(t_line.split(",")[1])]
            if len(params.rb9809) != 0:
                f_in = ""
                D = ""
                BL = ""
                Energy = []
                ut = []
                for rb in params.rb9809:
                    if rb.isChecked():
                        f_in = params.dir9809 + "/" + rb.objectName()
                        data = open(f_in, "r")
                        for line in data:
                            line.rstrip()
                            if re.match(r"\s+9809\s+KEK\-PF\s+(\w+)", line):
                                BL = re.match(r"\s+9809\s+KEK\-PF\s+(\w+)", line).group(1)
                            elif re.match(r"\s+9809\s+KEK\-PF\s+(\w+)", line):
                                BL = re.match(r"\s+9809\s+SPring\-8\s+(\w+)", line).group(1)
                            elif re.match(r".+D=(.+)A.+", line):
                                D = float(re.match(r".+D=\s+(.+)\sA.+", line).group(1))
                            elif re.match(r"^\s+\d+\.\d+.+", line):
                                t_array = line.split()
                                Energy.append(12398.52 / (2 * D * np.sin(float(t_array[1]) / 180 * np.pi)))
                                if self.u.comboBox_6.currentText() == "SSSD_wCorrection":
                                    ut.append(
                                        calc_ut_wcollection(float(t_array[3]), float(t_array[4]), float(t_array[5]),
                                                            float(t_array[2]), t1, t2))
                                else:
                                    ut.append(
                                        calc_ut(float(t_array[3]), float(t_array[4]), self.u.comboBox_6.currentText()))
                        ax4.plot(np.array(Energy), np.array(ut))
                        params.grid4.addWidget(canvas4, 0, 0)
                        params.grid4.addWidget(navibar_4)
                        break

        def readREX(fname):
            E_ = []
            ut = []
            f = open(fname, "r")
            for line in f:
                line.rstrip()
                if re.match(r"^\d+\.\d+\s+\-?\d+\.\d+", line):
                    t_array = line.split()
                    E_.append(float(t_array[0]))
                    ut.append(float(t_array[1]))
            return np.array(E_), np.array(ut), len(E_)


        def readREX_for_save(fname):
            E_ = []
            ut = []
            edge = ""
            atom = ""
            f = open(fname, "r")
            for line in f:
                line.rstrip()
                if re.match(r"^\d+\.\d+\s+\-?\d+\.\d+", line):
                    t_array = line.split()
                    E_.append(float(t_array[0]))
                    ut.append(float(t_array[1]))
                elif re.match(r"\*EX_ATOM\=(\s*)(\w+)",line):
                    atom = re.match(r"\*EX_ATOM\=(\s*)(\w+)",line).group(2)
                elif re.match(r"\*EX_EDGE\=(\s*)(\w+)",line):
                    edge = re.match(r"\*EX_EDGE\=(\s*)(\w+)",line).group(2)
            return E_, ut, atom, edge

        def saveXANES():
            dat_dir =  params.path_to_xanes
            FO_dialog = QtGui.QFileDialog(self)
            dir = FO_dialog.getExistingDirectory(parent=None, dir=dat_dir,)
            print dir
            if len(params.xanes) != 0:
                for cb in params.xanes:
                    if cb.isChecked():
                        file = cb.objectName()
                        name = os.path.basename(cb.objectName())
                        name_replaced = re.sub('.ex3','_xan.ex3',name)
                        print "--readREX--"
                        [Energy,tmp_ut,atom,edge] = readREX_for_save(file)
                        lower = np.average(tmp_ut[self.u.doubleSpinBox.value():self.u.doubleSpinBox_2.value()+1])
                        upper = np.average(tmp_ut[self.u.doubleSpinBox_3.value():self.u.doubleSpinBox_4.value()+1])
                        ut_ = (tmp_ut-lower)/(upper-lower)
                        xan = dir + '/' +name_replaced
                        fout = open(xan,'w')
                        line1 = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                        atom = "*EX_ATOM=" + atom + "\n"
                        edge = "*EX_EDGE=" + edge + "\n"
                        line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                        line3 = "\n[EX_BEGIN]\n"
                        header_str = line1 + atom + edge + line2 + line3
                        fout.write(header_str)
                        for term in Energy:
                            str_ = "%7.3f  %1.8f\n" % (term, ut_[Energy.index(term)])
                            fout.write(str_)
                        fout.write("\n[EX_END]\n")

        def calc_delta_ut(file):
            energy_, ut_, length = readREX(file)
            delta_ut_ = []
            i = 1
            while i+1 < len(ut_):
                delta_ut_.append(((ut_[i+1]-ut_[i])/(energy_[i+1]-energy_[i])+(ut_[i]-ut_[i-1])/(energy_[i]-energy_[i-1]))/2)
                i += 1
            delta_ut_.append(0.0)
            delta_ut_.insert(0,0.0)
            return energy_, ut_, np.array(delta_ut_)

        def XANES_norm(datafile,fit_s,fit_e,nor_bE0_s,nor_bE0_e,nor_aE0_s,nor_aE0_e,func_type):
            energy, ut_, length = readREX(datafile)
            print len(ut_)
            delta_ut = []
            i = 1
            while i+1 < len(ut_):
                delta_ut.append(((ut_[i+1]-ut_[i])/(energy[i+1]-energy[i])+(ut_[i]-ut_[i-1])/(energy[i]-energy[i-1]))/2)
                i += 1
            delta_ut.append(0.0)
            delta_ut.insert(0,0.0)
            #find nearest point
            startpoint = find_near(energy,fit_s)
            endpoint = find_near(energy,fit_e)
            print startpoint
            #print energy[startpoint:endpoint]
            if func_type == 1:
                fit_r = np.polyfit(energy[startpoint:endpoint],ut_[startpoint:endpoint],1)
                print fit_r
                pre_edge = fit_r[0]*energy + fit_r[1]
                ut_wo_bk = ut_ - pre_edge
                base = np.average(ut_wo_bk[find_near(energy,nor_bE0_s):find_near(energy,nor_bE0_e)])
                after_edge = np.average(ut_wo_bk[find_near(energy,nor_aE0_s):find_near(energy,nor_aE0_e)])
                ut_nor = (ut_wo_bk-base)/(after_edge-base)
                return energy, ut_, np.array(delta_ut), pre_edge, ut_nor
            elif func_type == 2:
                fit_lin = np.polyfit(energy[startpoint:endpoint],ut_[startpoint:endpoint],1)
                def fit_f(x,C,D,Y):
                    return Y + C/x**3 - D/x**4
                E_s_and_e = [energy[startpoint],energy[endpoint]]
                ut_s_and_e = [ut_[startpoint],ut_[endpoint]]
                X = np.vstack([E_s_and_e ,np.ones(len(E_s_and_e))]).T
                DAT = [energy[startpoint]**4*(ut_[startpoint]-fit_lin[1]),energy[endpoint]**4*(ut_[endpoint]-fit_lin[1])]
                c, d = linalg.lstsq(X,DAT)[0]
                print c,d
                opt, pconv = optim.curve_fit(fit_f,energy[startpoint:endpoint],ut_[startpoint:endpoint],p0=[c,d,fit_lin[1]])
                print opt
                pre_edge = fit_f(energy,opt[0],opt[1],opt[2])
                ut_wo_bk = ut_ - pre_edge
                base = np.average(ut_wo_bk[find_near(energy,nor_bE0_s):find_near(energy,nor_bE0_e)])
                after_edge = np.average(ut_wo_bk[find_near(energy,nor_aE0_s):find_near(energy,nor_aE0_e)])
                ut_nor = (ut_wo_bk-base)/(after_edge-base)
                return energy, ut_, np.array(delta_ut), pre_edge, ut_nor
            elif func_type == 0:
                pre_edge = np.average(ut_[find_near(energy,nor_bE0_s):find_near(energy,nor_bE0_e)])
                ut_wo_bk = ut_ - pre_edge
                after_edge = np.average(ut_wo_bk[find_near(energy,nor_aE0_s):find_near(energy,nor_aE0_e)])
                ut_nor = ut_wo_bk/after_edge
                return energy, ut_, np.array(delta_ut), pre_edge*np.ones(len(ut_)), ut_nor


        def plot_xanes():
            while len(self.ax5.lines) !=0:
                self.ax5.lines.pop()
            if len(params.xanes) != 0:
                print '----plot_XANES----'
                for cb in params.xanes:
                    if cb.isChecked():
                        index = params.xanes.index(cb)%len(params.colors)
                        file = cb.objectName()
                        fit_s = self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_L').value()
                        #print fit_s
                        fit_e = self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_H').value()
                        #print fit_e
                        nor_bE0_s = self.u.doubleSpinBox.value()
                        nor_bE0_e = self.u.doubleSpinBox_2.value()
                        nor_aE0_s = self.u.doubleSpinBox_3.value()
                        nor_aE0_e = self.u.doubleSpinBox_4.value()
                        func_type = self.u.comboBox_bk.currentIndex()
                        Energy, ut_, delta_ut, pre_edge, ut_nor = XANES_norm(file,fit_s,fit_e,nor_bE0_s,nor_bE0_e,nor_aE0_s,nor_aE0_e,func_type)
                        self.ax5.plot(Energy,ut_nor,label = os.path.basename(cb.objectName()),color = params.colors[index])
                #self.ax5.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
                self.ax5.relim()
                self.ax5.autoscale_view()
                self.navibar_5.update()
                self.canvas5.draw()

        def set_dialog_parameters():
            #self.plot_dialog.comboBox.setCurrentIndex(0)
            index = self.plot_dialog.comboBox.currentIndex()
            dSpinBox = self.findChild(QtGui.QDoubleSpinBox,params.xanes[index].objectName()+'dSB_L')
            self.plot_dialog.doubleSpinBox_LE.setValue(dSpinBox.value())
            dSpinBox = self.findChild(QtGui.QDoubleSpinBox,params.xanes[index].objectName()+'dSB_H')
            self.plot_dialog.doubleSpinBox_HE.setValue(dSpinBox.value())
            self.plot_dialog.comboBox.setCurrentIndex(self.u.comboBox_bk.currentIndex())

        def plot_xanes_in_dialog():
            if len(self.ax_dialog.lines) != 0:
                self.annotate1.remove()
                self.annotate2.remove()
            while len(self.ax_dialog.lines) !=0:
                self.ax_dialog.lines.pop()
            if len(params.xanes) != 0:
                print '----plot_xanes_in_dialog----'
                index = self.plot_dialog.comboBox.currentIndex()
                #print index
                file = params.xanes[index].objectName()
                #print file
                fit_s = self.plot_dialog.doubleSpinBox_LE.value()
                #print fit_s
                fit_e = self.plot_dialog.doubleSpinBox_HE.value()
                #print fit_e
                nor_bE0_s = self.u.doubleSpinBox.value()
                nor_bE0_e = self.u.doubleSpinBox_2.value()
                nor_aE0_s = self.u.doubleSpinBox_3.value()
                nor_aE0_e = self.u.doubleSpinBox_4.value()
                func_type = self.plot_dialog.comboBox_Ftype.currentIndex()
                Energy, ut_, delta_ut, pre_edge, ut_nor = XANES_norm(file,fit_s,fit_e,nor_bE0_s,nor_bE0_e,nor_aE0_s,nor_aE0_e,func_type)
                self.ax_dialog.plot(Energy,ut_,label = 'XANES',color = params.colors[index], linewidth=2.0)
                self.ax_dialog.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
                self.ax_dialog.plot(Energy,pre_edge,label = 'bk',color = 'Black', linewidth=1.0)
                self.ax_dialog.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
                self.ax_dialog.relim()
                self.ax_dialog.autoscale_view()
                self.navibar_dialog.update()
                yrange = self.ax_dialog.get_ylim()
                print yrange
                self.annotate1 = matplotlib.text.Annotation("bk start",xy=(fit_s, ut_[find_near(Energy,fit_s)]),
                                                            xytext=(fit_s, ut_[find_near(Energy,fit_s)]-(yrange[1]-yrange[0])/5.0),
                                                            xycoords='data',
                                                            arrowprops=dict(arrowstyle="->"),
                                                            )
                self.annotate2 = matplotlib.text.Annotation("bk end",xy=(fit_e, ut_[find_near(Energy,fit_e)]),
                                                            xytext=(fit_e, ut_[find_near(Energy,fit_e)]-(yrange[1]-yrange[0])/5.0),
                                                            xycoords='data',
                                                            arrowprops=dict(arrowstyle="->"),
                                                            )
                #self.ax_dialog.annotate('bk end',
                #                        xy=(fit_e, ut_[find_near(Energy,fit_e)]),  # theta, radius
                #                        xytext=(fit_e, ut_[find_near(Energy,fit_e)]-(yrange[1]-yrange[0])/10.0),    # fraction, fraction
                #                        xycoords='data',
                #                        arrowprops=dict(arrowstyle="->"),
                #                        )
                self.ax_dialog.add_artist(self.annotate1)
                self.ax_dialog.add_artist(self.annotate2)
                self.canvas_dialog.draw()
        def plot_norm_XANES():
            if len(params.xanes) != 0:
                while len(self.ax_dialog_norm.lines) !=0:
                        self.ax_dialog_norm.lines.pop()
                for cb in params.xanes:
                    if cb.isChecked():
                        print '---plot norm XANES---'
                        index_ = params.xanes.index(cb)
                        #print index
                        file = params.xanes[index_].objectName()
                        #print file
                        fit_s = self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_L').value()
                        #print fit_s
                        fit_e = self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_H').value()
                        #print fit_e
                        nor_bE0_s = self.u.doubleSpinBox.value()
                        nor_bE0_e = self.u.doubleSpinBox_2.value()
                        nor_aE0_s = self.u.doubleSpinBox_3.value()
                        nor_aE0_e = self.u.doubleSpinBox_4.value()
                        func_type = self.plot_dialog.comboBox_Ftype.currentIndex()
                        Energy, ut_, delta_ut, pre_edge, ut_nor = XANES_norm(file,fit_s,fit_e,nor_bE0_s,nor_bE0_e,nor_aE0_s,nor_aE0_e,func_type)
                        self.ax_dialog_norm.plot(Energy,ut_nor,label = os.path.basename(params.xanes[index_].objectName()),color = params.colors[index_], linewidth=2.0)
                       #self.ax_dialog_norm.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, mode="expand", borderaxespad=0.)
                       #self.ax_dialog_norm.plot(Energy,pre_edge,label = os.path.basename(params.xanes[index].objectName()),color = 'Black', linewidth=1.0)
                       #self.ax_dialog_norm.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
                        self.ax_dialog_norm.relim()
                        self.ax_dialog_norm.autoscale_view()
                        #xrange = self.ax_dialog_norm.get_xlim()
                        self.ax_dialog_norm.axhline(y=1.0,color='k',linestyle='--')
                        self.ax_dialog_norm.axhline(y=0.0,color='k',linestyle='--')
                        #self.navibar_dialog.update()
                        self.canvas_dialog.draw()



        def find_near(Energy,req_Energy):
            array = np.absolute(Energy - req_Energy)
            return np.argmin(array)

        def openXANES_Files():
            print '---open XANES Files---'
            while scroll_layout4.count() > 0:
                b = scroll_layout4.takeAt(len(params.xanes) - 1)
                params.xanes.pop()
                b.widget().deleteLater()
            if params.path_to_xanes =="":
                dat_dir = params.homedir
            else:
                dat_dir = params.path_to_xanes
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir,
                                               filter="xas files(*.ex3 *.dat)")
            finfo = QtCore.QFileInfo(files[0][0])
            params.path_to_xanes = finfo.path()
            j = 0
            spinBoxes_L = []
            spinBoxes_H = []
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                cb = QtGui.QCheckBox(info.fileName())
                cb.setObjectName(info.absoluteFilePath())
                #print cb.objectName()
                params.xanes.append(cb)
                cb.setCheckState(QtCore.Qt.Checked)
                widget = QtGui.QWidget()
                layout = QtGui.QHBoxLayout()
                widget.setLayout(layout)
                layout.addWidget(cb)
                doubleSB_L = QtGui.QDoubleSpinBox()
                doubleSB_L.setObjectName(cb.objectName()+'dSB_L')
                spinBoxes_L.append(doubleSB_L)
                doubleSB_H = QtGui.QDoubleSpinBox()
                doubleSB_H.setObjectName(cb.objectName()+'dSB_H')
                spinBoxes_H.append(doubleSB_H)
                layout.addWidget(doubleSB_L)
                layout.addWidget(doubleSB_H)
                scroll_layout4.addWidget(widget)
                j += 1
            file =params.xanes[0].objectName()
            energy_, ut_, delta_ut_ = calc_delta_ut(file)
            E0 = energy_[np.argmax(delta_ut_)]
            [tmp_Energy,tmp_ut,length] = readREX(file)
            spinboxes = [self.u.doubleSpinBox,self.u.doubleSpinBox_2,self.u.doubleSpinBox_3,self.u.doubleSpinBox_4]
            for sB in spinboxes:
                sB.setMinimum(tmp_Energy[0])
                sB.setMaximum(tmp_Energy[-1])
                #print self.findChild(QtGui.QDoubleSpinBox,sB.objectName())
            print E0
            print energy_[find_near(energy_,E0-30)]
            print energy_[find_near(energy_,E0-55)]
            self.u.doubleSpinBox_2.setValue(energy_[find_near(energy_,E0-30)])
            self.u.doubleSpinBox.setValue(energy_[find_near(energy_,E0-55)])
            for sB in spinBoxes_L:
                sB.setMinimum(tmp_Energy[0])
                sB.setMaximum(tmp_Energy[-1])
                sB.setValue(energy_[find_near(energy_,E0-55)])
            for sB in spinBoxes_H:
                sB.setMinimum(tmp_Energy[0])
                sB.setMaximum(tmp_Energy[-1])
                sB.setValue(energy_[find_near(energy_,E0-30)])
            self.u.doubleSpinBox_3.setValue(energy_[find_near(energy_,E0+40)])
            self.u.doubleSpinBox_4.setValue(energy_[find_near(energy_,E0+70)])
            for cb in params.xanes:
                text = "color: "+params.colors[params.xanes.index(cb)%len(params.colors)]
                cb.setStyleSheet(text)
            plot_xanes()


        def addXANES_Files():
            print params.homedir
            if params.path_to_xanes =="":
                dat_dir = params.homedir
            else:
                dat_dir = params.path_to_xanes
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir, filter="xas files(*.ex3 *.dat)")
            finfo = QtCore.QFileInfo(files[0][0])
            params.path_to_xanes = finfo.path()
            j = 0
            if len(params.xanes) == 0:
                spinBoxes_L = []
                spinBoxes_H = []
                for fname in files[0]:
                    info = QtCore.QFileInfo(fname)
                    cb = QtGui.QCheckBox(info.fileName())
                    cb.setObjectName(info.absoluteFilePath())
                    params.xanes.append(cb)
                    cb.setCheckState(QtCore.Qt.Checked)
                    widget = QtGui.QWidget()
                    layout = QtGui.QHBoxLayout()
                    widget.setLayout(layout)
                    layout.addWidget(cb)
                    doubleSB_L = QtGui.QDoubleSpinBox()
                    doubleSB_L.setObjectName(cb.objectName()+'dSB_L')
                    spinBoxes_L.append(doubleSB_L)
                    doubleSB_H = QtGui.QDoubleSpinBox()
                    doubleSB_H.setObjectName(cb.objectName()+'dSB_H')
                    spinBoxes_H.append(doubleSB_H)
                    layout.addWidget(doubleSB_H)
                    layout.addWidget(doubleSB_L)
                    scroll_layout4.addWidget(widget)
                    j += 1
                file = params.xanes[0].objectName()
                energy_, ut_, delta_ut_ = calc_delta_ut(file)
                E0 = energy_[np.argmax(delta_ut_)]
                [tmp_Energy,tmp_ut,length] = readREX(file)
                spinboxes = [self.u.spinBox,self.u.spinBox_2,self.u.spinBox_3,self.u.spinBox_4]
                self.u.doubleSpinBox_2.setValue(find_near(energy_,E0-30))
                self.u.doubleSpinBox.setValue(find_near(energy_,E0-55))
                for sB in spinboxes:
                    sB.setMinimum(tmp_Energy[0])
                    sB.setMaximum(tmp_Energy[-1])
                self.u.doubleSpinBox_2.setValue(energy_[find_near(energy_,E0-30)])
                self.u.doubleSpinBox.setValue(energy_[find_near(energy_,E0-55)])
                for sB in spinBoxes_H:
                    sB.setMinimum(tmp_Energy[0])
                    sB.setMaximum(tmp_Energy[-1])
                    sB.setValue(energy_[find_near(energy_,E0-30)])
                for sB in spinBoxes_L:
                    sB.setMinimum(tmp_Energy[0])
                    sB.setMaximum(tmp_Energy[-1])
                    sB.setValue(energy_[find_near(energy_,E0-55)])
                self.u.doubleSpinBox_3.setValue(energy_[find_near(energy_,E0+40)])
                self.u.doubleSpinBox_4.setValue(energy_[find_near(energy_,E0+70)])
            else:
                spinBoxes_L = []
                spinBoxes_H = []
                for fname in files[0]:
                    info = QtCore.QFileInfo(fname)
                    sign = "add"
                    for cb in params.xanes:
                        if info.fileName() == cb.objectName():
                            sign = "not add"
                    if sign == "add":
                        cb = QtGui.QCheckBox(info.fileName())
                        cb.setObjectName(info.absoluteFilePath())
                        params.xanes.append(cb)
                        cb.setCheckState(QtCore.Qt.Checked)
                        widget = QtGui.QWidget()
                        layout = QtGui.QHBoxLayout()
                        widget.setLayout(layout)
                        layout.addWidget(cb)
                        doubleSB_L = QtGui.QDoubleSpinBox()
                        doubleSB_L.setObjectName(cb.objectName()+'dSB_L')
                        spinBoxes_L.append(doubleSB_L)
                        doubleSB_H = QtGui.QDoubleSpinBox()
                        doubleSB_H.setObjectName(cb.objectName()+'dSB_H')
                        spinBoxes_H.append(doubleSB_H)
                        layout.addWidget(doubleSB_H)
                        layout.addWidget(doubleSB_L)
                        scroll_layout4.addWidget(widget)
                        j += 1
                    file = params.xanes[0].objectName()
                [tmp_Energy,tmp_ut,length] = readREX(file)
                file = params.xanes[0].objectName()
                energy_, ut_, delta_ut_ = calc_delta_ut(file)
                E0 = energy_[np.argmax(delta_ut_)]
                for sB in spinBoxes_H:
                    sB.setMinimum(tmp_Energy[0])
                    sB.setMaximum(tmp_Energy[-1])
                    sB.setValue(energy_[find_near(energy_,E0-30)])
                for sB in spinBoxes_L:
                    sB.setMinimum(tmp_Energy[0])
                    sB.setMaximum(tmp_Energy[-1])
                    sB.setValue(energy_[find_near(energy_,E0-30)])
            for cb in params.xanes:
                text = "color: "+params.colors[params.xanes.index(cb)]
                cb.setStyleSheet(text)
            plot_xanes()

        def ShowDialog():
            if self.u.checkBox.isChecked():
                self.dialog.show()
                set_dialog_parameters()
                if self.plot_dialog.comboBox.count != 0:
                    self.plot_dialog.comboBox.clear()
                data = []
                for item in params.xanes:
                    data.append(os.path.basename(item.objectName()))
                model = self.plot_dialog.comboBox.model()
                for term in data:
                    item = QtGui.QStandardItem(term)
                    item.setForeground(QtGui.QColor(params.colors[data.index(term)]))
                    #font = item.font()
                    #font.setPointSize(10)
                    #item.setFont(font)
                    model.appendRow(item)
                #self.plot_dialog.comboBox.addItems(data)
                self.plot_dialog.comboBox_Ftype.setCurrentIndex(self.u.comboBox_bk.currentIndex())
                plot_xanes_in_dialog()
                plot_norm_XANES()
            else:
                pass

        def HideDialog():
            if self.u.checkBox.isChecked():
                self.dialog.done(1)
                self.u.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.u.pushButton_15.click()

        def comboBox_changed():
            text = "color: "+params.colors[self.plot_dialog.comboBox.currentIndex()]
            self.plot_dialog.comboBox.setStyleSheet(text)

        def pB_refresh_clicked():
            index = self.plot_dialog.comboBox.currentIndex()
            target_value = self.plot_dialog.doubleSpinBox_LE.value()
            self.findChild(QtGui.QDoubleSpinBox,params.xanes[index].objectName()+'dSB_L').setValue(target_value)
            target_value = self.plot_dialog.doubleSpinBox_HE.value()
            self.findChild(QtGui.QDoubleSpinBox,params.xanes[index].objectName()+'dSB_H').setValue(target_value)
            self.u.comboBox_bk.setCurrentIndex(self.plot_dialog.comboBox_Ftype.currentIndex())
            plot_xanes_in_dialog()

        def copy_to_main_LE(value):
            i = self.plot_dialog.comboBox.currentIndex()
            sB = self.findChild(QtGui.QDoubleSpinBox,params.xanes[i].objectName()+'dSB_L')
            if abs(value - sB.value()) > 0.05:
                sB.setValue(value)

        def copy_to_main_HE(value):
            i = self.plot_dialog.comboBox.currentIndex()
            sB = self.findChild(QtGui.QDoubleSpinBox,params.xanes[i].objectName()+'dSB_H')
            if abs(value - sB.value()) > 0.05:
                sB.setValue(value)

        def copy_to_all_data():
            for cb in params.xanes:
                self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_L').setValue(self.plot_dialog.doubleSpinBox_LE.value())
                self.findChild(QtGui.QDoubleSpinBox,cb.objectName()+'dSB_H').setValue(self.plot_dialog.doubleSpinBox_HE.value())


        #self.plot_dialog.comboBox.currentIndexChanged.connect(comboBox_changed)
        self.plot_dialog.pushButton.clicked.connect(HideDialog)
        self.plot_dialog.pB_refresh.clicked.connect(pB_refresh_clicked)
        self.plot_dialog.doubleSpinBox_LE.valueChanged[float].connect(copy_to_main_LE)
        self.plot_dialog.doubleSpinBox_HE.valueChanged[float].connect(copy_to_main_HE)
        self.plot_dialog.pB_copy_for_all.clicked.connect(copy_to_all_data)

        self.u.pushButton_2.clicked.connect(openFiles)
        self.u.pushButton.clicked.connect(define_outdir)
        self.u.pushButton_5.clicked.connect(select_or_release_all)
        self.u.pushButton_6.clicked.connect(Save)
        self.u.pB_save_all_SSD.clicked.connect(Save_all_as_Current)
        self.u.pushButton_3.clicked.connect(func_pushButton_3)
        self.u.pushButton_4.clicked.connect(click_pB4)
        self.u.pushButton_7.clicked.connect(define_outdir_for_sum)
        self.u.pushButton_8.clicked.connect(Save_sum_and_avg)
        self.u.pushButton_12.clicked.connect(set_interpolation_file)
        self.u.rb_sum.clicked.connect(plot_sum)
        self.u.rb_avg.clicked.connect(plot_avg)
        self.u.comboBox_2.currentIndexChanged.connect(change_CB3)
        self.u.comboBox.currentIndexChanged.connect(change_CB4)
        self.u.comboBox_6.currentIndexChanged.connect(plot_9809)
        self.u.lineEdit.textChanged.connect(change_lineEdit2)
        self.u.pushButton_9.clicked.connect(open_9809)
        self.u.pushButton_10.clicked.connect(define_outdir9809)
        self.u.pushButton_11.clicked.connect(convert_9809)
        self.u.pushButton_14.clicked.connect(openXANES_Files)
        self.u.pushButton_13.clicked.connect(addXANES_Files)
        self.u.pushButton_15.clicked.connect(plot_xanes)
        self.u.pushButton_16.clicked.connect(saveXANES)
        for cb in params.cbs:
            cb.clicked.connect(plot_each_ch)
        self.u.checkBox.toggled.connect(ShowDialog)

        self.u.EXAFSBK_type.addItems(['autobk','spline_smoothing'])
        self.u.comboBox_preEdge.addItems(['average','linear','victoreen'])
        self.u.comboBox_preEdge.setCurrentIndex(1)
        scroll_layout_exafs = QtGui.QVBoxLayout()
        scroll_widgets_exafs = QtGui.QWidget()
        scroll_widgets_exafs.setLayout(scroll_layout_exafs)
        self.u.scrollArea_6.setWidget(scroll_widgets_exafs)
        self.u.FT_kweight.addItems(['3','2','1','0'])

        #Figure for EXAFS Compare
        ##XAFS##
        params.grid_exafs_bk_ut = QtGui.QGridLayout()
        self.fig_exafsbk_ut = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_exafsbk_ut = self.fig_exafsbk_ut.add_subplot(111)
        self.ax_exafsbk_ut.set_xlabel("E / eV")
        self.ax_exafsbk_ut.set_ylabel("$\mu$ t")
        self.canvas_exafsbk_ut = FigureCanvas(self.fig_exafsbk_ut)
        self.navibar_exafsbk_ut = NavigationToolbar(self.canvas_exafsbk_ut, self.u.widget_EXAFS)
        self.u.widget_EXAFS.setLayout(params.grid_exafs_bk_ut)
        params.grid_exafs_bk_ut.addWidget(self.canvas_exafsbk_ut, 0, 0)
        params.grid_exafs_bk_ut.addWidget(self.navibar_exafsbk_ut)
        ##chi(k) in EXAFS##
        params.grid_exafs_bk_chi = QtGui.QGridLayout()
        self.fig_exafsbk_chi = Figure(figsize=(200, 200), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_exafsbk_chi = self.fig_exafsbk_chi.add_subplot(111)
        self.ax_exafsbk_chi.set_xlabel("k / $\AA^{-1}$")
        self.ax_exafsbk_chi.set_ylabel("$k^{3}\chi$ (k)")
        self.canvas_exafsbk_chi = FigureCanvas(self.fig_exafsbk_chi)
        self.fig_exafsbk_chi.subplots_adjust(bottom=0.15)
        #self.navibar_exafsbk_chi = NavigationToolbar(self.canvas_exafsbk_chi, self.u.mini_chi_k)
        self.u.mini_chi_k.setLayout(params.grid_exafs_bk_chi)
        params.grid_exafs_bk_chi.addWidget(self.canvas_exafsbk_chi, 0, 0)

        ##chi(r) in EXAFS##
        params.grid_exafs_bk_chir = QtGui.QGridLayout()
        self.fig_exafsbk_chir = Figure(figsize=(200, 200), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_exafsbk_chir = self.fig_exafsbk_chir.add_subplot(111)
        self.ax_exafsbk_chir.set_xlabel("r / $\AA$")
        self.ax_exafsbk_chir.set_ylabel("FT(r)")
        self.canvas_exafsbk_chir = FigureCanvas(self.fig_exafsbk_chir)
        self.fig_exafsbk_chir.subplots_adjust(bottom=0.15)
        #self.navibar_exafsbk_chi = NavigationToolbar(self.canvas_exafsbk_chi, self.u.mini_chi_k)
        self.u.mini_FT.setLayout(params.grid_exafs_bk_chir)
        params.grid_exafs_bk_chir.addWidget(self.canvas_exafsbk_chir, 0, 0)

        ##chi(k) in chi##
        params.grid_chi_k = QtGui.QGridLayout()
        self.fig_chi_k = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_chi_k = self.fig_chi_k.add_subplot(111)
        self.ax_chi_k.set_xlabel("k / $\AA{-1}$")
        self.ax_chi_k.set_ylabel("$k^{n}\chi$ (k)")
        self.canvas_chi_k = FigureCanvas(self.fig_chi_k)
        self.fig_chi_k.subplots_adjust(bottom=0.15)
        self.u.w_chi_k.setLayout(params.grid_chi_k)
        params.grid_chi_k.addWidget(self.canvas_chi_k, 0, 0)

        ###FT(r) in FT###
        params.grid_FT = QtGui.QGridLayout()
        self.fig_FT = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax_ft = self.fig_FT.add_subplot(111)
        self.ax_ft.set_xlabel("r / $\AA$")
        self.ax_ft.set_ylabel("$FT")
        self.canvas_FT = FigureCanvas(self.fig_FT)
        self.fig_FT.subplots_adjust(bottom=0.15)
        self.u.w_FT.setLayout(params.grid_FT)
        params.grid_FT.addWidget(self.canvas_FT, 0, 0)

        def comboBox_EXAFSBK_changed():
            return

        def subtract_exafsbk(button):
            print '--- subtract exafs ---'
            #button = params.exafs_rb.checkedButton()
            name = os.path.basename(button.objectName())
            Energy = params.data_and_conditions[name+':'+'Energy']
            ut = params.data_and_conditions[name+':'+'ut']
            E0 = self.u.double_sB_E0_bk.value()
            k_min = self.u.double_sB_sP_start.value()
            k_max = self.u.double_sB_sP_end.value()
            pre_start = self.u.double_sB_pre_start.value()
            pre_end = self.u.double_sB_pre_end.value()
            post_start = self.u.double_sB_post_start.value()
            post_end = self.u.double_sB_post_end.value()
            EXAFSBK_type = self.u.EXAFSBK_type.currentIndex()
            preEdge_type = self.u.comboBox_preEdge.currentIndex()
            kweight = self.u.sB_kweight.value()
            degree_SS = self.u.degree_SS.value()
            rbkg = self.u.double_sB_rbkg.value()
            sf = self.u.SmoothF.value()
            [bkg, Lpre_edge, Lpost_edge, k, chi_k, r, ft_mag, ft_im] = [np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy)), np.zeros(len(Energy))]
            if len(params.data_and_conditions[name+':'+'ut']) != 0:
                if self.u.EXAFSBK_type.currentIndex() == 0:
                    print '--run autobk--'
                    bkg, Lpre_edge, Lpost_edge, chi_k, k, r, ft_mag, ft_im = use_larch.run_autobk(Energy,ut,E0,rbkg,kweight,k_min,k_max,
                                                                                              pre_start,pre_end,post_start,post_end,
                                                                                              preEdge_type)
                    params.data_and_conditions[name+':'+'bkg'] = bkg
                    params.data_and_conditions[name+':'+'Lpre_edge'] = Lpre_edge
                    params.data_and_conditions[name+':'+'Lpost_edge'] = Lpost_edge
                    params.data_and_conditions[name+':'+'chi_k'] = chi_k
                    params.data_and_conditions[name+':'+'k'] = k
                    params.data_and_conditions[name+':'+'r'] = r
                    params.data_and_conditions[name+':'+'ft_mag'] = ft_mag
                    params.data_and_conditions[name+':'+'ft_im'] = ft_im
                elif self.u.EXAFSBK_type.currentIndex() == 1:
                    print '--use spline smoothing--'
                    if self.u.checkBox_2.isChecked():
                        bkg, Lpre_edge, Lpost_edge, chi_k, k, r, ft_mag, ft_im, sf_ = use_larch.Cook_Sayers_rotine_(Energy,ut,E0,pre_start,pre_end,post_start,post_end,
                                                             preEdge_type,degree_SS,kweight,sf)
                        self.u.sB_kweight.setValue(kweight)
                        self.u.SmoothF.setValue(sf_)
                        params.data_and_conditions[name+':'+self.u.SmoothF.objectName()] = sf_
                        params.data_and_conditions[name+':'+'bkg'] = bkg
                        params.data_and_conditions[name+':'+'Lpre_edge'] = Lpre_edge
                        params.data_and_conditions[name+':'+'Lpost_edge'] = Lpost_edge
                        params.data_and_conditions[name+':'+'chi_k'] = chi_k
                        params.data_and_conditions[name+':'+'k'] = k
                        params.data_and_conditions[name+':'+'r'] = r
                        params.data_and_conditions[name+':'+'ft_mag'] = ft_mag
                        params.data_and_conditions[name+':'+'ft_im'] = ft_im
                        params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = kweight
                        #params.data_and_conditions[name+':'+self.u.SmoothF.objectName()] = sf
                    else:
                        bkg, Lpre_edge, Lpost_edge, chi_k,\
                            k, r, ft_mag, ft_im, sf_ = use_larch.calc_exafs_SplineSmoothing(Energy,ut, E0, pre_start,pre_end,post_start,
                                                                                                post_end,preEdge_type,degree_SS,kweight,sf)
                        #self.u.sB_kweight.setValue(kweight)
                        #self.u.SmoothF.setValue(sf)
                        params.data_and_conditions[name+':'+self.u.SmoothF.objectName()] = sf
                        params.data_and_conditions[name+':'+'bkg'] = bkg
                        params.data_and_conditions[name+':'+'Lpre_edge'] = Lpre_edge
                        params.data_and_conditions[name+':'+'Lpost_edge'] = Lpost_edge
                        params.data_and_conditions[name+':'+'chi_k'] = chi_k
                        params.data_and_conditions[name+':'+'k'] = k
                        params.data_and_conditions[name+':'+'r'] = r
                        params.data_and_conditions[name+':'+'ft_mag'] = ft_mag
                        params.data_and_conditions[name+':'+'ft_im'] = ft_im
                        params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = kweight


                return Energy, ut, bkg, Lpre_edge, Lpost_edge, k, chi_k, r, ft_mag, ft_im

        def setup_exafsbk():
            print '---setup_exafsbk---'
            rb = params.exafs_rb.checkedButton()
            name = os.path.basename(rb.objectName())
            E0 = params.data_and_conditions[name+':'+self.u.double_sB_E0_bk.objectName()]
            energy = params.data_and_conditions[name+':'+'Energy']
            kmax = math.sqrt(0.2626*abs(E0-energy[-1]))
            self.u.double_sB_pre_start.setMinimum(energy[0])
            self.u.double_sB_pre_start.setMaximum(E0+10.0)
            self.u.double_sB_pre_end.setMinimum(energy[0])
            self.u.double_sB_pre_end.setMaximum(E0+10.0)
            self.u.double_sB_post_start.setMinimum(E0-10.0)
            self.u.double_sB_post_start.setMaximum(energy[-1])
            self.u.double_sB_post_end.setMinimum(E0-10.0)
            self.u.double_sB_post_end.setMaximum(energy[-1])
            self.u.double_sB_sP_end.setMaximum(kmax)
            pre_start = params.data_and_conditions[name+':'+self.u.double_sB_pre_start.objectName()]
            pre_end = params.data_and_conditions[name+':'+self.u.double_sB_pre_end.objectName()]
            post_start = params.data_and_conditions[name+':'+self.u.double_sB_post_start.objectName()]
            post_end = params.data_and_conditions[name+':'+self.u.double_sB_post_end.objectName()]
            bk_method = params.data_and_conditions[name+':'+self.u.EXAFSBK_type.objectName()]
            preEdge_method = params.data_and_conditions[name+':'+self.u.comboBox_preEdge.objectName()]
            k_min = params.data_and_conditions[name+':'+self.u.double_sB_sP_start.objectName()]
            k_max = params.data_and_conditions[name+':'+self.u.double_sB_sP_end.objectName()]
            weight = params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()]
            Factor_SS = params.data_and_conditions[name+':'+self.u.degree_SS.objectName()]
            rbkg = params.data_and_conditions[name+':'+self.u.double_sB_rbkg.objectName()]
            if params.data_and_conditions.__getitem__(name+':'+self.u.sB_kweight.objectName()):
                self.u.sB_kweight.setValue(params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()])
            self.u.double_sB_E0_bk.setValue(E0)
            self.u.double_sB_pre_start.setValue(pre_start)
            self.u.double_sB_pre_end.setValue(pre_end)
            self.u.double_sB_post_start.setValue(post_start)
            self.u.double_sB_post_end.setValue(post_end)
            self.u.EXAFSBK_type.setCurrentIndex(bk_method)
            self.u.double_sB_sP_start.setValue(k_min)
            self.u.double_sB_sP_end.setValue(k_max)
            self.u.comboBox_preEdge.setCurrentIndex(preEdge_method)
            self.u.sB_kweight.setValue(weight)
            self.u.degree_SS.setValue(Factor_SS)
            self.u.double_sB_rbkg.setValue(rbkg)


        def preserve_condition():
            print '---preserve condition---'
            rb = params.exafs_rb.checkedButton()
            name = os.path.basename(rb.objectName())
            params.data_and_conditions[name+':'+self.u.double_sB_E0_bk.objectName()] = self.u.double_sB_E0_bk.value()
            params.data_and_conditions[name+':'+self.u.double_sB_pre_start.objectName()] = self.u.double_sB_pre_start.value()
            params.data_and_conditions[name+':'+self.u.double_sB_pre_end.objectName()] = self.u.double_sB_pre_end.value()
            params.data_and_conditions[name+':'+self.u.double_sB_post_start.objectName()] = self.u.double_sB_post_start.value()
            params.data_and_conditions[name+':'+self.u.double_sB_post_end.objectName()] = self.u.double_sB_post_end.value()
            params.data_and_conditions[name+':'+self.u.EXAFSBK_type.objectName()] = self.u.EXAFSBK_type.currentIndex()
            params.data_and_conditions[name+':'+self.u.comboBox_preEdge.objectName()] = self.u.comboBox_preEdge.currentIndex()
            params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = self.u.sB_kweight.value()
            params.data_and_conditions[name+':'+self.u.degree_SS.objectName()] = self.u.degree_SS.value()
            params.data_and_conditions[name+':'+self.u.double_sB_rbkg.objectName()] = self.u.double_sB_rbkg.value()
            params.data_and_conditions[name+':'+self.u.SmoothF.objectName()] = self.u.SmoothF.value()
            params.data_and_conditions[name+':'+self.u.double_sB_sP_start.objectName()] = self.u.double_sB_sP_start.value()
            params.data_and_conditions[name+':'+self.u.double_sB_sP_end.objectName()] = self.u.double_sB_sP_end.value()

        def plot_exafs():
            print '---plot exafs---'
            Energy, ut, bkg, Lpre_edge, Lpost_edge, k, chi_k, r, ft_mag, ft_im = subtract_exafsbk(params.exafs_rb.checkedButton())
            while len(self.ax_exafsbk_ut.lines) > 0:
                self.ax_exafsbk_ut.lines.pop()
            while len(self.ax_exafsbk_chi.lines)>0:
                self.ax_exafsbk_chi.lines.pop()
            while len(self.ax_exafsbk_chir.lines)>0:
                self.ax_exafsbk_chir.lines.pop()
            for ax in [self.ax_exafsbk_ut,self.ax_exafsbk_chi,self.ax_exafsbk_chir]:
                ax.relim()
                ax.autoscale_view()
            E0 = self.u.double_sB_E0_bk.value()
            self.ax_exafsbk_ut.plot(Energy, ut, 'r')
            self.ax_exafsbk_ut.plot(Energy,Lpre_edge,'k')
            self.ax_exafsbk_ut.plot(Energy[find_near(Energy,E0):],Lpost_edge[find_near(Energy,E0):],'k')
            self.ax_exafsbk_chi.plot(k,chi_k*k**3,'b')
            self.ax_exafsbk_chir.plot(r,ft_mag,'b',r,ft_im,'r')
            self.ax_exafsbk_chir.set_xlim([0.0,6.0])
            for canvas in [self.canvas_exafsbk_ut,self.canvas_exafsbk_chi,self.canvas_exafsbk_chir]:
                canvas.draw()

        def plot_chi_k():
            print  '---- plot chi(k) ----'
            while len(self.ax_chi_k.lines) > 0:
                self.ax_chi_k.lines.pop()
            self.ax_chi_k.relim()
            self.ax_chi_k.autoscale_view()
            if len(params.exafs) != 0:
                for cb in params.exafs:
                    name = os.path.basename(cb.objectName())
                    if params.data_and_conditions.__contains__(name+':'+'chi_k') and cb.isChecked():
                        self.ax_chi_k.plot(params.data_and_conditions[name+':'+'k'],params.data_and_conditions[name+':'+'chi_k']*params.data_and_conditions[name+':'+'k']**self.u.sB_chi_kw.value(),params.colors[params.exafs.index(cb)%len(params.colors)])
                    else:
                        pass
                self.canvas_chi_k.draw()
        def plot_ft():
            while len(self.ax_ft.lines) > 0:
                self.ax_ft.lines.pop()
            self.ax_ft.relim()
            self.ax_ft.autoscale_view()
            self.ax_ft.set_xlim([0.0,6.0])
            if len(params.exafs) != 0:
                for cb in params.exafs:
                    name = os.path.basename(cb.objectName())
                    if params.data_and_conditions.__contains__(name+':'+'chi_k') and cb.isChecked():
                        k = params.data_and_conditions[name+':'+'k']
                        chi = params.data_and_conditions[name+':'+'chi_k']
                        kweight = abs(self.u.FT_kweight.currentIndex()-3)
                        kmin = self.u.double_sB_kmin.value()
                        kmax = self.u.double_sB_kmax.value()
                        r, ft_mag, ft_img = use_larch.calc_FT(k,chi,kmin,kmax,kweight)
                        self.ax_ft.plot(r,ft_mag,params.colors[params.exafs.index(cb)%len(params.colors)])
                self.canvas_FT.draw()

        def plot_ft_():
            currentI = 3 - self.u.sB_chi_kw.value()
            self.u.FT_kweight.setCurrentIndex(abs(currentI))
            print 'FT_kweight CurrentIndex is ' + str(self.u.FT_kweight.currentIndex())
            print 'FT kweight is ' + self.u.FT_kweight.currentText()
            self.u.tabWidget_2.setCurrentIndex(2)
            plot_ft()

        def plot_exafs_chi_ft(currentI):
            if currentI == 0:
                plot_exafs
            elif currentI == 1:
                plot_chi_k()
            elif currentI == 2:
                plot_ft()

        def func_for_cb_exafs():
            if self.u.tabWidget_2.currentIndex() == 1:
                plot_chi_k()
            elif self.u.tabWidget_2.currentIndex() == 2:
                plot_ft()


        def func_rb():
            setup_exafsbk()
            plot_exafs()

        def func_pB20():
            plot_exafs()
            preserve_condition()

        def open_exafs_files():
            print '---open EXAFS Files---'
            while scroll_layout_exafs.count() > 0:
                #params.current_EXAFS = ''
                b = scroll_layout_exafs.takeAt(len(params.exafs) - 1)
                params.exafs.pop()
                params.exafs_rb.removeButton(params.exafs_rb.buttons().pop())
                b.widget().deleteLater()
            if params.path_to_exafs =="":
                dat_dir = params.homedir
            else:
                dat_dir = params.path_to_xanes
            FO_dialog = QtGui.QFileDialog(self)
            if self.u.tabWidget_2.tabText(self.u.tabWidget_2.currentIndex()) == 'chi_k':
                files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir,
                                                   filter="xas files(*.rex *.xi *.chi)")
                finfo = QtCore.QFileInfo(files[0][0])
                params.path_to_exafs = finfo.path()
                j = 0
                for fname in files[0]:
                    info = QtCore.QFileInfo(fname)
                    cb = QtGui.QCheckBox(info.fileName())
                    cb.setObjectName(info.absoluteFilePath())
                    cb.clicked.connect(func_for_cb_exafs)
                    params.exafs.append(cb)
                    k, chi = use_larch.read_chi_file(cb.objectName())
                    name = os.path.basename(cb.objectName())
                    params.data_and_conditions[name+':'+'k'] = k[:]
                    params.data_and_conditions[name+':'+'chi_k'] = chi[:]
                for cb in params.exafs:
                    text = "color: "+params.colors[params.exafs.index(cb)%len(params.colors)]
                    cb.setStyleSheet(text)
                    scroll_layout_exafs.addWidget(cb)
            else:
                files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir,
                                                   filter="xas files(*.ex3 *.dat)")
                finfo = QtCore.QFileInfo(files[0][0])
                params.path_to_exafs = finfo.path()
                j = 0
                for fname in files[0]:
                    info = QtCore.QFileInfo(fname)
                    cb = QtGui.QCheckBox(info.fileName())
                    cb.setObjectName(info.absoluteFilePath())
                    cb.clicked.connect(func_for_cb_exafs)
                    params.exafs.append(cb)
                    energy, ut = use_larch.read_file(cb.objectName())
                    first_div, num_of_E0 = use_larch.calc_1st_derivative(energy,ut)
                    k_max = math.sqrt(0.2626*abs(energy[num_of_E0]-energy[-1]))
                    print k_max
                    name = os.path.basename(cb.objectName())
                    params.data_and_conditions[name+':'+'Energy'] = energy[:]
                    params.data_and_conditions[name+':'+'ut'] = ut[:]
                    params.data_and_conditions[name+':'+self.u.double_sB_E0_bk.objectName()] = energy[num_of_E0]
                    params.data_and_conditions[name+':'+self.u.double_sB_pre_start.objectName()] = energy[0]
                    params.data_and_conditions[name+':'+self.u.double_sB_pre_end.objectName()] = energy[num_of_E0] - 30.0
                    params.data_and_conditions[name+':'+self.u.double_sB_post_start.objectName()] = energy[num_of_E0] + 10.0
                    params.data_and_conditions[name+':'+self.u.double_sB_post_end.objectName()] = energy[-1]
                    params.data_and_conditions[name+':'+self.u.double_sB_sP_start.objectName()] = 0.5
                    params.data_and_conditions[name+':'+self.u.double_sB_sP_end.objectName()] = k_max
                    params.data_and_conditions[name+':'+self.u.EXAFSBK_type.objectName()] = self.u.EXAFSBK_type.currentIndex()
                    params.data_and_conditions[name+':'+self.u.comboBox_preEdge.objectName()] = self.u.comboBox_preEdge.currentIndex()
                    params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = self.u.sB_kweight.value()
                    params.data_and_conditions[name+':'+self.u.degree_SS.objectName()] = self.u.degree_SS.value()
                    params.data_and_conditions[name+':'+self.u.double_sB_rbkg.objectName()] = self.u.double_sB_rbkg.value()
                    cb.setCheckState(QtCore.Qt.Checked)
                    widget = QtGui.QWidget()
                    layout = QtGui.QHBoxLayout()
                    widget.setLayout(layout)
                    rb = QtGui.QRadioButton()
                    rb.setObjectName(cb.objectName())
                    print rb.objectName()
                    rb.toggled.connect(func_rb)
                    params.exafs_rb.addButton(rb)
                    layout.addWidget(cb)
                    layout.addWidget(rb)
                    scroll_layout_exafs.addWidget(widget)
                    j += 1
                for cb in params.exafs:
                    text = "color: "+params.colors[params.exafs.index(cb)%len(params.colors)]
                    cb.setStyleSheet(text)
                params.exafs_rb.buttons()[0].toggle()

        def add_exafs_files():
            if len(params.exafs) == 0:
                open_exafs_files()
            else:
                print '---add EXAFS Files---'
                if params.path_to_exafs =="":
                    dat_dir = params.homedir
                else:
                    dat_dir = params.path_to_xanes
                FO_dialog = QtGui.QFileDialog(self)
                if self.u.tabWidget_2.tabText(self.u.tabWidget_2.currentIndex()) == 'chi_k':
                    files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir,
                                                       filter="xas files(*.rex *.xi *.chi)")
                    finfo = QtCore.QFileInfo(files[0][0])
                    params.path_to_exafs = finfo.path()
                    j = 0
                    num = len(params.exafs) -1
                    for fname in files[0]:
                        info = QtCore.QFileInfo(fname)
                        sign = 'make'
                        for cb in params.exafs:
                            if cb.objectName() == info.absoluteFilePath():
                                sign = 'not make'
                            else:
                                pass
                        if sign == 'not make':
                            pass
                        elif sign == 'make':
                            cb = QtGui.QCheckBox(info.fileName())
                            cb.setObjectName(info.absoluteFilePath())
                            cb.clicked.connect(func_for_cb_exafs)
                            params.exafs.append(cb)
                            k, chi = use_larch.read_chi_file(cb.objectName())
                            name = os.path.basename(cb.objectName())
                            params.data_and_conditions[name+':'+'k'] = k[:]
                            params.data_and_conditions[name+':'+'chi_k'] = chi[:]
                    for cb in params.exafs[num+1:]:
                        text = "color: "+params.colors[params.exafs.index(cb)%len(params.colors)]
                        cb.setStyleSheet(text)
                        scroll_layout_exafs.addWidget(cb)
                else:
                    files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir,
                                                       filter="xas files(*.ex3 *.dat)")
                    finfo = QtCore.QFileInfo(files[0][0])
                    params.path_to_exafs = finfo.path()
                    j = 0
                    num = len(params.exafs) -1
                    for fname in files[0]:
                        info = QtCore.QFileInfo(fname)
                        sign = 'make'
                        for cb in params.exafs:
                            if cb.objectName() == info.absoluteFilePath():
                                sign = 'not make'
                            else:
                                pass
                        if sign == 'not make':
                            pass
                        elif sign == 'make':
                            cb = QtGui.QCheckBox(info.fileName())
                            cb.setObjectName(info.absoluteFilePath())
                            cb.clicked.connect(func_for_cb_exafs)
                            params.exafs.append(cb)
                            energy, ut = use_larch.read_file(cb.objectName())
                            first_div, num_of_E0 = use_larch.calc_1st_derivative(energy,ut)
                            name = os.path.basename(cb.objectName())
                            k_max = math.sqrt(0.2626*abs(energy[num_of_E0]-energy[-1]))
                            params.data_and_conditions[name+':'+'Energy'] = energy[:]
                            params.data_and_conditions[name+':'+'ut'] = ut[:]
                            params.data_and_conditions[name+':'+self.u.double_sB_E0_bk.objectName()] = energy[num_of_E0]
                            params.data_and_conditions[name+':'+self.u.double_sB_pre_start.objectName()] = energy[0]
                            params.data_and_conditions[name+':'+self.u.double_sB_pre_end.objectName()] = energy[num_of_E0] - 30.0
                            params.data_and_conditions[name+':'+self.u.double_sB_post_start.objectName()] = energy[num_of_E0] + 10.0
                            params.data_and_conditions[name+':'+self.u.double_sB_post_end.objectName()] = energy[-1]
                            params.data_and_conditions[name+':'+self.u.double_sB_sP_start.objectName()] = 0.5
                            params.data_and_conditions[name+':'+self.u.double_sB_sP_end.objectName()] = k_max
                            params.data_and_conditions[name+':'+self.u.EXAFSBK_type.objectName()] = self.u.EXAFSBK_type.currentIndex()
                            params.data_and_conditions[name+':'+self.u.comboBox_preEdge.objectName()] = self.u.comboBox_preEdge.currentIndex()
                            params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = self.u.sB_kweight.value()
                            params.data_and_conditions[name+':'+self.u.degree_SS.objectName()] = self.u.degree_SS.value()
                            params.data_and_conditions[name+':'+self.u.double_sB_rbkg.objectName()] = self.u.double_sB_rbkg.value()
                            cb.setCheckState(QtCore.Qt.Checked)
                            widget = QtGui.QWidget()
                            layout = QtGui.QHBoxLayout()
                            widget.setLayout(layout)
                            rb = QtGui.QRadioButton()
                            rb.setObjectName(cb.objectName())
                            print rb.objectName()
                            rb.toggled.connect(func_rb)
                            params.exafs_rb.addButton(rb)
                            layout.addWidget(cb)
                            layout.addWidget(rb)
                            scroll_layout_exafs.addWidget(widget)
                            j += 1
                    for cb in params.exafs[num+1:]:
                        text = "color: "+params.colors[params.exafs.index(cb)%len(params.colors)]
                        cb.setStyleSheet(text)

        def copy_current_to_all():
            if len(params.exafs) != 0:
                for cb in params.exafs:
                    name = os.path.basename(cb.objectName())
                    if cb.isChecked() and len(params.data_and_conditions[name+':'+'Energy']) !=0:
                        params.data_and_conditions[name+':'+self.u.double_sB_E0_bk.objectName()] = self.u.double_sB_E0_bk.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_pre_start.objectName()] = self.u.double_sB_pre_start.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_pre_end.objectName()] = self.u.double_sB_pre_end.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_post_start.objectName()] = self.u.double_sB_post_start.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_post_end.objectName()] = self.u.double_sB_post_end.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_sP_start.objectName()] = self.u.double_sB_sP_start.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_sP_end.objectName()] = self.u.double_sB_sP_end.value()
                        params.data_and_conditions[name+':'+self.u.EXAFSBK_type.objectName()] = self.u.EXAFSBK_type.currentIndex()
                        params.data_and_conditions[name+':'+self.u.comboBox_preEdge.objectName()] = self.u.comboBox_preEdge.currentIndex()
                        params.data_and_conditions[name+':'+self.u.sB_kweight.objectName()] = self.u.sB_kweight.value()
                        params.data_and_conditions[name+':'+self.u.degree_SS.objectName()] = self.u.degree_SS.value()
                        params.data_and_conditions[name+':'+self.u.double_sB_rbkg.objectName()] = self.u.double_sB_rbkg.value()
                        subtract_exafsbk(cb)
                if self.u.EXAFSBK_type.currentIndex() == 1:
                    self.u.checkBox_2.setCheckState(QtCore.Qt.Unchecked)

        def Save_chi_ft():
            if self.u.tabWidget_2.currentIndex() == 0:
                print '--- Save current chi file ---'
                if len(params.exafs) !=0:
                    dat_dir =  os.path.dirname(params.exafs_rb.checkedButton().objectName())
                    FO_dialog = QtGui.QFileDialog(self)
                    file = FO_dialog.getSaveFileName(parent=None, dir=dat_dir,filter="chi files(*.dat)")
                    f = open(file[0],'w')
                    df = pd.DataFrame(columns=['#k','chi'])
                    name = os.path.basename(params.exafs_rb.checkedButton().objectName())
                    df['#k'] = params.data_and_conditions[name+':'+'k'][:]
                    df['chi'] = params.data_and_conditions[name+':'+'chi_k'][:]
                    df.to_csv(f,index=False,sep='\t')
            elif self.u.tabWidget_2.currentIndex() == 1:
                print '--- Save chi files ---'
                if len(params.exafs) !=0:
                    dat_dir =  os.path.dirname(params.exafs[0].objectName())
                    FO_dialog = QtGui.QFileDialog(self)
                    file = FO_dialog.getSaveFileName(parent=None, dir=dat_dir,filter="chi files(*.dat)")
                    f = open(file[0],'w')
                    df = pd.DataFrame(columns=['#k'])
                    i = 0
                    b_name = os.path.basename(params.exafs[0].objectName())
                    for cb in params.exafs:
                        if cb.isChecked() and i == 0:
                            df['#k'] = params.data_and_conditions[b_name+':'+'k']
                            df.add_prefix('chi_'+b_name)
                            df['chi_'+b_name] = params.data_and_conditions[b_name+':'+'chi_k']
                            i += 1
                        elif cb.isChecked() and i > 0:
                            name = os.path.basename(cb.objectName())
                            df.add_prefix('chi_'+name)
                            k_interp = params.data_and_conditions[b_name+':'+'k']
                            t_k = params.data_and_conditions[name+':'+'k']
                            chi_interp = np.interp(k_interp,t_k,params.data_and_conditions[name+':'+'chi_k'])
                            df['chi_'+name] = chi_interp[:]
                            i += 1
                        else:
                            i += 1
                    df.to_csv(f,index=False,sep='\t')
            elif self.u.tabWidget_2.currentIndex() == 2:
                print '--- Save FT files ---'
                if len(params.exafs) !=0:
                    dat_dir =  os.path.dirname(params.exafs[0].objectName())
                    FO_dialog = QtGui.QFileDialog(self)
                    file = FO_dialog.getSaveFileName(parent=None, dir=dat_dir,filter="FT files(*.dat)")
                    f = open(file[0],'w')
                    df = pd.DataFrame(columns=['#r'])
                    i = 0
                    b_name = os.path.basename(params.exafs[0].objectName())
                    for cb in params.exafs:
                        if cb.isChecked() and i == 0:
                            df['#r'] = params.data_and_conditions[b_name+':'+'r']
                            df.add_prefix('FT_mag:'+b_name)
                            df['FT_mag:'+b_name] = params.data_and_conditions[b_name+':'+'ft_mag']
                            df.add_prefix('FT_im:'+b_name)
                            df['FT_im:'+b_name] = params.data_and_conditions[b_name+':'+'ft_im']
                            i += 1
                        elif cb.isChecked() and i > 0:
                            name = os.path.basename(cb.objectName())
                            df.add_prefix('FT_mag:'+name)
                            r_interp = params.data_and_conditions[b_name+':'+'r']
                            t_r = params.data_and_conditions[name+':'+'r']
                            ft_interp_mag = np.interp(r_interp,t_r,params.data_and_conditions[name+':'+'ft_mag'])
                            df['FT_mag:'+name] = ft_interp_mag[:]
                            df.add_prefix('FT_im:'+name)
                            ft_interp_im = np.interp(r_interp,t_r,params.data_and_conditions[name+':'+'ft_im'])
                            df['FT_im:'+name] = ft_interp_im[:]
                            i += 1
                        else:
                            i += 1
                    df.to_csv(f,index=False,sep='\t')




        self.u.EXAFSBK_type.currentIndexChanged.connect(comboBox_EXAFSBK_changed)
        self.u.pushButton_17.clicked.connect(open_exafs_files)
        self.u.pushButton_18.clicked.connect(add_exafs_files)
        self.u.pushButton_20.clicked.connect(func_pB20)
        self.u.tabWidget_2.currentChanged[int].connect(plot_exafs_chi_ft)
        self.u.pushButton_21.clicked.connect(plot_ft_)
        self.u.FT_kweight.currentIndexChanged.connect(plot_ft)
        self.u.pB_cp_to_all_EXAFS.clicked.connect(copy_current_to_all)
        self.u.pushButton_19.clicked.connect(Save_chi_ft)

        params.cBs_36XU = [self.u.BL36XU_ch1,self.u.BL36XU_ch2,self.u.BL36XU_ch3,self.u.BL36XU_ch4,self.u.BL36XU_ch5,
                           self.u.BL36XU_ch6,self.u.BL36XU_ch7,self.u.BL36XU_ch8,self.u.BL36XU_ch9,self.u.BL36XU_ch10,
                           self.u.BL36XU_ch11,self.u.BL36XU_ch12,self.u.BL36XU_ch13,self.u.BL36XU_ch14,self.u.BL36XU_ch15,
                           self.u.BL36XU_ch16,self.u.BL36XU_ch17,self.u.BL36XU_ch18,self.u.BL36XU_ch19,self.u.BL36XU_ch20,
                           self.u.BL36XU_ch21,self.u.BL36XU_ch22,self.u.BL36XU_ch23,self.u.BL36XU_ch24,self.u.BL36XU_ch25]
        params.colours5 = ["#FF0000","#0000FF","#00CC00","#FF007F","#000000"]
        #palette = self.u.frame.palette()
        for cb in params.cBs_36XU:
            cb.setAutoFillBackground(True)
            plt = cb.palette()
            j = params.cBs_36XU.index(cb)%5
            print j
            plt.setColor(cb.backgroundRole(), params.colours5[j])
            plt.setColor(cb.foregroundRole(), "#FFFFFF")
            cb.setPalette(plt)
            palette.setColor(cb.foregroundRole(), "Grey")

        params.BL36XU_ShapingTimes = ["no correction","C:0.5 us"]
        self.u.BL36XU_ST.addItems(params.BL36XU_ShapingTimes)
        self.u.BL36XU_ST.setCurrentIndex(0)
        self.u.BL36XU_Edge.addItems(["K","L"])
        self.u.BL36XU_rB_REX.toggle()

        fig_36XU_1 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax_36XU_1 = fig_36XU_1.add_subplot(111)
        ax_36XU_1.set_xlabel("E / eV")
        ax_36XU_1.set_ylabel("$\mu$ t")
        canvas_BL36XU_1 = FigureCanvas(fig_36XU_1)
        self.u.BL36XU_widget1.setLayout(params.grid6)
        BL36XU_navibar_1 = NavigationToolbar(canvas_BL36XU_1, self.u.BL36XU_widget1)
        params.grid6.addWidget(canvas_BL36XU_1, 0, 0)
        params.grid6.addWidget(BL36XU_navibar_1)

        fig_36XU_2 = Figure(figsize=(320, 320), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax_36XU_2 = fig_36XU_2.add_subplot(111)
        ax_36XU_2.set_xlabel("E / eV")
        ax_36XU_2.set_ylabel("$\mu$ t")
        canvas_BL36XU_2 = FigureCanvas(fig_36XU_2)
        self.u.BL36XU_widget2.setLayout(params.grid7)
        BL36XU_navibar_2 = NavigationToolbar(canvas_BL36XU_2, self.u.BL36XU_widget2)
        params.grid7.addWidget(canvas_BL36XU_2, 0, 0)
        params.grid7.addWidget(BL36XU_navibar_2)

        scroll_layout_36XU = QtGui.QVBoxLayout()
        scroll_widgets_36XU = QtGui.QWidget()
        scroll_widgets_36XU.setLayout(scroll_layout_36XU)
        self.u.scrollArea_17.setWidget(scroll_widgets_36XU)

        def plot_each_ch_36XU():
            conf = cwd + "/" + "BL36XU.conf"
            str_tconst = open(conf).read()
            DT = yaml.load(str_tconst)
            sum = np.zeros(len(params.Energy))
            while len(ax_36XU_1.lines) != 0:
                ax_36XU_1.lines.pop(0).remove
            while len(ax_36XU_2.lines) != 0:
                ax_36XU_2.lines.pop(0).remove

            for axis in [ax_36XU_1,ax_36XU_2]:
                axis.relim()
                axis.autoscale_view(True,True,True)

            if self.u.BL36XU_ST.currentText() == "no correction":
                for cb in params.cBs_36XU:
                    if cb.isChecked():
                        ut = np.divide(np.array(params.darray[params.cBs_36XU.index(cb)]), np.array(params.i0))
                        sum = np.add(sum, np.array(params.darray[params.cBs_36XU.index(cb)]))
                        ax_36XU_1.plot(params.Energy, ut, color=params.colours5[params.cBs_36XU.index(cb)%5])
            elif self.u.BL36XU_ST.currentText() != "no correction":
                params.mode = self.u.BL36XU_ST.currentText().split(":")[0]+"-Mode"
                #print self.u.BL36XU_ST.currentText().split(":")
                params.shaping_time = "us" + "{0:0>3}".format(int(float(self.u.BL36XU_ST.currentText().split(":")[1].split(" ")[0])*100.0))
                print params.shaping_time
                micro = math.pow(10, -6)
                #k = 0
                #while k < 25:
                t1 = float(DT[params.mode]["uni"]["preamp"])*micro
                print DT[params.mode]["uni"]["preamp"]
                t2 = float(DT[params.mode]["uni"]["amp"][params.shaping_time])*micro
                print DT[params.mode]["uni"]["amp"][params.shaping_time]
                for cb in params.cBs_36XU:
                    if cb.isChecked():
                        ut = np.divide(np.array(params.darray[params.cBs_36XU.index(cb)])*(1.0+t1*params.t_ICR[params.cBs_36XU.index(cb)])/(1.0-t2*params.t_ICR[params.cBs_36XU.index(cb)]), np.array(params.i0))
                        sum = np.add(sum, np.array(params.darray[params.cBs_36XU.index(cb)])*(1.0+t1*params.t_ICR[params.cBs_36XU.index(cb)])/(1.0-t2*params.t_ICR[params.cBs_36XU.index(cb)]))
                        ax_36XU_1.plot(params.Energy, ut, color=params.colours5[params.cBs_36XU.index(cb)%5])
                #    if params.cbs[k].isChecked():
                #        j = 0
                #        ut = np.zeros(len(params.Energy))
                #        while j < len(params.Energy):
                #            ut[j] = params.darray[k][j] * (
                #                1 + micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                #                    DT["PF"]["individual"]["preamp"][k])) / (
                #                        1 - micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                #                            DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #ut[j] = params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[j])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                #            sum[j] += params.darray[k][j] * (
                #                1 + micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                #                    DT["PF"]["individual"]["preamp"][k])) / (
                #                          1 - micro * float(params.ICR[j][k]) / float(params.aq_time[j]) * float(
                #                              DT["PF"]["individual"]["amp"][params.shaping_time][k]))
                            #sum[j] += params.darray[k][j]/(1-micro*float(params.ICR[j][k])/float(params.aq_time[j])*(float(DT["PF"]["individual"]["amp"][params.shaping_time][k])+float(DT["PF"]["individual"]["preamp"][k])))
                #            j += 1
                #        ax.plot(params.Energy, np.divide(ut, params.i0), color=params.colors[k])
                #    k += 1
            #params.grid.addWidget(canvas, 0, 0)
            #params.grid.addWidget(navibar_1)
            ax_36XU_2.plot(params.Energy, np.divide(sum, params.i0),color = "red")
            canvas_BL36XU_1.draw()
            canvas_BL36XU_2.draw()


        def read_dat_36XU(Test_Dat):
            params.ignore_or_not = []
            params.angles = []
            params.aq_time = []
            params.i0 = []
            params.dat = []
            params.ICR = []
            params.Energy = []
            params.darray = np.empty([1, 1])
            params.t_ICR = np.empty([1, 1])
            f = open(Test_Dat, "r")
            i = 0
            for line in f:
                line.rstrip()
                if re.match(r".+D=(.+)A.+", line):
                    params.D = float(re.match(r".+D=\s+(.+)\sA.+", line).group(1))
                    print str(params.D)
                elif re.match(r"\s+Angle\(c\).+", line):
                    t_array = line.split()
                #print t_array[0]
                elif re.match(r"\s+Mode", line):
                    t_array = line.split()
                    params.ignore_or_not = t_array[3:28]
                #print params.ignore_or_not
                elif re.match(r"\s+Offset", line):
                    pass
                elif len(line.split()) > 23:
                    t_array = line.split()
                    params.angles.append(t_array[1])
                    params.aq_time.append(float(t_array[2]))
                    params.i0.append(float(t_array[28]))
                    params.dat.append(t_array[3:28])
                    params.ICR.append(t_array[31:56])
                    #print t_array[31:56]
                #print i
                i += 1
            print params.aq_time
            k = 0
            while k < 25:
                if params.ignore_or_not[k] != "0":
                #print params.cbs[k].checkState()
                    params.cBs_36XU[k].setCheckState(QtCore.Qt.CheckState.Checked)
                elif params.ignore_or_not[k] == "0":
                    params.cBs_36XU[k].setEnabled(False)
                k += 1
            params.darray.resize(25, len(params.dat))
            params.t_ICR.resize(25, len(params.dat))
            k = 0
            while k < 25:
                j = 0
                while j < len(params.dat):
                    params.darray[k][j] = float(params.dat[j][k])
                    params.t_ICR[k][j] = float(params.ICR[j][k])
                    j += 1
                k += 1
            #print params.darray[1]
            j = 0
            while j < len(params.dat):
                E = 12398.52 / (2 * float(params.D) * np.sin(float(params.angles[j]) / 180 * np.pi))
                params.Energy.append(E)
                j += 1
            #print len(params.Energy)


        def select_or_release_all_36XU():
            checked_cb = []
            for cb in params.cBs_36XU:
                if cb.isChecked():
                    checked_cb.append(cb)
            if len(checked_cb) > 0:
                self.u.pushButton_5.setText("Select All")
                for cb in checked_cb:
                    cb.setCheckState(QtCore.Qt.CheckState.Unchecked)
            elif len(checked_cb) == 0:
                self.u.pushButton_5.setText("Release All")
                k = 0
                print len(params.ignore_or_not)
                while k < 25:
                    if params.ignore_or_not[k] != "0":
                        params.cBs_36XU[k].setCheckState(QtCore.Qt.CheckState.Checked)
                    elif params.ignore_or_not[k] == "0":
                        params.cBs_36XU[k].setEnabled(False)
                    k += 1
            plot_each_ch_36XU()

        def plot_36XU():
            params.current_dfile = ""
            params.current_ofile = ""
            for cb in params.cBs_36XU:
                cb.setEnabled(True)
                cb.setCheckState(QtCore.Qt.CheckState.Unchecked)
            for t_rb in params.d_rbs_36XU:
                if t_rb.isChecked():
                    params.current_dfile = params.dir + "/" + t_rb.objectName()
                    if re.match(r"(.+)\.\d+", t_rb.objectName()) is None:
                        #params.current_ofile = o_dir + "/" + t_rb.objectName() + "_000" + ".ex3"
                        break
                    elif re.match(r"(.+)\.(\d+)", t_rb.objectName()):
                        t_line = t_rb.objectName().split(".")
                        #params.current_ofile =o_dir + "/" + t_line[0] + "_" + t_line[1]  + ".ex3"
                        break
            read_dat_36XU(params.current_dfile)
            plot_each_ch_36XU()

        def func_for_rb_36XU():
            plot_36XU()
            self.u.BL36XU_RSall.setText("Release all")

        def openFiles_BL36XU():
            while scroll_layout_36XU.count() > 0:
                b = scroll_layout_36XU.takeAt(len(params.d_rbs_36XU) - 1)
                params.dfiles_36XU.pop()
                params.d_rbs_36XU.pop()
                b.widget().deleteLater()
            dat_dir = home_dir.homePath()
            if params.dir == "":
                dat_dir = home_dir.homePath()
            elif params.dir != "":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent=None, caption="", dir=dat_dir)
            finfo = QtCore.QFileInfo(files[0][0])
            params.dir = finfo.path()
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                params.dfiles_36XU.append(info.fileName())
            for d_file in params.dfiles_36XU:
                rb = QtGui.QRadioButton(d_file)
                rb.setObjectName(d_file)
                params.d_rbs_36XU.append(rb)
                scroll_layout_36XU.addWidget(rb)
            for t_rb in params.d_rbs_36XU:
                t_rb.toggled.connect(func_for_rb_36XU)
            #print scroll_layout_36XU.count()
            params.d_rbs_36XU[0].toggle()

        def define_outdir_36XU():
            self.u.BL36XU_textBrowser.clear()
            FO_dialog = QtGui.QFileDialog(self)
            params.outdir = FO_dialog.getExistingDirectory(parent=None, dir=params.dir)
            self.u.BL36XU_textBrowser.append(params.outdir)
            #if self.u.textBrowser_2.toPlainText() == "":
            #    self.u.textBrowser_2.append(params.outdir)

        def Save_36XU():
            conf = cwd + "/" + "BL36XU.conf"
            str_tconst = open(conf).read()
            DT = yaml.load(str_tconst)
            sum = np.zeros(len(params.Energy))
            ut = np.zeros(len(params.Energy))
            o_dir = params.dir
            exd = ""
            if self.u.BL36XU_rB_REX.isChecked():
                exd = ".ex3"
            else:
                exd = ".dat"
            if params.outdir == "":
                o_dir = params.dir
            elif os.path.exists(params.outdir):
                o_dir = params.outdir
            for t_rb in params.d_rbs_36XU:
                if t_rb.isChecked():
                    params.current_ofile = o_dir + "/" + t_rb.objectName() + exd
                    break
                else:
                    pass
            out = open(params.current_ofile, "w")
            if self.u.BL36XU_rB_REX.isChecked():
                line = "[EX_DATA]\n*DATE=\n*EX_SAMPLE=\n"
                atom = "*EX_ATOM=" + self.u.BL36XU_Atom.text() + "\n"
                edge = "*EX_EDGE=" + self.u.BL36XU_Edge.currentText() + "\n"
                line2 = "*EX_COMMENT=\n*EX_GONIO=\n*EX_ATTACHIMENT=\n*EX_TARGET=\n*EX_FILAMENT=\n*EX_MEASURE=\n*EX_I0_DETECTOR=\n*EX_I_DETECTOR=\n*EX_CRYSTAL=\n*EX_2D=\n*EX_KV=\n*EX_MA=\n*EX_SLIT_DS=\n*EX_SLIT_RS=\n*EX_SLIT_H=\n*EX_REPEAT=\n*EX_AREA1=\n*EX_AREA2=\n*EX_AREA3=\n*EX_AREA4=\n*EX_AREA5=\n"
                line3 = "\n[EX_BEGIN]\n"
                out.write(line + atom + edge + line2 + line3)
            else:
                out.write("#Energy  ut\n")
            if self.u.BL36XU_ST.currentText() == "no correction":
                for cb in params.cBs_36XU:
                    if cb.isChecked():
                        #ut = np.divide(np.array(params.darray[params.cBs_36XU.index(cb)]), np.array(params.i0))
                        sum = np.add(sum, np.array(params.darray[params.cBs_36XU.index(cb)]))
                        ax_36XU_1.plot(params.Energy, ut, color=params.colours5[params.cBs_36XU.index(cb)%5])
            elif self.u.BL36XU_ST.currentText() != "no correction":
                params.mode = self.u.BL36XU_ST.currentText().split(":")[0]+"-Mode"
                #print self.u.BL36XU_ST.currentText().split(":")
                params.shaping_time = "us" + "{0:0>3}".format(int(float(self.u.BL36XU_ST.currentText().split(":")[1].split(" ")[0])*100.0))
                print params.shaping_time
                micro = math.pow(10, -6)
                #k = 0
                #while k < 25:
                t1 = float(DT[params.mode]["uni"]["preamp"])*micro
                print DT[params.mode]["uni"]["preamp"]
                t2 = float(DT[params.mode]["uni"]["amp"][params.shaping_time])*micro
                print DT[params.mode]["uni"]["amp"][params.shaping_time]
                for cb in params.cBs_36XU:
                    if cb.isChecked():
                        #ut = np.divide(np.array(params.darray[params.cBs_36XU.index(cb)])*(1.0+t1*params.t_ICR[params.cBs_36XU.index(cb)])/(1.0-t2*params.t_ICR[params.cBs_36XU.index(cb)]), np.array(params.i0))
                        sum = np.add(sum, np.array(params.darray[params.cBs_36XU.index(cb)])*(1.0+t1*params.t_ICR[params.cBs_36XU.index(cb)])/(1.0-t2*params.t_ICR[params.cBs_36XU.index(cb)]))
                        ax_36XU_1.plot(params.Energy, ut, color=params.colours5[params.cBs_36XU.index(cb)%5])
            ut = np.divide(sum, params.i0)
            k = 0
            while k < len(params.Energy):
                str_ = "%7.3f  %1.8f\n" % (params.Energy[k], ut[k])
                out.write(str_)
                k += 1
            if self.u.BL36XU_rB_REX.isChecked():
                out.write("\n[EX_END]\n")
            else:
                pass

        self.u.BL36XU_Open.clicked.connect(openFiles_BL36XU)
        self.u.BL36XU_RSall.clicked.connect(select_or_release_all_36XU)
        self.u.BL36XU_outpath.clicked.connect(define_outdir_36XU)
        self.u.BL36XU_ST.currentIndexChanged.connect(plot_each_ch_36XU)
        self.u.BL36XU_Save.clicked.connect(Save_36XU)
        for cb in params.cBs_36XU:
            cb.clicked.connect(plot_each_ch_36XU)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wid = MainWindow()
    sys.exit(app.exec_())
