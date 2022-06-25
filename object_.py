"""
objects
"""
from constant import *
import copy

class Trial(object):
    """
    The trial
    """
    # Attribute _position: the position of the rat
    # Invariant: _position is a list of [x,y,frame], this fram is the frame in video

    # Attribut _t: the number of trial this frame belongs to
    # Invariant: _t is a number

    # Attribute _o: the object in this frame
    # Invariant: _o is a number or None

    # Attribute _p: the potential object in this frame
    # Invariant: _p is a list of positive int or None

    def __init__ (self,t):
        """
        Create an empty frame
        """
        self._position=[]
        self._t=t
        self._o=None
        self._p=[]

    def getposition(self):
        """
        return the position of the rat
        """
        return self._position
    
    def gettrial(self):
        """
        return the trial number
        """
        return self._t

    def getobject(self):
        """
        return the object in this frame
        """
        return self._o

    def setobject(self,o):
        """
        set the object in this frame

        Parameter o: the object to set
        Precondition: o is a number or None
        """
        self._o=o

    def addposition(self,x,y,f):
        """
        add the position of the rat

        Parameter x: the x position
        Parameter y: the y position
        Parameter f: the frame number in video
        Precondition: x,y,t are numbers
        """
        self._position.append([x,y,f])
    
    def addpotential(self,p):
        """
        add the potential object in this frame

        Parameter p: the potential object to add
        Precondition: p is a positive int or None
        """
        self._p.append(p)

    def compute_o(self,cupscount):
        """
        compute the object in this frame
        if there is no potential object in this frame, set _o to be None
        if there is 30 more in a potential object, set _o to be that object
        if there is no 30 more of any potential object, set _o to be None

        Parameter cupscount: the number of cups in the frame
        Precondition: cupscount is a number
        """
        #print("cupscount:",cupscount)
        if len(self._p)==0:
            self.setobject(None)
        else:
            count=[]
            for i in range(cupscount):
                count.append(self._p.count(i+1)) #count the number of each potential object
                #print(count)
            self.test=copy.deepcopy(count)
            a=max(count)
            a_index=count.index(a)
            if len(count)==1:
                self.setobject(a_index+1)
            else:
                count_2=count[:a_index]+count[a_index+1:] #remove the max
                b=max(count_2)
                if a-b>30:
                    self.setobject(a_index+1)
                else:
                    self.setobject(None)