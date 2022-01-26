"""
1.0 version of rat-object collision detector

# Jiarui Fang (jf659@cornell.edu)
# December 23, 2021
"""

import cv2
import os
from working_on import*

worktype=input("what do you want? \n type 1 if only need none zore frame \n type 2 if need modified video \n type 3 if need contact frame\n")
name=input("please type the name (do not include 'mp4' or 'txt'): ")
# get the path of this file
path1=os.path.abspath('.')
path2=path1+"\\"+name+"\\"+name
f = open(path2+'.txt')
info=read_txt(f)
f.close()

if worktype=='2':
    functwo(path2,info)
if worktype=='1':
    funcone(path1,info,name)
if worktype=='3':
    functhree(path1,info,name)