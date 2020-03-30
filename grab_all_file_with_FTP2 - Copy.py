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


sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')

arr_tot_wrk_no_mbr = np.array([],dtype=np.str)
arr_tot_wrk_mbr1 = np.array([],dtype=np.str)
arr_tot_wrk_mbr2 = np.array([],dtype=np.str)
for x1 in List_seed :

    try:
        sess.cwd("'" + x1 + "'")
        #file_list = sess.nlst()
        f = io.StringIO()
        with redirect_stdout(f):
            sess.dir()
            
        arr_1 = np.array(f.getvalue().splitlines())      
        
        arr_ARCIVE = arr_1[pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        arr_NOT_ARCIVE = arr_1[~pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        
        arr_NOT_ARCIVEx = arr_NOT_ARCIVE[1:5]
        
        
        t_ar1 = np.array([ re.findall(r'\S+', x) for x in arr_NOT_ARCIVEx ])        
        
        
        '''        
        t_ar3 = np.array([[xk for xk in xj] for xj in f.getvalue().splitlines()], ndmin=2)

        x = np.random.rand(10,2)
        
        
        x1 = x[:, np.newaxis, : ]
        x2 = x[np.newaxis, : , : ]
        
        xt = x1 - x2
        
        x1 =np.array([0,1,2])
        x2 =np.array([2,3,4])
        
        x5 =np.array([[2,3,4],[7,8,9]])
        
        x = x1 * x2
        
        
        x2x =x2[:,np.newaxis]
        
        xt = x1 * x2x
        

        
        arr_1 = np.array(f.getvalue().splitlines())  
        
        t_ar1 = np.array([ re.findall(r'\S+', x) for x in arr_test ])
        
        t_list1 = [ re.findall(r'\S+', x) for x in arr_test ]
        
        t_ar2 = np.array(t_list1)
        
        
        t_ar3 = np.array([[xk for xk in xj] for xj in t_list1], ndmin=2)
        
        new_array=np.array([[[coord for coord in xk] for xk in xj] for xj in xi], ndmin=3) 
        
        arr_title = arr_1[0]   
        arr_1 = arr_1[1:]
        
        
        lists = [[1, 2], [3, 4]]
        tt = np.array(lists)
        

        arr_ARCIVE = arr_1[pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        arr_NOT_ARCIVE = arr_1[~pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        
        arr_test = arr_NOT_ARCIVE [0:3]
        
        arr = [   [x.strip() for x in y.strip('[]').split(',')] for y in arr_test  ]
        
        s = string[1:len(string)-1].split(", ")
        
        t = [arr_NOT_ARCIVE]
        '''
        print(x1 + " : " + str(len(file_list)))   
    except:
        print (x1 + ' :not found or no permission')
        continue 

    file_list = [x1 + "." + e for e in file_list]
    
    file_array = np.array(file_list)
    file_array_3lv = file_array[pd.Series(len(re.findall('\.', el)) == 2 for el in file_array)]
    file_array_not_3lv = file_array[pd.Series(len(re.findall('\.', el)) != 2 for el in file_array)]

    arr_tot_wrk_no_mbr = np.append(arr_tot_wrk_no_mbr, file_array_not_3lv)

    for x2 in file_array_3lv:
        try:
            sess.cwd("'"+x2+"'")
            mbr_list = sess.nlst()
            print(x2 + " : " + str(len(mbr_list)))   
        except:
            print (x2 + ' :not found or no permission')
            continue    
         
        if len(mbr_list) == 0 :
            arr_tot_wrk_no_mbr = np.append(arr_tot_wrk_no_mbr, np.array([x2]))
        else :    
            #test = np.array([x2]* len(mbr_list))
            arr_tot_wrk_mbr1 = np.append(arr_tot_wrk_mbr1, np.array([x2] * len(mbr_list)))
            arr_tot_wrk_mbr2 = np.append(arr_tot_wrk_mbr2, np.array(mbr_list))




list1 = list(arr_tot_wrk_no_mbr)
list2 = [''] * len(arr_tot_wrk_no_mbr) 
df_tot_zip = list(zip(list1,list2))
df_out1 = pd.DataFrame(df_tot_zip, columns=['file', 'mbr'])

list1 = list(arr_tot_wrk_mbr1)
list2 = list(arr_tot_wrk_mbr2)
df_tot_zip = list(zip(list1,list2))
df_out2 = pd.DataFrame(df_tot_zip, columns=['file', 'mbr'])

df_out = df_out1.append(df_out2)
df_out = df_out.sort_values(by=['file', 'mbr'])
df_out.reset_index(inplace=True, drop=True) 

path = os.getcwd()        
out_file = path+"\\result\\"+'Mainframe_List_out1.csv'

if os.path.exists(out_file):
    os.remove(out_file)	

df_out.to_csv(out_file,mode = 'w',header=True, index = False)


