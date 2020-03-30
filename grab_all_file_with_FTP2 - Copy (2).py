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


def call_cobol_sql(file_sel,mbr_sel):  
    global acum_txt, search_identification
    def append_newline(input):
        global acum_txt
        acum_txt = acum_txt + input + "\n"  
   
    acum_txt = ''
    sess.cwd("'" + file_sel + "'")
    print(sess.pwd())        
    sess.retrlines('RETR ' + mbr_sel, append_newline)
      
    return_list = re.findall('EXEC SQL(.+?)END-EXEC', acum_txt,re.DOTALL)        

    
    return return_list 


path = os.getcwd()        
in_file = path+"\\input\\"+'Grab_all_file_with_FTP.csv'


search_identification  = re.compile('IDENTIFICATION DIVISION')


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


arr_tot = np.array([],dtype=np.str)

for x1 in List_seed :
    print( x1 )
    try:
        sess.cwd("'" + x1 + "'")
        #file_list = sess.nlst()
        f = io.StringIO()
        with redirect_stdout(f):
            sess.dir()
     
        #[1:] we start after header
        #test = np.array(f.getvalue().splitlines())[0]
        #Volume Unit    Referred Ext Used Recfm Lrecl BlkSz Dsorg Dsname
        
        arr_1 = np.array(f.getvalue().splitlines())[1:]
        
        arr_ARCIVE = arr_1[pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        arr_ARCIVE_s = np.array([re.findall(r'\S+', x) for x in arr_ARCIVE])  
        arr_ARCIVE_s1 = np.array([x1 + "." + x[5] for x in arr_ARCIVE_s ]) 
        arr_tot = np.append(arr_tot, arr_ARCIVE_s1)
        
        arr_NOT_ARCIVE = arr_1[~pd.Series(arr_1).str.contains(re.compile('ARCIVE'))] 
        arr_NOT_ARCIVE_s = np.array([re.findall(r'\S+', x) for x in arr_NOT_ARCIVE])   
        arr_NOT_ARCIVE_s1 = arr_NOT_ARCIVE_s[[ (x[1] != 'Tape') & (x[1] != 'Error') for x in arr_NOT_ARCIVE_s ]] 
        
        arr1_NOT_PO = np.array([x1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr2_NOT_PO = np.array([x1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr_NOT_PO = np.hstack([arr1_NOT_PO,arr2_NOT_PO])
        arr_tot = np.append(arr_tot, arr_NOT_PO)
        
        
        arr1_PO = np.array([x1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr2_PO = np.array([x1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr_PO = np.hstack([arr1_PO,arr2_PO])
        
        arr_accum_hit_list = []

        
        t1 = np.array([['a','a1'],['b','b1']])
        
        t2 = np.array([['k','k1'],['j','j1']])
        
        t = np.vstack([t1,t2])
        
        arr_accum_hit_list = np.append(arr_accum_hit_list, t1)
        
        arr_accum_hit_list1 = np.concatenate(arr_accum_hit_list,t1)
        
        arr_accum_hit_list = np.array(xx)
                            
                          
    acum_txt = " ad EXEC SQL  daf END-EXEC   ad EXEC SQL  daf END-EXEC "
    
        a0 = np.array( [ ['' , ''] ])
        a0.reshape(0,2)
        
        lx = 'mb1'
        l1 = [' a1 ', 'a2', 'a3'] 
        l2 = [' b1 ', 'b2'] 
        l3 = []
        
        tb = np.dtype([('file','S80'), ('mat', 'S80',(1,10))])
        arr1 = np.array([lx,l1], dtype = tb)
        
        
        
        t1 = [[lx][l1]]
        t2 = [lx,l2]
        t3 = [lx,l3]
        
        
        
        T1 = [['xx',[11, 12, 5, 2,8,9]], ['yy',[15, 6,10]]]
        T2 = [['zz',[]]]
        
        
        
        
        a1 = np.array(l1)
        #a1 = np.array(l1)
        a1 = np.vstack([a1,np.array(l1)])
x = np.array(l1)
        
        for file_sel in arr_PO:
            try:
                sess.cwd("'" + file_sel + "'")      
                mbr_list = sess.nlst()
                
            except:
                print (file_sel + ' :not found or no permission')
                arr_tot = np.append(arr_tot, [file_sel])
                continue                 
                
 
            if re.match("(.*SOURCE.*)",file_sel)  :
                for mbr_sel in mbr_list:                    
                    hit_list = call_cobol_sql(file_sel,mbr_sel)                
                    arr_accum_hit_list = np.vstack(arr_accum_hit_list, np.array(hit_list))
            else:
                for mbr_sel in mbr_list:                              
                    arr_accum_hit_list = np.vstack(arr_accum_hit_list, np.array( [ ['' , ''] ]))
                    
                    arr_accum_hit_list = np.append(arr_accum_hit_list, 'ttt')
                    

                    
                    
            arr_PO_with_MBR = [ x + "(" + y + ")" for y in mbr_list]
            arr_tot = np.append(arr_tot, arr_PO_with_MBR)

    except:
        print (x1 + ' :not found or no permission')
        continue 

sess.quit


df_out1 = pd.DataFrame({'File':arr_tot[:]})


path = os.getcwd()        
out_file = path+"\\result\\"+'Mainframe_List_out1.csv'

if os.path.exists(out_file):
    os.remove(out_file)	

df_out1.to_csv(out_file,mode = 'w',header=True, index = False)


