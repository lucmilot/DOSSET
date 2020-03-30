# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import os, sys

import win32com.client as win32

import tkinter as tk

import numpy as np

import pandas as pd

import re

import sqlparse

from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

from tkinter.filedialog import askopenfilename

import pyparsing

#import sys
#sys.setrecursionlimit(10000) # 10000 is an example, try with different values

'''
pat_SIUD = re.compile(".*(?=SELECT|INSERT|DELETE|UPDATE).*",flags = re.DOTALL)
pat_strt_double_quote = re.compile(r"^\"",flags = re.DOTALL)
pat_end_double_quote = re.compile("(\"$)",flags = re.DOTALL)
pat_strt_newline = re.compile("(^\r\n)",flags = re.DOTALL)
pat_strt_blank_SELECT = re.compile("(?:^\s)(\s*)(?:SELECT)",flags = re.DOTALL) 
'''

pat_select_overall = re.compile(".*(?=SELECT).*",flags = re.DOTALL)
#pat_DECLARE = re.compile("(?:^DECLARE)(.+?)(?:FOR)",flags = re.DOTALL)

pat_view = re.compile("(^(V|T)\S*(\s|$))|(^\S*\.(V|T)\S*(\s|$))",re.IGNORECASE)
pat_FROM = re.compile("^FROM$",re.IGNORECASE)
pat_WHERE = re.compile("^WHERE$",re.IGNORECASE)
pat_SELECT = re.compile("^SELECT$",re.IGNORECASE)
pat_ON = re.compile("^ON$",re.IGNORECASE)

#------------------------------------------------------------------------

def parse_gen(tree_list,lvl):
    global keep, full_keep, ix_keep, from_sw

    if len(tree_list) == 0 : 
        if lvl == 0 :
            return
        else : 
            yield from parse_gen(keep[lvl-1],lvl-1 ) 


    print('LEVEL:' + str(lvl) + " : ")
    print(keep[lvl]) 
    print(keep[lvl][0])
    print(type(keep[lvl][0]).__name__)
    print(full_keep)

    if len(keep[lvl]) == 0 :
        return

    if keep[lvl][0].is_group: 
        print(keep[lvl]) 
        keepx = keep[lvl][0]
        keepy = keep[lvl]
        keep[lvl] = keep[lvl][1:]
        # when keep[lvl1] is empty the next 'yield from'  will hit len(tree_list) == 0
        #  and calling yield from parse_gen(keep[lvl-1],lvl-1 )
        #  the lvl-1 is pointing to the next token to execute
        ix_keep[lvl] = ix_keep[lvl] + 1
        
        print(type(keepx).__name__)

        if type(keepx).__name__ == 'Identifier':           
        #if isinstance(keepx, Identifier):
            #yield str(keepx)   
            yield from parse_gen(keep[lvl],lvl )

        elif type(keepx).__name__ == 'IdentifierList':
        #elif isinstance(keepx, IdentifierList):            
            #print ('idendifier list length\n')
            for t in keepx.get_identifiers():
                pass
                #yield str(t)
            yield from parse_gen(keep[lvl],lvl )   
                
        elif type(keepx).__name__ == 'Where':
            #yield str(keepx)   
            ix_keep[lvl+1] = 0
            keep[lvl+1] = keepx.tokens
            #print ('going to group : ' + str(lvl+1))
            yield from parse_gen(keep[lvl+1],lvl+1 )             

        #Comparison, Operation, Parenthesis
        elif type(keepx).__name__ == 'Comparison':
            #yield str(keepx)   
            yield from parse_gen(keep[lvl],lvl )    
            
        elif type(keepx).__name__ == 'Operation':
            #yield str(keepx)   
            yield from parse_gen(keep[lvl],lvl )                
            
        elif type(keepx).__name__ == 'Parenthesis':
            #yield str(keepx)   
            yield from parse_gen(keep[lvl],lvl )    
            
        else:
            print ('WARNING ????? : ' , type(keepx).__name__)

        
    else:
        keepx = keep[lvl][0]
        keep[lvl] = keep[lvl][1:]
        ix_keep[lvl] = ix_keep[lvl] + 1
        
        
        print (keepx)

        
        #if   re.search(pat_FROM ,str(keepx)) is not None and keep[lvl][0].ttype <> 'Token.Operator' : 
        if   re.search(pat_FROM ,str(keepx)) is not None  :             
            # if the next token (i.e keep[lvl][0]) is an operator
            #  it means that it is a vairable like WS-FROM-STN-333 
            '''
            print ('keepx : ' +  str(keepx))
            print ('ix_keep : ' + str(ix_keep[lvl]))
            
            lvl = 1
            print(full_keep[lvl])
            print(full_keep[lvl][0].ttype)
            print(full_keep[lvl][0].value)
            print(full_keep[lvl][1].ttype)   
            print(full_keep[lvl][1].value)                   
            print(full_keep[lvl][2].ttype)     
            print(full_keep[lvl][2].value)                
            print(full_keep[lvl][3].ttype)     
            print(full_keep[lvl][3].value)                 
            print(full_keep[lvl][4].ttype)                  
            print(full_keep[lvl][4].value)              
            print(full_keep[lvl][5].ttype)                  
            print(full_keep[lvl][5].value)   
            ttt0 = full_keep[lvl][11] 
            print ('ttto ' + str(ttt0))  
            print
            ttt = full_keep[lvl][ix_keep[lvl]] 
            print ('ttt ' + str(ttt))              
            if ix_keep[lvl] - 1 > 0 : print (full_keep[lvl][ix_keep[lvl] - 1].value)
            print (full_keep[lvl][ix_keep[lvl] ].value)
            if ix_keep[lvl] + 1 <= len(full_keep[lvl]) : print (full_keep[lvl][ix_keep[lvl] + 1].value)
            '''
            print(full_keep[lvl])
            
            from_sw = 1
        elif re.search(pat_WHERE ,str(keepx)) is not None : 
            from_sw = 0
        elif re.search(pat_SELECT ,str(keepx)) is not None : 
            from_sw = 0
        elif re.search(pat_ON ,str(keepx)) is not None : 
            from_sw = 0
        else :              
            if (re.search(pat_view ,str(keepx)) is not None) and (from_sw == 1):     
            #if   re.search(pat_view ,str(keepx)) is not None and from_sw == 1: 
                yield str(keepx)
                
                
        yield from parse_gen(keep[lvl],lvl ) 


 

#------------------------------------------------------------------------


                    
sql ="""
  SELECT RTE_MILE, ORIG_STN_NBR, DEST_STN_NBR                
INTO :LS-RTE-MILE,:LS-ORIG-STN-NBR,:LS-DEST-STN-NBR           
FROM VLINE_SEGMENT                                         
WHERE ORIG_333 = :WS-FROM-STN-333                          
  AND ORIG_PRST = :WS-FROM-STN-ST                          
  AND DEST_333 = :WS-TO-STN-333                            
  AND DEST_PRST  = :WS-TO-STN-ST                              
  AND EFF_DT   <= :IN-TRN-SCH-DPT-DT                       
  AND EXP_DT   >= :IN-TRN-SCH-DPT-DT
  and  ddd in (select ddd from VTTT)
  and ttt = 'xxx'
"""

sql1 = re.sub('\n', r'**NL**', sql)

pat_new_line = re.compile("(?:EXEC SQL)(.+?)(?:END-EXEC)",flags = re.DOTALL)
        x1 = re.sub(pat_DECLARE, '', x)  #dont line suffix  number

sql = "aa ( bb ) cc"

thecontent = pyparsing.Word(pyparsing.alphanums) | '+' | '-'
parens     = pyparsing.nestedExpr( '(', ')', content=thecontent)
res = parens.parseString(sql)
res.asList()



from pyparsing import *

# an element within the list can be:
# - a single alphabetic letter
# - one of + - * or /
# - an unsigned integer
element = oneOf(list(alphas+"+-*/")) | Word(alphanums)

element = Word(alphanums)

expr = OneOrMore(element |
        nestedExpr("(", ")", content=OneOrMore(element))
        )

src = " A  [  B  [ C+2 ] + 3 ] "
print (expr.parseString(sql2) )

sql2 = 'dasdsdsafdsa ( sad  (  ddd  )fsad )  dsafsa  (safsadf ) '

l1 = []
keep = [([]) for i in range(1000)]
full_keep = [([]) for i in range(1000)]
ix_keep = [(0) for i in range(1000)]
parsed = sqlparse.parse(sql)[0]
keep[0] =  parsed.tokens
full_keep[0] = keep[0]
ix_keep[0] = 0
from_sw = 0   
stream = parse_gen(keep[0],0)
for k in stream:
    if len(l1) == 0 : 
        l1 = [k]  
    else :
        l1.extend([k]) 

'''

print(re.sub('\n', r'\\n', sql))   
'''

r'''
l_pgm = ['p1','p2']

df_select_1['pgm'] =  l_pgm

list_of_list = [[1,2],[1,2,3]]

df_select_1['view_list'] =  list_of_list


pd_t['mbr'] =  pd.DataFrame([[l1_nodup],[l1_nodup]])

c2 = np.array([[l1_nodup]])

c1 = np.array([file_sel] * len(tot_PO_mbr_1))[: , np.newaxis]
c2 = np.array([l1_nodup])[: , np.newaxis]
c3 = np.array(tot_PO_mbr_2)

arrx_PO_MBR = np.hstack([c1,c2,c3])

                
    l1_nodup = sorted(list(set(l1)))  
    
    pd_t[0][:] =  pd.DataFrame([[l1_nodup],[l1_nodup]])
 
    c2 = np.array(l1_nodup)[: , np.newaxis]    
    
    c2 = np.array(l1_nodup)[:]        
    
    
    c1 = np.array([file_sel] * len(tot_PO_mbr_1))[: , np.newaxis]
    c2 = np.array(tot_PO_mbr_1)[: , np.newaxis]
    c3 = np.array(tot_PO_mbr_2)
    
    
    
    arr0 = np.array(pgm)  
    arr1 = np.array([[l1_nodup]]) 
    
    arr2 = np.hstack([arr0,arr1 ]) 
    
    if len(arry_PO_MBR) == 0 : 
        arry_PO_MBR = arrx_PO_MBR 
    else :
        arry_PO_MBR = np.vstack([arry_PO_MBR,arrx_PO_MBR ]) 
    
    
    
    c2 = np.array(l1_nodup)[: , np.newaxis]
    
    arr_select_1  = np.array(pgm,np.array(l1_nodup) 
    
    df
    if len(l1_tot) == 0 : 
        l1_tot = [pgm,l1_nodup]  
    else :
        l1.extend([k]) 

                 
    if index == 3  : break

        arrx_PO = np.hstack([np.array([file_sel] * len(tot_PO_1))[: , np.newaxis] ,np.array(tot_PO_1)[: , np.newaxis]])

        if len(arry_PO_MBR) == 0 : 
            arry_PO_MBR = arrx_PO
        else :
            arry_PO_MBR = np.vstack([arry_PO_MBR,arrx_PO])                     



        
    #df_select_crud  = pd.concat([df_0_1, df_1_select ], axis = 1)



#with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sql2acum.txt', 'w') as f:
#    for k in parse_gen(keep[0],0):
#        f.write(str(k))
'''