"""
find the place of multiple cups
w/a/s/d move 10 pixels; up/down/left/right move 1 pixel
use esc to exit

# Jiarui Fang (jf659@cornell.edu)
# Apr 29, 2022
"""

import keyboard
import constant
import cv2

#name=input("please type the name of the picture :")
image = cv2.imread("D:\\OneDrive - Dawn\\Research_David_Smith\\video\\R2142_05-09-2022\\white.jpg")
shape=image.shape
print(shape)
T=True

def escape():
    """
    escape the program
    """
    global T
    T=False

def up_10(circle):
    """
    move up 10 pixels
    """
    circle[1]=circle[1]-10
    print(circle)

def down_10(circle):
    """
    move down 10 pixels
    """
    circle[1]=circle[1]+10
    print(circle)

def left_10(circle):
    """
    move left 10 pixels
    """
    circle[0]=circle[0]-10
    print(circle)

def right_10(circle):
    """
    move right 10 pixels
    """
    circle[0]=circle[0]+10
    print(circle)

def up_1(circle):
    """
    move up 1 pixel
    """
    circle[1]=circle[1]-1
    print(circle)

def down_1(circle):
    """
    move down 1 pixel
    """
    circle[1]=circle[1]+1
    print(circle)

def left_1(circle):
    """
    move left 1 pixel
    """
    circle[0]=circle[0]-1
    print(circle)

def right_1(circle):
    """
    move right 1 pixel
    """
    circle[0]=circle[0]+1
    print(circle)



circle=[int(shape[1]/2),int(shape[0]/2)]
keyboard.add_hotkey('w',up_10,args=[circle])
keyboard.add_hotkey('s',down_10,args=[circle])
keyboard.add_hotkey('a',left_10,args=[circle])
keyboard.add_hotkey('d',right_10,args=[circle])
keyboard.add_hotkey('up',up_1,args=[circle])
keyboard.add_hotkey('down',down_1,args=[circle])
keyboard.add_hotkey('left',left_1,args=[circle])
keyboard.add_hotkey('right',right_1,args=[circle])
keyboard.add_hotkey('esc',escape)


# input coordinate of a print
while T:
    img_show=image.copy()
    #print(circles)
    cv2.circle(img_show, (int(circle[0]), int(circle[1])), constant.RAD, (0, 0, 255), 1)
    cv2.imshow("image2",img_show)
    cv2.waitKey(0)