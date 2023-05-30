
#this code precedes imports to indicate that the system is busy importing modules and loading data models
import board
import adafruit_dotstar

#set up for the LED's
DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6
dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.1)
for i in range(3):
    dots[i] = (18, 16, 78)



#set up for button push
from digitalio import DigitalInOut, Direction, Pull
button = DigitalInOut(board.D17)
button.direction = Direction.INPUT
button.pull = Pull.UP



import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
from deepgram import Deepgram
import json
import pyttsx3
import time as timer

import random
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import sys
import re
import pyttsx3
from scipy.io.wavfile import write
from deepgram import Deepgram
import sounddevice as sd
import os

import sys
import tensorflow as tf
from tensorflow import keras


AssistantFile = open("/home/auxilium/web-interface/src/assets/assistant_name.txt", "r")
assistant_name = AssistantFile.readline().lower()


#following functions used to show that the system is busy or not by using leds on the voice bonnet
#to show the system is busy, then execute this function
def ledsON(brightness = 0.1):
    dots.brightness= brightness
    dots.show()

#to show the system is idle, then execute this function
def ledsOFF():
    dots.brightness= 0.0
    dots.show()



#import subscripts
import commandProcessing

#timer is set to ensure that the current core is clear
timer.sleep(1.5)

#Load NLP Model and necessary data


with open("Intent.json") as file:
    data = json.load(file)

stemmer = LancasterStemmer()

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["intent"])

    if intent["intent"] not in labels:
        labels.append(intent["intent"])

words = [stemmer.stem(w.lower()) for w in words if w != ("?" or "!")]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = np.array(training)
output = np.array(output)


#Load model and create word bag for model
def loadModel(model_name="auxilium"):
    try:
        model = keras.models.load_model('KerasModels/' + model_name + '.h5')
        return model
    except:
        #model not found exception
        print("model: " + model_name + " could not be found")
        return "model: " + model_name + " could not be found"

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array([bag])

#LOAD MODEL
MODEL = loadModel()


#Initiallize Text To Speech Engine
engine = pyttsx3.init()
#Sets speech rate at a comfortable speed
engine.setProperty('rate', 125)



#TO DO: make environ variable
API_KEY = '619838795b88f3e51cda87cdb4b7aa87ab35cdf2'

PATH_TO_FILE = '/home/auxilium/important_sound_files/output.wav'
MIMETYPE = 'audio/wav'


#Set up sound device so it can monitor and record audio input
fs = 16000 
sd.default.samplerate = fs
sd.default.channels = 2
volume_norm = 0

#Call back that monitors audio input volume thresh hold
def audio_callback(indata, frames, time, status):
   global count
   count = count + 1
   global volume_norm
   volume_norm = np.linalg.norm(indata) * 10
   






def startRecording(time):
    #show that the system is recording input
    ledsON() 
    file = sd.rec(int(time*16000))
    sd.wait()
    write(PATH_TO_FILE, fs, file)
    #show that the system is done recording
    ledsOFF()
    


#Transcibes recorded audio at the filepath - really fast and
def sendRequestandTranscribe(filepath):
    ledsON()
    # Initializes the Deepgram SDK
    dg_client = Deepgram(API_KEY)
    
    with open(filepath, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": False, "model": "nova", "language": "en-US" }
        print("transcribing. . . \n")
        response = dg_client.transcription.sync_prerecorded(source, options)
        r = (json.dumps(response, indent=4))
        responseJSON = json.loads(r)
        ledsOFF()
        return responseJSON["results"]["channels"][0]["alternatives"][0]["transcript"]
    

#show system is idle
ledsOFF()

#stream that uses the audio callback continuously and pauses recording audio input to run command process
stream = sd.InputStream(samplerate=16000, callback=audio_callback, channels=2)
with stream:
    count = 0
    while True:
        #DEBUG: Average volume level should be around 3 and count resets after every recording. If the background process records every fifteen counts, something is wrong and system must be rebooted
        # print("Volume:" + str(volume_norm))
        # print("\ncount: " + str(count))

        if not button.value:
            commandProcessing.cancelAllProcesses()
            
        if(volume_norm > 17 and count > 15):
                print("Trigger Volume:" + str(volume_norm))
                startRecording(3.5)
                
                try:
                    response = sendRequestandTranscribe(PATH_TO_FILE)
                    if response != '':
                        #to debug uncomment the commented code below
                        print(response)
                        if "oxy" in response.lower() or "ilium" in response.lower() or "oxi" in response.lower() or "sea" in response.lower() or assistant_name.lower() in response.lower():
                            stream.stop()
                            engine.say("What would you like me to do?")
                            engine.runAndWait()
                            startRecording(8)
                            command = sendRequestandTranscribe(PATH_TO_FILE)
                            print(command)
                            if command != '':
                                # Input, TTSEngine, Model, bag_of_words, labels, data, numpy
                                commandProcessing.processInput(command, engine, MODEL, bag_of_words(command, words), labels, data, np)
                                # os.system("python3 nlp.py \""+ command +"\"")
                                  
                except:
                    pass
                
                timer.sleep(0.1)
                count = 0
                stream.start()
                