# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 11:46:46 2018

@author: XT21586
"""

import sqlparse

from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML


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


def parse_gen(tree_list,lvl):
    global keep
    
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
        yield '\n\n>>>>>>>>>GROUP' + str(lvl) + '\n'
        yield keepx
        yield '\n>>>>>>>>>END-GROUP\n\n'
        
        keep[lvl+1] = keepx.tokens
        yield from parse_gen(keep[lvl+1],lvl+1 ) 
        
    else:
        keepx = keep[lvl][0]
        keep[lvl] = keep[lvl][1:]
        #print (keepx)
        yield keepx
        yield from parse_gen(keep[lvl],lvl ) 






#    for item in parsed.tokens:
#        if item.ttype is DML and item.value.upper() == 'SELECT':
#            return True

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



keep = [([]) for i in range(10)]
parsed = sqlparse.parse(sql)[0]
keep[0] =  parsed.tokens

with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sql2acum.txt', 'w') as f:
    for k in parse_gen(keep[0],0):
        f.write(str(k))


#print('TATA')
    
#for k in parse_gen(keep[0],0):
#    print(k)   

