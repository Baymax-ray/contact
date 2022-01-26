"""
objects
"""
class Currentobject(object):
    """
    The object currently recognized
    """
    # Attribute _x: the x-coordinate of the object
    # Invariant: _x is a number

    # Attribute _y: the y-coordinate of the object
    # Invariant: _y is a number

    # Attribute _r: the radius of the object
    # Invariant: _r is a number

    # Attribute _s: the state of the contuniuty of the object
    # Invariant: _s is True or False

    # Attribute _c: the state of the contact with the cup
    # Invariant: _c is True or False

    # Attribute _no: form the latency for the cup to disappear
    # Invariant: _no is a number

    def __init__ (self):
        """
        Create an empty object
        """
        self._x=0
        self._y=0
        self._r=0
        self._s=False
        self._c=False
        self._no=0
    
    def check_state(self,x,y,r):
        """
        change the state to false is the next object is too different in radius or in location & return the state
        """
        if abs(r-self._r)>10:
            self._s=False
        elif ((x-self._x)**2+(y-self._y)**2)**0.5>self._r:
            self._s=False
        else:
            self._s=True
        return self._s

    def check_delay(self):
        """
        change the object to empty when it reaches the latency
        """
        if self._no==60:
            self._x=0
            self._y=0
            self._r=0
            self._s=False
            self._c=False
            self._no=0

    def noadd(self):
        """
        add one to _no
        """
        self._no=self._no+1

    def noclear(self):
        """
        set _no to 0
        """
        self._no=0

    def changestate(self,state):
        """
        change the state to true

        Parameter state: the state to change
        Precondition: state is True or False
        """
        self._s=state

    def getlocation(self):
        """
        return the location in a list of [x,y]
        """
        return [self._x,self._y]
    
    def getradius(self):
        """
        return the radius
        """
        return self._r
    
    def getstate(self):
        """
        return the state
        """
        return self._s

    def getcontact(self):
        """
        return the contact
        """
        return self._c

    def changecontact(self):
        """
        change the contact
        """
        self._c=not self._c

    def update(self,l):
        """
        change the current object

        Parameter l: the information about the object---[x,y,r]
        Precondition: l is a list
        """
        self._x=l[0]
        self._y=l[1]
        self._r=l[2]
        self._s=True
        self._c=False
    
class Potentialobject(object):
    """
    All the potential objects
    """
    # Attribute _l: all potential objects
    # Invariant: _l is a list

    def __init__ (self):
         """
         create an empty list
         """
         self._l=[]
    
    def add(self,c):
        """
        add a new potential list

        Parameter c: the information about the object---[x,y,r]
        Precondition: c is a list
        """
        r=self.selfcheck_helper(c)
        if r==False or r==None:
            c.append(0)
            self._l.append(c)
        else:
            n=self._l.index(r)
            self._l[n][3]=self._l[n][3]+1
            #print("num"+str(self._l[n][3]))
    
    def check(self):
        """
        return the object if it repeats 5 times
        return false if there is no such object
        """
        for p in self._l:
            if p[3]==5:
                self.clear()
                return p
        return False

    def clear(self):
        """
        clear the list
        """
        self._l=[]

    def selfcheck_helper(self,c):
        """
        help to check if c can be considered in self
        return false if c is new

        Parameter c: the information about the object---[x,y,r]
        Precondition: c is a list
        """
        for al in self._l:
            if abs(al[2]-c[2])<10 and ((al[0]-c[0])**2+(al[1]-c[1])**2)**0.5<al[2]/2:
                return al
        return False
    
