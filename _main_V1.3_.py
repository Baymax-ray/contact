"""
1.3 version of rat-object contact detector

# Jiarui Fang (jf659@cornell.edu)
# Apr 5, 2022
"""
import os
from body import *


name=input("Please type the name (do not include '.mpg' or '.txt'): ")
path1=os.path.abspath('.')
path2=path1+"\\"+name
sequence=int(input("Which box goes first? (white=1 or black=2): "))
boxcount=int(input("How many boxes are there? (it should be >=2) eg white/black/white is 3: "))
while boxcount<2:
    boxcount=int(input("How many boxes are there? (it should be >=2): "))
framesplit=[]
cupsinbox=[]
cups=input("The position of the cups in the 1st box (eg [[1,2],[3,4]]): ")
cupsinbox.append(eval(cups))
split1=input("When is the end of the 1st box (in integer frames): ")
framesplit.append(int(split1))
cups=input("The position of the cups in the 2nd box (eg [[1,2],[3,4]]): ")
cupsinbox.append(eval(cups))
if boxcount>=3:
    split2=input("When is the end of the 2nd box (in integer frames): ")
    framesplit.append(int(split2))
    cups=input("The position of the cups in the 3rd box (eg [[1,2],[3,4]]): ")
    cupsinbox.append(eval(cups))
    if boxcount>=4:
        split3=input("When is the end of the 3rd box (in integer frames): ")
        framesplit.append(int(split3))
        cups=input("The position of the cups in the 4th box (eg [[1,2],[3,4]]): ")
        cupsinbox.append(eval(cups))
        if boxcount>4:
            for i in range(boxcount-4):
                split=input("When is the end of the "+str(i+4)+"th box (in integer frames): ")
                framesplit.append(int(split))
                cups=input("The position of the cups in the "+str(i+5)+"th box (eg [[1,2],[3,4]]): ")
                cupsinbox.append(eval(cups))

print("一条龙 type: 1还没有做完，不要用！！！！")
print("生成data type: 2")
print("读取data type: 3")
print("视频版 type: 4")
while cv2.waitKey(1) != 27:
    type=(input("please input the type of the program: "))
    while type!="1" and type!="2" and type!="3" and type!="4":
        type=(input("please input the type of the program: "))
    type=int(type)
    print("start")
    if type==1 or type==2:
        trialscount=int(input("How many trials do we have? "))
        functionthree(path2,name,sequence,framesplit,cupsinbox,trialscount,type)
    elif type==3:
        print("Which trials do we want to read?")
        print("eg: [1,2,3] or [1:3] or all")
        range=input()
        if range=="all":
            functionfour(path2,name)
        elif range.find(":")>=0:
            a=range.split(":")
            f=int(a[0][1:])
            e=int(a[1][:-1])
            r=[]
            for i in range(f,e+1):
                r.append(i)
            functionfour(path2,name,r)
        else:
            range=eval(range)
            functionfour(path2,name,range)
    elif type==4:
        functionfive(path2,name,framesplit,cupsinbox)



