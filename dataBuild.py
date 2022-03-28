# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 08:30:40 2021

@author: A90127
"""

'''
從路徑檔建立回傳基礎資料
'''

import numpy as np
from pandas import read_csv, read_excel

#判斷該資料格是否存在 ''
def isdata(d):
    NoneType = type(None)
    if type(d)==NoneType:
        return False
    elif type(d)==str and len(d)==0:
        return False
    elif type(d)==float:
        return not np.isnan(d)
    else:
        return True
def myfunc(path):
    data = np.array(read_csv(path,low_memory=False))
    heads = np.array(read_csv(path[:-4]+'-head.csv').columns)
    return data, heads
#回傳在染房待染工卡數據 
def app_waitDye(path):
    data, heads = myfunc(path)
    subheads = ('工卡號','染單單號','表頭狀態','開卡量','站別','刷卡日期')
    inds = [i for i,t in enumerate(heads) if t in subheads]
    data = data[:,inds]
    data = [d for d in data if d[2] not in ['作廢','結案','強迫結案']]
    data = [d2 for d1,d2 in zip(data[0:-1],data[1:]) if d2[4]=='染色' and not isdata(d2[5]) and isdata(d1[5])]
    return np.array(data)

# 給待染色工卡資料waitDye,工卡配方資料recipeE,併染工卡資料mergeE,搜尋缸量範圍 m~M
# 回傳 ('工卡號','指染單號','開卡量','併染量','顏色','配方')等欄位資料矩陣
def app_meargeSearch(waitDye,recipeE,mergeE,m,M):
    #工卡號對應開卡量小程式
    def card2mass(card):
        ind = list(waitDye[:,0]).index(card)
        return waitDye[ind,3]
    #工卡號對應顏色小程式
    def card2colour(card):
        try:
            ind = list(recipeE[:,0]).index(card)
            return recipeE[ind,1]
        except:
            return ''
    #工卡號對應配方小程式:
    def card2recipe(card):
        #可能還沒打色打好 沒配方
        try:
            mat = [d for d in recipeE if d[0]==card]
            return [[d[2],d[3]] for d in mat]
        except:
            return []
    def card2mergemass(card):
        if card in Etotal.keys():
            return Etotal[card]
        else:
            return card2mass(card)
    #建立併染工卡併染量字典
    Etotal = {}    
    for c in mergeE.keys():
        if c != 'AllChildren':
            a = card2mass(c)
            b = [card2mass(cc) for cc in mergeE[c]]
            Etotal[c] = round(a+sum(b),2)
            
    #過濾掉併染子工卡
    waitDye = [ [d[0],d[1],d[3],card2mergemass(d[0]), card2colour(d[0]),card2recipe(d[0])] 
        for d in waitDye if d[0] not in mergeE['AllChildren'] ] 
    #過濾掉重量不在範圍內工卡
    waitDye = [d for d in waitDye if m<=max(d[2],d[3])<M]
    return waitDye
#回傳工卡的配方數據
def app_recipeE(path):
    data, heads = myfunc(path)
    subheads = ('工卡號','顏色','染劑代號','配方濃度(化驗)')
    inds = [i for i,t in enumerate(heads) if t in subheads]
    data = data[:,inds]
    return data
#回傳工卡->配方字典
def app_recipeDict(data):
    recipeDict ={}
    class Build:
        inner = []
        def __init__(self,name,color,dyes,concs):
            #工卡號
            self.name = name
            #顏色敘述
            self.color = color
            #濃度序列
            self.concs = concs
            #染劑序列
            self.dyes = dyes
    i0 = 0
    card = data[0,0]
    for i,d in enumerate(data):
        if d[0]!=card:
            recipeDict[card] = Build(card,data[i0,1],data[i0:i,2],data[i0:i,3])
            i0 = i
            card = d[0]
    recipeDict[card] = Build(card,data[i0,1],data[i0:,2],data[i0:,3])
    return recipeDict

#回傳染劑名稱->濃度陣列 光譜陣列字典
def app_spectrum(path):
    st_fiber_data = np.array(read_excel(path, 0))
    stT = np.array(read_excel(path, 1))
    stN = np.array(read_excel(path, 2))
    stD = np.array(read_excel(path, 3))
    matrials = ['T','N','D']
    sts = [stT,stN,stD]
    class Build:
        inner = []
        def __init__(self,material,conc,spec):
            self.material = material
            self.conc = conc
            self.spec = spec
            #self.wavelength = np.array(range(360,710,10))
    Dyes = {}
    for i,(m,st) in enumerate(zip(matrials,sts)):
        names = list(set(st[:,0]))
        for n in names:
            fiber_spec = st_fiber_data[i,2:]
            data = np.array([d for d in st if d[0]==n])
            spec = data[:,2:]
            conc = data[:,1]
            spec = np.vstack((fiber_spec,spec))
            conc = np.array([0]+list(data[:,1]))
            Dyes[n] = Build(m,conc.astype(float),spec.astype(float))        
    return Dyes

#回傳主工卡號->併染子工卡陣列字典
def mergeE(path):
    data =  np.array(read_excel(path))
    #建立併染字典 主工卡->子工卡序列
    merges = {}
    i0 = 0
    card = data[0,0]
    for i,d in enumerate(data):
        if d[0]!=card:
            merges[card] = data[i0:i,1]
            i0 = i
            card = data[i,0]
    merges[card] = data[i0:,1]
    merges['AllChildren'] = data[:,1] 
    return merges

#---------測試碼-------

if __name__ == '__main__':
    path = r'D:\A90127\ColorPermutation\excel\spectrum_dye_ver1.xlsx'
    Dyes = app_spectrum(path) 
