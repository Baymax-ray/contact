"""
body part of the program

# Jiarui Fang (jf659@cornell.edu)
# Feb 12, 2022
"""
import cv2
from helpers import *
from constant import *
from math import sqrt


def functionthree(path2,name,sequence,framesplit,cupsinbox,trialcount,ty):
    """
    semi-automatic process for contact analysis
    create a project file for future use

    Parameter path2: the path of the folder that contains the video
    Precondition: path2 is a string

    Parameter name: the name of the video
    Precondition: name is a string

    Parameter sequence: the sequence of the white and black boxes
    Precondition: sequence is an int 1 (white first) or 2 (black first)

    Parameter framesplit: the end of a box
    Precondition: framesplit is a list of ints of a framenumber

    Parameter cupsinbox: the position of cups in a box
    Precondition: cupsinbox is a list of a list of two coordinates-[[[x,y],[x,y],...],[[x,y],[x,y],...],...]
    
    Parameter trialcount: the amount of trials we have
    Precondition: trialcount is an int (usually it should be an even number)

    Parameter ty: the type of the video
    Precondition: ty is a 1 or 2 (int)
    """
    boxcount=len(cupsinbox)
    video_capture = cv2.VideoCapture(path2+"//"+name+".mp4")
    frameCount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    #print(fps)
    interval=1/fps
    timesplit=[]
    for i in framesplit:
        timesplit.append(int(i*interval))
    
    timestamps=gettimestamps(path2,name)
    right_timestamp=conformcount(timestamps,trialcount)
    
    if type(right_timestamp)==int:
        print("wrong count, we are missing"+str(right_timestamp)+"timestamps")
        print(timestamps)
        return
    print("right count")
    
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width),int(height))
    frame_index=0 # we do not compensate the difference between video and timestamp here
    print("total frame: "+str(frameCount))

    Trials=[] #Trials store Trial objects
    boxindicator=0 #start from the first box
    cupscount=len(cupsinbox[boxindicator])
    trialindex=0

    success, frame_un = video_capture.read()
    while success: #and not cv2.waitKey(1) == 27: #读完退出或者按下 esc 退出
        time=frame_index*interval
        time_next=time+interval
        y,x=rat_detecter(frame_un)
        #if y!=None and x!=None:
            #cv2.circle(frame_un, (int(x),int(y)), 1, (0, 255, 255), 3)
        boxindicator=bisect.bisect(framesplit,frame_index)
        if sequence%2!=boxindicator%2: #white box
            cup=cup_detecter(frame_un,cupsinbox[boxindicator],[x,y],0)
        else: #black box
            cup=cup_detecter(frame_un,cupsinbox[boxindicator],[x,y],1)
        cupscount=len(cupsinbox[boxindicator])
        
        trialnumber=bisect.bisect(right_timestamp,time)
        

        if trialnumber==1 and trialindex==0:
            print("first trial")
            trialindex=1
            thisTrial=Trial(trialindex)
            
        elif trialnumber!=trialindex:
            # thistrial compute
            thisTrial.compute_o(cupscount)
            count12=thisTrial.test
            Trials.append(thisTrial)
            print("trial "+str(trialindex)+" finished"+" count: "+str(count12))
            #new trial
            trialindex=trialnumber
            thisTrial=Trial(trialindex)
        
        if frame_index==frameCount-50:#save the last trial
            thisTrial.compute_o(cupscount)
            Trials.append(thisTrial)
            print("we get " +str(len(Trials))+" trials")

        if trialnumber ==0: #we have not started a trial
            pass
        else:
            if y!=None and x!=None:
                thisTrial.addposition(x,y,frame_index)
            thisTrial.addpotential(cup)

        #print(frame_index)
        
        #cv2.imshow('img',frame_un)
        #cv2.waitKey()
        if boxindicator<len(timesplit) and time_next>timesplit[boxindicator]:#we have just finished a box
            print("we have just finished a box")
            n=bisect.bisect(right_timestamp,timesplit[boxindicator])
            frame_index_nextbox=int(right_timestamp[n]/interval)
            frame_index=frame_index_nextbox-1 #because we will add 1 later
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index_nextbox)
        frame_index=frame_index+1
        if trialindex>=144:
            print("frame_index",frame_index)
        success, frame_un = video_capture.read()
    video_capture.release()
    
    # write data into a file
    writedata(Trials,sequence,name,path2,right_timestamp,timesplit,cupsinbox,fps)

    if ty==1:
        functionfour(path2,name,Trials)
    print("Done!")



def functionfour(path2,name,Trials=None,scope=None):
    """
    semi-automatic process for contact analysis
    use the project file created by functionthree

    Parameter path2: the path of the folder that contains the video
    Precondition: path2 is a string

    Parameter name: the name of the video
    Precondition: name is a string

    Parameter Trials: the list of Trial objects
    Precondition: Trials is a list of Trial objects

    Parameter scope: the scope of this function
    Precondition: scope is a list of ints or None
    """
    video_capture = cv2.VideoCapture(path2+"//"+name+".mp4")
    frameCount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    #print(fps)
    interval=1/fps
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width),int(height))

    path=path2+"//trials"
    isExist = os.path.exists(path)
    #print(isExist)
    if not isExist:
        os.makedirs(path)
        print("The new directory is created!")
    
    #read the project file
    workbook = openpyxl.load_workbook(path2+"//"+name+"_data.xlsx")
    sheet = workbook['data']
    workbook.create_sheet('check')
    sheet2 = workbook['check']
    print("create new sheet")
    max=sheet.max_row
    num=1
    f_comment=True
    while f_comment:
        if sheet.cell(row=1,column=num).value=="Comment":
            f_comment=False
        else:
            num=num+1
    n_cups=num-5 #the number of cups
    for i in range(2,max+1):
        if scope==None or i-1 in scope:
            if scope!=None and i-1 in scope:
                remove_pre_data(path,i-1)
            print("Trial"+str(i-1))
            number=PICTURE_NUMBER
            write=True #we only write the first frame into sheet2
            
            # get the position of cup
            for k in range(5,num):
                if sheet.cell(row=i,column=k).value!=None:
                    cup=eval(sheet.cell(row=i,column=k).value)
                    break
            frame_start=int(hmstoseconds(sheet.cell(row=i,column=2).value)/interval)+1
            frame_end=int(hmstoseconds(sheet.cell(row=i,column=3).value)/interval)+1 if not i==max else frameCount-1
            frame_index=frame_start
            if Trials!=None:
                trial=Trials[i-2] #trial is an object Trial
                rats=trial.getposition()
            else:#Trials==None, we need to find the postion of rat by ourselves
                #read through all the frames
                rats=[]
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                success, frame_un = video_capture.read()
                while success and frame_index<frame_end:
                    y,x=rat_detecter(frame_un)
                    if x!=None and y!=None:
                        rats.append([x,y,frame_index])
                    frame_index=frame_index+1
                    success, frame_un = video_capture.read()
            shortestdistance=[100000,None]
            previousdistance=100000
            for j in range(len(rats)):
                if rats[j][0]!=None and rats[j][1]!=None:
                # check if rat is inside the cup
                    #calculate the distance between the rat and the cup
                    distance=sqrt(int((rats[j][0]-cup[0])**2+(rats[j][1]-cup[1])**2))
                    if distance<shortestdistance[0]:
                        shortestdistance[0]=distance
                        shortestdistance[1]=rats[j][2]
                    if distance<=RAD+BOU and previousdistance>RAD+BOU:#find the frame that the rat enters the cup
                        video_capture.set(cv2.CAP_PROP_POS_FRAMES, rats[j][2])
                        #save this frame
                        success, frame = video_capture.read()
                        frame_done=prepare(frame)
                        if write==True:
                            sheet2.cell(row=i,column=1).value=int(rats[j][2])
                            write=False
                        if number!=0:
                            cv2.imwrite(path+"//"+str(i-1)+"_"+str(rats[j][2])+".jpg",frame_done)
                            number=number-1
                        #print(distance)
                    previousdistance=distance
                    
            if write==True: #if no frame is saved, write the closest frame
                #print("not find: "+str(shortestdistance[0]))
                sheet2.cell(row=i,column=1).value="find nothing at trial "+str(i-1)\
                    +" may check this frame "+str(shortestdistance[1])

    video_capture.release()
    convertformat(sheet2,fps)
    #save
    workbook.save(path2+"//"+name+"_data_a.xlsx")
    print("Done!")

def functionfive(path,name,framesplit,cupsinbox):
    """
    This function is to find the position of the rat in the video

    Parameter path: the path of the folder that contains the videos
    Precondition: path is a string

    Parameter name: the name of the video
    Precondition: name is a string

    Parameter cupsinbox: the position of cups in a box
    Precondition: cupsinbox is a list of a list of two coordinates-[[[x,y],[x,y],...],[[x,y],[x,y],...],...]

    Parameter framesplit: the end of a box
    Precondition: framesplit is a list of ints of a framenumber

    """
    path2=path+"//"+name
    video_capture = cv2.VideoCapture(path2+".mp4")
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps=video_capture.get(cv2.CAP_PROP_FPS)
    size=(int(width),int(height))
    frameCount=int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_write = cv2.VideoWriter(path2+"_helper.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    frame_index=0
    boxindicator=0
    success, frame_un = video_capture.read()
    while success:
        boxindicator=bisect.bisect(framesplit,frame_index)
        cup=cupsinbox[boxindicator]
        n_cups=len(cup)
        frame=frame_un.copy()
        y,x=rat_detecter(frame)
        if x!=None and y!=None:
            for i in range(n_cups):
                d=round(sqrt(int((x-cup[i][0])**2+(y-cup[i][1])**2)),3) #round them to three decimal places
                if i%2==0:
                    cv2.putText(frame_un,str(d),(5,40*(i//2+1)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                else:
                    cv2.putText(frame_un,str(d),(int(width-150),40*(i//2+1)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            # draw the position of the rat
            cv2.circle(frame_un,(int(x),int(y)),1,(0,0,255),2)
            
        # write this frame into the video
        video_write.write(frame_un)
            #cv2.imshow('img',frame_un)
            #cv2.waitKey(0)
            # read next frame
        frame_index=frame_index+1
        success, frame_un = video_capture.read()
        progress=frame_index
        if progress%(frameCount//DI)==0:
            print(str(progress//(frameCount//DI)*P)+"%")
    video_capture.release()
    print("Done!")

