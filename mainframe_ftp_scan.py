# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import ftplib
import os, sys


def append_newline(input):
#    fhandle.write(input + "\n")    
    if ' CALL' in input :
        print(mx, input)
        
sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')
dir_1 = 'D09120.CNDWTEST.COBSRCE'
t1 = sess.cwd("'"+dir_1+"'")
# for partition dataset we could parse partitioned data set
#250 The working directory "D09120.CNDWTEST.COBSRCE" is a partitioned data set

dir_list = []
sess.dir(dir_list.append)
mbr_list = [line[0:10].strip().split(' ')[0] for line in dir_list[1:3] ]   #the first line of dir_list is the header 


path = os.getcwd()   
outx = "testiterator"     
out_file = path+"\\"+ outx + ".txt"
#fhandle = open(out_file, 'w')
for mx in mbr_list[0:3]:   # first 3 member for test
    sess.retrlines('RETR ' + mx , append_newline)
#fhandle.close()   
 
sess.quit()

