from numpy import math


def Evolventa():
    """
    docstring
    """
    # Исходные данные
    z1= 10
    z2= 26
    m= 4
    a= 20
    # 1.1.2 Определение размеров зубчатого зацепления
    #Передаточное отношение зубчатой передачи:
    j= z2 / z1
    if z1 + z2 < 60:
        x1 = 0.60
        x2 = 0.12
    else:
        print("z1 + z2 > 60 ",z1+z2)
    # Шаг зацепления по дуге делительной окружности:    
    p = m * math.pi
    print("p= ",p)
    # Делительный диаметр:
    d1 = z1 * m
    d2 = z2 * m
    print("d1 = ",d1," d2 = ",d2)
    # Диаметр основной окружности:
    db1 = d1 * math.cos(a) 
    #db1 = d1 * math.cos(math.radians(a))
    db2 = d2 * math.cos(a) 
    #db2 = d2 * math.cos(math.radians(a))
    print("db1 = ",db1," db2 = ",db2)
    # Суммарный коэффициент смещений:
    X = x1+x2
    print("X = ",X)
    # Толщина зуба по дуге делительной окружности:
    S1= 0.5 * p + 2 * x1 * m * math.tan(math.radians(a))
    S2= 0.5 * p + 2 * x2 * m * math.tan(math.radians(a))
    print("S1 = ",S1," S2 = ",S2)
    # Угол зацепления
    #inv a 
    inv_a=math.tan(math.radians(a))- math.radians(a)
    #Угол зацепления invαw
    inv_aw= (2 * X - math.tan(math.radians(a))) / (z1+z2) + inv_a
    # для invαw по справочнику Анурьева (Т2, таблица 16, стр. 421 ) подбираем αw = 24°25'.
    a_w = 24.25
    # Начальное межосевое расстояние:
    aw = ( (z1 +z2) * m * math.cos(math.radians(a))) / (2 * math.cos(math.radians(a_w)))
    print("aw = ",aw)




Evolventa()






"""angie_A:float = 90 #
#print(" Первый Угол  =  ",angie_A)
#angie_B:float = 3.3
angie_B:float = float(input("Введите уго наклона зуба  ")) #
#print("Вы вели Угол наклона зуба = ",angie_B)
angie_Y:float = 180 - (angie_A + angie_B) #
#print("angie_Y ",angie_Y)

side_c:float = float(input("Введите высоту детали  ")) #
#print("Вы ввели = ",side_c)

side_a = side_c * math.sin(math.radians(angie_A)) / math.sin(math.radians(angie_Y))
#print("side_a ",side_a)        

side_b = side_c * math.sin(math.radians(angie_B)) / math.sin(math.radians(angie_Y))
print("сторона по оси Х = ",side_b)   

sid_a:float = float(input("Введите диаметр детали "))/2

sid_c:float = sid_a

angi_B = float('{:.3f}'.format(math.degrees(math.acos((sid_a**2+sid_c**2-side_b**2)/(2*sid_a*sid_c)))))
print("Угол поворота стола ",angi_B)
print("")
print("")

a=20

inva=math.tan(math.radians(a))-math.radians(a)
print(math.radians(a))
print(math.tan(math.radians(a)))
print(inva)
inva=math.tan(math.radians(a))-math.radians(a)"""


