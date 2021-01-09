#-*- coding:utf-8 -*-
# Control-Program-Editor-CNC-Ver.4.0.0

import csv,sys,os
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtPrintSupport
from PyQt5.Qt import Qt
from numpy import math
import pyqtgraph as pg
import ezdxf
import datetime


Clear_plots = True
ValkosZub=False
ValNaklon=False
ValM6 = "M66"
Axis=" Z-"

class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        # Фаил формы
        uic.loadUi("forma.ui",self)
        # Заголовок 
        self.setWindowTitle("Control Program Editor CNC. Ver.4.0.0 ")
        #ициализируем переменную имя файла 
        self.fileName = ""
        #имя файла по умолчанию 
        self.fname = "Liste"
        #Таблица 
        item = QtGui.QStandardItem()
        self.model =  QtGui.QStandardItemModel(self)
        self.model.appendRow(item)
        self.model.insertColumn(1)
        self.model.setHeaderData(0,Qt.Horizontal,"Ось Х  ")
        self.model.setHeaderData(1,Qt.Horizontal,"Ось Z  ") 
        self.tableView.resizeColumnsToContents()      
        self.tableView.setModel(self.model)
        self.tableView.setShowGrid(True)
        # Кнопки 
        self.Add_Row_Button.clicked.connect(self.AddRow)
        self.Remove_Row_Button.clicked.connect(self.RemoveRow)
        self.WriteCsv_Button.clicked.connect(self.WriteCsv)
        self.Button_Open_File.clicked.connect(self.Open_File)
        self.NewFile_Button.clicked.connect(self.NewFile)
        self.Open_Dxf_Button.clicked.connect(self.OpenDXF)
        self.GenerateProgramButon.clicked.connect(self.GenerateControlProg)
        self.WriteFile_CProg_Button.clicked.connect(self.WriteControlProg)
        self.Print_Button.clicked.connect(self.handlePrint)
        self.Wi_print_Button.clicked.connect(self.handlePreview)  
        self.pushButtonEvolvent.clicked.connect(self.Evolvent)        

        self.checkBoxClearPlot.stateChanged.connect(self.ClearGrafik)
        self.checkBoxKoc.stateChanged.connect(self.Kos)
        self.checkBoxKosLev.stateChanged.connect(self.Naklon)
        self.checkBoxWZ.stateChanged.connect(self.AxisW)

        self.doubleSpinBox_Z.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_m.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_a.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_ha.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_c.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_pf.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_x.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_y.valueChanged.connect(self.Evolvent)
        self.doubleSpinBox_b.valueChanged.connect(self.Evolvent)

        self.radioButtonM66.pressed.connect(self.M66)
        self.radioButtonM6.pressed.connect(self.M6)

        self.Evolvent()

    def AddRow(self):
        """Добавляем новую строку
        """
        items = QtGui.QStandardItem("")
        self.model.appendRow(items)    

    def RemoveRow(self):
        """Удаляем выделеную строку
        """
        indices = self.tableView.selectionModel().selectedRows() 
        for index in sorted(indices):
            self.model.removeRow(index.row())      
    
    def WriteCsv(self,fileName):
        """ сохраняем все в CSV Файлы и текстовый 
        """
        fname = "Liste"
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row,column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)

        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранит файл", 
                    (QtCore.QDir.homePath() + "/Volumes/dis/qtZub/zub/" + fname + ".csv"),"CSV Файлы (*.csv)")
                
        if fileName:
            f = open(fileName,'w')
            with f:
                writer = csv.writer(f, delimiter = ',')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),Qt.DisplayRole)
                        for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                    fname = os.path.splitext(str(fileName))[0].split("/")[-1] 
                    self.setWindowTitle(fname)
    
            SAxis = self.lineEditAxisS.text()
            XAxis = self.lineEditAxisX.text()
            YAxis = self.lineEditAxisY.text()
            Visota_Y_Axis = self.lineEditVisota.text()
            ExitFreza = self.lineEditVilet.text()
            DFreza = self.lineEditDFreza.text()
            z = int(self.doubleSpinBox_Z.value())
            ORA = self.lineEditOra.text()
            b = self.doubleSpinBox_b.value()
            saveText=[SAxis,XAxis,YAxis,Visota_Y_Axis,ExitFreza,DFreza,str(z),ORA,str(b)]
        
            fileTxt=open(fileName+".txt","w") 
         
            for i in saveText:
                fileTxt.writelines(i+"\n")
            fileTxt.close()

    def ClearGrafik(self,val):
        """ Очистить График  по кнопке 
        """
        global Clear_plots

        if val == Qt.Checked:        
            Clear_plots = True
        else:
            Clear_plots = False    
    
    def plots(self,x, y, plotname, color,val=False):
        """функция отрисовки графика graphWidget\n
       
        """
        # переменная цвет линии
        pen = pg.mkPen(color=color)
        if Clear_plots:
            self.graphWidget.clear()
       #надпись наименование осей 
        self.graphWidget.setLabel('left', 'Ось Z', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Ось X', color='red', size=30)
       #включаем сетку
        self.graphWidget.showGrid(x=True, y=True)
       #рисуем сам график 
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='o', symbolSize=10, symbolBrush=(color))

    def Open_File(self):
        """ Читаем CSV Файлы
        """
       
        #Читаем имя файла из вджита
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть CSV файл",
               (QtCore.QDir.homePath() + "/Volumes/dis/qtZub/zub/" + ".csv"), "CSV (*.csv *.tsv)")
        # проверяем наличие имя файла 
        if fileName[0]:#!= ('', '')
       
            f = open(fileName, 'r')
            mytext = f.read()
            f.close()

            file = open(fileName, 'r')
            self.lineEdit.setText("Открыли файл - " + fileName)
           
            with file:
                fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(fname)
                if mytext.count(';') <= mytext.count(','):
                    reader = csv.reader(file, delimiter = ',')
                             
                    self.model.clear()
                    x_list=[]
                    z_list=[]
                    for row in reader: 
                        x_list.append(float(row[0]))
                        z_list.append(float(row[1])) 
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                        self.model.setHeaderData(0,Qt.Horizontal,"Ось Х   ")
                        self.model.setHeaderData(1,Qt.Horizontal,"Ось Z   ")
                    self.tableView.resizeColumnsToContents()
                   # print(x_list,"   ",z_list)
                    self.plots(x_list,z_list,"plotname","b")
                else:
                    reader = csv.reader(file, delimiter = ';')
                
                    self.model.clear()
                
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                        self.model.setHeaderData(0,Qt.Horizontal,"Ось Х   ")
                        self.model.setHeaderData(1,Qt.Horizontal,"Ось Z   ")
                    
                    self.tableView.resizeColumnsToContents()
        try:            
            with open(fileName+".txt","r",) as fileTxe:
                listFile = fileTxe.readlines()
                            
            self.lineEditAxisS.setText(str(listFile[0].rstrip('\n')))
            self.lineEditAxisX.setText(str(listFile[1].rstrip('\n')))
            self.lineEditAxisY.setText(str(listFile[2].rstrip('\n')))
            self.lineEditVisota.setText(str(listFile[3].rstrip('\n')))
            self.lineEditVilet.setText(str(listFile[4].rstrip('\n')))
            self.lineEditDFreza.setText(str(listFile[5].rstrip('\n')))
            self.doubleSpinBox_Z.setValue(float(listFile[6].rstrip('\n')))
            self.lineEditOra.setText(str(listFile[7].rstrip('\n')))
            self.doubleSpinBox_b.setValue(float(listFile[8].rstrip('\n')))
        except IOError:    

            reply = QMessageBox.question(self,'Внимание', "Нет файла конфигурации \n Нужно создать новый \n СОЗДАДИМ ? ", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.WriteCsv(fileName)

    def NewFile(self):
        """Заполняем таблицу нулями
        """
        fileName="NewFile.csv"
        self.lineEdit.setText("Открыли файл - " + fileName)
        item = QtGui.QStandardItem()
        
        self.model.clear()
        self.model.appendRow(item)
        self.model.insertColumn(1)
        self.model.setHeaderData(0,Qt.Horizontal,"Ось Х   ")
        self.model.setHeaderData(1,Qt.Horizontal,"Ось Z   ") 
    
        self.lineEditAxisS.setText('0')
        self.lineEditAxisX.setText('0')
        self.lineEditAxisY.setText('0')
        self.lineEditVisota.setText('0')
        self.lineEditVilet.setText('0')
        self.lineEditDFreza.setText('0')
        self.doubleSpinBox_Z.setValue(0)
        self.lineEditOra.setText('0')
        self.doubleSpinBox_b.setValue(0)

    
    def OpenDXF(self):
        """
        Читаем  DXF фаил
        """
        list_line=[]
        
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть dxf файл",
               (QtCore.QDir.homePath() + "/Volumes/dis/qtZub/zub/" + ".dxf"), "dxf (*.dxf)")
        if fileName:
            doc = ezdxf.readfile(fileName)
   
            msp = doc.modelspace()
            for point in msp.query('LINE[layer=="'+str(self.comboBoxProcess.itemText(self.comboBoxProcess.currentIndex()))+'"]'):
                point_list=[]
                for i in range(0,2):
                    point_list.append(str(round(point.dxf.start[i],3)))
                list_line.append(point_list)
            #print(list_line)  
            x_list=[]
            z_list=[]
            for i in list_line:
                #print(i)
                x_list.append(float(i[0]))
                z_list.append(float(i[1]))
            #print(x_list,"  ",z_list)    
            
            self.plots(x_list,z_list,"plotname","b")
            
            self.model.clear()
            for row in list_line:    
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
                self.model.setHeaderData(0,Qt.Horizontal,"Ось Х   ")
                self.model.setHeaderData(1,Qt.Horizontal,"Ось Z   ")
                       
            self.tableView.resizeColumnsToContents()

    def Kos(self,kosZub):
        """ Проверяем галочку  косой зуб
        """
        global ValkosZub
        if kosZub == Qt.Checked:
           ValkosZub=True
        else:
           ValkosZub=False
        self.texUgol()

    def Naklon(self,LevNaklon):
        """Проверяем галочку наклона зуба
        """
        global ValNaklon
        if LevNaklon == Qt.Checked:
           ValNaklon = True
        else:
           ValNaklon = False
        self.texUgol()

    def texUgol(self):
        """Выводим на экран какой зуб 
        """
        global ValkosZub
        if ValkosZub:
           global ValNaklon
           if ValNaklon:
               self.labelKos.setText(" Левый Косой зуб ")
               
           else:
               self.labelKos.setText("Правый Косой зуб")
              
        else:
            self.labelKos.setText("Прямой зуб")

    def textRezultat(self):
        """
        заполняем текстовые поля 
        """
        z = self.doubleSpinBox_Z.value()
        m = self.doubleSpinBox_m.value() 
        b = self.doubleSpinBox_b.value()
        # Делительный диаметр:
        d = z * m
        # a = Угол главного профиля
        a = self.doubleSpinBox_a.value()
        #ha = Коэффициент высоты головки
        ha = self.doubleSpinBox_ha.value()
        #x = К-т смещения исходного контура
        x = self.doubleSpinBox_x.value()
        #y =Коэффициент уравнительного смещения
        y = self.doubleSpinBox_y.value()
        #Диаметр вершин зубьев
        da = d + 2 * (ha + x - y) * m    
        # Делительный диаметр
        d = z * m

        self.label_da.setText(str(da))
        self.label_d.setText(str(d))

    def M6(self):
        """
        проверяем галочку м6
        """
        global ValM6
        ValM6 = "M6"
    
    def M66(self):
        """
        проверяем галочку м66
        """
        global ValM6
        ValM6 = "M66" 

    def AxisW(self,val):
        """
        """
        global Axis
        if val ==Qt.Checked:
            Axis="  W-"
        else:
            Axis="  Z-"       

    def GenerateControlProg(self):
        """
        Генерируем код управляющей программы
        """
        n=0
        nom=0
        
        Obrab = self.comboBoxProcess.itemText(self.comboBoxProcess.currentIndex())
        DFreza = self.lineEditDFreza.text()
        E25 = self.lineEditAxisX.text()
        E26 = self.lineEditAxisY.text()
        VisotaYAxis = self.lineEditVisota.text()
        DFreza = self.lineEditDFreza.text()
        ExitFreza = self.lineEditVilet.text()
        if DFreza and ExitFreza and VisotaYAxis:
           E30 = (int(DFreza)/2)+(int(ExitFreza)*2)+float(VisotaYAxis)
        else:
           E30 = 0
        M3 = self.lineEditAxisS.text()
        UAO = self.lineEditOra.text()
        z = int(self.doubleSpinBox_Z.value())
        m = self.doubleSpinBox_m.value() 
        b = self.doubleSpinBox_b.value()
        # Делительный диаметр:
        d = z * m
        # a = Угол главного профиля
        a = self.doubleSpinBox_a.value()
        #ha = Коэффициент высоты головки
        ha = self.doubleSpinBox_ha.value()
        #x = К-т смещения исходного контура
        x = self.doubleSpinBox_x.value()
        #y =Коэффициент уравнительного смещения
        y = self.doubleSpinBox_y.value()
        #Диаметр вершин зубьев
        da = d + 2 * (ha + x - y) * m

        data=datetime.datetime.now()
        datatext=data.strftime("%d-%m-%Y %H:%M") 
        
        printt = False

        if not DFreza or not E25 or not E26 or not M3 or not UAO or not z or not Obrab :
            printt = False
        else:
            printt = True    

        listText=[";ЛАИТ",";Program created",";automatically",";Дата создания "+datatext,
            ";Обработка "+Obrab,";Диаметр фрезы D "+str(DFreza),";Скорость подачи по Х и Z","E25="+str(E25),
                  ";Скорость подачи по Y","E26="+str(E26),";Высота по Y","E30="+str(E30),";Номер корректора","T1.3 " + ValM6,
                  ";Начальная точка","(UAO,"+str(UAO)+")","(UOT,"+str(UAO)+",Y0,Z0,W0)",";Скорость оборотов шпинделя","M3 S"+str(M3),
                  "G90G01 X0 Y0 W0 Z0 F1500","(UCG,2,X-100X100,Y20Y60,Z-150Z0,1,-5)",
                  "(RPT,"+str(z)+")","E1="+str(z),"#TIM1=TIM0"]
        self.textEdit.clear()

        if ValkosZub and not ValNaklon:
            self.textEdit.append("Косой правый Зуб!!!!")
        elif ValkosZub and ValNaklon:    
            self.textEdit.append(";Косой левый Зуб !!!!")
        else:    
            self.textEdit.append(";Прямой Зуб !!!!")

        self.textEdit.append(";"+self.lineEditComent.text())


        for i in range(len(listText)):
            y=listText[i] 
            
            self.textEdit.append(y)
        
        xAxis=zAxis=bAxis=0
        if printt:
            for rowNumber in range(self.model.rowCount()):
                n=n+1
                self.textEdit.append(";Проход № "+str(n))
                fii = [self.model.data(self.model.index(rowNumber,0),QtCore.Qt.DisplayRole)]
                fi = [self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole)]
                if self.model.data(self.model.index(rowNumber,1),QtCore.Qt.DisplayRole) == None or fii == [''] or fi == ['']:
                    self.textEdit.append("В таблице есть Пустое поле  ")
                    self.labelKos.setText("Ошибка!!!!")
                    QMessageBox.about (self, "Ошибка " , "В таблице есть пустые поля  " )
                else:
                
                    for i in range(len(fii)):
                        xAxis= fii[i]
                    for i in range(len(fi)):
                        zAxis= fi[i] 
                    nom=nom+1
                    if ValkosZub and not ValNaklon:  
                        self.textEdit.append("N" + str(nom) + " X" + xAxis + Axis + zAxis + " FE25")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " YE30 FE26")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " X-" + xAxis)
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " Y0 FE26")
                        self.textEdit.append(" Угол правый" )
                    elif ValkosZub and ValNaklon:
                        self.textEdit.append("N" + str(nom) + " X" + xAxis + Axis + zAxis + " FE25")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " YE30 FE26")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " X-" + xAxis)
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " Y0 FE26")
                        self.textEdit.append(" Угол Левый " )
                    else:    
                        self.textEdit.append("N" + str(nom) + " X" + xAxis + Axis + zAxis + " FE25")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " YE30 FE26")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " X-"+xAxis+" FE25")
                        nom=nom+1
                        self.textEdit.append("N" + str(nom) + " Y0 FE26")
                        bAxis=round(360/int(z),3)  


            self.textEdit.append("")
            self.textEdit.append("G90 Z0 F1000")
            self.textEdit.append("G91 G01 B-"+str(bAxis)+" F150" )
            self.textEdit.append("G90 G01 X0 Y0 W0 F 1500")
            self.textEdit.append("# TOTO=TIMO-TIM1")
            self.textEdit.append("TOT1=TOTO*E1")
            self.textEdit.append("TOT2=TOT1/3600")
            self.textEdit.append("(DIS,E1,TOT2)")
            self.textEdit.append("(ERP)")
            self.textEdit.append("M5")

    def WriteControlProg(self):
        """Записываем результат в фаил

        """        
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Сохранить фаил как",
                    (QtCore.QDir.homePath() + "/Volumes/dis/qtZub/zub/" + self.fname +"")," Файлы cnc (*.)")
        if fileName:
            f=open(fileName, "w" ,encoding="cp866")
            f.writelines(self.textEdit.toPlainText())

    def handlePrint(self):
        """По кнопке печать
        """
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
           self.handlePaintRequest(dialog.printer())
 
    def handlePreview(self):
        """ По кнопке предварительный просмотр
        """
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.setFixedSize(1000,700)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
 
    def handlePaintRequest(self, printer):
        """Функция вывода на печать
        """
        printer.setDocName(self.fname)
        document = QtGui.QTextDocument(self.textEdit.toPlainText())
        cursor = QtGui.QTextCursor(document)
        document.print_(printer)        



    def Evolvent(self):
        '''Расчет эвольвенты зуба
        '''
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
        #n=int(self.doubleSpinBox_n.value())
        n=100
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
        #da = d + (2 * m)*(ha+x+y)
        da = d + 2 * (ha + x - y) * m
        #Диаметр впадин (справочно)
        #df = d -(2 * hf)
        df = d -2 * (ha + c - x) * m
        #Окружной шаг зубьев или Шаг зацепления по дуге делительной окружности: Pt или p
        pt = math.pi * m
        #Окружная толщина зуба или Толщина зуба по дуге делительной окружности: St или S
        #Суммарный коэффициент смещений: XΣ
        X = 0.60 + 0.12
       # St = 0.5 * pf
       # St = 0.5 * pt
        St = 0.5 * pt + 2 * x * m * math.tan(math.radians(a))
        #inv a 
        inva=math.tan(math.radians(a))-math.radians(a)
        #Угол зацепления invαw
        invaw= (2 * X - math.tan(math.radians(a))) / (10+26) + inva
        #Угол профиля
        at = math.ceil(math.degrees(math.atan(math.tan(math.radians(a))
            /math.cos( math.radians(b)))))
        # Диаметр основной окружности
        db = d * math.cos(math.radians(at)) 
        #Диаметр начала выкружки зуба
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
    #    self.lineEdit_d.setText(str(d))
        # Высота зуба h=
    #    self.lineEdit_h.setText(str(h))
        # Высота головки ha =
    #    self.lineEdit_ha.setText(str(hav))
        # Высота ножки hf=
    #    self.lineEdit_hf.setText(str(hf))
        # Диаметр вершин зубьев
    #    self.lineEdit_da.setText(str(da))
        # Диаметр впадин (справочно)
    #    self.lineEdit_df.setText(str(df))
        # Окружной шаг зубьев Pt=
    #    self.lineEdit_Pt.setText(str(math.ceil(pt)))
        # Окружная толщина зуба St=
    #    self.lineEdit_St.setText(str(math.ceil(St)))
        # Угол профиля
    #    self.lineEdit_at.setText(str(at))
        # Диаметр основной окружности
    #    self.lineEdit_db.setText(str(math.ceil(db)))
        
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

       # self.WiPfileZub(List_Yei,List_Xei,List_Minus_Xei,List_Ypki,List_Xpki,List_Minus_Xpki,List_Ydai,List_Xdai)
        self.GragEvolvent(List_Minus_Xei+List_Minus_Xpki,List_Yei+List_Ypki,n)


        self.label_da.setText(str(round(da,1)))
        self.label_d.setText(str(round(d,1)))
        self.label_at.setText(str(round(at,1)))
        self.label_db.setText(str(round(db,1)))
        self.label_df.setText(str(round(df,1)))
        self.label_St.setText(str(round(St,1)))
        self.label_Pt.setText(str(round(pt,1)))
        self.label_hf.setText(str(round(hf,1)))
        self.label_ha.setText(str(round(ha,1)))
        self.label_h.setText(str(round(h,1)))


    def WiPfileZub(self,Yei,Xei,Minus_Xei,Ypki,Xpki,Minus_Xpki,Ydai,Xdai):
        """   Рисуем профиль зуба 
         
        """
        global Clear_plots

        Clear_plots=False
        #Отправляем листы на прорисовку в график 
        self.plots(Yei,Xei, "Evalvent", 'b')
        self.plots(Yei,Minus_Xei, "mEvalvent", 'b')
        self.plots(Ypki,Xpki, "Perehod", 'b')
        self.plots(Ypki,Minus_Xpki, "mPerehod", 'b')
        self.plots(Ydai,Xdai, "Naryg", 'b')
    
    def GragEvolvent(self,AxisX,AxisZ,n):
        """ Эта функция выводит на график  профель впадины\n
            AxisX= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист  \n
            AxisZ= [1,2,3] или [1,2,3] +[4,5,6] нужно вставить Лист  
        """
        List_Axis_X=[]
        List_Axis_Z=[]
   
        global Clear_plots

       # Clear_plots=False

        i=0
        for i in range(len(AxisX)):
            #List_Axis_X.append(AxisX[i]-(AxisX[n*2-1]+(AxisX[0]/2)))
            List_Axis_X.append(AxisX[i]-(AxisX[n*2-1]+(AxisX[0])))
            List_Axis_Z.append(AxisZ[i])
           
        
        self.plots(List_Axis_X,List_Axis_Z, "Vpadina", 'g')
         
        

if __name__ == "__main__":
       
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
   
    sys.exit(app.exec_())