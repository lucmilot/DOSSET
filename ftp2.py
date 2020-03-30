# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""



import subprocess




commands = b'''
"lls"
"ls"
"cd luc"
"ls"
'''

process = subprocess.Popen('psftp -pw LucLuc01 xt21586@r59s2e5.CN.CA', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(commands)


print (out.decode(encoding="utf-8"))



print ('tata')


process.kill()



'''



process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(commands)
print (out)

process.kill()



import time
import subprocess

p = subprocess.Popen(['psftp -pw LucLuc01 xt21586@r59s2e5.CN.CA'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)  
testresult = p.communicate()[0]
print (testresult)



p = subprocess.Popen(['dir', 'm*'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)  
p.stdin.write('one\n')
time.sleep(0.5)   
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)




p = subprocess.check_output(['dir', 'm*'], stdout=PIPE, stdin=PIPE, stderr=subprocess.STDOUT)    
p.stdin.write('one\n')
time.sleep(0.5)
p.stdin.write('two\n')
time.sleep(0.5)
p.stdin.write('three\n')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)




psftp -pw LucLuc01  xt21586@r59s2e5.CN.CA 

p = subprocess.Popen(["psftp", "xt21586@r59s2e5.CN.CA"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
print (p.communicate("LucLuc01\n"))




 p = subprocess.Popen(["sudo", "-S", "whoami"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
 print p.communicate("password\n") 



command = ['sftp', 'xt21586@r59s2e5.CN.CA']

#p = subprocess.Popen(command, stdin=subprocess.PIPE,shell=True))
p = subprocess.Popen(command,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=subprocess.PIPE,
                 shell=True,
                 bufsize=0)

print('tata')

try:
    print('titi')
    outs, errs = p.communicate(timeout=15)
except :
    p.kill()
    outs, errs = p.communicate()

'''
