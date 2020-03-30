# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:04:49 2018

@author: XT21586
"""

import ftplib
import pyodbc
import pandas as pd
import re


in_sql = '''
select distinct
DDS_DSN 
from 
re.bjdds
where
DDS_DSN <> ' '
order by DDS_DSN
;
'''

labels = [
'DDS_DSN'
]



cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF9;CURRENTSCHEMA=RE')
cursor = cnxn.cursor()
cursor.execute(in_sql)
print('Starting fetchall.......')
rows = cursor.fetchall()
cursor.close()
cnxn.close()

df = pd.DataFrame.from_records(rows, columns=labels) 



t3 = []
x1 = []
for index, row in df.iterrows():
    x1 = re.split(r"\.",row['DDS_DSN'])
    if len(x1) >= 2:
        t3.append(str.strip(x1[0]))    

df_t3 = pd.DataFrame(t3)

df_t3.drop_duplicates(inplace = True)
df_t4 = df_t3.sort_values( [0]) 
df_t4.reset_index(inplace=True, drop=True) 


df_t4  = df_t4[~df_t4[0].str.contains(re.compile(r"(\%)|(\&)"))] 

df_t4  = df_t4[~df_t4[0].str.contains(re.compile(r"^(\*)|^(\')"))] 





sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')


sess.cwd("'PRODUCL'")

file_list = sess.nlst()

mbr_list = []
df_tot = pd.DataFrame()
for x in file_list:
    try:
        mbr_list = sess.nlst()
        for y in mbr_list:
            mbr_list
        
    except:
        print("NO member or NO permission to access: "+ x )




sess.cwd("'CHANGEI.AMANPROD'")

AMANPROD