# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:04:49 2018

@author: XT21586
"""

import ftplib
import pyodbc
import numpy as np
import pandas as pd
import re
import io

import win32com.client as win32

import os,sys

from contextlib import redirect_stdout




path = os.getcwd()        
in_file = path+"\\input\\"+'Grab_all_file_with_FTP.csv'


search_identification  = re.compile('IDENTIFICATION DIVISION')


debug_iter_limit = 10


'''
    
print( 'calling excel....')

excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(in_file)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()
excel.Quit()


input("Save Excel and quit excel before pressing enter? ") 

'''


labels = [
'flag', 'lv1'
]
df_seed = pd.read_csv(in_file , names=labels , skiprows = 1)
df_seed.fillna('', inplace=True)
# \w Any word character (letter, number, underscore )
df_seed  = df_seed[df_seed['flag'].str.contains(re.compile('\w'))] 


List_seed = df_seed['lv1'].values.tolist()

if len(List_seed) == 0 :
    print( "nothing selected in input : " + in_file)
    sys.exit(0)

sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')

out_file_PO = path+"\\result\\"+'Grab_all_file_PO.csv' 
if os.path.exists(out_file_PO):
    os.remove(out_file_PO)	
        

for lv1 in List_seed :
    tot_PO = []   
    #arr_tot = np.array([],dtype=np.str)
    arr_PO = np.array([],dtype=np.str)
    print( lv1 )
    try:
        sess.cwd("'" + lv1 + "'")
        #file_list = sess.nlst()
        f = io.StringIO()
        with redirect_stdout(f):
            sess.dir()

    except:
        print (lv1 + ' :not found or no permission')
        continue             
     
    #[1:] we start after header
    #test = np.array(f.getvalue().splitlines())[0]
    #Volume Unit    Referred Ext Used Recfm Lrecl BlkSz Dsorg Dsname
    
    arr_1 = np.array(f.getvalue().splitlines())[1:]
    
    #arr_ARCIVE = arr_1[pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
    #arr_ARCIVE_s = np.array([re.findall(r'\S+', x) for x in arr_ARCIVE])  
    #arr_ARCIVE_s1 = np.array([lv1 + "." + x[5] for x in arr_ARCIVE_s ]) 
    #arr_tot = np.append(arr_tot, arr_ARCIVE_s1)
    
    arr_NOT_ARCIVE = arr_1[~pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
    arr_NOT_ARCIVE_s = np.array([re.findall(r'\S+', x) for x in arr_NOT_ARCIVE])   
 
    
    arr_NOT_ARCIVE_s1 = arr_NOT_ARCIVE_s[[ (x[1] != 'Tape') & (x[1] != 'Error') & (x[0] != 'GDG') for x in arr_NOT_ARCIVE_s ]] 

    
    #arr1_NOT_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    #arr2_NOT_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    #arr_NOT_PO = np.hstack([arr1_NOT_PO,arr2_NOT_PO])
    #arr_tot = np.append(arr_tot, arr_NOT_PO)
   

    
    arr1_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    arr2_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    
    if len(arr2_PO) > 0 : 
        arr_PO = np.hstack([arr1_PO,arr2_PO])
    else:
        arr_PO = arr1_PO

    for file_sel in arr_PO:
        debug_iter = 0   
        tot_PO_1 = []
        try:
            sess.cwd("'" + file_sel + "'")      
            mbr_list = sess.nlst()
            if len(tot_PO_1) == 0 : 
                tot_PO_1 = mbr_list
            else :
                tot_PO_1 = tot_PO_1.append(mbr_list)            
            
        except:
            if len(tot_PO_1) == 0 : 
                tot_PO_1 =  [' :not found or no permission']  
            else :
                tot_PO_1 = tot_PO_1.append( [' :not found or no permission'])
            continue                   

        arrx_PO = np.hstack([np.array([file_sel] * len(tot_PO_1))[: , np.newaxis] ,np.array(tot_PO_1)[: , np.newaxis]])
        
 
        
        
        if len(arr2_PO) > 0 : 
            arr_PO = np.hstack([arr1_PO,arr2_PO])
        else:
            arr_PO = arr1_PO
        
        
        mbr_list = ['a','b']
        tot_PO_1 = np.array(mbr_list)
        tot_PO_1 = tot_PO_1.append( ['DDDDD'])
        
        
        #for mbr_sel in mbr_list:                             
        #    tot = tot + [[file_sel,mbr_sel]]
            
        tot = tot.append(list(arr_PO))   
        
        
            
        print(file_sel,str(len(mbrlist)))    





df_out = pd.DataFrame(tot, columns= ['file','mbr','sql_list'])
    
#df_out.reindex
    
for i in range(50) :
    df_out = pd.concat((df_out,pd.DataFrame([ x[i]  for x in df_out['sql_list'] ], columns = ["sql"+str(i)] ) ), axis = 1)
 




sess.quit

print (arr_PO)

lv1 = 'xxxxx'
     
out_file = path+"\\result\\Mainframe_List_PO_"+lv1+".csv"

if os.path.exists(out_file):
    os.remove(out_file)	

df_out.to_csv(out_file,mode = 'w',header=True, index = False)

df_out.to_csv(out_file,mode = 'a', header=False, index = False)

df_out.columns
