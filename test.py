from gtts import gTTS
import time, sys, os
from pygame import mixer
import tempfile
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage




#replace with the folder for image and sound you want to read from and store at
image_folder = "C:/Users/Simon/AppData/Local/Programs/Python/Python35/"
sound_folder = "C:/Users/Simon/AppData/Local/Programs/Python/Python35/sounds/"
sound_counter = 0


#initializing Clarifai (for recognition) and mixer (for sound playing)
#need to update key every 24 hrs or so

app = ClarifaiApp("-M71CRq9OEBaXMNx7uCxq-7a30NXjgzSCCHTw-Pi", "WMr0tRBsNhwFcoJoXZy815Dk_yPkBDjvGHDhJ5rp")
face_model = app.models.get('c0c0ac362b03416da06ab3fa36fb58e3')

object_model = app.models.get('aaa03c23b3724a16a56b629203edc62c')

mixer.init()


def getObjResult(imageName):
    imagePath = image_folder + imageName
    image = ClImage(file_obj = open(imagePath,'rb'))
    result = object_model.predict([image])
    obj = result['outputs'][0]['data']['concepts']
    return formObjSentence(obj)


def formObjSentence(obj):
    sent = obj[0]['name'] + " and " + obj[1]['name']
    return sent





def getFaceResult(imageName):
    imagePath = image_folder + imageName
    image = ClImage(file_obj = open(imagePath,'rb'))
    result = face_model.predict([image])
    gender = result['outputs'][0]['data']['regions'][0]['data']['face']['gender_appearance']['concepts'][0]['name']
    age = result['outputs'][0]['data']['regions'][0]['data']['face']['age_appearance']['concepts'][0]['name']
    race = result['outputs'][0]['data']['regions'][0]['data']['face']['multicultural_appearance']['concepts'][0]['name']

    return formFaceSentence(gender, age, race)


def formFaceSentence(gender, age, race):
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
    mixer.init()
    soundPath = sound_folder + name
    sound = mixer.music.load(soundPath)
    mixer.music.play()
    sound_counter += 1



speakResult(getFaceResult("test2.jpg"))

time.sleep(5)

speakResult(getObjResult("test3.jpg"))

