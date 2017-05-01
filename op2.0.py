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
    error = 30
    
    x = math.floor(x+(w/2))
    y = math.floor(y+(h/2)) #center of face x,y


    dist = (x-center[0], y-center[1])
   		
   
   	####### if y dist is less than the error and not at top left corner
    if (math.fabs(dist[1])>error and math.fabs(dist[1]) != 240):
    	valy = -1 * math.ceil(interp(dist[1],[-240,240], [-5,5]))
    	tmp = 'y'+str(valy)
    	ser.write(bytes(tmp, 'utf-8'))

    if(math.fabs(dist[0])>(error+35) and math.fabs(dist[0]) != 320):

    	if(dist[0]<0):
    		ser.write(b'r')# send it right
    		sleep(.05)
    		
    	if(dist[0]>0):
    		ser.write(b'l')# send it left
    		sleep(.05)


    print (ser.readline())


    ##draw everything#########
    
    cv2.line(frame,center,(x,y),(0,0,255),3)

    # Display the resulting frame
    cv2.imshow('Video', frame)


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()