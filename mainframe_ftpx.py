# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:47:14 2018

@author: XT21586
"""

import ftplib
import os
from sys import exc_info


sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')

filelist = sess.nlst()

print(ftp.ls)

ftplib.list

sess.quit()


ftp.retrlines("File To be Downloaded")











I am trying to parse / download some of the files from Mainframe using ftplib but it's unsuccesful after few attempts. 

My code Till now is :
import ftplib
ftp = ftplib.FTP('host','username','password')
ftp.retrlines("File To be Downloaded")


sess = ftplib.FTP("imftpb", "CNDWLMM", "LCJFMHF8")
sess.sendcmd("site sbd=(IBM-1047,ISO8859-1)")
for dir in ["ASM", "ASML", "ASMM", "C", "CPP", "DLLA", "DLLC", "DLMC", "GEN", "HDR", "MAC"]:
    sess.cwd("'ZLTALM.PREP.%s'" % dir)
    try:
        filelist = sess.nlst()
    except ftplib.error_perm as x:
        if (x.args[0][:3] != '550'):
            raise
    else:
        try:
            os.mkdir(dir)
        except:
            continue
        for hostfile in filelist:
            lines = []
            sess.retrlines("RETR "+hostfile, lines.append)
            pcfile = open("%s/%s"% (dir,hostfile), 'w')
            for line in lines:
                pcfile.write(line+"\n")
            pcfile.close()
        print ("Done: " + dir)
sess.quit()