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

    

parsed = sqlparse.parse(sql)[0]
for x0 in   parsed.tokens:
    print('lv0')
    print(x0)
    
    if x0.is_group : 
        x0_group = x0.tokens
        for x1 in x0.tokens:
            print('lv1')
            print(x1)
            print(x1.ttype)
            
            if x1.is_group : 
                for x2 in x1.tokens:
                    print('lv2')
                    print(x2)     
                    print(x2.ttype)                    

                    if x2.is_group : 
                        for x3 in x2.tokens:
                            print('lv3')
                            print(x3)            
                            print(x3.ttype)     