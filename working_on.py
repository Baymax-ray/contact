"""
1.0 version of rat-object collision detector

# Jiarui Fang (jf659@cornell.edu)
# December 23, 2021
"""
import cv2
import os
from object_ import *

def read_txt(f):
    """
    Return information about the time, the location (x,y), and the neuron activity of the rat from an text

    Note that the data should be seperated by ","

    Parameter f: The name of that text
    Precondition: NONE (name can be anything)
    """
    lines = f.readlines()
    number=len(lines)
    time=[]
    x_l=[]
    y_l=[]
    n_l=[]
    for i in range(number):
        #print(i)
        line=lines[i]
        a=line.find(',')
        b=line.find(',',a+1)
        c=line.find(',',b+1)
        time.append(float(line[:a]))
        x_l.append(line[a+1:b])
        y_l.append(line[b+1:c])
        if line.find('\n')>0:
            n_l.append(float(line[c+1:-1]))
        else:
            n_l.append(float(line[c+1:]))
    return [time,x_l,y_l,n_l]

def end_detect(x):
    """
    return false if the location is NaN
    """
    if x=="NaN":
        return False
    else:
        return True

def deeperorbrighter(image,x,y,sta):
    """
    Return true if the circle is solid and return false otherwise

    Parameter image: the frame to use
    Precondition: image is a picture

    Parameter x: the x-axis of the circle center
    Precondition: x is int and x>0 and x<wid-5

    Parameter y: the y-axis of the circle center
    Precondition: y is int and y>0 and y<height-5

    Parameter sta: the average brightness of the picture
    Precondition: sta is a number
    """
    # 颠倒xy，因为image[高，宽]
    q=int(x)
    x=int(y)
    y=int(q)
    sum=0
    shape=image.shape
    if x+5>=shape[0] or y+5>=shape[1]:
        return False
    s=False
    for t in range(5):
        for u in range(5):
            sum=int(image[x+t,y+u][0])+int(image[x+t,y+u][1])+int(image[x+t,y+u][2])+sum
    if (sum//25>1.3*sta)or(sum//25<0.7*sta):
        s=True
    #print ("sum:"+str(sum))
    return s

def deeperorbrighter_helper(image):
    """
    return the average brightness of the picture
    the larger, the brighter

    Parameter image: the frame to use
    Precondition: image is a picture
    """
    shape=image.shape
    sum=0
    number=image.size//3
    for y in range(0,shape[0]):
        for x in range (0,shape[1]):
            sum=sum+image[y,x,0]+image[y,x,1]+image[y,x,2]
            #if x%100==0:
                #print (image[y,x,0]+image[y,x,1]+image[y,x,2])
    print(number)
    print(sum)
    print ("sta:"+str(sum//number))
    return sum//number


def circle_detect(image,sta,current,potential):
    """
    Return the circle's center and radius in a list [x,y,r]
    return [0,0,0] if no circle detected

    Parameter image: the frame to use
    Precondition: image is a picture

    Parameter sta: the average brightness of the picture
    Precondition: sta is a number

    Parameter curent: the current object to draw
    Precondition: current is a Currentobject

    Parameter potential: the list of potential objects to draw
    Precondition: potential is a Potentialobject
    """
    # 增加亮度
    # image=increase_brightness(image)
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
    # 增加对比度
    #img = cv2.convertScaleAbs(gray,alpha=1.3,beta=0)
    # 进行中值滤波
    img = cv2.medianBlur(gray, 5)
    # 霍夫变换圆检测
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 30, param1=100, param2=20, minRadius=10, maxRadius=30)
    x=0
    y=0
    r=0
    temp=[]
    if not circles is None:
        print('find')
        rr=0
        xx=0
        yy=0
        for circle in circles[0]:
            # 半径
            r = int(circle[2])
            # 找出代表medium的圆
            if r>=10 and r<=25:
                x = int(circle[0])
                y = int(circle[1])
                if deeperorbrighter(image,x,y,sta)==False:
                    r=rr
                    x=xx
                    y=yy
                else:
                    rr=r
                    xx=x
                    yy=y
                    temp.append([x,y,r])
                    print(x,y,r)
                    #cv2.circle(image, (x, y), r, (0, 0, 255), 3)
            else:
                r=rr
    ok=False
    if len(temp)==0:
        current.noadd()
        current.check_delay()
        current.changestate(False)
    else:
        current.noclear()
        for t in temp:
            if current.check_state(t[0],t[1],t[2])==True:
                ok=True
                print("continue")
        if ok==True:
        #  this means the current object is still there
            current.changestate(True)
            potential.clear()
        else:
            for t in temp:
                potential.add(t)
            p=potential.check()
            if p!=False:
                current.update(p)
                potential.clear()
    return(current.getlocation()+[current.getradius()])

def functwo(path,info):
    """
    draw the location of rat and cup on the video

    Parameter path: the path of the video
    Precondition: patj is a string

    Parameter info: infomation from the txt
    Precondition: info is a list
    """
    time=info[0]
    x_l=info[1]
    y_l=info[2]
    n_l=info[3]
    video_caputre = cv2.VideoCapture(path+".mp4")
    frameCount = video_caputre.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_caputre.get(cv2.CAP_PROP_FPS)
    print(fps)
    interval=1/fps
    width = video_caputre.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_caputre.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width),int(height))
    success, frame_src = video_caputre.read()
    # start with frame 0
    index=0
    # skip some time
    skip=input("do we need to skip any time? (in seconds): ")
    skip=int(skip)
    if skip!=0:
        index_skip=int(skip*fps)
        frameCount=frameCount-index_skip
        while success and index_skip!=0:
            index_skip=index_skip-1
            success, frame_src = video_caputre.read()
    a=len(time)
    #print(a)
    video_write = cv2.VideoWriter(path+"_skip"+str(skip)+"sec.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    current=Currentobject()
    potential=Potentialobject()
    i_txt=0
    while success and not cv2.waitKey(1) == 27: #读完退出或者按下 esc 退出
        if index==0:
            sta=deeperorbrighter_helper(frame_src)
        while time[i_txt]<skip:
            i_txt=i_txt+1
        #print('i:'+str(i_txt))
        while  i_txt<a-1 and time[i_txt]-skip<=index*interval:
            # draw the point from last frame to this frame
            if end_detect(x_l[i_txt])==True:
                #print(int(float(x_l[i_txt])), int(float(y_l[i_txt])))
                cv2.circle(frame_src, (int(float(x_l[i_txt])), int(float(y_l[i_txt]))), 2, (0, 0, 255), -1)
            i_txt=i_txt+1
        draw=circle_detect(frame_src,sta,current,potential)
        if draw[2]!=0:
            # we have circle to draw
            cv2.circle(frame_src, (draw[0], draw[1]), 15, (255, 255, 0), 3)
        cv2.imshow("video", frame_src)
        cv2.waitKey(0)
        video_write.write(frame_src)
        if index%(frameCount//20)==0:
            sta=deeperorbrighter_helper(frame_src)
            print(str(index//(frameCount//20)*5)+"%")
        index=index+1
        success, frame_src = video_caputre.read()
    video_write.release()
    print("Done!")

def funcone(path,info,name):
    """
    save the frame in which there exists neuron activity

    Parameter path: the path of the video
    Precondition: patj is a string

    Parameter info: infomation from the txt
    Precondition: info is a list

    Parameter name: name of the project
    Precondition: name is a string
    """
    time=info[0]
    n_l=info[3]
    a=len(time)
    i_time=0
    path1=path+"\\"+name+"\\"+"potential"
    path2=path+"\\"+name+"\\"+name
    print(path1)
    isExist = os.path.exists(path1)
    #print(isExist)
    if not isExist:
        os.makedirs(path1)
        print("The new directory is created!")
    video_caputre = cv2.VideoCapture(path2+".mp4")
    frameCount = video_caputre.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_caputre.get(cv2.CAP_PROP_FPS)
    print(fps)
    interval=1/fps
    framelist=[]
    while i_time<a-1:
        if n_l[i_time]!=0:
            # time between n and n+1 frame should belong to n frame
            fra=time[i_time]//interval
            #print(n_l[i_time])
            #print(time[i_time])
            #print(fra)
            framelist.append(fra)
        i_time=i_time+1
    print("list get")
    framelist2=list(set(framelist))
    framelist2.sort()
    #print(framelist2)
    index=0
    success, frame = video_caputre.read()
    while len(framelist2)!=0:
        stop=False
        i=framelist2.pop(0)
        while success and not stop:
            if index==i:
                cv2.imwrite(path1+"\\"+str(index)+".jpg",frame)
                #print(index)
                #cv2.imshow("video", frame)
                #cv2.waitKey(0)
                stop=True
            index=index+1
            success, frame = video_caputre.read()
    print("Done!")

def contact_helper(current,points):
    """
    return True if at least one point contacts the cup, return False otherwise

    Parameter current: the cup
    Precondition: current is a list

    Parameter points: infomation of points
    Precondition: points is a list
    """
    for point in points:
        if ((point[0]-current[0])**2+(point[1]-current[1])**2)**0.5<=15:
            return True
    return False

def functhree(path,info,name):
    """
    get the frame in which the rat contact the cup

    Parameter path: the path of the video
    Precondition: path is a string

    Parameter info: infomation from the txt
    Precondition: info is a list

    Parameter name: name of the project
    Precondition: name is a string
    """
    time=info[0]
    x_l=info[1]
    y_l=info[2]
    n_l=info[3]
    path1=path+"\\"+name+"\\"+"contact"
    path2=path+"\\"+name+"\\"+name
    isExist = os.path.exists(path1)
    #print(isExist)
    if not isExist:
        os.makedirs(path1)
        print("The new directory is created!")
    video_caputre = cv2.VideoCapture(path2+".mp4")
    frameCount = video_caputre.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_caputre.get(cv2.CAP_PROP_FPS)
    print(fps)
    interval=1/fps
    width = video_caputre.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_caputre.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width),int(height))
    success, frame_src = video_caputre.read()
    # start with frame 0
    index=0
    # skip some time
    skip=input("do we need to skip any time? (in seconds): ")
    skip=int(skip)
    if skip!=0:
        index_skip=int(skip*fps)
        frameCount=frameCount-index_skip
        while success and index_skip!=0:
            index_skip=index_skip-1
            success, frame_src = video_caputre.read()
    a=len(time)
    #print(a)
    current=Currentobject()
    potential=Potentialobject()
    i_txt=0
    while success and not cv2.waitKey(1) == 27: #读完退出或者按下 esc 退出
        points=[]
        if index==0:
            sta=deeperorbrighter_helper(frame_src)
        while time[i_txt]<skip:
            i_txt=i_txt+1
        #print('i:'+str(i_txt))
        while  i_txt<a-1 and time[i_txt]-skip<=index*interval:
            # draw the point from last frame to this frame
            if end_detect(x_l[i_txt])==True:
                #print(int(float(x_l[i_txt])), int(float(y_l[i_txt])))
                #cv2.circle(frame_src, (int(float(x_l[i_txt])), int(float(y_l[i_txt]))), 2, (0, 0, 255), -1)
                points.append((int(float(x_l[i_txt])), int(float(y_l[i_txt]))))
            i_txt=i_txt+1
        draw=circle_detect(frame_src,sta,current,potential)
        if draw[2]!=0:
            # we have circle to draw
            if not current.getcontact():
                if contact_helper(draw,points):
                    current.changecontact()
                    cv2.imwrite(path1+"\\"+str(index)+".jpg",frame_src)
        if index%(frameCount//20)==0:
            sta=deeperorbrighter_helper(frame_src)
            print(str(index//(frameCount//20)*5)+"%")
        index=index+1
        success, frame_src = video_caputre.read()
    print("Done!")