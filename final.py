import cv2
import sys
import serial
from time import sleep
import math
from numpy import interp
from gtts import gTTS
import time, sys, os
from pygame import mixer
import tempfile
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import webbrowser














################simons code





#replace with the folder for image and sound you want to read from and store at
image_folder = "C:/Users/Scooter/OneDrive/ComputerScience/Physical Computing/Final Project/PhysicalComputing/images/"
sound_folder = "C:/Users/Scooter/OneDrive/ComputerScience/Physical Computing/Final Project/PhysicalComputing/images/"
sound_counter = 0


#initializing Clarifai (for recognition) and mixer (for sound playing)
#need to update key every 24 hrs or so

c_id = '7VPRtrQ2yIdMMw_3hexn3vza9pZo5m8HU6X_4Lxn'
c_key = 'c6Y-3qEX8qo4Vcw05e5Z2gqsEm5ntcg29vBB43fP'

app = ClarifaiApp(c_id, c_key)

model = app.models.get('c0c0ac362b03416da06ab3fa36fb58e3')

object_model = app.models.get('aaa03c23b3724a16a56b629203edc62c')


def getObjResult(imageName):
    imagePath = image_folder + imageName
    image = ClImage(file_obj = open(imagePath,'rb'))
    result = object_model.predict([image])
    obj = result['outputs'][0]['data']['concepts']
    return formObjSentence(obj)


def formObjSentence(obj):
    sent = obj[0]['name'] + " and " + obj[1]['name']
    return sent








def getResult(imageName):
    imagePath = image_folder + imageName
    image = ClImage(file_obj = open(imagePath,'rb'))
    result = model.predict([image])
    gender = result['outputs'][0]['data']['regions'][0]['data']['face']['gender_appearance']['concepts'][0]['name']
    age = result['outputs'][0]['data']['regions'][0]['data']['face']['age_appearance']['concepts'][0]['name']
    race = result['outputs'][0]['data']['regions'][0]['data']['face']['multicultural_appearance']['concepts'][0]['name']

    return formSentence(gender, age, race)


def formSentence(gender, age, race):
    sent = race
    if(gender == "feminine"):
        if(int(age) < 5):
            sent += " baby girl around "
        if(int(age) < 20):
            sent += " girl around "
        elif(int(age) < 40):
            sent += " lady around "
        else:
            sent += " woman around "
    else:
        if(int(age) < 5):
            sent += " baby boy around "
        if(int(age) < 20):
            sent += " boy around "
        elif(int(age) < 40):
            sent += " gentleman around "
        else:
            sent += " man around "
    sent += age
    return sent
        

def speakResult(result_text):
    global sound_counter
    os.chdir(sound_folder)
    tts = gTTS(text = result_text, lang = 'en', slow = False)
    name = "output" + str(sound_counter) + ".mp3"
    tts.save(name)
    
    soundPath = sound_folder + name
    webbrowser.open(soundPath)
    sound_counter += 1








#####################Scooters face tracking and serial code

#serial setup
ser = serial.Serial('COM3', 9600, timeout=.1)
##cascPath = sys.argv[1]

faceCascade = cv2.CascadeClassifier("faces.xml")

video_capture = cv2.VideoCapture(1)  #might need to change based on how many webcams there are

##just to map the numbers to a range
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

count = 0
timer = 300 #set the time interval for talkiing
while True:
    count = count + 1

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

        if (count>timer): ##do some talking!
            cv2.imwrite(image_folder+"EyeSee.jpg", frame)

            count = 0
            speakResult(getResult("EyeSee.jpg"))
    else:
        if (count>timer):
            cv2.imwrite(image_folder+"EyeSee.jpg", frame)

            count = 0
            speakResult(getObjResult("EyeSee.jpg"))
        

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





