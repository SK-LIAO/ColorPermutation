# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 08:12:54 2021

@author: A90127
"""

'''
混色光譜計算 與 光譜找配方 
1. SpecEst 給定濃度陣列 conc 與光譜陣列 spec, 回傳推測濃度C 的光譜

'''

import numpy as np

from cieMath import KS, KS2R, Spec2LAB,Spec2RGB ,DE2000
from itertools import product, combinations
from math import factorial

def SpecEst(concls,specls,C,flour=False):     
    if C<0:
        print('Error : 濃度出現負值')
        return specls[0]
    elif C > concls[-1]:
        #螢光劑使用最大力度相似形估計法、非螢光劑使用KS力度加法估計(因為螢光劑反射率大於1,於公式不符)
        if flour:
            #print('Note : 濃度超出實驗範圍、採取K-M Theory估計法')
            #計算表觀濃度
            ks = KS(min(specls[-1]))
            x = C/concls[-1]
            #1.078為調修參數
            est_ks = x*ks/1.078 if x*ks/1.078>ks else x*ks
            
            #est_KS利用K-M theory估計最小值並扣掉修正量(因實驗結果總是 實際的濃度比值大於力度)
            est_R_min = 1 + est_ks - np.sqrt(est_ks**2+2*est_ks)
            if min(specls[-1])-min(specls[-2]) == 0:
                est_R = specls[-1] + (est_R_min - min(specls[-1]))
            else:
                R = specls[-1] + (est_R_min - min(specls[-1]))/(min(specls[-1])-min(specls[-2]))*(specls[-1]-specls[-2])
                est_R = np.array([max(i,est_R_min) for i in R])
        else:
            #KS力度加法估計
            n = int(C//concls[-1])
            concs = np.array([concls[-1] for _ in range(n)] + [ C%concls[-1] ])
            specs = np.array([SpecEst(concls, specls, c) for c in concs])
            est_R = Merge(concs,specs,specls[0])
        
    else:
        #找出中心點的ind、並根據是否為端點改變鄰近點的ind
        ind = np.argmin(abs(concls-C)) 
        if ind == 0:
            ref_ind = [0,1,2]
        elif ind == len(concls)-1:
            ref_ind = [ind,ind-1,ind-2]   
        else:
            ref_ind = [ind,ind-1,ind+1]
        
        #求一皆導數 與 二皆導數
        x = np.array([concls[i] for i in ref_ind])
        f = np.array([specls[i,:] for i in ref_ind])
        Dx1 = x[1]-x[0]
        Dx2 = x[2]-x[0]
        Df1 = f[1]-f[0]
        Df2 = f[2]-f[0]
        det = Dx1*Dx2*(Dx2-Dx1)
        df_dx = (Df1*Dx2**2-Df2*Dx1**2)/det
        d2f_dx2 = 2*(Dx1*Df2-Dx2*Df1)/det
        
        #泰勒多項式二街插值
        Dx = C-x[0]
        est_R = f[0] + df_dx*Dx  + d2f_dx2*Dx**2/2
    return np.array(est_R)

    
#給定染劑濃度陣列concls 和對映濃度光譜陣列specls
#方法有: 'equi'(等效),'noequi'(非等效), 'KSaddition'(力度加法)
#注意:等效、非等效的方法光譜數據為總濃度的光譜、力度加法的光譜為各自濃度的光譜。
#若含有螢光劑flour=True, 則採用非等效估計
def Merge(concs,specs,specfiber,method='KSadd',flour=False):
    if flour:
        method = 'nonequi'
    specs = [j for i,j in zip(concs,specs) if i!=0]
    concs = [i for i in concs if i!=0]
    if  len(concs)== 0:
        return specfiber
    elif len(concs) == 1:
        return specs[0]
    C = sum(concs)
    if method=='nonequi':                   
        impls = [c*np.power(abs(np.array(specfiber-R)),0.35) for c,R in zip(concs,specs)]
        R_est = np.zeros(len(specfiber))
        for coe, R in zip(impls,specs):
            R_est += np.array(coe)*np.array(R)/sum(np.array(impls))
    elif method=='equi':
        DR_dye = [R-specfiber for R in specs]
        R_est = np.zeros(len(specfiber)) + specfiber 
        for c, R in zip(concs,DR_dye):
            if C>0:
                R_est += c/C*R
    else:
        ksfiber = np.array([KS(r) for r in specfiber])
        ksls = np.array([[KS(r1)-KS(r2) for r1,r2 in zip(spec,specfiber)] for spec in specs ])
        ks_est = sum(ksls) + ksfiber
        R_est = np.array([KS2R(i) for i in ks_est])
    return R_est


def IsFluo(dyes):
    FDye = ['TF405','TF406','TR106','TR117','TY206','NR105','NY202',
               'NF404','DR102','DR103','DR104','DY203']
    for dye in dyes:
        if dye in FDye:
            return True
    else:
        return False



#給定targetLAB、數支染劑濃度concls、光譜陣列specls
#回傳配方組序列
def DyeMatch(targetLAB,conclsls,speclsls):
    #給定targetLAB、數據庫裡數支染劑的濃度陣列conclsls、光譜陣列speclsls
    #回傳濃度網格點最靠近目標LAB的濃度陣列
    specfiber = speclsls[0][0]
    def GridConcMin():
        Specs = [Merge(np.array(cs),np.array(ls),specfiber) for cs,ls in zip(product(*conclsls),product(*speclsls))] 
        LabCs = [(Spec2LAB(s),c) for s,c in zip(Specs,product(*conclsls))]
        DeLabCs = [(DE2000(i[0],targetLAB),i[0],i[1]) for i in LabCs]
        S = sorted(DeLabCs,key= lambda x:x[0])
        return S[0][0],np.array(S[0][1]) ,np.array(S[0][2])  
    #設定 初始色差 與 濃度
    deltaE, labAprox, cAprox = GridConcMin()
    #初始步近距離
    stepdis = sum(cAprox)/6
    #步近距離調整參數
    n = 0
    #計算差分(用來取代微分)
    def dE_dConc(concs,lab):
        DEDC = np.zeros(len(concs))
        dc = 0.0000001 #配方濃度精度0.0001, 取精度的1/1000取代微分
        for i,c in enumerate(concs):
            newconcs = np.array([c+dc if i==j else c for j,c in enumerate(concs)])
            specs = np.array([SpecEst(conclsls[i], speclsls[i], c) for i,c in enumerate(newconcs)])
            newlab = Spec2LAB(Merge(newconcs, specs, specfiber))
            DEDC[i] = (DE2000(newlab,targetLAB)-DE2000(lab,targetLAB))/dc
        if np.linalg.norm(DEDC)>1:
            DEDC = DEDC/np.linalg.norm(DEDC)
        return DEDC
        
    #當步近距離和色差都不夠小時、則繼續疊代找Minimizer
    while n<15 and deltaE > 0.02: #配方濃度精度 0.0001(0.5**13=0.000122),測色機精度 0.02
        #沿梯度下降    
        cAprox_temp = cAprox - 0.5**n*stepdis*dE_dConc(cAprox,labAprox)
        #修正濃度出現負值
        for i in range(len(cAprox_temp)):
            if cAprox_temp[i] < 0:
                cAprox_temp[i] = 0                
        #測試修正後色差，若有變小則取代、若無變小則修正步進距離參數 n
        specs_temp = np.array([SpecEst(conclsls[i], speclsls[i], c) for i,c in enumerate(cAprox_temp)])
        lab_temp = Spec2LAB(Merge(cAprox_temp, specs_temp, specfiber))
        if DE2000(targetLAB,lab_temp) >= deltaE:
            n += 1
        else:
            deltaE = DE2000(targetLAB,lab_temp)
            cAprox = cAprox_temp
            labAprox = lab_temp
            print('^{}'.format(n),', DE=',deltaE)
    return cAprox, deltaE


#給n支染劑濃度序列組成的矩陣 concs 與 測色後色差矩陣 Dlabs
#回傳 建議染劑濃度序列
def ConcCentroid(concs,Dlabs):
    #給定n維空間n+1點 為基底的矩陣 Mat =  [[-v1-],[-v2-],...,[-vn+1-]]
    #回傳原點的線性組合係數
    def LineCoe(Mat):
        n = len(Mat)
        bag = np.array(list(combinations(list(range(n)), n-1)))    
        weight = np.zeros(n)
        for i in range(n):
            vectors = Mat[bag[i]]
            weight[n-i-1] = abs(np.linalg.det(vectors))/factorial(n-1)
        W = sum(weight)    
        return weight/W
    weight = LineCoe(Dlabs)
    Dconcs = np.array([c-concs[0] for c in concs])
    return concs[0] + np.array([w*v for w,v in zip(weight,Dconcs)]).sum(axis=0)

#給定兩張工卡、配方字典、光譜字典,回傳接色後的色差
def ContactDE(card1,card2,recipeDict,specDict):
    dyes1, concs1 = recipeDict[card1].dyes, recipeDict[card1].concs
    dyes2, concs2 = recipeDict[card2].dyes, recipeDict[card2].concs
    #色差矩陣
    err = np.zeros((3,3))
    #殘留量矩陣
    residue = np.array([[ 0.05, 0.05, 0.05],
                        [ 0.00, 0.05, 0.00],
                        [ 0.01, 0.01, 0.05]])
    fibtype = ['T','N','D']
    fiberSpec = [specDict[i].spec[0,:] for i in ['TR101','NR101','DR101']] 
    for i in range(3):
        for j in range(3):
            conc1 = [c for c, n in zip(concs1,dyes1) if specDict[n].material==fibtype[i] ]
            name1 = [n for n in dyes1 if specDict[n].material==fibtype[i] ]
            conc2 = [c for c, n in zip(concs2,dyes2) if specDict[n].material==fibtype[j] ]
            name2 = [n for n in dyes2 if specDict[n].material==fibtype[j] ]
            #判定是否含螢光劑
            fl = IsFluo(list(name1)+list(name2))

        #若沒接到色則色差為0，有接色才計算色差
            if name2==[] or name1==[]:
                continue
            else:
                #根據殘留矩陣估計殘留染劑給下一缸、且先不考慮缸量差
                #但前一缸無染劑則殘留係數為0,避免下一缸被稀釋。
                if len(conc1)==0:
                    r = 0
                else:
                    r = residue[i,j]
                #如果含有螢光劑採用nonequi演算法
                if fl:
                    #理想光譜
                    specls_re = [SpecEst(specDict[n].conc,specDict[n].spec,sum(conc2),IsFluo([n])) for n in name2]
                    spec_re = Merge(conc2,specls_re,fiberSpec[j],'nonequi',True)
                    #混色光譜
                    conc1_mer = [c*r/(1+r) for c in conc1]
                    conc2_mer = [c/(1+r) for c in conc2]
                    c = sum(conc1_mer+conc2_mer)
                    specls1_mer = [SpecEst(specDict[n].conc,specDict[n].spec,c,IsFluo([n])) for n in name1]
                    specls2_mer = [SpecEst(specDict[n].conc,specDict[n].spec,c,IsFluo([n])) for n in name2]        
                    spec_mer = Merge(conc2_mer+conc1_mer,specls2_mer+specls1_mer,fiberSpec[j],'nonequi',True)
                #不含螢光劑才用KSadd演算法
                else:
                    #找理想光譜
                    specls_re = [SpecEst(specDict[n].conc,specDict[n].spec,c,IsFluo([n])) for c,n in zip(conc2,name2)]
                    spec_re = Merge(conc2,specls_re,fiberSpec[j],'KSadd',False)
                    #找混色光譜
                    conc1_mer = [c*r/(1+r) for c in conc1]
                    conc2_mer = [c/(1+r) for c in conc2]
                    #將同染劑融合
                    name = list(set(name1+name2))
                    conc_mer = [sum([c for c,n in zip(conc1_mer+conc2_mer,name1+name2) if n==m]) for m in name]
                    specls_mer = [SpecEst(specDict[n].conc,specDict[n].spec,c,IsFluo([n])) for c,n in zip(conc_mer,name)]
                    spec_mer = Merge(conc_mer, specls_mer, fiberSpec[j],'KSadd',False)                   
                #存進色差矩陣
                err[i,j] = DE2000(Spec2LAB(spec_re),Spec2LAB(spec_mer))
    return round(np.max(err),2)

#給定工卡號、配方字典、光譜字典
#回傳材質對應顏色的RGB字典
def app_colorVisual(card,recipeDict,Dyes): 
    allconcs = recipeDict[card].concs
    alldyes = recipeDict[card].dyes
    
    colorDict={}
    material = ['T','N','D']
    for m in material:
        dyes = [n for n in alldyes if Dyes[n].material==m]
        if len(dyes)>0:
            concs = [c for c,n in zip(allconcs,alldyes) if Dyes[n].material==m]
            cl = IsFluo(dyes)
            fiberspec = Dyes[dyes[0]].spec[0]
            if cl:
                specs = [SpecEst(Dyes[n].conc,Dyes[n].spec,sum(concs),IsFluo([n])) for n in dyes]
                spec_est = Merge(concs, specs, fiberspec,'nonequi',True)
            else:
                specs = [SpecEst(Dyes[n].conc,Dyes[n].spec,c,IsFluo([n])) for c,n in zip(concs,dyes)]
                spec_est = Merge(concs, specs, fiberspec,'KSadd',False)  
            rgb = RGB2Hex(Spec2RGB(spec_est))
            colorDict[m] = rgb
    return colorDict

# RGB格式顏色轉換爲16進制顏色格式
def RGB2Hex(RGB):            
    color = '#'
    for i in RGB:
        # 將R、G、B分別轉化爲16進制拼接轉換並大寫  hex() 函數用於將10進制整數轉換成16進制，以字符串形式表示
        color += str(hex(i))[-2:].replace('x', '0').upper()
    return color


    

    