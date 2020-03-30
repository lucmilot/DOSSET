# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import ftplib
import os
from sys import exc_info
import tkinter as tk

def append_newline(input):
    fhandle.write(input + "\n")
    
def select_level1():  

    def clicked_Entry_Submit():
        global lvl_1
        lvl_1 = txt.get()
    #    lbl.configure(text= "")
        window1.destroy()    
    
    window1 = tk.Tk()
    window1.title("Enter Level1")
    #window.geometry('100x200')
    window1.config(height=100, width=200, bg="#C2C2D6")
        
    txt = tk.Entry(window1,width=40)
    txt.grid(column=1, row=1)
    #txt.pack(padx=100, pady=100, side = 'bottom')
    
    btn = tk.Button(window1, text="Submit", bg="white", fg="green",  height = 2, width = 10, command=clicked_Entry_Submit)
    btn.grid(column=2, row=1)
    
    window1.mainloop()


def select_level_2_3(file_list):  
     
    def clicked_List_Submit(e):
        global choice_return
        
        tte = e
        
        ttt = listbox1.curselection()
        choice_return = file_list[listbox1.curselection()[0]]
        
        #tt = mylist.curselection()[0]
        #choice_return = 'tata'
        master2.destroy()
   
    choice_return = "" 
    
    master2 = tk.Tk()
    
    listbox1 = tk.Listbox(master2)
    for line in file_list:
       listbox1.insert(tk.END, str(line))
    listbox1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    listbox1.bind("<<ListboxSelect>>", clicked_List_Submit)

    scroll1 = tk.Scrollbar(master2)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    scroll1.configure(command=listbox1.yview)
    listbox1.configure(yscrollcommand=scroll1.set)    

    master2.mainloop()
  
    return  
 


#select_level1()
lvl_1 = "D09128"


sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')
sess.cwd("'"+lvl_1+"'")

filelist = sess.nlst()
select_level_2_3(filelist)
print(choice_return)



#dir_list = []
#sess.dir(dir_list.append)
#[print (line) for line in sess.retrlines('NLST')]
    
#-------------------------------------------------------------------------------------    
#-------------------------------------------------------------------------------------       
#-------------------------------------------------------------------------------------   
'''

choice_return = select_project()    
    

print(os.getcwd())

sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')

filelist = sess.nlst()

print(sess.pwd())

sess.cwd("'D09128.CNDWENVT.JCLMASTR'")

print(sess.pwd())

#print(sess.retrlines('NLST'))

dir_list = []
sess.dir(dir_list.append)

filename = 'DWTW06E2'
fhandle = open(filename, 'w')
sess.retrlines('RETR ' + filename, append_newline)
fhandle.close()


directory ="/home/FTP" #dir i want to download files from, can be changed or left for user input
filematch = '*.*' # a match for any file in this case, can be changed or left for user to input

ftp.cwd(directory)

for filename in ftp.nlst(filematch): # Loop - looking for matching files
    fhandle = open(filename, 'wb')
    print 'Getting ' + filename #for confort sake, shows the file that's being retrieved
    ftp.retrbinary('RETR ' + filename, fhandle.write)
    fhandle.close()



with ftplib.FTP(FTP_IP, FTP_LOGIN, FTP_PASSWD) as ftp:
    ftp.cwd('movies')
    with open(FILENAME, 'wb') as f:
        ftp.retrbinary('RETR ' + FILENAME, f.write)

#DWTW06E2

print(sess.ls)

dir_list = []
sess.dir(dir_list.append)

for line in dir_list:
   print (line[29:].strip().split(' ') )# got yerself an array there bud!
   # EX ['545498', 'Jul', '23', '12:07', 'FILENAME.FOO']



sess.retrlines('LIST')



sess.retrlines("D09128.CNDWENVT.JCLMASTR(DWTW06E2)")







sess.cwd("'D09128.CNDWENVT.JCLMASTR'")

print(ftp.ls)

ftplib.list

sess.quit()


ftp.retrlines("File To be Downloaded")
'''