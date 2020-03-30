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



def parse_gen(parsed):
    yield parsed.tokens[0]    
    yield from parse_gen(parsed.tokens[1:]) 
    
 
    
    
for k in recursive_generator([6, 3, 9, 1]):
    print(k)
    
    
    
    for item in parsed.tokens:

        if item.ttype is Keyword : 
            print('++keyword')
            print(item)
            print('++')
            yield item            

        elif is_subselect(item):
            print('++subselect')
            print(item)
            for x in extract_from_part(item):
                print('+++++++++++')                
                print(x)
                print('+++++++++++')                          
                yield x

        else:
            print('+++++++++++other')
            print(item)
            print('+++++++++++')
            yield item

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

lll = parsed.tokens



stream = extract_from_part(ttt)



def is_subselect(parsed):
    if not parsed.is_group:
        return False
    else :
        return True


def extract_from_part(parsed):
    #from_seen = False
    print('tata')
    
    for item in parsed.tokens:

        if item.ttype is Keyword : 
            print('++keyword')
            print(item)
            print('++')
            yield item            

        elif is_subselect(item):
            print('++subselect')
            print(item)
            for x in extract_from_part(item):
                print('+++++++++++')                
                print(x)
                print('+++++++++++')                          
                yield x

        else:
            print('+++++++++++other')
            print(item)
            print('+++++++++++')
            yield item


def extract_table_identifiers(token_stream):
    for item in token_stream:
        #print (item)
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_real_name()
        elif isinstance(item, Identifier):
            yield item.get_real_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value


def extract_tables(sql):
    
    ttt = sqlparse.parse(sql)[0]
    stream = extract_from_part(ttt)
    
    tt = extract_table_identifiers(stream)
    
    #print('toto')

    #tx = list(extract_table_identifiers(stream))




#if __name__ == '__main__':
                    
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
extract_tables(sql)

#tables = ', '.join(extract_tables(sql))[0]