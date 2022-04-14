# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 09:57:47 2022

@author: A90127
"""

import numpy as np
from pandas import read_excel

def specDict(path):    
    #回傳染劑名稱->濃度陣列 光譜陣列字典
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

if __name__ == '__main__':
    path = r'D:\A90127\ColorPermutation\excel\spectrum_dye_ver1.xlsx'
    Dyes = specDict(path)