# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import os, sys

import win32com.client as win32

import tkinter as tk

import numpy as np

import pandas as pd

import re

import sqlparse

from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

from tkinter.filedialog import askopenfilename

import sys
sys.setrecursionlimit(10000) # 10000 is an example, try with different values

'''
pat_SIUD = re.compile(".*(?=SELECT|INSERT|DELETE|UPDATE).*",flags = re.DOTALL)
pat_strt_double_quote = re.compile(r"^\"",flags = re.DOTALL)
pat_end_double_quote = re.compile("(\"$)",flags = re.DOTALL)
pat_strt_newline = re.compile("(^\r\n)",flags = re.DOTALL)
pat_strt_blank_SELECT = re.compile("(?:^\s)(\s*)(?:SELECT)",flags = re.DOTALL) 
'''

pat_select_overall = re.compile(".*(?=SELECT).*",flags = re.DOTALL)
pat_DECLARE = re.compile("(?:^DECLARE)(.+?)(?:FOR)",flags = re.DOTALL)

pat_view = re.compile("(^(V|T)\S*(\s|$))|(^\S*\.(V|T)\S*(\s|$))",re.IGNORECASE)
pat_FROM = re.compile("^FROM$",re.IGNORECASE)
pat_WHERE = re.compile("^WHERE$",re.IGNORECASE)
pat_SELECT = re.compile("^SELECT$",re.IGNORECASE)
pat_ON = re.compile("^ON$",re.IGNORECASE)

#------------------------------------------------------------------------

def parse_gen(tree_list,lvl):
    global keep, from_sw

    if len(tree_list) == 0 : 
        if lvl == 0 :
            return
        else : 
            yield from parse_gen(keep[lvl-1],lvl-1 ) 
    
    if len(keep[lvl]) == 0 : 
        keep[lvl] = tree_list 

    print('LEVEL:' + str(lvl))
    if len(keep[lvl]) == 0 :
        return

    if keep[lvl][0].is_group: 
        #print ('group')
        #print (keep[lvl][0])
        keepx = keep[lvl][0]
        keep[lvl] = keep[lvl][1:]

        if isinstance(keepx, IdentifierList):

            for t in keepx.get_identifiers():
                pass
                #yield str(t) + "\n"
        else: 
            #yield str(len(keepx.tokens)) + str(keepx)

            if len(keepx.tokens) > 1 :
                for k in keepx.tokens:
                    #yield str(k) + "\n"
                    pass

        
        keep[lvl+1] = keepx.tokens
        print ('going to group : ' + str(lvl+1))
        yield from parse_gen(keep[lvl+1],lvl+1 ) 

        
    else:
        keepx = keep[lvl][0]
        keep[lvl] = keep[lvl][1:]
        print (keepx)
        if   re.search(pat_FROM ,str(keepx)) is not None : 
            from_sw = 1
        elif re.search(pat_WHERE ,str(keepx)) is not None : 
            from_sw = 0
        elif re.search(pat_SELECT ,str(keepx)) is not None : 
            from_sw = 0
        elif re.search(pat_ON ,str(keepx)) is not None : 
            from_sw = 0
        else :              
            if (re.search(pat_view ,str(keepx)) is not None) and (from_sw == 1):     
            #if   re.search(pat_view ,str(keepx)) is not None and from_sw == 1: 
                yield str(keepx)
        yield from parse_gen(keep[lvl],lvl ) 


 

#------------------------------------------------------------------------
root = tk.Tk() 
root.withdraw()
filename = askopenfilename(parent=root)

df_in = pd.read_csv(filename )

df_in = df_in.fillna('')


df_0_1= df_in.iloc[:,0:2]


df_1_n = df_in.iloc[:,2:]


df_1_n = df_1_n.applymap(lambda x: re.sub(pat_DECLARE, '', x))

df_1_n = df_1_n.applymap(lambda x: x.strip())

df_1_select = df_1_n[df_1_n.applymap(lambda x: (re.search(pat_select_overall,x)  is not None) )]
df_1_select  = df_1_select .fillna('')

df_select_1 = pd.concat([df_0_1, df_1_select ], axis = 1)

#df_select = df_select_1.iloc[24:25,:]
df_select = df_select_1 

r'''
with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sqlacum.txt', 'w') as f:
    for index, row in df_select.iterrows():
        pgm = row[1]
        for x in row[2: ]:
            if x != '':
                f.write('\n------------------------------------------------\n')     
                f.write('>>>>:  '+pgm)      
                f.write('\n------------------------------\n')                
                f.write(x)  
'''
    
                    
sql ="""
SELECT A.BU_CD,
        A.MJR_SGRP_CD,                                           
        A.MJR_SGRP_SHRT_DSC,
        A.MJR_SGRP_EXP_DT
   FROM VMAJOR_SUBGROUP A                                        
  WHERE A.MJR_SGRP_CD <> '00'
   AND  A.MJR_SGRP_EXP_DT = (SELECT MAX(B.MJR_SGRP_EXP_DT)
                              FROM VMAJOR_SUBGROUP B
                              WHERE A.BU_CD = B.BU_CD
                               AND  A.MJR_SGRP_CD =
                                    B.MJR_SGRP_CD)
  ORDER BY A.MJR_SGRP_CD
    FOR FETCH ONLY                                               
   WITH UR
"""

df_select_view = pd.DataFrame(columns=['pgm','view_list'])

l1_tot = [([]) for i in range(10000)]
for index, row in df_select.iterrows():
    pgm = row[1]
    l1 = []
    print (index)
    for sql in row[2: ]:
        if sql != '':
            keep = [([]) for i in range(1000)]
            parsed = sqlparse.parse(sql)[0]
            keep[0] =  parsed.tokens
            from_sw = 0   
            stream = parse_gen(keep[0],0)
            for k in stream:
                if len(l1) == 0 : 
                    l1 = [k]  
                else :
                    l1.extend([k]) 
                    
    l1_tot[index] = sorted(list(set(l1)))  



r'''
l_pgm = ['p1','p2']

df_select_1['pgm'] =  l_pgm

list_of_list = [[1,2],[1,2,3]]

df_select_1['view_list'] =  list_of_list


pd_t['mbr'] =  pd.DataFrame([[l1_nodup],[l1_nodup]])

c2 = np.array([[l1_nodup]])

c1 = np.array([file_sel] * len(tot_PO_mbr_1))[: , np.newaxis]
c2 = np.array([l1_nodup])[: , np.newaxis]
c3 = np.array(tot_PO_mbr_2)

arrx_PO_MBR = np.hstack([c1,c2,c3])

                
    l1_nodup = sorted(list(set(l1)))  
    
    pd_t[0][:] =  pd.DataFrame([[l1_nodup],[l1_nodup]])
 
    c2 = np.array(l1_nodup)[: , np.newaxis]    
    
    c2 = np.array(l1_nodup)[:]        
    
    
    c1 = np.array([file_sel] * len(tot_PO_mbr_1))[: , np.newaxis]
    c2 = np.array(tot_PO_mbr_1)[: , np.newaxis]
    c3 = np.array(tot_PO_mbr_2)
    
    
    
    arr0 = np.array(pgm)  
    arr1 = np.array([[l1_nodup]]) 
    
    arr2 = np.hstack([arr0,arr1 ]) 
    
    if len(arry_PO_MBR) == 0 : 
        arry_PO_MBR = arrx_PO_MBR 
    else :
        arry_PO_MBR = np.vstack([arry_PO_MBR,arrx_PO_MBR ]) 
    
    
    
    c2 = np.array(l1_nodup)[: , np.newaxis]
    
    arr_select_1  = np.array(pgm,np.array(l1_nodup) 
    
    df
    if len(l1_tot) == 0 : 
        l1_tot = [pgm,l1_nodup]  
    else :
        l1.extend([k]) 

                 
    if index == 3  : break

        arrx_PO = np.hstack([np.array([file_sel] * len(tot_PO_1))[: , np.newaxis] ,np.array(tot_PO_1)[: , np.newaxis]])

        if len(arry_PO_MBR) == 0 : 
            arry_PO_MBR = arrx_PO
        else :
            arry_PO_MBR = np.vstack([arry_PO_MBR,arrx_PO])                     



        
    #df_select_crud  = pd.concat([df_0_1, df_1_select ], axis = 1)



#with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sql2acum.txt', 'w') as f:
#    for k in parse_gen(keep[0],0):
#        f.write(str(k))
'''