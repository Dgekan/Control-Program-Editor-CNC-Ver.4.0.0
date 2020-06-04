from numpy import math
    
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

        hy = yi/(100-1)

        x0 = math.pi/(4*math.cos(math.radians(b))
             )+pf*math.cos(math.radians(at))+math.tan(math.radians(at))

        y0 = 1-pf*math.sin(math.radians(at))-x

        C  = (math.pi/2+2*x*math.tan(math.radians(a))
             )/z+math.tan(math.radians(at))-math.radians(at)
        #Расчетный шаг точек эвольвенты
        hdy = (da-D)/(100-1)
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
        hda=(List_Xei[0]-List_Minus_Xei[0])/(100-1)
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
        while i < 98:  
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
        List_dyi[99]=D
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
        while i < 98:
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
        List_Ai.append(z/(2*math.cos(math.radians(b)))-y0-pf*math.cos(List_yi[99]) )  
        List_Bi.append(y0*math.tan(List_yi[99])+pf*math.sin(List_yi[99])) 
        List_fi.append(2*math.cos(math.radians(b))/z*(x0+y0*math.tan(List_yi[99])))
        List_Ypki.append((List_Ai[99] * math.cos(fi)+List_Bi[99] * math.sin(List_fi[99])) * m)
        List_Xpki.append((List_Ai[99] * math.sin(fi)-List_Bi[99] * math.cos(List_fi[99])) * m)
        List_Minus_Xpki.append(-List_Xpki[99])