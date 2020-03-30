# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import os, sys

import win32com.client as win32

import tkinter as tk

import pandas as pd

import re

import sqlparse

from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML



#------------------------------------------------------------------------

 

from tkinter.filedialog import askopenfilename
root = tk.Tk() 
root.withdraw()
filename = askopenfilename(parent=root)

df_in = pd.read_csv(filename )

df_in = df_in.fillna('')

pat_SIUD = re.compile(".*(?=SELECT|INSERT|DELETE|UPDATE).*",flags = re.DOTALL)
pat_select = re.compile(".*(?=SELECT).*",flags = re.DOTALL)
pat_DECLARE = re.compile("(?:^DECLARE)(.+?)(?:FOR)",flags = re.DOTALL)
pat_strt_double_quote = re.compile(r"^\"",flags = re.DOTALL)
pat_end_double_quote = re.compile("(\"$)",flags = re.DOTALL)
pat_strt_newline = re.compile("(^\r\n)",flags = re.DOTALL)
pat_strt_blank_SELECT = re.compile("(?:^\s)(\s*)(?:SELECT)",flags = re.DOTALL) 


df_0_1= df_in.iloc[:,0:2]


df_1_n = df_in.iloc[:,2:]


df_1_n = df_1_n.applymap(lambda x: re.sub(pat_DECLARE, '', x))

df_1_n = df_1_n.applymap(lambda x: x.strip())

df_1_select = df_1_n[df_1_n.applymap(lambda x: (re.search(pat_select,x)  is not None) )]
df_1_select  = df_1_select .fillna('')

df_select = pd.concat([df_0_1, df_1_select ], axis = 1)

with open(r'C:\Users\XT21586\Documents\document\_DOSSET\result\sqlacum.txt', 'w') as f:
    for index, row in df_select.iterrows():
        pgm = row[1]
        for x in row[2: ]:
            if x != '':
                f.write('\n------------------------------------------------\n')     
                f.write('>>>>:  '+pgm)      
                f.write('\n------------------------------\n')                
                f.write(x)  

print ('tata')
    
def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed):
    #from_seen = False
    for item in parsed.tokens:
        print(item)
        print('--------------')
        if item.ttype is Keyword : print ('keyword')

        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                raise StopIteration
            else:
                #print (item)
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True
        '''

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
    stream = extract_from_part(sqlparse.parse(sql)[0])
    return list(extract_table_identifiers(stream))


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


tables = ', '.join(extract_tables(sql))[0]
print('Tables: {0}'.format(tables))
    

parsed = sqlparse.parse(sql)[0]
for item in   parsed .tokens:
    print('lv0')
    print(item)
    
    if item.is_group : 
        for item in item.tokens:
            print('lv1')
            print(item)
            print(item.ttype)
            
            if item.is_group : 
                for item in item.tokens:
                    print('lv2')
                    print(item)     
                    print(item.ttype)                    

                    if is_subselect(parsed) : 
                        for x in extract_from_part(item):
                            yield x
                    if item.is_group : 
                        for item in item.tokens:
                            print('lv3')
                            print(item)            
                            print(item.ttype)     