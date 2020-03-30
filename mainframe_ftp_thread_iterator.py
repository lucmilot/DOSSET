# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import ftplib


import threading, queue

def ftp_chunk_iterator(FTP, mbr_list):
    # Set maxsize to limit the number of chunks kept in memory at once.
    queuex = queue.queue(maxsize=200)

    def ftp_thread_target():
        for mx in mbr_list[0:3]:   # first 3 member for test
            sess.retrlines('RETR ' + mx , callback=queuex.put)
        queuex.put(None)

    ftp_thread = threading.Thread(target=ftp_thread_target)
    ftp_thread.start()

    while True:
        chunk = queuex.get()
        if chunk is not None:
            yield chunk
        else:
            return
        
sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')
dir_1 = 'D09120.CNDWTEST.COBSRCE'
t1 = sess.cwd("'"+dir_1+"'")
# for partition dataset we could parse partitioned data set
#250 The working directory "D09120.CNDWTEST.COBSRCE" is a partitioned data set

dir_list = []
sess.dir(dir_list.append)
#mbr_list = [line[0:10].strip().split(' ')[0] for line in dir_list[1:] ]   #the first line of dir_list is the header 
mbr_list = [line[0:10].strip() for line in dir_list[1:3] ]   #the first line of dir_list is the header 



ftp_chunk_iterator(sess, mbr_list) 

sess.quit()


