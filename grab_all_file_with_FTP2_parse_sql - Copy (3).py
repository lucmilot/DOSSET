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

#dont line suffix like CL*64
#pat2 = re.compile(r"(\b\w*\**\d+$)",flags = re.MULTILINE)
pat2 = re.compile(r"(\s\d{8}$)",flags = re.MULTILINE)


#dont keep comment line
pat_comment = re.compile(r"(^\s{6}\*)")


def call_cobol_sql(file_sel,mbr_sel):  

    global acum_txt, search_identification
    def append_newline(input):
        global acum_txt
        if re.search(pat_comment,input ) : 
            pass
        else :
            acum_txt = acum_txt + input + "\n"  
   
    acum_txt = ''
    sess.cwd("'" + file_sel + "'")
    print(file_sel, mbr_sel)        
    sess.retrlines('RETR ' + mbr_sel, append_newline)
    

    acum_txt = re.sub(pat1, '      ', acum_txt)
    acum_txt = re.sub(pat2, '        ', acum_txt)
    
    
    #test_first = acum_txt[0:80] 
    #print(test_first)   
     
    list1  = []  
    #if re.match("(.*IDENTIFICATION DIVISION.*)",acum_txt[0:80])  :
    list2 = re.findall('(?:EXEC SQL)(.+?)(?:END-EXEC)', acum_txt,re.DOTALL)   

    for x in list2:
        if re.match(".*(?=SELECT|INSERT|DELETE|UPDATE).*",x, re.DOTALL) : 
            if len(list1) == 0 : 
                list1 = [x]
            else :
                list1.extend([x])           
    else :
        list1  = []    
  
    return_list = []    
    if len(list1) > 0 :  
        for i in range(50) :   
            if i < len(list1) :
                return_list.append(list1[i])
            else:
                return_list.append('')
            
    return return_list 


path = os.getcwd()        
in_file = path+"\\input\\"+'Grab_all_file_with_FTP.csv'


search_identification  = re.compile('IDENTIFICATION DIVISION')



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


#from time import gmtime, strftime
#tt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#tt = tt.replace(" ", "_")

#out_file_PO = path+"\\result\\"+"Grab_all_file_PO_"+tt+".csv" 
#if os.path.exists(out_file_PO):
#    os.remove(out_file_PO)	    



sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')


for lv1 in List_seed :

    out_file_PO_MBR = path+"\\result\\"+"Grab_all_file_PO_MBR_" + lv1 + ".csv" 
    if os.path.exists(out_file_PO_MBR):
        os.remove(out_file_PO_MBR)	            
    
    
    tot_PO = []   
    #arr_tot = np.array([],dtype=np.str)
    arr_PO = np.array([],dtype=np.str)
    arrx_PO = np.array([],dtype=np.str)
    arry_PO_MBR = np.array([],dtype=np.str)
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
    tot_PO_2 = []
    for file_sel in arr_PO:
        print(file_sel)

      
        #if re.match("(?=.*SRCE.*)",file_sel) :    
        if re.match("(?=.*SRCE.*)",xxx) is not None and re.match("(?=.*ASM.*)",xxx) is None: 
            pass 
        else : 
            continue

        try:
            sess.cwd("'" + file_sel + "'")   
        
            mbr_list = sess.nlst()
            
        except:
            print( file_sel + " no permission")
            if len(tot_PO_1) == 0 : 
                tot_PO_1 =  [' :not found or no permission']  
                tot_PO_2 =  [['']]  
            else :
                tot_PO_1.append(' :not found or no permission')
                tot_PO_2.append([''])
            continue                
        
        print(file_sel + " :nb mbr: " + str(len(mbr_list)))
        
        #DEBUG
        mbr_list = mbr_list[0:100]
            
        mbr_list_1 = []
        for mbr_sel in mbr_list:                    
            hit_list = call_cobol_sql(file_sel,mbr_sel)     
           
            if len(hit_list) > 0:
                mbr_list_1.extend([mbr_sel])
                if len(tot_PO_2) == 0 : 
                    tot_PO_2 = [hit_list]
                else :
                    tot_PO_2.extend([hit_list])

        if len(tot_PO_1) == 0 : 
            tot_PO_1 = mbr_list_1 
        else :
            tot_PO_1.extend(mbr_list_1)            

        
        c1 = np.array([file_sel] * len(tot_PO_1))[: , np.newaxis]
        c2 = np.array(tot_PO_1)[: , np.newaxis]
        c3 = np.array(tot_PO_2)
        
        arrx_PO = np.hstack([c1,c2,c3])


        if len(arry_PO_MBR) == 0 : 
            arry_PO_MBR = arrx_PO
        else :
            arry_PO_MBR = np.vstack([arry_PO_MBR,arrx_PO]) 
    
 

    
    
    if len(arry_PO_MBR) > 0 :
        df_out_mbr = pd.DataFrame(arry_PO_MBR, columns= ['file','mbr'] +  ["sql"+str(i) for i in range(50)])
        
        df_out_mbr1 = df_out_mbr.replace(to_replace=pat1, value='      ', regex=True) 
        
        df_out_mbr1 = df_out_mbr1.replace(to_replace=pat2, value='', regex=True) 
        
        
"      *"
        
      
    print(df_out_mbr1.iloc[0,0])   
    
    txt = ''
    for index, row in df_out_mbr.iterrows(): 
        txt = txt + ">>>" + row.iloc[1] + "\n"
        for y in row[2:52] :
            if len(y) > 0 :
                txt = txt + y                
                
                
                if re.match(pat_comment,y) is  None : 
                    txt = txt + y
        
        k1 = [row[2:52] for index, row in df_out_mbr.iterrows()]
        
        k2 = [ x[0] for x in k1]
        k3 = [ x for x in k1]
        
        k4 = [ y for y in k3]
        
        
        
        kkk  = [ (len(y) for y in  [row[2:52] for index, row in df_out_mbr.iterrows()]]
        
        ttt = [[ (len(x) == 9) & (x[7] == 'PO') for index, row in df_out_mbr.iterrows() ]]
        
        df_out_mbr1 = df_out_mbr1[[ (len(x) == 9) & (x[7] == 'PO') for index, row in df_out_mbr.iterrows() ]]
        
                
        
 df.replace(to_replace=r'^ba.$', value='new', regex=True)       
        
        
        df_out_mbr.to_csv(out_file_PO_MBR,mode = 'a',header=True, index = False)
        
#        df_out = df_out_mbr.drop_duplicates(['file'])['file']
#        df_out.to_csv(out_file_PO,mode = 'a',header=True, index = False)    

xxx = 'YYYYYY a asdfas   YYY"

xxx = '''   YY    
xxxxxx ** 2003-03-18 KL
                   ,CARR_REV_PPRT_WC
yyyyy            ,CARR_REV_PPRT_EJE
                   ,CARR_REV_PPRT_SSAM
                   ,CARR_REV_PPRT_AC
KXL002             ,COST_REV_PPRT_BCOL
KXL002*            ,CARR_REV_PPRT_DMIR
KXL002             ,CARR_REV_PPRT_BLE 
'''   

sess.quit

ttt = re.match(r"(YY).*(asd)*",xxx,flags=re.MULTILINE|re.DOTALL) 

ttt.group(2)

                if re.search(r"(^\w{6})",xxx,flags=re.MULTILINE ) : 
                    print ('Y')
                else   : 
                    print ('N')
                    
if re.match(pat1,xxx) : 
    print ('Y')
else   : 
    print ('N')                    

print ( re.match(r"(^\w{6})",xxx,re.MULTILINE))
#dont keep line number
pat1 = re.compile(r"(^\w{6})",flags = re.MULTILINE)

#dont line suffix like CL*64
pat2 = re.compile(r"(\b\w*\**\d+$)",flags = re.MULTILINE)

pat_comment = re.compile(r"(?=^.{6}\*)")


#dont keep line number
pat1 = re.compile(r"^\d+",flags = re.MULTILINE)

#dont line suffix like CL*64
pat2 = re.compile(r"(\b\w*\**\d+$)",flags = re.MULTILINE)


out = re.sub(pat1, ' ', xxx)
print (out)

out = re.sub(pat2, ' ', out)
print (out)


