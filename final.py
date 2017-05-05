import cv2
import sys
import serial
from time import sleep
import math
from numpy import interp
#serial setup
ser = serial.Serial('COM3', 9600, timeout=.1)
##cascPath = sys.argv[1]

faceCascade = cv2.CascadeClassifier("faces.xml")

video_capture = cv2.VideoCapture(0)  #might need to change based on how many webcams there are

##just to map the numbers to a range
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE #had to change this for newer python version
    )

    ##lets grab our values from image
    x=0;
    y=0;
    w=0;
    h=0;
    if (type(faces) != tuple): #only if we have a face do we do anything
        x = faces[0,0]
        y = faces[0,1]
        w = faces[0,2]
        h = faces[0,3]
        
        

    # Draw a rectangle around the face
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.circle(frame, (int(math.ceil(x+(w/2))),int(math.ceil(y+h/2))), 5, (0,255,0),2)
    cv2.circle(frame,(320,240),4,(255,0,0),2) #center

   
    
    # end the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ##this is where i will put serial out to arduino to tell us where to move
    ## image is 480 by 640 pixels

    center = (320,240)
    xCenter = 320;
    error = 30
    
    x = math.floor(x+(w/2))
    y = math.floor(y+(h/2)) #center of face x,y


    dist = (x-center[0], y-center[1])
   	
    maxX = 180;
    minX = 95;
    midX = 137;
    ##########new stuff here#############
    faceVal = scale(x, (0,640),(maxX,minX))
    if (x == 0):
        faceVal = midX;
    serVal = 'y'+ str(int(faceVal))
    ser.write(bytes(serVal,'utf-8'))


    print (ser.readline())


    ##draw everything#########
    
    cv2.line(frame,center,(x,y),(0,0,255),3)

    # Display the resulting frame
    cv2.imshow('Video', frame)


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

