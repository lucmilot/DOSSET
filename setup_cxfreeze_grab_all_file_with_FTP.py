# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 05:41:13 2018

@author: XT21586
"""

import os
import sys
from cx_Freeze import setup, Executable

#run with : python setup_cxfreeze_grab_all_file_with_FTP.py build


build_exe_options = {"includes": ["tkinter"]}
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

os.environ['TCL_LIBRARY'] = r'C:\Users\XT21586\AppData\Local\Continuum\anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\XT21586\AppData\Local\Continuum\anaconda3\tcl\tk8.6'


pathx = os.getcwd()
print (pathx)

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "grab_all_file_with_FTP_V1",
        version = "1.0",
        description = "luc!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("grab_all_file_with_FTP.py", base=base)])

'''
mplBackendsPath = os.path.join(os.path.split(sys.executable)[0],
                        "Lib/site-packages/matplotlib/backends/backend_*")

fileList = glob.glob(mplBackendsPath)

moduleList = []

for mod in fileList:
    modules = os.path.splitext(os.path.basename(mod))[0]
    if not module == "backend_qt4agg":
        moduleList.append("matplotlib.backends." + modules)

build_exe_options = {"excludes": ["tkinter"] + moduleList, "optimize": 2}
'''