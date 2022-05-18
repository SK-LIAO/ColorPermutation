# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 10:53:11 2020

@author: A90127
"""

'''
CIE國際照明協會資訊相關計算
1. KS(ls) 給一個光譜數據ls, 回傳表觀濃度值
2. Strength(ls1,ls2) 給兩光譜數據ls1、ls2, 回傳力度 (光譜需相似才適用)
3. LAB2LCH(lab) 給定CIELAB座標lab, 回傳CIELCH座標
4. Spec2XXX(ls) 給定光譜數據ls, 回傳XXX色座標, 'XXX' 可以是 LAB LCH XYZ RGB
5. XXX2YYY(ls) 色座標的轉換, 'XXX' 'YYY' 可以是 LAB LCH XYZ RGB
6. DE2000(lab1,lab2) 給兩個CIELab座標lab1、labs, 回傳CIE deltaE 2000 色差 

'''


import numpy as np

from cieData import observer, SPD_D65, XYZ_D65
#給定表觀濃度ks 回傳反射率 
def KS2R(ks):
    r = 1+ks-(ks**2+2*ks)**0.5
    return r
#給特定波長反射率r 回傳表觀濃度KS值 
# *注意反射率r必須<=1
def KS(r):
    ks = (1-r)**2/2/r
    return ks
#給標準樣及批次樣的波長對映反射率 ls1 & ls2 回傳力度
def Strength(ls1, ls2):
    Str = KS(min(ls2))/KS(min(ls1))*100
    return Str
    
#給定反射率光譜陣列 spe, 光譜最小波長 lmin, 光譜最大波長 lmax, 波長間距 dl
#回傳 該光譜之 CIEXYZ 值  X_ref/Y_D65, Y_ref/Y_D65, Z_ref/Y_D65
def Spec2XYZ(ls):
    ls = np.array([1 if np.isnan(i) else i for i in ls])
    x, y, z = observer   
    S = SPD_D65
    Sx, Sy, Sz = S*x, S*y, S*z 
    X_ref = numInt(Sx*ls,10)
    Y_ref = numInt(Sy*ls,10)
    Z_ref = numInt(Sz*ls,10)
    Y_D65 = numInt(Sy,10)    
    return np.array([X_ref/Y_D65, Y_ref/Y_D65, Z_ref/Y_D65])
def Spec2RGB(ls):
    return XYZ2RGB(Spec2XYZ(ls))
#給定反射率光譜陣列 spe, 光譜最小波長 lmin, 光譜最大波長 lmax, 波長間距 dl
#回傳該光譜下之CIELab值 L a b
def Spec2LAB(ls):
    return XYZ2LAB(Spec2XYZ(ls))
def Spec2LCH(ls):
    return XYZ2LCH(Spec2XYZ(ls))

#CIELab座標轉換成CIELCH , 0<=H<360
def LAB2LCH(lab):
    l, a, b = lab
    C = np.sqrt(a**2+b**2)
    yi = 180/np.pi
    arct = np.arctan2(b,a)
    if b>=0:
        H = arct*yi
    else:
        H = arct*yi + 360
    return np.array([l, C, H])
def LCH2LAB(lch):
    L,C,H = lch
    deg = H/180*np.pi
    return np.array([L,C*np.cos(deg),C*np.sin(deg)])


#sRGBcom=True: 使用sRGB companding, 
#sRGBcom=True: 使用L* companding
def XYZ2RGB(xyz,sRGBcom = True):
    M_inv = np.array([[3.2404542, -1.5371385, -0.4985314],
                      [-0.9692660, 1.8760108, 0.0415560],
                      [0.0556434,-0.2040259,1.0572252]])
    if sRGBcom:
        def companding(x):
            if x <= 0.0031308:
                return 12.92*x
            else:
                return 1.055*np.power(x,1/2.4)-0.055
    else:
        def companding(x):
            if x<=216/24389:
                return x*24389/27/100
            else:
                return 1.16*np.power(x,1/3)-0.16
    sRGB = np.array([companding(x) for x in M_inv.dot(np.array(xyz))])
    RGB = [255 if i>255 else 0 if i<0 else int(i) for i in 255*sRGB]
    return np.array(RGB)
def RGB2XYZ(rgb,sRGBcom = True):        
    if max(rgb)>1:
        rgb = rgb/255
    if sRGBcom:
        def companding(x):
            if x <= 0.04045:
                return x/12.92
            else:
                return np.power((x+0.055)/1.055,2.4)
    else:
        def companding(x):
            if x<=0.08:
                return 2700*x/24389
            else:
                return ((x+0.16)/1.16)**3
    rgb = np.array([companding(x) for x in rgb])
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    return M.dot(np.array(rgb))



#給定CIEXYZ陣列 XYZ, 回傳該光譜下之CIELAB陣列 
def XYZ2LAB(xyz):
    X_D65, Y_D65, Z_D65 = XYZ_D65
    X , Y, Z = xyz
    def fLAB(t):
        if t>(6/29)**3:
            t = t**(1/3)
        else:
            t=t*(29/6)**2/3+16/116
        return t
    L = 116*fLAB(Y/Y_D65)-16
    a = 500*(fLAB(X/X_D65)-fLAB(Y/Y_D65))
    b = 200*(fLAB(Y/Y_D65)-fLAB(Z/Z_D65))    
    return np.array([L, a, b])
def LAB2XYZ(lab):
    X_D65, Y_D65, Z_D65 = XYZ_D65
    L , a, b = lab
    epsilon = 216/24389
    kappa = 24389/27
    def fXYZ_1(t):
        if t**3>epsilon:
            t = t**3
        else:
            t = (116*t-16)/kappa
        return t
    def fXYZ_2(t):
        if L>kappa*epsilon:
            t = t**3
        else:
            t = (116*t-16)/kappa
        return t
    fy = (L+16)/116
    fx = a/500 + fy
    fz = fy - b/200
    X = X_D65*fXYZ_1(fx)
    Y = Y_D65*fXYZ_2(fy)
    Z = Z_D65*fXYZ_1(fz)
    return np.array([X,Y,Z])

def LAB2RGB(lab):
    return XYZ2RGB(LAB2XYZ(lab))
def RGB2LAB(rgb):
    return XYZ2LAB(RGB2XYZ(rgb))

def XYZ2LCH(xyz):
    return LAB2LCH(XYZ2LAB(xyz))
def LCH2XYZ(lch):
    return LAB2XYZ(LCH2LAB(lch))

def LCH2RGB(lch):
    return XYZ2RGB(LCH2XYZ(lch))
def RGB2LCH(rgb):
    return LAB2LCH(RGB2LAB(rgb))

    
#給定標準樣及批次樣的波長對映陣列 LAB1 LAB2  回傳CIE2000色差 DE00    
def DE2000(Lab1,Lab2):
    if len(Lab1) == 3 and len(Lab2)==3:
        [StL, StA, StB] = Lab1
        [BaL, BaA, BaB] = Lab2 #定義標準樣及批次樣的 LCH座標
        #紡織業推薦比例 2:1:1
        KL, KC, KH = 2, 1, 1
        yi = 180/np.pi
        
        _, StC, StH = LAB2LCH(Lab1)
        _, BaC, BaH = LAB2LCH(Lab2)
        
        DEL = BaL - StL
        DELL = DEL
        avL = (StL+BaL)/2
        avLL = avL
        avC = (StC+BaC)/2
        
        coe = np.sqrt(avC**7/(avC**7+25**7))
        
        StAA = StA*(1.5-coe/2)
        BaAA = BaA*(1.5-coe/2)
        
        _, StCC, StHh = LAB2LCH([StL,StAA,StB])
        _, BaCC, BaHh = LAB2LCH([BaL,BaAA,BaB])
        
        avCC = (StCC+BaCC)/2
        DECC = BaCC-StCC
        
        if abs(StHh-BaHh)<=180:
            DEHh = BaHh-StHh
        elif BaHh<=StHh:
            DEHh = BaHh-StHh+360
        else:
            DEHh = BaHh-StHh-360
        #DEHH不確定最後是否乘yi 考量單位 應該需要!但網路沒有 且結果吻合網路計算機 
        DEHH = 2*np.sqrt(StCC*BaCC)*np.sin(DEHh/2/yi) 
               
        #avHH有兩種寫法 三段分式為英文版wiki寫法
        #兩段分式 為 計算機網站寫法
        '''    
        if abs(StHh-BaHh)<=180:
            avHH = (StHh+BaHh)/2
        elif StHh+BaHh<360 :
            avHH = (StHh+BaHh+360)/2
        else:
            avHH = (StHh+BaHh-360)/2
        ''' 
        if abs(StHh-BaHh)<=180:
            avHH = (StHh+BaHh)/2
        else:
            avHH = (StHh+BaHh+360)/2
    
        
        T = 1-0.17*np.cos((avHH-30)/yi)+0.24*np.cos(2*avHH/yi)\
            +0.32*np.cos((3*avHH+6)/yi)-0.2*np.cos((4*avHH-63)/yi)
        
        SL = 1+0.015*(avLL-50)**2/np.sqrt(20+(avLL-50)**2)
        SC = 1+0.045*avCC
        SH = 1+0.015*avCC*T
        
        coe2 = np.sqrt(avCC**7/(avCC**7+25**7))
        RT = -2*coe2*np.sin((60*np.exp(-(avHH/25-11)**2))/yi)
        
        DE00 = np.sqrt((DELL/KL/SL)**2+(DECC/KC/SC)**2+(DEHH/KH/SH)**2+RT*DECC*DEHH/KC/SC/KH/SH)
    else:
        print('座標長度不正確')
        DE00 = False
    return DE00


#計算數值積分 偶區間用辛普森 奇區間用 梯形
# ls:函數值陣列 dt:切割大小 
def numInt(ls,dt):
    coe = np.ones(len(ls))
    if len(ls) % 2 == 0:
        coe[1:-1] = np.array([2 for _ in range(len(coe[1:-1]))])
        return sum(ls*coe)*dt/2
    else:
        coe[1:-1:2] = np.array([4 for _ in range(len(coe[1:-1:2]))])
        coe[2:-2:2] = np.array([2 for _ in range(len(coe[2:-2:2]))])
        return sum(ls*coe)*dt/3





