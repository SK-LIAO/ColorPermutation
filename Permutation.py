# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:02:38 2022

@author: A90127
"""

from DyeMerge import IsFluo,SpecEst,Merge,ContactDE
from cieMath import Spec2LAB 
from numpy import array
from DyeMerge import app_E2LAB

'''
將工卡依照接色後汙染最小排序
'''
#接受工卡序列、工卡配方字典、染劑光譜字典
#回傳重新接色排序後送回重新排序 矩陣資訊。                
class app_colorPermutation:
    def __init__(self, Ecards, recipeDict,dyesDict):
        self.Ecards = Ecards
        #工卡字典 -> concs & dyes
        self.E2recipe = recipeDict
        #染劑字典 -> conc & spec
        self.D2spec  = dyesDict
        #工卡對映Lab座標的字典,將會再分類螢光非螢光工卡時建立細節
        self.LABdict = {}
        #螢光色工卡 與 非螢光色工卡
        self.Fcards, self.NFcards = self.allfluo()
        #紀錄重排的結果 
        self.resort = self.DYBest()
        #儲存接色的的陣列  ['工卡','顏色','色差','配方']
        self.lst = []
        for c1,c2 in zip(self.resort[:-1], self.resort[1:]):
            color = [] if c1=='清缸' else self.LABdict[c1]
            try:
                DE = ContactDE(c1,c2,self.E2recipe,self.D2spec)
            except:
                DE = ''
            try:
                recipe = ', '.join([d+': {}'.format(n) for d,n in zip(self.E2recipe[c1].dyes,self.E2recipe[c1].concs)])
            except:
                recipe = ''
            self.lst += [ [c1,color,DE,recipe] ]
        #補進最後一列
        color = [] if c2=='清缸' else self.LABdict[c2]
        DE = ''
        try:
            recipe = ', '.join([d+': {}'.format(n) for d,n in zip(self.E2recipe[c2].dyes,self.E2recipe[c2].concs)])
        except:
            recipe = ''
        self.lst += [ [c2,color,DE,recipe] ]
        

    
    
    #將所有工卡分成螢光類與非螢光類 並將螢光類由淺至深回傳
    def allfluo(self):
        F = [[e,self.E2LAB(e)] for e in self.Ecards if IsFluo(self.E2recipe[e].dyes)]
        NF = [[e,self.E2LAB(e)] for e in self.Ecards if not IsFluo(self.E2recipe[e].dyes)]
        F = sorted(F,key=lambda x:x[1][0],reverse=True)
        NF = sorted(NF,key=lambda x:x[1][0],reverse=True)
        return [c[0] for c in F], [c[0] for c in NF]
   
    #給工卡號、染劑字典、回傳LAB值，非單色回傳較深顏色的LAB。
    def E2LAB(self,e):
        material = ['T','N','D']
        '''
        labs = []
        for m in material:
            dyes = [d for d in self.E2recipe[e].dyes if self.D2spec[d].material==m]
            if dyes:
                concs = [c for d,c in zip(self.E2recipe[e].dyes,self.E2recipe[e].concs) if self.D2spec[d].material==m ]
                specfib = self.D2spec[dyes[0]].spec[0]
                fl = IsFluo(dyes)
                if fl:
                    specs = [SpecEst(self.D2spec[d].conc,self.D2spec[d].spec,sum(concs),IsFluo([d])) for d in dyes]
                    spec = Merge(concs,specs,specfib,'nonequi',fl)
                    labs += [ array([round(i,2) for i in Spec2LAB(spec)]) ]
                else:
                    specs = [SpecEst(self.D2spec[d].conc,self.D2spec[d].spec,c,IsFluo([d])) for c,d in zip(concs,dyes)]
                    spec = Merge(concs,specs,specfib,'KSadd',fl)
                    labs += [ array([round(i,2) for i in Spec2LAB(spec)]) ]
            else:
                labs += [ array([100,0,0]) ]
        '''
        
        _dict = app_E2LAB(e,self.E2recipe,self.D2spec)
        labs = [_dict[m] if m in _dict.keys() else array([100,0,0]) for m in material]
        #順便儲存下工卡的Lab座標
        self.LABdict[e] = [[] if i[0]==100 else list(i) for i in labs]
        #回傳最深色Lab座標
        return sorted(labs,key = lambda x:x[0])[0]
      
    def DYBest(self):
        def c2cDE(c1,c2):
            return ContactDE(c1,c2,self.E2recipe,self.D2spec)
        paragraph = []    #蒐集段,每段間需要洗缸
        for i in (self.Fcards, self.NFcards):
            #若工卡串為空則跳過
            if not i:
                continue
            cs = i.copy()
            ls = [ cs[0] ] #蒐集卡,可接色卡完成後就成為一段
            cs.remove(ls[-1])
            while len(cs)>0:
                #找出可接色的色卡 先設定小於0.6則可接色
                candidate = [ [c,c2cDE(ls[-1],c)] for c in cs if c2cDE(ls[-1], c)<0.6 ]
                #若有可接色就接
                while len(candidate)>0:
                    cmin = sorted(candidate, key=lambda x:x[1])[0]
                    ls += [ cmin[0] ]
                    cs.remove(cmin[0])
                    candidate = [ [c,c2cDE(ls[-1],c)] for c in cs if c2cDE(ls[-1], c)<0.6 ]
                #將剩下色卡、找出該段可以插入位置插入，
                while len(cs)>0:
                    for c in cs:
                        inds = [ [ i,max([c2cDE(c1,c),c2cDE(c,c2)]) ] 
                                for i, (c1,c2) in enumerate(zip(ls[:-1],ls[1:])) 
                                if c2cDE(c1,c)<0.6 and c2cDE(c,c2)<0.6 ]
                        if len(inds)>0:
                            i = sorted(inds,key=lambda x:x[1])[0][0]
                            ls = ls[0:i+1]+[c]+ls[i+1:]
                            cs.remove(c)
                            break
                    #當剩下的工卡都插不進去時、另外開啟新段重跑
                    else:
                        paragraph += [ls]
                        ls = []
                        if len(cs)>0:
                            ls += [ cs[0] ]
                            cs.remove(ls[-1])
                        break
            #將最後一段也補進排程裡
            if len(ls)>0:                      
                paragraph += [ls]

        #補進不能接色的清缸段
        ccs = []
        for i in paragraph[:-1]:
            ccs +=  i+['清缸'] 
        ccs +=  paragraph[-1] 
        return ccs
    