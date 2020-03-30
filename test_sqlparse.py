# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 11:46:46 2018

@author: XT21586
"""

import sqlparse

from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

import re

'''    
def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False
'''

'''
def recursive_generator(lis):
    if not lis: return
    yield lis[0]
    yield from recursive_generator(lis[1:])

for k in recursive_generator([6, 3, 9, 1]):
    print(k)


def recursive_generator(lis):
    if not lis: return
    yield lis.pop(0)
    yield from recursive_generator(lis)

for k in recursive_generator([6, 3, 9, 1]):
    print(k)
'''
'''
def parse_gen(tree_list):
    if len(tree_list) == 0 : return
 
    
    if tree_list[0].is_group: 
        yield from parse_gen(tree_list[0].tokens)     
    else: 
        yield tree_list[0]
        yield from parse_gen(tree_list[1:]) 
'''    

# check for VIEW starting and ending a line i.e. only a view
pat_view = re.compile("(^(V|T)\S*(\s|$))|(^\S*\.(V|T)\S*(\s|$))",re.IGNORECASE)
pat_FROM = re.compile("^FROM$",re.IGNORECASE)
pat_WHERE = re.compile("^WHERE$",re.IGNORECASE)

def parse_gen(tree_list,lvl):
    global keep, from_sw

    if len(tree_list) == 0 : 
        if lvl == 0 :
            return
        else : 
            yield from parse_gen(keep[lvl-1],lvl-1 ) 
    
    if len(keep[lvl]) == 0 : 
        keep[lvl] = tree_list 

    #print('LEVEL:' + str(lvl))
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

        yield from parse_gen(keep[lvl+1],lvl+1 ) 

        
    else:
        keepx = keep[lvl][0]
        keep[lvl] = keep[lvl][1:]
        #print (keepx)
        if   re.search(pat_FROM ,str(keepx)) is not None : 
            from_sw = 1
        elif re.search(pat_WHERE ,str(keepx)) is not None : 
            from_sw = 0
        else : 
            if (re.search(pat_view ,str(keepx)) is not None) and (from_sw == 1):     
            #if   re.search(pat_view ,str(keepx)) is not None and from_sw == 1: 
                yield str(keepx) + "\n"
        yield from parse_gen(keep[lvl],lvl ) 



#    for item in parsed.tokens:
#        if item.ttype is DML and item.value.upper() == 'SELECT':
#            return True

sql ="""
SELECT  'I'                                                       
      , CARI.CAR_INIT                                             
      , CARI.CAR_NUMB                                             
      , CARI.CAR_LOC_CD                                           
      , CARI.WB_ID                                                
      , CARI.TRN_BLK                                              
      , CARI.CUST_SWTCH_CD                                        
      , CARI.HITCH_SETUP                                          
      , CARI.DIR_CD                                               
      , CARI.NXT_TRK_NUMB                                         
      , CARI.STN_333                                              
      , CARI.STN_ST                                               
      , CARI.TRK_NUMB                                             
      , CARI.TRK_SEQ_NUMB                                         
      , CARI.YD_BLK                                               
      , CARI.TRN_TYPE                                             
      , CARI.TRN_SECT                                             
      , CARI.TRN_SYM                                              
      , CARI.TRN_DAY                                              
      , CARI.TRN_SEQ_NUMB                                         
      , CARI.NXT_TRN_BLK                                          
      , CARI.ARR_333                                              
      , CARI.ARR_ST                                               
      , CARI.CURR_SPOT                                            
      , CARI.ASGN_TRN_TYPE                                        
      , CARI.ASGN_TRN_SECT                                        
      , CARI.ASGN_TRN_SYM                                         
      , CARI.ASGN_TRN_DAY                                         
      , CARI.WB_VRSN                                              
      , CARI.CUST_633_SHPR                                        
      , CARI.ORIG_333                                             
      , CARI.ORIG_ST                                              
      , CARI.CUST_633_CNSG                                        
      , CARI.DEST_333                                             
      , CARI.DEST_ST                                              
      , CARI.CAR_KIND                                             
      , CARI.OP_CUST_633                                          
      , CARI.OP_CITY_333                                          
      , CARI.OP_ST                                                
      , CARI.OP_RAJP                                              
      , CARI.OP_ZTS                                               
      , CARI.STCC_NUMBER                                          
      , CARI.CMDTY_DES_ABBR                                       
      , CARI.SPL_COND_CD1                                         
      , CARI.SPL_COND_CD2                                         
      , CARI.SPL_COND_CD3                                         
      , CARI.SPL_COND_CD4                                         
      , CARI.SPL_COND_CD5                                         
      , CARI.SPL_COND_CD6                                         
      , CARI.JT_SVC_CD                                            
      , CARI.MECH_STAT_CD1                                        
      , CARI.MECH_STAT_CD2                                        
      , CARI.MECH_STAT_CD3                                        
      , CARI.GRS_TONS                                             
      , CARI.NET_TONS                                             
      , CARI.EQP_TARE                                             
      , CARI.PPSI_CD                                              
      , CARI.OS_LGTH_FT                                           
      , CARI.OS_LGTH_IN                                           
      , CARI.PER_DIEM_RATE                                        
      , CARI.LOAD_EMPTY                                           
      , CARI.SCO_FCO_ID                                           
      , CARI.WB_AXLE_CNT                                          
      , CARI.TSO_333                                              
      , CARI.TSO_ST                                               
      , CARI.AAR_POOL_ID                                          
      , CARI.ARR_SEQ_NBR                                          
      , CARI.CARR_ABBR_ON                                         
      , CARI.CSD_CD                                               
      , CARI.DFO_333                                              
      , CARI.DFO_ST                                               
      , CARI.DSTN_SEQ_NBR                                         
      , CARI.EVST_CD                                              
      , CARI.EVT_CD                                               
      , CARI.FGN_SYS_CD                                           
      , CARI.KEY_TRN_CD                                           
      , CARI.LOG_COUNTER                                          
      , CARI.PGM_NME                                              
      , CARI.PREV_TRK_NUMB                                        
      , CARI.PROC_DTTM                                            
      , CARI.SFE_POOL_ID                                          
      , CARI.SPD_RESTR_CD                                         
      , CARI.ST_INTERST                                           
      , CARI.STN_SEQ_NBR                                          
      , CARI.SWTCH_CD                                             
      , CARI.USER_ID                                              
      , CARI.WB_DT                                                
      , CARI.WB_ERR_CD                                            
      , CARI.WB_NUMB                                              
      , CARI.EVT_DT                                               
      , CARI.EVT_TM                                               
      , CARI.ARR_DT                                               
      , CARI.ARR_TM                                               
      , CARI.CAR_FLG                                              
      , CARI.CAR_NOTE_FLG                                         
      , CARI.NXT_YRD_BLK                                          
      , CARI.RAJP2                                                
      , CARI.LVL_SVC_CD                                           
      , CARI.SYS_BLK                                              
      , CARI.STOP_PROF                                            
      , CARI.DISP_CHG_DT                                          
      , CARI.DISP_CHG_TM                                          
      , CARI.RFO_EQP_NOTE                                         
      , CARI.MVMT_REV_CODE                                        
      , CARI.AUTH_TYPE                                            
      , CARI.AUTH_NUMB                                            
      , CARI.CAR_KIND_AAR                                         
      , CARI.DRF_GEAR_CPLR                                        
      , CARI.GST_CD                                               
      , CARI.GRN_CD                                               
      , CARI.LOT_NUMB                                             
      , CARI.LOT_NUMB_PREV                                        
      , CARI.CLRC_CD                                              
      , CARI.CLN_CD                                               
      , CARI.TRCK_CPTY_CD                                         
      , CARI.DOOR_SIZE_CD                                         
      , CARI.FLR_COND_CD                                          
      , CARI.LNG_COND_CD                                          
      , CARI.CBODY_COND_CD                                        
      , CARI.BO_CD                                                
      , CARI.OP_ORIG_333                                          
      , CARI.OP_ORIG_ST                                           
      , CARI.PARK_STN_333                                         
      , CARI.PARK_STN_ST                                          
      , CARI.BO_ETR_HRS                                           
      , CARI.ERT_CD                                               
      , CARI.MPTY_ASGN_CD                                         
      , CARI.CAR_ORD_NBR                                          
      , CARI.OBND_420_BLK                                         
  FROM  OY.TCAR_INVENTORY CARI  
  INNER JOIN 
  tddddd_ddd   as b  
ON (asaf  asdfsa )                             
 WHERE (                                                          
       CARI.EVT_CD IN ('RR','DD','TA','TD')                       
     )                                                            
 AND (                                                            
       CARI.GST_CD NOT LIKE 'E%'                                  
     )                                                            
 AND (                                                            
      NOT EXISTS                                                  
         (SELECT 1 FROM OY.TCAR_HISTORY X                         
           WHERE X.CAR_NUMB  = CARI.CAR_NUMB                      
             AND X.CAR_INIT  = CARI.CAR_INIT                      
             AND TIMESTAMP(X.EVT_DT,X.EVT_TM)                     
               > TIMESTAMP(CARI.EVT_DT,CARI.EVT_TM)               
             AND X.EVT_CD IN ('RR','DD','TA','TD') )              
     )                                                            
UNION ALL                                                         
SELECT  'H'                                                       
      , CARI.CAR_INIT                                             
      , CARI.CAR_NUMB                                             
      , ' '                                                       
      , CARI.WB_ID                                                
      , CARI.TRN_BLK                                              
      , CARI.CUST_SWTCH_CD                                        
      , CARI.HITCH_SETUP                                          
      , CARI.DIR_CD                                               
      , ' '                                                       
      , CARI.STN_333                                              
      , CARI.STN_ST                                               
      , CARI.TRK_NUMB                                             
      , CARI.TRK_SEQ_NUMB                                         
      , CARI.YD_BLK                                               
      , CARI.TRN_TYPE                                             
      , CARI.TRN_SECT                                             
      , CARI.TRN_SYM                                              
      , CARI.TRN_DAY                                              
      , CARI.TRN_SEQ_NUMB                                         
      , CARI.NXT_TRN_BLK                                          
      , CARI.ARR_333                                              
      , CARI.ARR_ST                                               
      , CARI.CURR_SPOT                                            
      , CARI.ASGN_TRN_TYPE                                        
      , CARI.ASGN_TRN_SECT                                        
      , CARI.ASGN_TRN_SYM                                         
      , CARI.ASGN_TRN_DAY                                         
      , CARI.WB_VRSN                                              
      , ' '                                                       
      , CARI.ORIG_333                                             
      , CARI.ORIG_ST                                              
      , CARI.CUST_633_CNSG                                        
      , CARI.DEST_333                                             
      , CARI.DEST_ST                                              
      , CARI.CAR_KIND                                             
      , CARI.OP_CUST_633                                          
      , CARI.OP_CITY_333                                          
      , CARI.OP_ST                                                
      , CARI.OP_RAJP                                              
      , CARI.OP_ZTS                                               
      , CARI.STCC_NUMBER                                          
      , CARI.CMDTY_DES_ABBR                                       
      , CARI.SPL_COND_CD1                                         
      , CARI.SPL_COND_CD2                                         
      , CARI.SPL_COND_CD3                                         
      , CARI.SPL_COND_CD4                                         
      , CARI.SPL_COND_CD5                                         
      , CARI.SPL_COND_CD6                                         
      , CARI.JT_SVC_CD                                            
      , CARI.MECH_STAT_CD1                                        
      , CARI.MECH_STAT_CD2                                        
      , CARI.MECH_STAT_CD3                                        
      , CARI.GRS_TONS                                             
      , CARI.NET_TONS                                             
      , CARI.EQP_TARE                                             
      , CARI.PPSI_CD                                              
      , CARI.OS_LGTH_FT                                           
      , CARI.OS_LGTH_IN                                           
      , CARI.PER_DIEM_RATE                                        
      , CARI.LOAD_EMPTY                                           
      , CARI.SCO_FCO_ID                                           
      , CARI.WB_AXLE_CNT                                          
      , CARI.TSO_333                                              
      , CARI.TSO_ST                                               
      , CARI.AAR_POOL_ID                                          
      , CARI.ARR_SEQ_NBR                                          
      , CARI.CARR_ABBR_ON                                         
      , CARI.CSD_CD                                               
      , CARI.DFO_333                                              
      , CARI.DFO_ST                                               
      , CARI.DSTN_SEQ_NBR                                         
      , CARI.EVST_CD                                              
      , CARI.EVT_CD                                               
      , CARI.FGN_SYS_CD                                           
      , CARI.KEY_TRN_CD                                           
      , 0                                                         
      , CARI.PGM_NME                                              
      , CARI.PREV_TRK_NUMB                                        
      , CARI.PROC_DTTM                                            
      , CARI.SFE_POOL_ID                                          
      , CARI.SPD_RESTR_CD                                         
      , CARI.ST_INTERST                                           
      , CARI.STN_SEQ_NBR                                          
      , CARI.SWTCH_CD                                             
      , CARI.USER_ID                                              
      , CARI.WB_DT                                                
      , CARI.WB_ERR_CD                                            
      , CARI.WB_NUMB                                              
      , CARI.EVT_DT                                               
      , CARI.EVT_TM                                               
      , DATE('0001-01-01')                                        
      , TIME('00.00.00')                                          
      , CARI.CAR_FLG                                              
      , ' '                                                       
      , ' '                                                       
      , ' '                                                       
      , ' '                                                       
      , ' '                                                       
      , ' '                                                       
      , DATE('0001-01-01')                                        
      , TIME('00.00.00')                                          
      , ' '                                                       
      , CARI.MVMT_REV_CODE                                        
      , CARI.AUTH_TYPE                                            
      , CARI.AUTH_NUMB                                            
      , '    '                                                    
      , 0                                                         
      , CARI.GST_CD                                               
      , CARI.GRN_CD                                               
      , CARI.LOT_NUMB                                             
      , CARI.LOT_NUMB_PREV                                        
      , ' '                                                       
      , CARI.CLN_CD                                               
      , CARI.TRCK_CPTY_CD                                         
      , CARI.DOOR_SIZE_CD                                         
      , CARI.FLR_COND_CD                                          
      , CARI.LNG_COND_CD                                          
      , CARI.CBODY_COND_CD                                        
      , CARI.BO_CD                                                
      , CARI.OP_ORIG_333                                          
      , CARI.OP_ORIG_ST                                           
      , ' '                                                       
      , ' '                                                       
      , CARI.BO_ETR_HRS                                           
      , CARI.ERT_CD                                               
      , CARI.MPTY_ASGN_CD                                         
      , CARI.CAR_ORD_NBR                                          
      , CARI.OBND_420_BLK                                         
  FROM  OY.TCAR_HISTORY CARI                                      
 WHERE (                                                          
       CARI.EVT_CD IN ('RR','DD','TA','TD')                       
     )                                                            
 AND (                                                            
       CARI.GST_CD NOT LIKE 'E%'                                  
     )                                                            
 AND (                                                            
      NOT EXISTS                                                  
         (SELECT 1 FROM OY.TCAR_HISTORY X                         
           WHERE X.CAR_NUMB  = CARI.CAR_NUMB                      
             AND X.CAR_INIT  = CARI.CAR_INIT                      
             AND(TIMESTAMP(X.EVT_DT,X.EVT_TM)                     
               > TIMESTAMP(CARI.EVT_DT,CARI.EVT_TM)               
              OR(TIMESTAMP(X.EVT_DT,X.EVT_TM)                     
               = TIMESTAMP(CARI.EVT_DT,CARI.EVT_TM)               
                 AND X.PROC_DTTM > CARI.PROC_DTTM))               
             AND X.EVT_CD IN ('RR','DD','TA','TD') )              
     )                                                            
 AND (                                                            
      NOT EXISTS                                                  
         (SELECT 1 FROM OY.TCAR_INVENTORY X                       
           WHERE X.CAR_NUMB  = CARI.CAR_NUMB                      
             AND X.CAR_INIT  = CARI.CAR_INIT                      
             AND TIMESTAMP(X.EVT_DT,X.EVT_TM)                     
              >= TIMESTAMP(CARI.EVT_DT,CARI.EVT_TM)               
             AND X.EVT_CD IN ('RR','DD','TA','TD') )              
     )                                                            
FOR FETCH ONLY WITH UR
"""



keep = [([]) for i in range(50)]
parsed = sqlparse.parse(sql)[0]
keep[0] =  parsed.tokens
from_sw = 0   
stream = parse_gen(keep[0],0)

with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sql2acum.txt', 'w') as f:
    for k in stream:
        f.write(str(k))

#with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sql2acum.txt', 'w') as f:
#    for k in parse_gen(keep[0],0):
#        f.write(str(k))


#print('TATA')
    
#for k in parse_gen(keep[0],0):
#    print(k)   

