#! /Users/uemura/Build/bin/python
import sys
import os
import string
import glob
import re
import yaml
import math
import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import pandas as PD
import shutil


from PySide import QtCore, QtGui
if 'win' in sys.platform:
    from UI_ppXAFS_win import Ui_MainWindow
else:
    from UI_ppXAFS import Ui_MainWindow
from textBrowser import Ui_Form

home_dir = QtCore.QDir()

#import progressbar as PB
import csv
#import h5py
#import time

class params:
    rbs = QtGui.QButtonGroup()
    rbs_ts = QtGui.QButtonGroup()
    cbs = []
    dfiles = []
    dir = ""
    mt_star_plus_c = []
    mt_plus_c = []
    delta_mt_plus = []
    mt_star_minus_c = []
    mt_minus_c = []
    delta_mt_minus = []
    cbs_t = []
    energy = []
    sumI0 = []
    sumI1 = []
    sumI2 = []
    mt = []
    mt_star = []
    delta_mt = []
    OR = "#FF4500"
    chi_data = []
    chi_cb = []
    colors = ["OrangeRed", "Blue", "Brown", "Chartreuse", "Coral", "Crimson", "DarkGreen", "DarkBlue", "DarkMagenta", "DarkRed",
              "DeepPink", "FireBrick", "GoldenRod", "Grey", "GreenYellow", "Indigo", "LightCoral", "MediumBlue",
              "MediumVioletRed"]



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self,parent)
        self.u = Ui_MainWindow()
        self.u.setupUi(self)
        self.textBrowser = Ui_Form()
        self.popup = QtGui.QDialog(self)
        self.textBrowser.setupUi(self.popup)
        self.popup.setParent(self)

        scroll_layout = QtGui.QVBoxLayout()
        scroll_widgets = QtGui.QWidget()
        scroll_widgets.setLayout(scroll_layout)
        self.u.scrollArea.setWidget(scroll_widgets)

        scroll_layout2 = QtGui.QVBoxLayout()
        scroll_widgets2 = QtGui.QWidget()
        scroll_widgets2.setLayout(scroll_layout2)
        self.u.scrollArea_2.setWidget(scroll_widgets2)

        self.u.pushButton_2.setText('Release All')

        #grid3.itemAt(0)
        self.grid = QtGui.QGridLayout()
        fig = Figure(figsize=(320, 320), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0),tight_layout=True)
        ax = fig.add_subplot(111)
        ax.set_xlabel("Energy / eV")
        ax.set_ylabel("$\mu$ t")
        ax_right = ax.twinx()
        ax_right.set_ylabel("$\Delta\mu$ t")
        canvas = FigureCanvas(fig)
        self.u.widget.setLayout(self.grid)
        self.grid.addWidget(canvas,0,0)
        navibar_0 = NavigationToolbar(canvas, self.u.widget)
        self.u.widget.setLayout(self.grid)
        self.grid.addWidget(canvas,0,0)
        self.grid.addWidget(navibar_0)

        self.grid3 = QtGui.QGridLayout()
        fig3 = Figure(figsize=(320, 320), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax4 = fig3.add_subplot(121)
        ax4.set_xlabel("t / ps")
        ax4.set_ylabel("$\mu$ t")
        ax4.set_title('Data')
        ax5 = fig3.add_subplot(122)
        ax5.set_xlabel("t / ps")
        ax5.set_ylabel("$\mu$ t")
        ax5.set_title('Sum')
        canvas3 = FigureCanvas(fig3)
        navibar_1 = NavigationToolbar(canvas3, self.u.widget_3)
        self.u.widget_3.setLayout(self.grid3)
        self.grid3.addWidget(canvas3,0,0)
        self.grid3.addWidget(navibar_1)

        self.gridI0 = QtGui.QGridLayout()
        fig_I0 = Figure(figsize=(320, 320), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0),tight_layout=True)
        canvasI0 = FigureCanvas(fig_I0)
        ax_I0 = fig_I0.add_subplot(211)
        ax_I0.set_xlabel("Energy / eV")
        ax_I0.set_ylabel("Intensity")
        ax_I0.set_title('I0')
        ax_ut = fig_I0.add_subplot(212)
        ax_ut.set_xlabel("Energy / eV")
        ax_ut.set_ylabel("$\mu$ t")
        ax_ut.set_title('Absorption')
        ax_dut = ax_ut.twinx()
        ax_dut.set_ylabel("$\Delta\mu$ t")
        self.u.widget_2.setLayout(self.gridI0)
        self.gridI0.addWidget(canvasI0,0,0)


        navibar_2 = NavigationToolbar(canvasI0, self.u.widget_2)
        self.u.widget_2.setLayout(self.gridI0)
        self.gridI0.addWidget(canvasI0,0,0)
        self.gridI0.addWidget(navibar_2)


        params.spinBoxes = [self.u.spinBox,self.u.spinBox_2,self.u.spinBox_3,self.u.spinBox_4]
        for sB in params.spinBoxes:
            sB.setMinimum(0)

        def makeplots(xlabel,ylabel):
            fig = Figure(figsize=(170, 120), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
            ax = fig.add_subplot(111)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            canvas = FigureCanvas(fig)
            return ax, canvas


        def plotXANES():
            #print len(params.cbs)
            axis = [ax,ax_right]
            for ax_ in axis:
                while len(ax_.lines) !=0:
                    ax_.lines.pop()
            if len(params.cbs) != 0:
                params.energy = []
                i = 0
                for cb in params.cbs:
                    if cb.isChecked():
                        switch = "not read"
                        print cb.objectName()
                        Fdat = open(cb.objectName(),"rU")
                        I0 = []
                        I1 = []
                        I2 = []
                        for line in Fdat:
                            line.rstrip()
                            t_array = line.split()
                            if switch == "not read":
                                switch = "read"
                            elif switch == "read":
                                I0.append(float(t_array[3]))
                                I1.append(float(t_array[4]))
                                I2.append(float(t_array[5]))
                                if i == 0:
                                    params.energy.append(float(t_array[0]))
                        if i == 0:
                            params.sumI0 = np.zeros(len(I0))
                            params.sumI1 = np.zeros(len(I0))
                            params.sumI2 = np.zeros(len(I0))
                            params.mt = np.zeros(len(I0))
                            params.mt_star = np.zeros(len(I0))
                            params.delta_mt = np.zeros(len(I0))
                            if params.spinBoxes[0].maximum() != len(I0)-1:
                                for sB in params.spinBoxes:
                                    sB.setMaximum(len(I0)-1)
                                self.u.spinBox.setValue(0)
                                self.u.spinBox_2.setValue(4)
                                self.u.spinBox_3.setValue(self.u.spinBox_3.maximum()-4)
                                self.u.spinBox_4.setValue(self.u.spinBox_4.maximum())
                        params.sumI0 += np.array(I0)
                        params.sumI1 += np.array(I1)
                        params.sumI2 += np.array(I2)
                        print len(params.energy)
                        print len(I0)
                        i +=1
                print "sB1, sB2, sB3, sB4 =" + str(self.u.spinBox.value()) +","+ str(self.u.spinBox_2.value()) +","+ str(self.u.spinBox_3.value()) +","+ str(self.u.spinBox_4.value())
                ut_star = params.sumI1/params.sumI0
                ut_star_temp = (ut_star - np.average(ut_star[self.u.spinBox.value():self.u.spinBox_2.value()+1]))
                params.mt_star = ut_star_temp/np.average(ut_star_temp[self.u.spinBox_3.value():self.u.spinBox_4.value()+1])
                ut_ = params.sumI2/params.sumI0
                ut_temp = (ut_ - np.average(ut_[self.u.spinBox.value():self.u.spinBox_2.value()+1]))
                params.mt = ut_temp/np.average(ut_temp[self.u.spinBox_3.value():self.u.spinBox_4.value()+1])
                ax.plot(params.energy,params.mt_star,color='b',label='$\mu t^*$')
                ax.plot(params.energy,params.mt,color='k',label='$\mu t$')
                params.delta_mt = params.mt_star - params.mt
                ax_right.plot(params.energy,params.delta_mt,"ro-")
                ax.legend(loc=4)
                for ax_ in [ax,ax_right]:
                    ax_.relim()
                    ax_.autoscale_view()
                canvas.draw()

        def plot_each_XANES():
            #print len(params.cbs)
            axis = [ax_I0,ax_ut,ax_dut]
            for ax_ in axis:
                while len(ax_.lines) !=0:
                    ax_.lines.pop()
            if len(params.cbs) != 0:
                params.energy = []
                i = 0
                for rb in params.rbs.buttons():
                    if rb.isChecked():
                        switch = "not read"
                        #print rb.objectName()
                        Fdat = open(rb.objectName(),"rU")
                        I0 = []
                        I1 = []
                        I2 = []
                        for line in Fdat:
                            line.rstrip()
                            t_array = line.split()
                            if switch == "not read":
                                switch = "read"
                            elif switch == "read":
                                I0.append(float(t_array[3]))
                                I1.append(float(t_array[4]))
                                I2.append(float(t_array[5]))
                                if i == 0:
                                    params.energy.append(float(t_array[0]))
                        ax_I0.plot(params.energy,I0,color='k')
                        t_ut = np.array(I1)/np.array(I0)
                        t_ut_corr = (t_ut - np.average(t_ut[self.u.spinBox.value():self.u.spinBox_2.value()+1]))
                        ut_star = t_ut_corr/np.average(t_ut_corr[self.u.spinBox_3.value():self.u.spinBox_4.value()+1])
                        ax_ut.plot(params.energy,ut_star,color='r',label='$ut^*$')
                        t_ut = np.array(I2)/np.array(I0)
                        t_ut_corr = (t_ut - np.average(t_ut[self.u.spinBox.value():self.u.spinBox_2.value()+1]))
                        ut = t_ut_corr/np.average(t_ut_corr[self.u.spinBox_3.value():self.u.spinBox_4.value()+1])
                        ax_ut.plot(params.energy,ut,color='b',label='$ut$')
                        ax_ut.legend()
                        ax_dut.plot(params.energy,ut_star-ut,color='b',label='$\Delta ut$')
                        for ax_ in axis:
                            ax_.relim()
                            ax_.autoscale_view()
                        canvasI0.draw()
                        break
                    else:
                        pass
                        print 'no plot'


        def openFiles():
            params.sumI0 = []
            params.sumI1 = []
            params.sumI2 = []
            while scroll_layout.count() >0:
                b = scroll_layout.takeAt(len(params.cbs)-1)
                params.cbs.pop()
                params.rbs.removeButton(params.rbs.buttons()[0])
                b.widget().deleteLater()
            if params.dir=="":
                dat_dir = home_dir.homePath()
            elif params.dir!="":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent = None,caption="",dir=dat_dir)
            finfo = QtCore.QFileInfo(files[0][0])
            params.dir = finfo.path()
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                cb = QtGui.QCheckBox(info.fileName())
                cb.setObjectName(fname)
                params.cbs.append(cb)
                cb.toggle()
                cb.clicked.connect(plotXANES)
                rb = QtGui.QRadioButton()
                rb.setObjectName(fname)
                rb.toggled.connect(plot_each_XANES)
                params.rbs.addButton(rb)
                widget = QtGui.QWidget()
                hlayout = QtGui.QHBoxLayout()
                widget.setLayout(hlayout)
                hlayout.addWidget(cb)
                hlayout.addWidget(rb)
                scroll_layout.addWidget(widget)
            params.rbs.buttons()[0].toggle()
            plotXANES()

        def Save_ut():
            if params.dir=="":
                dat_dir = home_dir.homePath()
            elif params.dir!="":
                dat_dir = params.dir
            if len(params.mt_star) != 0:
                print "Save"
            F0_dialog = QtGui.QFileDialog(self)
            file = F0_dialog.getSaveFileName(parent = None,caption="",dir=dat_dir)
            fout = open(file[0],"wb")
            title = ['#Energy', 'ut*', 'ut', 'delta_ut']
            writer = csv.writer(fout, delimiter=' ')
            M = [['#Energy']+params.energy[:],['ut*']+params.mt_star.tolist()[:],['ut']+params.mt.tolist()[:],['delta_ut']+params.delta_mt.tolist()[:]]
            for term in zip(*M):
                writer.writerow(term)
            fout.close()
            fout = open(file[0].split('.')[0]+"_raw"+"."+file[0].split('.')[1],"wb")
            writer = csv.writer(fout, delimiter=' ')
            ut_star = params.sumI1/params.sumI0
            ut = params.sumI2/params.sumI0
            M = [['#Energy']+params.energy[:],['ut*']+ut_star.tolist()[:],['ut']+ut.tolist()[:]]
            for term in zip(*M):
                writer.writerow(term)
            fout.close()

        def selectAll():
            if len(params.cbs) != 0:
                for cb in params.cbs:
                    if cb.isChecked():
                        pass
                    else:
                        cb.toggle()
            plotXANES()

        def calcDecay():
            if len(params.cbs_t) != 0:
                params.t = []
                params.dict_mt_star={}
                params.dict_mt={}
                for cb in params.cbs_t:
                    switch = "not read"
                    print cb.objectName()
                    Fdat = open(cb.objectName(),"rU")
                    t_ = []
                    mt_star = []
                    mt_ = []
                    for line in Fdat:
                        line.rstrip()
                        t_array = line.split()
                        if switch == "not read":
                            switch = "read"
                        elif switch == "read":
                            t_.append(float(t_array[2]))
                            mt_star.append(float(t_array[6]))
                            mt_.append(float(t_array[7]))
                    if len(params.t) == 0:
                        if len(t_)%2 == 0:
                            params.t = t_[0:(len(t_)/2)]
                        elif len(t_)%2 == 1:
                            params.t = t_[0:((len(t_)-1)/2)]
                    #print mt_star
                    if len(t_)%2 == 0:
                        mt_star_shalf = mt_star[(len(mt_star)/2):len(mt_star)]
                        mt_star_shalf.reverse()
                        mt_star_fhalf = mt_star[0:(len(mt_star)/2)]
                        mt_star_sum = np.add(mt_star_fhalf,mt_star_shalf)
                        mt_shalf = mt_[len(mt_star)/2:len(mt_star)]
                        mt_shalf.reverse()
                        mt_fhalf = mt_[0:len(mt_star)/2]
                        mt_sum = np.add(mt_fhalf,mt_shalf)
                    elif len(t_)%2 == 1:
                        mt_star_shalf = mt_star[((len(mt_star)+1)/2):(len(mt_star))]
                        mt_star_shalf.reverse()
                        print len(mt_star_shalf)
                        mt_star_fhalf = mt_star[0:len(mt_star_shalf)]
                        print len(mt_star_fhalf)
                        mt_star_sum = np.add(mt_star_fhalf,mt_star_shalf)
                        mt_shalf = mt_[((len(mt_)+1)/2):len(mt_)]
                        mt_shalf.reverse()
                        mt_fhalf = mt_[0:len(mt_shalf)]
                        mt_sum = np.add(mt_fhalf,mt_shalf)
                    print len(params.t)
                    params.dict_mt_star[cb] = mt_star_sum
                    params.dict_mt[cb] = mt_sum
                    #cb.clicked.connect(plotDecay)

        def plotDecay():
            while len(ax5.lines) != 0:
                ax5.lines.pop(0)
            sum_mt_star = []
            sum_mt = []
            for key in params.dict_mt_star.keys():
                if key.isChecked():
                    if len(sum_mt_star) == 0:
                        for term in params.dict_mt_star[key]:
                            sum_mt_star.append(term)
                    elif len(sum_mt_star) != 0:
                        i = 0
                        while i < len(params.dict_mt_star[key]):
                            sum_mt_star[i] += params.dict_mt_star[key][i]
                            i += 1
            for key in params.dict_mt.keys():
                if key.isChecked():
                    if len(sum_mt) == 0:
                        for term in params.dict_mt[key]:
                            sum_mt.append(term)
                    elif len(sum_mt) != 0:
                        i = 0
                        while i < len(params.dict_mt[key]):
                            sum_mt[i] += params.dict_mt[key][i]
                            i += 1
            ax5.plot(params.t,sum_mt_star,'ro-',label='pumped')
            ax5.plot(params.t,sum_mt,'bs-',label='unpumped')
            ax5.relim()
            ax5.autoscale_view()
            ax5.legend(loc=4)
            canvas3.draw()

        def Save_TimeDecay():
            if params.dir=="":
                dat_dir = home_dir.homePath()
            elif params.dir!="":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getSaveFileName(parent = None,caption="",dir=dat_dir)
            finfo = QtCore.QFileInfo(files[0])
            params.dir = finfo.path()
            filename = finfo.fileName()
            sum_mt_star = []
            sum_mt = []
            out_mt_star = []
            out_mt = []
            measurements = []
            for key in params.dict_mt_star.keys():
                if key.isChecked():
                    measurements.append(key)
                    out_mt_star.append(params.dict_mt_star[key])
                    out_mt.append(params.dict_mt[key])
                    if len(sum_mt_star) == 0:
                        for term in params.dict_mt_star[key]:
                            sum_mt_star.append(term)
                    elif len(sum_mt_star) != 0:
                        i = 0
                        while i < len(params.dict_mt_star[key]):
                            sum_mt_star[i] += params.dict_mt_star[key][i]
                            i += 1
            for key in params.dict_mt.keys():
                if key.isChecked():
                    if len(sum_mt) == 0:
                        for term in params.dict_mt[key]:
                            sum_mt.append(term)
                    elif len(sum_mt) != 0:
                        i = 0
                        while i < len(params.dict_mt[key]):
                            sum_mt[i] += params.dict_mt[key][i]
                            i += 1
            out = open(params.dir+'/'+filename,"wb")
            title = ['#time','ut*','ut']
            writer = csv.writer(out, delimiter=' ')
            writer.writerow(title)
            M = [params.t,sum_mt_star,sum_mt]
            for term in zip(*M):
                writer.writerow(term)
            out.close()
            dat_mt_star =[]
            dat_mt = []
            for key in measurements:
                array = [key.objectName()]
                for term in out_mt_star[measurements.index(key)]:
                    array.append(str(term))
                dat_mt_star.append(array)
                array = [key.objectName()]
                for term in out_mt_star[measurements.index(key)]:
                    array.append(str(term))
                dat_mt.append(array)
            out = open(params.dir+'/'+'mt_star.csv',"wb")
            time = ['time'] + params.t[:]
            M = [time]
            for array in dat_mt_star:
                M.append(array)
            writer = csv.writer(out, delimiter=' ')
            for term in zip(*M):
                writer.writerow(term)
            out.close()
            out = open(params.dir+'/'+'mt_.csv',"wb")
            M = [time]
            for array in dat_mt:
                M.append(array)
            writer = csv.writer(out, delimiter=' ')
            for term in zip(*M):
                writer.writerow(term)
            out.close()

        def plot_each_Delay():
            while len(ax4.lines) != 0:
                ax4.lines.pop()
            objName = ""
            for rb in params.rbs_ts.buttons():
                if rb.isChecked():
                    objName = rb.objectName()
                    break
            for cb in params.cbs_t:
                if cb.objectName() == objName:
                    print params.t
                    print params.dict_mt_star[cb]
                    ax4.plot(params.t,params.dict_mt_star[cb],'-', marker = 'o',color=params.OR,label='pumped')
                    ax4.plot(params.t,params.dict_mt[cb],'bo-',label='unpumped')
                    break
                else:
                    pass
            ax4.autoscale_view()
            ax4.relim()
            ax4.legend(loc=4)
            canvas3.draw()

        def openFiles_TimeDecay():
            while scroll_layout2.count() >0:
                b = scroll_layout2.takeAt(len(params.cbs_t)-1)
                params.cbs_t.pop()
                params.rbs_ts.removeButton(params.rbs_ts.buttons()[0])
                b.widget().deleteLater()
            checkDecay()
            if params.dir=="":
                dat_dir = home_dir.homePath()
            elif params.dir!="":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            files = FO_dialog.getOpenFileNames(parent = None,caption="",dir=dat_dir)
            finfo = QtCore.QFileInfo(files[0][0])
            params.dir = finfo.path()
            for fname in files[0]:
                info = QtCore.QFileInfo(fname)
                cb = QtGui.QCheckBox(info.fileName())
                cb.setObjectName(fname)
                rb = QtGui.QRadioButton()
                rb.setObjectName(fname)
                widget = QtGui.QWidget()
                hlayout = QtGui.QHBoxLayout()
                widget.setLayout(hlayout)
                cb.clicked.connect(plotDecay)
                params.cbs_t.append(cb)
                hlayout.addWidget(cb)
                cb.toggle()
                rb.toggled.connect(plot_each_Delay)
                params.rbs_ts.addButton(rb)
                hlayout.addWidget(rb)
                scroll_layout2.addWidget(widget)
            calcDecay()
            plotDecay()
            params.rbs_ts.buttons()[0].toggle()

        def checkDecay():
            if len(params.cbs_t) != 0:
                fname = params.dir +"/"+"I0.csv"
                f_I0 = open(fname, "w")
                fname = params.dir +"/"+"mt_star.csv"
                f_mt_star = open(fname, "w")
                fname = params.dir +"/"+"mt.csv"
                f_mt = open(fname,"w")
                for cb in params.cbs_t:
                    Fdat = open(cb.objectName(),"rU")
                    info = os.path.basename(cb.objectName())
                    t_ = []
                    t_I0 = []
                    t_mt_star = []
                    t_mt = []
                    for line in Fdat:
                        if re.match(r"^energy",line):
                            print "here!"
                            pass
                        else:
                            line.rstrip()
                            t_array = line.split()
                            t_.append(t_array[1])
                            t_I0.append(t_array[3])
                            t_mt_star.append(t_array[6])
                            t_mt.append(t_array[7])
                    I0 = []
                    mt_star = []
                    mt = []
                    if len(t_)%2 == 0:
                        print "the length of t is even"
                        i = 0
                        half = len(t_)/2
                        while i < half:
                            I0.append(float(t_I0[i])+float(t_I0[len(t_)-1-i]))
                            mt_star.append(float(t_mt_star[i])+float(t_mt_star[len(t_)-1-i]))
                            mt.append(float(t_mt[i])+float(t_mt[len(t_)-1-i]))
                            i += 1
                    elif len(t_)%2 == 1:
                        i = 0
                        half = (len(t_)-1)/2
                        while i < half-1:
                            I0.append(float(t_I0[i])+float(t_I0[len(t_)-1-i]))
                            mt_star.append(float(t_mt_star[i])+float(t_mt_star[len(t_)-1-i]))
                            mt.append(float(t_mt[i])+float(t_mt[len(t_)-1-i]))
                            i += 1
                    text = info+", "
                    for term in I0:
                        text += str(term) +","
                    f_I0.write(text+"\n")
                    text = info+", "
                    for term in mt_star:
                        text += str(term) +","
                    f_mt_star.write(text+"\n")
                    text = info+", "
                    for term in mt:
                        text += str(term) +","
                    f_mt.write(text+"\n")


        def release_all():
            num = 0
            if len(params.cbs_t) != 0:
                for cb in params.cbs_t:
                    if cb.isChecked():
                        num += 1
            print num
            if num >= 1 and self.u.pushButton_2.text() == "Release All":
                for cb in params.cbs_t:
                    cb.setCheckState(QtCore.Qt.Unchecked)
                self.u.pushButton_2.setText("Select All")
                print self.u.pushButton_2.text()
            elif len(params.cbs_t) > num and self.u.pushButton_2.text() == "Select All":
                for cb in params.cbs_t:
                    cb.setCheckState(QtCore.Qt.Checked)
                self.u.pushButton_2.setText("Release All")

        def changePage():
            self.u.stackedWidget.setCurrentIndex(self.u.comboBox.currentIndex())

        scroll_layout_exafs = QtGui.QVBoxLayout()
        scroll_widgets_exafs = QtGui.QWidget()
        scroll_widgets_exafs.setLayout(scroll_layout_exafs)
        self.u.scrollArea_3.setWidget(scroll_widgets_exafs)
        self.u.rB_kpower0.setChecked(QtCore.Qt.Checked)

        self.grid_chi = QtGui.QGridLayout()
        fig_chi = Figure(figsize=(320, 640), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax_chi = fig_chi.add_subplot(121)
        ax_chi.set_xlabel("k / \AA^-1")
        ax_chi.set_ylabel("k^x*$\chi$(k)")
        ax_chi.set_title('chi_k')
        ax_ft = fig_chi.add_subplot(122)
        ax_ft.set_xlabel("r / \AA")
        ax_ft.set_ylabel("FT[k^x*$\chi$(k)]")
        ax_ft.set_title('FT')
        canvas_chi = FigureCanvas(fig_chi)
        navibar_chi = NavigationToolbar(canvas_chi, self.u.widget_4)
        self.u.widget_4.setLayout(self.grid_chi)
        self.grid_chi.addWidget(canvas_chi,0,0)
        self.grid_chi.addWidget(navibar_chi)

        def open_chi():
            self.textBrowser.textBrowser.clear()
            self.textBrowser.textBrowser_2.clear()
            if params.dir=="":
                dat_dir = home_dir.homePath()
            elif params.dir!="":
                dat_dir = params.dir
            FO_dialog = QtGui.QFileDialog(self)
            file = FO_dialog.getOpenFileName(parent = None,filter ="chi file (*.chi *.dat)", caption="",dir=dat_dir)
            if file[0] == "":
                pass
            else:
                f = open(file[0],'r')
                self.textBrowser.textBrowser_2.append(file[0])
                i = 1
                for line in f:
                    self.textBrowser.textBrowser.append(str(i)+": "+line.rstrip()+"\n")
                    i += 1
                self.textBrowser.spinBox.setMaximum(i-1)
                self.textBrowser.textBrowser.moveCursor(QtGui.QTextCursor.Start)
                self.popup.exec_()

        def read_chi():
            for comb in [self.u.comBox_Pos, self.u.comBox_Neg]:
                while comb.count() > 0:
                    comb.removeItem(comb.takeAt(comb.count()-1))
            while scroll_layout_exafs.count() >0:
                b = scroll_layout_exafs.takeAt(scroll_layout_exafs.count()-1)
                params.chi_cb.pop()
                b.widget().deleteLater()
            params.chi_data =[]
            num = self.textBrowser.spinBox.value()-1
            chi = PD.read_csv(self.textBrowser.textBrowser_2.toPlainText(), header=num, delim_whitespace=True)
            i = 0
            map = {}
            while i < len(list(chi)):
                if i+1 == len(list(chi)):
                    map[list(chi)[i]] = list(chi)[0]
                else:
                    map[list(chi)[i]] = list(chi)[i+1]
                i += 1
            #print map
            #print params.chi
            params.chi = chi.rename(columns=map)
            #print params.chi
            for key in list(params.chi):
                if re.match(r"k",key):
                    pass
                elif re.match(r"#",key):
                    params.chi.pop(key)
                else:
                    cb = QtGui.QCheckBox(key)
                    cb.setObjectName(key)
                    cb.clicked.connect(plot_chi)
                    scroll_layout_exafs.addWidget(cb)
                    params.chi_cb.append(cb)
                    params.chi_data.append(key)
            print list(params.chi)
            self.u.comBox_Pos.addItems(params.chi_data)
            print self.u.comBox_Pos.currentIndex()
            self.u.comBox_Neg.addItems(params.chi_data)
            self.u.comBox_Neg.setCurrentIndex(1)
            self.popup.done(1)

        def plot_chi():
            if params.chi_data != []:
                i = 0
                kweight = 0
                for rB in [self.u.rB_kpower0,self.u.rB_kpower1,self.u.rB_kpower2,self.u.rB_kpower3]:
                    if rB.isChecked():
                        kweight = float(rB.text())
                print kweight
                while len(ax_chi.lines) !=0:
                        ax_chi.lines.pop()
                for cb in params.chi_cb:
                    if cb.isChecked():
                        ax_chi.plot(params.chi["k"],(params.chi["k"]**(kweight))*params.chi[cb.objectName()],label=cb.objectName(),color=params.colors[params.chi_cb.index(cb)])
                    i += 1
                #print params.chi["k"]
                ax_chi.autoscale_view()
                ax_chi.relim()
                canvas_chi.draw()



        self.u.pushButton_7.clicked.connect(openFiles_TimeDecay)
        self.u.pushButton_2.clicked.connect(release_all)
        self.u.pushButton_9.clicked.connect(Save_TimeDecay)
        self.u.pushButton.clicked.connect(openFiles)
        self.u.pushButton_13.clicked.connect(Save_ut)
        self.u.pushButton_11.clicked.connect(plotXANES)
        self.u.pushButton_10.clicked.connect(selectAll)
        self.u.pB_openchi.clicked.connect(open_chi)
        self.textBrowser.pushButton.clicked.connect(read_chi)
        for rB in [self.u.rB_kpower0,self.u.rB_kpower1,self.u.rB_kpower2,self.u.rB_kpower3]:
            rB.clicked.connect(plot_chi)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wid = MainWindow()
    sys.exit(app.exec_())
