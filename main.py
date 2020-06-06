#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Control-Program-Editor-CNC-Ver.3.0.1
import csv,sys,os
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from numpy import math
from PyQt5.Qt import Qt
import datetime
"""

"""
WiZubValue=False
WiVpadinaValue=False
WiEvolventValue=False
n:int=0
ValkosZub=True
ValNaklon=True
#Основное окно
class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        # Фаил формы
        uic.loadUi("Window.ui",self)
        # Заголовок 
        self.setWindowTitle("Control Program Editor CNC. Pre-Alpha Ver.3.0.1 ")
        #ициализируем переменную имя файла 
        self.fileName = ""
        #имя файла по умолчанию 
        self.fname = "Liste"
        #Таблица
        item = QtGui.QStandardItem()
        self.model =  QtGui.QStandardItemModel(self)
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
    #   self.model.dataChanged.connect(self.finishedEdit)
        self.tableView.setModel(self.model)
        self.tableView.setShowGrid(True)
        self.tableView.resizeColumnsToContents()
        # Кнопки 
        self.WriteCsv_Button.clicked.connect(self.WriteCsv)
        self.Add_Row_Button.clicked.connect(self.AddRow)
        self.Remove_Row_Button.clicked.connect(self.RemoveRow)
        self.NewFile_Button.clicked.connect(self.NewFile)
        #self.Print_Button.clicked.connect(self.HandlePrint)
        #self.Wi_print_Button.clicked.connect(self.HandlePreview)
        #self.Change_Button.clicked.connect(self. WriteFileList)
        #self.WriteFile_CProg_Button.clicked.connect(self.СontrolProgPrint)
        self.GenerateProgramButon.clicked.connect(self.GenerateControlProg)
        self.Button_Open_File.clicked.connect(self.Open_File)
       
        self.Build_evolvent_Button.clicked.connect(self.ClearGrafik)
        self.Build_evolvent_Button.clicked.connect(self.Evolvent)  
        #выбираем чекбоксы
        self.checkBoxKoc.stateChanged.connect(self.Kos)
        self.checkBoxKosLev.stateChanged.connect(self.Naklon)
        self.checkBoxZub.stateChanged.connect(self.WiZub)
        self.checkBoxVpadina.stateChanged.connect(self.WiVpadina)
        self.checkBoxEvolvent.stateChanged.connect(self.WiEvolvent)

    def Evolvent(self):
        #Расчет эвольветы зуба 
        # Читаем данные из полей формы
        # z = Количество зубьев
        z = self.doubleSpinBox_Z.value() 
        # m = Модуль зуба
        m = self.doubleSpinBox_m.value() 
        # a = Угол главного профиля
        a = self.doubleSpinBox_a.value()
        #b = Угол наклона зубьев
        b = self.doubleSpinBox_b.value()
        #ha = Коэффициент высоты головки
        ha = self.doubleSpinBox_ha.value()
        #pf = К-т радиуса кривизны переходной кривой
        pf = self.doubleSpinBox_pf.value()
        #c = Коэффициент радиального зазора
        c = self.doubleSpinBox_c.value()
        #x = К-т смещения исходного контура
        x = self.doubleSpinBox_x.value()
        #y =Коэффициент уравнительного смещения
        y = self.doubleSpinBox_y.value()
        # n= Количество точек (точность построения)
        n=int(self.doubleSpinBox_n.value())
        # заполня переменные 
        # Делительный диаметр
        d = z * m
        # Высота зуба h=
        h = 2.25 * m
        # Высота головки ha =
        hav = m
        # Высота ножки hf=
        hf = 1.25 * m
        #Диаметр вершин зубьев
        da = d + (2 * m)*(ha+x+y)
        #Диаметр впадин (справочно)
        df = d -(2 * hf)
        #Окружной шаг зубьев Pt=
        pt = math.pi * m
        #Окружная толщина зуба St=
        St = 0.5 * pf
        #Угол профиля
        at = math.ceil(math.degrees( math.atan( math.tan(math.radians(a))
            /math.cos( math.radians(b)))))
        # Диаметр основной окружности
        db = d*math.cos(math.radians(at)) 
        #Делительный диаметр
        D  = 2 * m * ( ( z/( 2 * math.cos(math.radians(b)) )-(1-x)) ** 2 +
            ((1-x)/math.tan(math.radians(at)))**2)**0.5
        #Промежуточные данные
        yi = math.pi/2-math.radians(at)

        hy = yi/(n-1)

        x0 = math.pi/(4*math.cos(math.radians(b))
             )+pf*math.cos(math.radians(at))+math.tan(math.radians(at))

        y0 = 1-pf*math.sin(math.radians(at))-x

        C  = (math.pi/2+2*x*math.tan(math.radians(a))
             )/z+math.tan(math.radians(at))-math.radians(at)
        #Расчетный шаг точек эвольвенты
        hdy = (da-D)/(n-1)
        dyi = da
        fi = 2*math.cos(math.radians(b))/z*(x0+y0*math.tan(yi))
    #Заполняем текстовые поля в форме
        # Делительный диаметр
        self.lineEdit_d.setText(str(d))
        # Высота зуба h=
        self.lineEdit_h.setText(str(h))
        # Высота головки ha =
        self.lineEdit_ha.setText(str(hav))
        # Высота ножки hf=
        self.lineEdit_hf.setText(str(hf))
        # Диаметр вершин зубьев
        self.lineEdit_da.setText(str(da))
        # Диаметр впадин (справочно)
        self.lineEdit_df.setText(str(df))
        # Окружной шаг зубьев Pt=
        self.lineEdit_Pt.setText(str(math.ceil(pt)))
        # Окружная толщина зуба St=
        self.lineEdit_St.setText(str(St))
        # Угол профиля
        self.lineEdit_at.setText(str(at))
        # Диаметр основной окружности
        self.lineEdit_db.setText(str(math.ceil(db)))
        
        # Создаем списки 
        List_dyi=[]
        List_Di=[]
        List_Yei=[]
        List_Xei=[]
        List_Minus_Xei=[]
        List_Xdai=[]
        List_Ydai=[]
        List_yi=[]
        List_Ai=[]
        List_Bi=[]
        List_fi=[]
        List_Ypki=[]
        List_Xpki=[]
        List_Minus_Xpki=[]
        # Заполняем нуливой (первый )индекс списка значениями
        List_dyi.append(dyi)
        List_Di.append( math.acos( db/ List_dyi[0] ) - math.tan( math.acos( db / List_dyi[0] ) ) + C )
        List_Yei.append(dyi / 2*math.cos( List_Di[0]))
        List_Xei.append(List_Yei[0]*math.tan(List_Di[0]))
        List_Minus_Xei.append(-List_Xei[0])
        List_Xdai.append(-List_Xei[0])
        List_Ydai.append(((da/2)**2-List_Xdai[0]**2)**0.5)
        hda=(List_Xei[0]-List_Minus_Xei[0])/(n-1)
        # Заполняем первый (второй по счету )индекс списка значениями 
        List_dyi.append(dyi-hdy)
        List_Di.append( math.acos(db/List_dyi[1])-math.tan(math.acos(db/List_dyi[1]))+C)
        List_Yei.append( List_dyi[1]/2*math.cos(List_Di[1]))
        List_Xei.append( List_Yei[1]* math.tan(List_Di[1]))
        List_Minus_Xei.append(-List_Xei[1])
        List_Xdai.append(List_Xdai[0]+hda)
        List_Ydai.append(((da/2)**2-List_Xdai[1]**2)**0.5)
        Xdai=List_Xdai[1]
        dyi=dyi-hdy
        # Начинаем  заполнять списки в цикле 
        i=0
        while i < n-2:  
            i=i+1
            dyi=dyi-hdy
            List_Di.append(math.acos(db/dyi)-math.tan(math.acos(db/dyi))+C)
            Di=math.acos(db/dyi)-math.tan(math.acos(db/dyi))+C
            Yei=dyi/2*math.cos(Di)
            Xei=Yei*math.tan(Di) 
            List_dyi.append(dyi) 
            List_Yei.append(dyi/2*math.cos(Di))
            List_Xei.append(Yei*math.tan(Di))
            List_Minus_Xei.append(-Xei) 
            Xdai=Xdai+hda
            List_Xdai.append(Xdai)
            List_Ydai.append(((da/2)**2-Xdai**2)**0.5)
        #Заполняем последний индекс  списка    
        List_dyi[n-1]=D
        # Заполняем нуливой (первый )индекс списка значениями
        List_yi.append(yi)
        List_Ai.append(z/(2*math.cos(math.radians(b)))-y0-pf*math.cos(List_yi[0]) )
        List_Bi.append(y0*math.tan(List_yi[0])+pf*math.sin(List_yi[0]))
        List_fi.append(fi)
        List_Ypki.append((List_Ai[0] * math.cos(fi)+List_Bi[0] * math.sin(fi)) * m)
        List_Xpki.append((List_Ai[0] * math.sin(fi)-List_Bi[0] * math.cos(fi)) * m)
        List_Minus_Xpki.append(-List_Xpki[0])
        # Начинаем  заполнять списки в цикле 
        i=0
        while i < n-2:
            i=i+1
            yi=yi-hy
            List_yi.append(yi)
            Ai = z / (2 * math.cos(math.radians(b)))-y0-pf*math.cos(yi)
            List_Ai.append( z / (2 * math.cos(math.radians(b)))-y0-pf*math.cos(yi))
            Bi =y0*math.tan(yi)+pf*math.sin(yi)
            List_Bi.append(y0*math.tan(yi)+pf*math.sin(yi))
            fi = 2*math.cos(math.radians(b))/z*(x0+y0*math.tan(yi))
            List_fi.append(2*math.cos(math.radians(b))/z*(x0+y0*math.tan(yi)))
            List_Ypki.append((Ai*math.cos(fi)+Bi*math.sin(fi))*m)
            Ypki=(Ai*math.cos(fi)+Bi*math.sin(fi))*m
            Xpki=(Ai*math.sin(fi)-Bi*math.cos(fi))*m
            List_Xpki.append((Ai*math.sin(fi)-Bi*math.cos(fi))*m)
            List_Minus_Xpki.append(-Xpki)
        #Заполняем последний индекс  списка  
        List_yi.append(yi-yi)
        List_Ai.append(z/(2*math.cos(math.radians(b)))-y0-pf*math.cos(List_yi[n-1]) )  
        List_Bi.append(y0*math.tan(List_yi[n-1])+pf*math.sin(List_yi[n-1])) 
        List_fi.append(2*math.cos(math.radians(b))/z*(x0+y0*math.tan(List_yi[n-1])))
        List_Ypki.append((List_Ai[n-1] * math.cos(fi)+List_Bi[n-1] * math.sin(List_fi[n-1])) * m)
        List_Xpki.append((List_Ai[n-1] * math.sin(fi)-List_Bi[n-1] * math.cos(List_fi[n-1])) * m)
        List_Minus_Xpki.append(-List_Xpki[n-1])

        self.GragEvolvent(List_Minus_Xei+List_Minus_Xpki,List_Yei+List_Ypki)
        self.TextEvolvent(List_Xei+List_Xpki,List_Yei+List_Ypki,da/2)
        self.WiPfileZub(List_Yei,List_Xei,List_Minus_Xei,List_Ypki,List_Xpki,List_Minus_Xpki,
            List_Ydai,List_Xdai)

    def WiPfileZub(self,Yei,Xei,Minus_Xei,Ypki,Xpki,Minus_Xpki,Ydai,Xdai):
        """   Рисуем профиль зуба 
              
             
        """
        #Отправляем листы на прорисовку в график 
        if WiZubValue == True:
       
            self.plot(Yei,Xei, "Evalvent", 'b')
            self.plot(Yei,Minus_Xei, "mEvalvent", 'b')

            self.plot(Ypki,Xpki, "Perehod", 'b')
            self.plot(Ypki,Minus_Xpki, "mPerehod", 'b')

            self.plot(Ydai,Xdai, "Naryg", 'b')    
        
    

    def plot(self,x, y, plotname, color):
        """функция отрисовки графика graphWidget\n
       
        """
        # переменная цвет линии
        pen = pg.mkPen(color=color)
       #надпись наименование осей 
        self.graphWidget.setLabel('left', 'Ось Х', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Ось Z', color='red', size=30)
       #включаем сетку
        self.graphWidget.showGrid(x=True, y=True)
       #рисуем сам график 
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='o', symbolSize=10, symbolBrush=(color))
    
    
    def GragEvolvent(self,AxisX,AxisZ):
        """ Эта функция выводит на график  профель впадины\n
            AxisX= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист  \n
            AxisZ= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист  
        """
        List_Axis_X=[]
        List_Axis_Z=[]
        global n
        i=0
        for i in range(len(AxisX)):
            List_Axis_X.append(AxisX[i]-(AxisX[n*2-1]+(AxisX[0]/2)))
            List_Axis_Z.append(AxisZ[i])
           
        if WiVpadinaValue == True:     
            self.plot(List_Axis_Z, List_Axis_X, "Vpadina", 'g')
         
        Var_X_list=[]
        Var_Z_list=[]
              
        i=0
        for i in range(len(AxisX)):
           Var_X_list.append(-List_Axis_X[i]) 
           Var_Z_list.append(List_Axis_Z[i])      
    
        if WiVpadinaValue == True:   
           self.plot(Var_Z_list, Var_X_list, "Vpadina", 'g')


    def TextEvolvent(self,AxisX,AxisZ,da):
        """Комент к функции пичать начальных точек \n
          TextEvolvent(self,AxisX,AxisZ) \n
          AxisX= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист  \n
          AxisZ= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист 
        """  
        # В цикле заполняем текстовое поле 
        
        global n
        ListX=[]       
        ListZ=[]
        
        file=open("CSv.csv","w")
        self.textEdit_toch.clear()
       
        i=0       
        for i in range(len(AxisX)):
            Var_X = AxisX[i]-(AxisX[n*2-1]+AxisX[0]/2)
            ListX.append(-Var_X)
            Var_Z = AxisZ[i]- da
            ListZ.append(AxisZ[i])  
            self.textEdit_toch.append(str(round(-Var_X,3))+","+str(round(-Var_Z,3)))
           
            file.write(str(round(-Var_X,3))+","+(str(round(-Var_Z,3)))+"\n")
        
        if WiEvolventValue == True:    
           self.plot(ListZ,ListX, "Prog", 'w')    
        
        f = open("CSv.csv", 'r')
        mytext = f.read()
        f.close()
        
        file = open("CSv.csv", 'r')
                   
        with file:
            if mytext.count(';') <= mytext.count(','):
                reader = csv.reader(file, delimiter = ',')
                self.model.clear()
                for row in reader:    
                    items = [QtGui.QStandardItem(field) for field in row]
                    self.model.appendRow(items)
                self.model.setHeaderData(0,Qt.Horizontal,"Ось Х")
                self.model.setHeaderData(1,Qt.Horizontal,"Ось Z")     
                self.tableView.resizeColumnsToContents()
            else:
                reader = csv.reader(file, delimiter = ';')
                self.model.clear()
                for row in reader:    
                    items = [QtGui.QStandardItem(field) for field in row]
                    self.model.appendRow(items)
                self.model.setHeaderData(0,Qt.Horizontal,"Ось Х")
                self.model.setHeaderData(1,Qt.Horizontal,"Ось Z")    
                self.tableView.resizeColumnsToContents()    
        
          
 


    def WiZub(self,val):
        """
        """
        global WiZubValue
        if val == Qt.Checked:
           WiZubValue= True
        else:
           WiZubValue=False 
    #    return True
               
    def WiVpadina(self,val):
        """
        """
        global WiVpadinaValue
        if val == Qt.Checked:
           WiVpadinaValue=True        
        else:
           WiVpadinaValue=False 

    def WiEvolvent(self,val):
        """
        """
        global WiEvolventValue
        if val == Qt.Checked:
            WiEvolventValue=True
        else:
            WiEvolventValue=False     
        

    def ClearGrafik(self):
        """ Очистить График  по кнопке 
        """
        self.graphWidget.clear()

    def NewFile(self):
        fileName="NewFile.csv"
        ff = open(fileName, 'r')
        mytext = ff.read()
        ff.close()
        f = open(fileName, 'r')
        self.lineEdit.setText("Открыли файл - " + fileName)
        with f:
            self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
            self.setWindowTitle(self.fname)
            if mytext.count(';') <= mytext.count(','):
                reader = csv.reader(f, delimiter = ',')
                self.model.clear()
                for row in reader:    
                    items = [QtGui.QStandardItem(field) for field in row]
                    self.model.appendRow(items)
                self.model.setHeaderData(0,Qt.Horizontal,"Ось Х")
                self.model.setHeaderData(1,Qt.Horizontal,"Ось Z")    
                self.tableView.resizeColumnsToContents()
         
    
    def AddRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
         
    
    def RemoveRow(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedRows() 
        for index in sorted(indices):
           model.removeRow(index.row()) 
        

    def WriteCsv(self,fileName):
        """
        """

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row,column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранит файл", 
                    (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),"CSV Файлы (*.csv)")
                
        if fileName:
            f = open(fileName, 'w')
            with f:
                writer = csv.writer(f, delimiter = ',')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                        QtCore.Qt.DisplayRole)
                    for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
    
        SAxis = self.lineEditAxisS.text()
        XAxis = self.lineEditAxisX.text()
        YAxis = self.lineEditAxisY.text()
        VisotaYAxis = self.lineEditVisota.text()
        ExitFreza = self.lineEditVilet.text()
        DFreza = self.lineEditDFreza.text()
        KolZub = self.lineEditKolZub.text()
        ORA = self.lineEditOra.text()
        Ugol = self.lineEditUgol.text()
        saveText=[SAxis,XAxis,YAxis,VisotaYAxis,ExitFreza,DFreza,KolZub,ORA,Ugol]

        fileTxt=open(fileName+".txt","w") 
         
        for i in saveText:
           fileTxt.writelines(i+"\n")
        fileTxt.close()
    
    def Open_File(self,fileName):
        #Читаем имя файла из вджита
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть CSV файл",
               (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
    # проверяем наличие имя файла 
        if fileName:
       
            f = open(fileName, 'r')
            mytext = f.read()
            f.close()

            file = open(fileName, 'r')
            self.lineEdit.setText("Открыли файл - " + fileName)
           
            with file:
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
                if mytext.count(';') <= mytext.count(','):
                    reader = csv.reader(file, delimiter = ',')
                    self.model.clear()
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.tableView.resizeColumnsToContents()
                else:
                    reader = csv.reader(file, delimiter = ';')
                    self.model.clear()
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.tableView.resizeColumnsToContents()
            #self.loadTxt(fileName)
            

    def GrafСontrolProg(self):
       Xlist = []
       Zlist = []
       mXList = []  
       self.graphWidget.clear()          
      
       for rowNumber in range(self.model.rowCount()):
           
           fii=[self.model.data(self.model.index(rowNumber,0),QtCore.Qt.DisplayRole)]
           fi=[self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole)]
        
           for i in range(len(fii)):
               x= fii[i]
               Xlist.append(float(x))
               mx=fii[i]
               mXList.append(float("-"+mx))
           for ii in range(len(fi)):
               z= fi[ii] 
               Zlist.append(float("-"+z))

      # print(Xlist,mXList,Zlist)        
      # self.plot(Xlist,Zlist) 
       self.plot(Zlist, Xlist, "Sensor1", 'b')
       self.plot(Zlist, mXList, "Sensor2", 'b')
           

    def GenerateControlProg(self):
        n=0
        no=0
        E25 = self.lineEditAxisX.text()
        E26 = self.lineEditAxisY.text()
        VisotaYAxis = self.lineEditVisota.text()
        DFreza = self.lineEditDFreza.text()
        ExitFreza = self.lineEditVilet.text()
        if DFreza and ExitFreza and VisotaYAxis:
           E30 = (int(DFreza)/2)+(int(ExitFreza)*2)+int(VisotaYAxis)
        else:
           E30=""   
        M3 = self.lineEditAxisS.text()
        UAO = self.lineEditOra.text()
        RPT = self.lineEditKolZub.text()
        Coment = self.lineEditComent.text()
        Obrab = self.comboBoxObrabotka.itemText(self.comboBoxObrabotka.currentIndex())
        Detal = self.comboBoxChert.itemText(self.comboBoxChert.currentIndex())
        Avtor = self.comboBoxFIO.itemText(self.comboBoxFIO.currentIndex()) 
        Ulol =  self.lineEditUgol.text()
        data=datetime.datetime.now()
        datatext=data.strftime("%d-%m-%Y %H:%M") 

        listText=[";ЛАИТ",";Program created",";automatically",";Программу заполнил "+Avtor,";Дата создания "+datatext,";Деталь "+ Detal,
            ";Обработка "+Obrab,";Диаметр фрезы D "+str(DFreza),";Скорость подачи по Х и Z","E25="+str(E25),
                  ";Скорость подачи по Y","E26="+str(E26),";Высота по Y","E30="+str(E30),";Скорость оборотов шпинделя",
                  "M3 S"+str(M3),";Начальная точка","(UOA,"+str(UAO)+")"]
        self.textEdit.clear()
        
        if E25 and E26 and VisotaYAxis and DFreza and ExitFreza and E30 and UAO and RPT:

            global ValkosZub
            if ValkosZub:
                #print("Опять ок")
                global ValNaklon     
                if ValNaklon:
                    #print("Левый да")
                    
                    self.textEdit.append(";Косой левый Зуб !!!!")
                    self.textEdit.append(";Косой левый Зуб !!!!")
                    self.textEdit.append(";Косой левый Зуб !!!!")
                    
                    for iii in range(len(listText)):
                        y=listText[iii] 
            
                        self.textEdit.append(y)
                   
                    for rowNumber in range(self.model.rowCount()):
                        n=n+1
                        self.textEdit.append(";Проход № "+str(n))
                        fii=[self.model.data(self.model.index(rowNumber,0),QtCore.Qt.DisplayRole)]
                        fi=[self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole)]
        
                        for i in range(len(fii)):
                            x= fii[i]
                        for ii in range(len(fi)):
                            z= fi[ii] 
                        no=no+1
                        self.textEdit.append("N"+str(no)+" X"+x+"  Z-"+z+" FE25")
                        no=no+1
                        self.textEdit.append("N"+str(no)+" YE30 FE26")
                        no=no+1
                        self.textEdit.append("N"+str(no)+" X-"+x)
                        no=no+1
                        self.textEdit.append("N"+str(no)+" Y0 FE26")
                        self.textEdit.append(" Угол "+Ulol)

                    self.textEdit.append("M5")
            
                
                else:
                #    print("Левый нет")
             
                    self.textEdit.append(";Косой правый Зуб !!!!")
                    self.textEdit.append(";Косой правый Зуб !!!!")
                    
                    for iii in range(len(listText)):
                        y=listText[iii] 
            
                        self.textEdit.append(y)
                   
                    for rowNumber in range(self.model.rowCount()):
                        n=n+1
                        self.textEdit.append(";Проход № "+str(n))
                        fii=[self.model.data(self.model.index(rowNumber,0),QtCore.Qt.DisplayRole)]
                        fi=[self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole)]
        
                        for i in range(len(fii)):
                            x= fii[i]
                        for ii in range(len(fi)):
                            z= fi[ii] 
                        no=no+1
                        self.textEdit.append("N"+str(no)+" X"+x+"  Z-"+z+" FE25")
                        no=no+1
                        self.textEdit.append("N"+str(no)+" YE30 FE26")
                        no=no+1
                        self.textEdit.append("N"+str(no)+" X-"+x)
                        no=no+1
                        self.textEdit.append("N"+str(no)+" Y0 FE26")
                        self.textEdit.append(" Другой Угол "+Ulol)

                    self.textEdit.append("M5")

            else:
                #print("Опять не ок ")   
             
                self.textEdit.append(";Прямой Зуб !!!!")
                
                
                for iii in range(len(listText)):
                    y=listText[iii] 
            
                    self.textEdit.append(y)
                   
                for rowNumber in range(self.model.rowCount()):
                    n=n+1
                    self.textEdit.append(";Проход № "+str(n))
                    fii=[self.model.data(self.model.index(rowNumber,0),QtCore.Qt.DisplayRole)]
                    fi=[self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole)]
        
                    for i in range(len(fii)):
                        x= fii[i]
                    for ii in range(len(fi)):
                        z= fi[ii] 
                    no=no+1
                    self.textEdit.append("N"+str(no)+" X"+x+"  Z-"+z+" FE25")
                    no=no+1
                    self.textEdit.append("N"+str(no)+" YE30 FE26")
                    no=no+1
                    self.textEdit.append("N"+str(no)+" X-"+x)
                    no=no+1
                    self.textEdit.append("N"+str(no)+" Y0 FE26")

                self.textEdit.append("M5")    
        else:        
            self.textEdit.append(";Дата создания "+datatext)
            self.textEdit.append("Нужно заполнить все поля !!!!")
            self.textEdit.append("Нужно заполнить все поля !!!!")
            self.textEdit.append("Кроме комментария")



    def Kos(self,kosZub):
        global ValkosZub
        if kosZub == Qt.Checked:
           ValkosZub=True
        else:
           ValkosZub=False
        self.texUgol()
    def Naklon(self,LevNaklon):
        global ValNaklon
        if LevNaklon == Qt.Checked:
           ValNaklon = True
        else:
           ValNaklon = False
        self.texUgol()   

    def texUgol(self):
        global ValkosZub
        if ValkosZub:
           global ValNaklon
           if ValNaklon:
               self.labelKos.setText(" Левый Косой зуб ")
           else:
               self.labelKos.setText("Правый Косой зуб")
        else:
            self.labelKos.setText("Прямой зуб")    



if __name__ == "__main__":
   
    app = QtWidgets.QApplication(sys.argv)
  # app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()

   

sys.exit(app.exec_())