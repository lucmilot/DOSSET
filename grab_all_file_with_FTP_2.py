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



#dont keep line number
pat1 = re.compile(r"(^\w{6})",flags = re.MULTILINE)

#dont line suffix  number
pat2 = re.compile(r"(\s\d{8}$)",flags = re.MULTILINE)

#dont line suffix like CL*64
pat3 = re.compile(r"(\b\w*\**\d+$)",flags = re.MULTILINE)

#dont keep comment line
pat_comment = re.compile(r"(^.{6}\*)|(^.{7}\s*\*)") # this is used line per line

pat_identification  = re.compile('IDENTIFICATION DIVISION',flags = re.DOTALL)

pat_exec_sql = re.compile('EXEC SQL',flags = re.DOTALL)   

pat_SIUD = re.compile(".*(?=SELECT|INSERT|DELETE|UPDATE).*",flags = re.DOTALL)

pat_EXEC_BLK = re.compile("(?:EXEC SQL)(.+?)(?:END-EXEC)",flags = re.DOTALL)

pat_not_blank_line = re.compile(r"(\S+)")  #any non white space character 

pat_sql_comment = re.compile(r"(^\*)")  #* as first charater 

pat_filter1_PO = re.compile("(?=.*CNDWPROD.*)")

pat_filter2_PO = re.compile("(?=.*COBSRCE.*)")

pat_DECLARE = re.compile("(?:DECLARE)(.+?)(?:FOR)",flags = re.DOTALL)
  

def call_cobol_sql(file_sel,mbr_sel):  

    global acum_txt, search_identification
    def append_newline(input):
        global acum_txt, ix
        if re.search(pat_comment,input ) : 
            pass
        else :
            acum_txt = acum_txt + input + "\n"  
            
    def call_sqeeze_sql(x):   
        
        x1 = re.sub(pat_DECLARE, '', x)  #dont line suffix  number

        s = io.StringIO(x1)
        x2 = ''
        shift_ix = 999
        for line in s:
            if re.search(pat_not_blank_line,line) and not re.search(pat_sql_comment,line) :
                x2 = x2  + line
                for i in range(len(line)):
                    if line[i] != ' ' : break
                if shift_ix > i :
                    shift_ix = i   
                    
        x_1 = ''           
        s = io.StringIO(x2)
        for line in s:
            if re.search(pat_not_blank_line,line) and not re.search(pat_sql_comment,line) :   
                x_1 = x_1  + line[shift_ix:] 
                
        return x_1                
        
   
    acum_txt = ''
    sess.cwd("'" + file_sel + "'")
    print(file_sel, mbr_sel)        
    sess.retrlines('RETR ' + mbr_sel, append_newline)

    '''
    if re.search(pat_identification,acum_txt)  is None  or re.search(pat_exec_sql,acum_txt) is None:
        print('Y')    
    else :
        print('N') 
    ttt = re.findall(pat_identification,acum_txt)     
        
    ttt = re.findall(pat_exec_sql,acum_txt)              
    '''
        
      

    return_list = []   
    if re.search(pat_identification,acum_txt)  is None  or re.search(pat_exec_sql,acum_txt) is None:
        return return_list      

    acum_txt = re.sub(pat1, '      ', acum_txt)    #dont keep line number
    acum_txt = re.sub(pat2, '        ', acum_txt)  #dont line suffix  number
    acum_txt = re.sub(pat3, '', acum_txt)  #dont line suffix  number

    list1  = []  
    list2 = re.findall(pat_EXEC_BLK , acum_txt)   
    for x in list2:
        if re.search(pat_SIUD,x) : 
            print (mbr_sel)
            x1 = call_sqeeze_sql(x)       
            
            if len(list1) == 0 : 
                list1 = [x1]
            else :
                list1.extend([x1])           
 
 
    if len(list1) > 0 :  
        for i in range(50) :   
            if i < len(list1) :
                return_list.append(list1[i])
            else:
                return_list.append('')
            
    return return_list 


    
def call_process_mbr():   
    global bdr1, bdr2, mbr_list, file_sel , out_file_PO_MBR 


    tot_PO_mbr_1 = []
    tot_PO_mbr_2 = []        
      
    mbr_list_1 = []

    arrx_PO_MBR = np.array([],dtype=np.str)

    bdr2x = min(len(mbr_list), bdr2)

    hit_sw = 0
    for mbr_sel in mbr_list[bdr1:bdr2x]:   
     
        hit_list = call_cobol_sql(file_sel,mbr_sel)     
       
        if len(hit_list) > 0:
            hit_sw = 1
            mbr_list_1.extend([mbr_sel])
            if len(tot_PO_mbr_2) == 0 : 
                tot_PO_mbr_1 = [mbr_sel]  
                tot_PO_mbr_2 = [hit_list]
            else :
                tot_PO_mbr_1.extend([mbr_sel]) 
                tot_PO_mbr_2.extend([hit_list])  
     
    
    if hit_sw == 1 : 
        c1 = np.array([file_sel] * len(tot_PO_mbr_1))[: , np.newaxis]
        c2 = np.array(tot_PO_mbr_1)[: , np.newaxis]
        c3 = np.array(tot_PO_mbr_2)
        
        arrx_PO_MBR = np.hstack([c1,c2,c3])         
    
        if len(arrx_PO_MBR) > 0 :
            df_out_mbr = pd.DataFrame(arrx_PO_MBR, columns= ['file','mbr'] +  ["sql"+str(i) for i in range(50)])
            if bdr1 == 0 :
                df_out_mbr.to_csv(out_file_PO_MBR,mode = 'a',header=True, index = False)
            else:
                df_out_mbr.to_csv(out_file_PO_MBR,mode = 'a',header=False, index = False)
                

                
    if bdr2x == len(mbr_list) :
        return 'complete'
    else:
        return 'not complete'



#-----------------------------------------------------------
path = os.getcwd()        
in_file = path+"\\input\\"+'Grab_all_file_with_FTP.csv'



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



#-----------------------------------------------------------
sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')


for lv1 in List_seed :


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
 
    
    #ttt = list(arr_NOT_ARCIVE_s)
    
    arr_NOT_ARCIVE_s1 = arr_NOT_ARCIVE_s[[ (x[1] != 'Tape') & (x[1] != 'Error') & (x[0] != 'GDG') & (x[0] != 'Migrated') & (x[1] != 'Not') for x in arr_NOT_ARCIVE_s ]] 

    
    #arr1_NOT_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    #arr2_NOT_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] != 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    #arr_NOT_PO = np.hstack([arr1_NOT_PO,arr2_NOT_PO])
    #arr_tot = np.append(arr_tot, arr_NOT_PO)
   

    arr1_PO = np.array([lv1 + "." + x[9] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 10) & (x[8] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
    arr2_PO = np.array([lv1 + "." + x[8] for x in arr_NOT_ARCIVE_s1[[ (len(x) == 9) & (x[7] == 'PO') for x in arr_NOT_ARCIVE_s1 ]] ])
 
    #debugx = np.array([lv1 + "." + x[0] + " " + x[1] + " " + x[2] + " " + x[3]for x in arr_NOT_ARCIVE_s1[[ (len(x) < 9) for x in arr_NOT_ARCIVE_s1 ]] ])
        
    
    if len(arr2_PO) > 0 : 
        arr_PO = np.hstack([arr1_PO,arr2_PO])
    else:
        arr_PO = arr1_PO

    tot_PO_1 = []
    for file_sel in arr_PO:
        print(file_sel)

        if re.search(pat_filter1_PO,file_sel) is not None and re.search(pat_filter2_PO,file_sel) is not None :   
            print (file_sel + " is selected")
            pass 
        else : 
            if len(tot_PO_1) == 0 : 
                tot_PO_1 = [' :not used']  
            else :
                tot_PO_1.append([' :not used']  )     

            continue

        try:
            sess.cwd("'" + file_sel + "'")   
            mbr_list = sess.nlst()
            
        except:
            print( file_sel + " no permission")
            if len(tot_PO_1) == 0 : 
                tot_PO_1 =  [' :not found or no permission']  
            else :
                tot_PO_1.append(' :not found or no permission')
            continue    

 
           
        
        print(file_sel + " :nb mbr: " + str(len(mbr_list)))
        if len(tot_PO_1) == 0 : 
            tot_PO_1 = [" :nb mbr: " + str(len(mbr_list))]  
        else :
            tot_PO_1.append(" :nb mbr: " + str(len(mbr_list)))
       
        #---------------------------------------------------------
        
        
        
        out_file_PO_MBR = path+"\\result\\"+"Grab_all_file_PO_MBR_" + file_sel + ".csv" 
        if os.path.exists(out_file_PO_MBR):
            os.remove(out_file_PO_MBR)	
            
        chnk = 20
        bdr1 = 0
        bdr2 = bdr1 + chnk
    
        # we process for a maximum of chnk * 100,  ex chnk 1000  >> 100,000 mbr 
        #for ic in range(100):
        for ic in range(5):
            cpx = call_process_mbr()
            
            bdr1 = bdr1 + chnk
            bdr2 = bdr2 + chnk         
            if cpx == 'complete' : break



sess.quit




