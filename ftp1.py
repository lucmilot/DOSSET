# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import tempfile

print (tempfile.gettempdir()) # prints the current temporary directory


import os
import subprocess
import sys
from tempfile import gettempdir

ProgPath = r"C:\Users\XT21586\Documents\document\Data Stage\SFTP\test"
absp = os.path.abspath(ProgPath)
fn = os.path.join(gettempdir(), 'test.bat')
script_lines = [
    '@rem Self Destruct Script',
    '@echo ERROR - Attempting to run expired test only software',
    '@pause',
    '@dir %s' % (absp),
    '@echo Deleted Offending File!',
    '@dir %s' %(fn)
    #'@exit\n',
    ]
bf = open(fn, 'wt')
bf.write('\n'.join(script_lines))
bf.flush()
bf.close()
p = subprocess.Popen([fn], shell=False)

testresult = p.communicate()[0]

sys.exit(-1)


import subprocess

command = ['sftp', 'xt21586@r59s2e5.CN.CA']
subprocess.Popen(command, stdin=subprocess.PIPE).wait(timeout=60)




import time
from subprocess import Popen, PIPE
import subprocess


p = Popen(['sftp', 'xt21586@r59s2e5.CN.CA'], stdout=PIPE, stdin=PIPE)    
p.stdin.write(b'LucLuc01')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)


import time
import subprocess
process = subprocess.Popen(['sftp', 'xt21586@r59s2e5.CN.CA'],
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=subprocess.PIPE,
                 shell=True,
                 bufsize=0)
time.sleep(0.5)
process.stdin.write(b'LucLuc01')
time.sleep(0.5)
testresult = process.communicate()[0]
print(testresult)




import subprocess
process = subprocess.Popen(['dir'],
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=subprocess.PIPE,
                 shell=True,
                 bufsize=0)
stdout = process.communicate()[0]
print (stdout.decode("utf-8"))

process.kill

process.






import subprocess
print (subprocess.check_output([r"C:\Users\XT21586\Documents\document\Data Stage\SFTP\test.bat"],shell=True).decode("utf-8"))



import time
from subprocess import Popen, PIPE
import subprocess
p = Popen([r"C:\Users\XT21586\Documents\document\Data Stage\SFTP\test.bat"], stdout=PIPE, stdin=PIPE)    
p.stdin.write(b'LucLuc01')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)





import subprocess
subprocess.check_output(["echo", "Hello World!"],shell=True)



import subprocess
process = subprocess.Popen(['echo', '"Hello stdout"'], stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print ('STDOUT:{}'.format(stdout))



import os

p = os.popen('dir m*')  
print(p.read())  



import time
from subprocess import Popen, PIPE
import subprocess


p = Popen(['sftp', 'xt21586@r59s2e5.CN.CA'], stdout=PIPE, stdin=PIPE)    
p.stdin.write(b'LucLuc01')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)



from subprocess import Popen, PIPE
print (Popen(['dir'],stdout=PIPE,stdin=PIPE).stdout.read())


from subprocess import Popen, PIPE
from tempfile import SpooledTemporaryFile as tempfile
f = tempfile()
f.write('one\ntwo\nthree\nfour\nfive\nsix\n')
f.seek(0)
print Popen(['/bin/grep','f'],stdout=PIPE,stdin=f).stdout.read()
f.close()




import time
from subprocess import Popen, PIPE
import subprocess

p = subprocess.Popen('dir',
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=PIPE,
                 shell=True,
                 bufsize=0)
p.stdin.write(b'START\n')
out = p.stdout.readline()
while out:
  line = out
  line = line.rstrip(b"\n")

  if "WHATEVER1" in line:
      pr = 1
      p.stdin.write('DO 1\n')
      out = p.stdout.readline()
      continue

  if "WHATEVER2" in line:
      pr = 2
      p.stdin.write('DO 2\n')
      out = p.stdout.readline()
      continue
"""
..........
"""

out = p.stdout.readline()

p.wait()





import time
from subprocess import Popen, PIPE
import subprocess


p = Popen(['sftp', 'xt21586@r59s2e5.CN.CA'], stdout=PIPE, stdin=PIPE)    
p.stdin.write(b'LucLuc01')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)



p = Popen(['dir', 'm*'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
p.stdin.write('one\n')
time.sleep(0.5)
p.stdin.write('two\n')
time.sleep(0.5)
p.stdin.write('three\n')
time.sleep(0.5)
testresult = p.communicate()[0]
time.sleep(0.5)
print(testresult)





import os
read, write = os.pipe()
os.write(write, "dir")
os.close(write)

subprocess.check_call(['your-command'], stdin=read)



import os
from subprocess import run, PIPE

p = run(['dir'], stdout=PIPE,
        input=r'm*', encoding='ascii')
print(p.returncode)





response = input("Please enter your name: ")

import subprocess

command = ['sftp', 'xt21586@r59s2e5.CN.CA']

tt = subprocess.Popen(command, stdin=subprocess.PIPE).wait(timeout=60)

subprocess.Popen(command, stdin=subprocess.PIPE).wait(timeout=60)






from subprocess import Popen, PIPE
import subprocess

proc = Popen(['sftp','xt21586@r59s2e5.CN.CA', 'stop'], stdin=PIPE, stdout=PIPE)
proc.communicate(r'LucLuc01')



import os

import subprocess

o=os.popen('sftp xt21586@r59s2e5.CN.CA','stop').read()
print(o)

 




import subprocess

cmd = "sftp xt21586@r59s2e5.CN.CA"

returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
print('returned value:', returned_value)






import subprocess

myProcess = subprocess.Popen(['dir'],shell = False)  #opens command prompt
myProcess.communicate('gdal2tiles -p raster -z 0-1 new.jpg abc') 
myProcess.wait()
print("my process has terminated")



from subprocess import Popen, PIPE

def sftp_rename(from_name, to_name):
    sftp_password = 'LucLuc01'
    sftp_username = 'xt21586'
    destination_hostname = 'r59s2e5.CN.CA'
    from_name = 'oldfilename.txt'
    to_name = 'newfilename.txt'
    commands = f"""
spawn sftp -o "StrictHostKeyChecking no" 
{sftp_username}@{destination_hostname}
expect "password:"
send "{sftp_password}\r"
expect "sftp>"
send "rename {from_name} {to_name}\r"
expect "sftp>"
send "bye\r"
expect "#"
"""
    sp = Popen(['expect', '-c', commands], stdin=PIPE, stdout=PIPE))
#    sp = subprocess.Popen(['expect', '-c', commands], stdin=subprocess.PIPE, stdout=subprocess







proc = Popen(['sftp','xt21586@r59s2e5.CN.CA', 'stop'], stdin=PIPE)
proc.communicate('LucLuc01')

sess = ftplib.FTP('r59s2e5.CN.CA','xt21586','LucLuc01')