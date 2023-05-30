import numpy

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
from word2number import w2n
import sys
import tensorflow as tf
from tensorflow import keras



invalid_responses = ["Please rephrase that.", "That is weird, I do not recognize that.", "Try again later.", "Could not come up with a response, try again."]

commandIntents = ["SMS", "EMAIL", "MUSIC", "NEWS", "FINDPHONE"]

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


training = numpy.array(training)
output = numpy.array(output)


def loadModel(model_name):
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

    return numpy.array([bag])




def debugchat(model_name, user_input):
    # Valid model check, does it exist?
    print("Test Debug Chat")
    model = loadModel(model_name)
    print("Model loaded")
    if (type(model) is str): return model
    
    results = model.predict([bag_of_words(user_input, words)])[0]

    results_index = numpy.argmax(results)
    intent = labels[results_index]
    print("Confidence:" + str(results[results_index]))
    print("Intent: " + intent)
    if results[results_index] > 0.60:
        for tg in data["intents"]:
            if tg["intent"] == intent:
                if intent in commandIntents:
                    pass
                    #put in command responses
                    # if intent == "SMS":
                    #     command = user_input.replace(" ","")
                    #     number = re.search(r"[0-9]{10}",command)

                    #     if number != None:
                    #         recordMessageAndSend(number)

                    #     else:
                    #         engine.say("What's the number you want to send the text to")
                    #         engine.runAndWait()
                    #         startRecording(8)
                    #         os.system('aplay ' + PATH_TO_FILE)
                    #         destinationNumber = sendRequestandTranscribe(PATH_TO_FILE)
                    #         print(destinationNumber)
                    #         PhoneNumArr = destinationNumber.split(" ")
                    #         destinationNumberNums = ""
                    #         for num in PhoneNumArr:
                    #             destinationNumberNums = destinationNumberNums + str(w2n.word_to_num(num))
                    #         print(destinationNumberNums)
                    #         destinationNumberNums = str(destinationNumberNums).replace(" ","")
                    #         number = re.match(r"[0-9]{10}", destinationNumberNums).group(0)
                    #         print(number)
                    #         if number != None:
                    #             recordMessageAndSend(number)
                    #         else:
                    #             engine.say("Couldn't hear the number")
                    #             engine.runAndWait()
                    #     pass
                    # elif intent == "EMAIL":
                    #     #code to ask for message and number
                    #     pass
                    # elif intent == "MUSIC":
                    #     #code to ask for message and number
                    #     pass
                    
                    # elif intent == "NEWS":
                    #     #code to ask for message and number
                    #     pass
                    # pass
                else:
                    responses = tg["responses"]
                    print(f"{random.choice(responses)}")
    else:
        #say dont understand
        print(f"{random.choice(invalid_responses)}")



while True:
    uinput = input(":")
    debugchat("auxilium", uinput)