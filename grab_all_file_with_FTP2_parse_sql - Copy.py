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
    print(file_sel, mbr_sel)        
    sess.retrlines('RETR ' + mbr_sel, append_newline)
     
    test_first = acum_txt[0:80] 
    print(test_first)   
    if re.match("(.*IDENTIFICATION DIVISION.*)",acum_txt[0:80])  :
        list1 = re.findall('EXEC SQL(.+?)END-EXEC', acum_txt,re.DOTALL)   
    else :
        list1  = []
            
    return_list = []          
    for i in range(50) :   
        if i < len(list1) :
            return_list.append(list1[i])
        else:
            return_list.append('')
            
    return return_list 


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
    tot = []   
    arr_tot = np.array([],dtype=np.str)
    print( lv1 )
    try:
        sess.cwd("'" + lv1 + "'")
        #file_list = sess.nlst()
        f = io.StringIO()
        with redirect_stdout(f):
            sess.dir()
     
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
        arr_NOT_ARCIVE_s1 = arr_NOT_ARCIVE_s[[ (x[1] != 'Tape') & (x[1] != 'Error') for x in arr_NOT_ARCIVE_s ]] 
        
        #arr1_NOT_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        #arr2_NOT_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        #arr_NOT_PO = np.hstack([arr1_NOT_PO,arr2_NOT_PO])
        #arr_tot = np.append(arr_tot, arr_NOT_PO)
   
        #tot = tot + [[x,'',[]] for x in arr_tot  ]     
        
        arr1_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr2_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
        arr_PO = np.hstack([arr1_PO,arr2_PO])
        
               
        df_out_PO = pd.DataFrame(tot, columns= ['file','mbr','sql_list'])
        
        df_out.to_csv(out_file_PO,mode = 'a', header=False, index = False)
        
        
        
        

        for file_sel in arr_PO:
            debug_iter = 0   
            
            if re.match("(.*SRCE.*)",file_sel)  :
                print ('SRCE : ', file_sel)
                try:
                    sess.cwd("'" + file_sel + "'")      
                    mbr_list = sess.nlst()
                    
                except:
                    print (file_sel + ' :not found or no permission')
                    #arr_tot = np.append(arr_tot, [file_sel])
                    #tot = tot + [[file_sel,'',[]]]
                    continue                   
                
                for mbr_sel in mbr_list:                    
                    hit_list = call_cobol_sql(file_sel,mbr_sel)                
                    tot = tot + [[file_sel,mbr_sel,hit_list]]
                    
                    debug_iter = debug_iter + 1
                    if debug_iter > debug_iter_limit:
                        break                  
                    
            else:
                print (file_sel)
                #for mbr_sel in mbr_list:                              
                #    tot = tot + [[file_sel,mbr_sel,[]]]

    except:
        print (lv1 + ' :not found or no permission')
        continue 



df_out = pd.DataFrame(tot, columns= ['file','mbr','sql_list'])
    
#df_out.reindex
    
for i in range(50) :
    df_out = pd.concat((df_out,pd.DataFrame([ x[i]  for x in df_out['sql_list'] ], columns = ["sql"+str(i)] ) ), axis = 1)
 


print (tot[11][2])


sess.quit

print (arr_PO)

lv1 = 'xxxxx'
     
out_file = path+"\\result\\Mainframe_List_PO_"+lv1+".csv"

if os.path.exists(out_file):
    os.remove(out_file)	

df_out.to_csv(out_file,mode = 'w',header=True, index = False)

df_out.to_csv(out_file,mode = 'a', header=False, index = False)

df_out.columns
