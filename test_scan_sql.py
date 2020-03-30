# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 07:04:29 2018

@author: XT21586
"""

import io
import re



acum_txt = '''

                 SELECT 'Y'
                 INTO :FULL-DISPLAY-FLAG
                 FROM VREFCODE
                 WHERE REF_CD_TYPE        = 'DB'
                   AND REF_CD_VAL         = :FULL-COMPILED-NAME
                   AND REF_CD_DSC_ENG     = 'DEBUG ON'
                 WITH UR
'''  


'''            
 UPDATE VRATAMNT
           SET SHIP_COND_SET_ID = :I-SHIP-COND-SET-ID
             , AUDT_UPD_TS      = :I-AUDT-UPD-TS
             , AUDT_UPD_USE_ID  = :I-AUDT-UPD-USE-ID
             , AUDT_UPD_PGM_ID  = :I-AUDT-UPD-PGM-ID
           WHERE RATE_ID          = :SQL-RATE-ID
             AND RATE_AMT_POST_TS = :SQL-RATE-AMT-POST-TS
             AND SHIP_COND_SET_ID = :W-VRATAMNT.SHIP-COND-SET-ID
*******    WHERE CURRENT OF READNEXT_VRATAMNT
           

'''

pat_not_blank_line = re.compile(r"(\S+)")  #any non white space character 
pat_sql_comment = re.compile(r"(^\*)")  #* as first charater 


acum_txt_1 = ''
s = io.StringIO(acum_txt)
sw1 = 0
col_cnt = 0
for line in s:
    if re.search(pat_not_blank_line,line) and not re.search(pat_sql_comment,line) :   
        if sw1 == 0 :
            sw1 = 1
            for i in range(len(line)):
                if line[i] != ' ' : break
            shift_ix = i
  
        acum_txt_1 = acum_txt_1  + line[shift_ix:]
