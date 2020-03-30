# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 13:08:55 2018

@author: XT21586
"""


import ftplib
import os
from sys import exc_info
import tkinter as tk

    
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


select_level1()

print (lvl_1)