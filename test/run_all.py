
import os
import subprocess

import glob

import numpy

def doTestIn(dir):
    os.chdir(dir)
    files = glob.glob('./test_*.py')
    python_path = r"C:\Users\taichi-kodama\BeautifulLiner\.venv\Scripts\python.exe"
    for file in files:
        subprocess.call(python_path + ' %s' % file)
    #end
#end

#pwd = os.getpwd() present? current? 
cwd = os.getcwd()

#subprocess.call(r'..\.venv\Scripts\activate')

doTestIn(r".\model\primitive")
os.chdir(cwd)

doTestIn(r".\model")
os.chdir(cwd)