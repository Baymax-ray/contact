"""
constant

# Jiarui Fang (jf659@cornell.edu)
# Feb 12, 2022
"""
# constant
N=100 #how many pixels to examine in each frame
A=2 #the multiplier for contrast
L=5 #the number of frames that the video is behind the txt in timeline, if it is negative, error may occur
DB=9 # the length of the square to check lightness inside the circle
sens=20 #the lower it is, the more likely to find 'circle'
P=5 #progress interval
DI=100/P
LATE_DISAPPEAR=30 #how much frames it take for a cup to disappear
GAP=9 #the sec of the smallest interval between to contact
cont=5 #existing for 5 frames, it can be recognize as a real object
DISTANCE=[15,24] #the range of distance between rat and object that will be considered as contact, two number can be equal but the second should not be larger
RAD=16 #the experiential radius of the object
S=20 #the standard of red and green
V=10 #the allowed variance of brightness
BOU=28-RAD #the bound to be considered as "contact"
PICTURE_NUMBER=3 #the number of pictures to be taken for each trial