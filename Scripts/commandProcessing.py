from word2number import w2n
import sys
import re
import os
from scipy.io.wavfile import write
from deepgram import Deepgram
import sounddevice as sd
import random
import json
import board
import adafruit_dotstar
from multiprocessing import current_process
from multiprocessing import Process
import multiprocessing as MP

#set up for the LED's
DOTSTAR_DATA = board.D5
DOTSTAR_CLOCK = board.D6
dots = adafruit_dotstar.DotStar(DOTSTAR_CLOCK, DOTSTAR_DATA, 3, brightness=0.1)
for i in range(3):
    dots[i] = (18, 16, 78)

#following functions used to show that the system is busy or not by using leds on the voice bonnet
#to show the system is busy, then execute this function
def ledsON():
    dots.brightness= 0.1
    dots.show()

#to show the system is idle, then execute this function
def ledsOFF():
    dots.brightness= 0.0
    dots.show()


invalid_responses = ["Please rephrase that.", "That is weird, I do not recognize that.", "Try again later.", "Could not come up with a response, try again."]

commandIntents = ["SMS", "EMAIL", "MUSIC", "NEWS", "FINDPHONE", "TimeQuery", "DATE", "VOLUMEUP", "VOLUMEDOWN", "VOLUMEUPBY", "VOLUMEDOWNBY", "REBOOT", "IP", "STOPNEWSANDMUSIC", "WEATHER", "MATHS", "NOTHING"]



import getDate
import getTime
import volumedown
import volumeup
import getHostIP
import getForecast




#Set up
API_KEY = '619838795b88f3e51cda87cdb4b7aa87ab35cdf2'

PATH_TO_FILE = '/home/auxilium/important_sound_files/output.wav'
MIMETYPE = 'audio/wav'



fs = 16000 
sd.default.samplerate = fs
sd.default.channels = 2
volume_norm = 0


#necessary functions
def recordMessageAndSend(number, TTSEngine):
    try:
        #What would you like to say
        TTSEngine.say("What would you like the message to say?")
        TTSEngine.runAndWait()
        startRecording(10)
        message = sendRequestandTranscribe(PATH_TO_FILE, True)
        print(message)
        os.system("python3 /home/auxilium/sendSMS.py \"" + message + "\" " + number)
        
        TTSEngine.say("Message Sent.")
        TTSEngine.runAndWait()
    except:
        TTSEngine.say("Message Could Not Be Sent.")
        TTSEngine.runAndWait()

def startRecording(time):
    ledsON()
    file = sd.rec(int(time*16000))
    sd.wait()
    write(PATH_TO_FILE, fs, file)
    ledsOFF()

def sendRequestandTranscribe(filepath, punctuate = False):
    print("Transcribing")
    # Initializes the Deepgram SDK
    dg_client = Deepgram(API_KEY)
    
    with open(filepath, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": punctuate, "model": "nova", "language": "en-US" }
    
        print('Requesting transcript...')
        print('Your file may take up to a couple minutes to process.')
        print('While you wait, did you know that Deepgram accepts over 40 audio file formats? Even MP4s.')
        print('To learn more about customizing your transcripts check out developers.deepgram.com')
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        r = (json.dumps(response, indent=4))
        responseJSON = json.loads(r)

        print("Test3")
        transcription = responseJSON["results"]["channels"][0]["alternatives"][0]["transcript"]
                # print(transcription)
        return transcription







def playMusicBackgroundTask(musicIdentifier="music"):
    os.system('youtube-viewer --no-video --quiet --min-seconds=1 --no-interactive --autoplay --std-input=1 "'+ musicIdentifier +'" --category="Music"')

def playNewsBackgroundTask():
    os.system('youtube-viewer --no-video --quiet --min-seconds=1 --no-interactive --autoplay --std-input=1 "US News Today" --category="News & Politics"')

#daemon declaration



def cancelAllProcesses():
    try:
        newsDaemon.terminate()
    except:
        pass
    try:
        musicDaemon.terminate()
    except:
        pass

    os.system("killall -9 mpv")
    
    

def processInput( Input, TTSEngine, Model, bag_of_words, labels, data, numpy):
    # Valid Model check, does it exist?
    print("Test Debug Chat")
    print("Model loaded")
    if (type(Model) is str): return Model
    
    results = Model.predict([bag_of_words])[0]

    results_index = numpy.argmax(results)
    intent = labels[results_index]
    print("Confidence:" + str(results[results_index]))
    if results[results_index] > 0.42:
        for tg in data["intents"]:
            if tg["intent"] == intent:
                if intent in commandIntents:
                    #put in command responses
                    if intent == "SMS":
                        commandArr = Input.split(" ")
                        commandConverted = ""
                        for word in commandArr:
                                try:
                                    commandConverted = commandConverted + str(w2n.word_to_num(word))
                                except:
                                    commandConverted = commandConverted + word
                        print(commandConverted)
                        commandConverted = commandConverted.replace(" ", "")
                        try:
                            number = re.search(r"\d{10}",commandConverted).group(0)
                            print("BAD if no number")
                            if number != None:
                                print(number)
                                recordMessageAndSend(number, TTSEngine)
                        except: 
                            

                        

                        
                            TTSEngine.say("What's the number you want to send the text to")
                            TTSEngine.runAndWait()
                            startRecording(8)
                            # os.system('aplay ' + PATH_TO_FILE)
                            destinationNumber = sendRequestandTranscribe(PATH_TO_FILE)
                            print(destinationNumber)
                            PhoneNumArr = destinationNumber.split(" ")
                            destinationNumberNums = ""
                            for num in PhoneNumArr:
                                try:
                                    destinationNumberNums = destinationNumberNums + str(w2n.word_to_num(num))
                                except:
                                    pass

                            print(destinationNumberNums)
                            destinationNumberNums = str(destinationNumberNums).replace(" ","")
                            print("Test 1")
                            try:
                                number = re.match(r"[0-9]{10}", destinationNumberNums).group(0)
                                if number != None:
                                    print("Test 2")
                                    print(number)
                                    recordMessageAndSend(number, TTSEngine)
                                else:
                                    TTSEngine.say("Couldn't hear the number")
                                    TTSEngine.runAndWait()
                            except:
                                TTSEngine.say(destinationNumberNums + " is not a usable number")
                                TTSEngine.runAndWait()
                            
                            
                        pass
                    elif intent == "EMAIL":
                        #code to ask for message and number
                        pass
                    elif intent == "MUSIC":
                        commands = Input.lower().replace("can you play some", "")
                        commands = commands.lower().replace("can you place some", "")
                        commands = commands.lower().replace("can you play", "")
                        commands = commands.lower().replace("can you place", "")
                        commands = commands.lower().replace("play some", "")
                        commands = commands.lower().replace("play", "")
                        commands = commands.lower().replace("place some", "")
                        commands = commands.lower().replace("place", "")
                        commands = commands.lower().replace("please some", "")
                        commands = commands.lower().replace("please", "")
                        musicIdentifier = commands.replace(" ", "")
                        print(musicIdentifier)
                        if musicIdentifier == "music" or musicIdentifier == "somemusic":
                            TTSEngine.say("is there anything specific that you would like to listen to?")
                            TTSEngine.runAndWait()
                            startRecording(5)
                            input = sendRequestandTranscribe(PATH_TO_FILE)
                            print(input)
                            yesWords = ["yeah", "yea", "sure", "yes", "there is"]
                            noWords = ["no", "naw", "not really", "not right now", "nope", "nah", "there isn't", "there is not"]
                            if any(word in input for word in yesWords):
                                TTSEngine.say("What would you like to listen to?")
                                TTSEngine.runAndWait()
                                startRecording(6)
                                musicRequest = sendRequestandTranscribe(PATH_TO_FILE)
                                
                                musicRequest = musicRequest.replace("how about some", "")
                                musicRequest = musicRequest.replace("what about some", "")
                                musicRequest = musicRequest.replace("how about", "")
                                musicRequest = musicRequest.replace("what about", "")
                                musicRequest = musicRequest.replace("play some", "")
                                musicRequest = musicRequest.replace("place some", "")
                                musicRequestArr = musicRequest.split(" ")
                                if musicRequestArr[0] == "play":
                                    musicRequestArr.pop(0)
                                finalRequest = "" 
                                for words in musicRequestArr:
                                    finalRequest = finalRequest + words +" "
                                print(finalRequest)
                                musicDaemon = Process(daemon=True, target=playMusicBackgroundTask, args=(finalRequest,))
                                musicDaemon.start()
                                TTSEngine.say("Now playing " + finalRequest)
                                TTSEngine.runAndWait()
                            
                        
                                pass
                            elif any(word in input for word in noWords):
                                musicDaemon = Process(daemon=True, target=playMusicBackgroundTask, args=(musicIdentifier,))
                                
                                musicDaemon.start()
                                TTSEngine.say("Now playing " + musicIdentifier)
                                TTSEngine.runAndWait()
                                pass
                            else:
                                
                                input = input.replace("how about some", "")
                                input = input.replace("what about some", "")
                                input = input.replace("how about", "")
                                input = input.replace("what about", "")
                                input = input.replace("play some", "")
                                input = input.replace("place some", "")
                                musicRequestArr = input.split(" ")
                                if musicRequestArr[0] == "play":
                                    musicRequestArr.pop(0)
                                finalRequest = "" 
                                for words in musicRequestArr:
                                    finalRequest = finalRequest + words +" "
                                print(finalRequest)
                                musicDaemon = Process(daemon=True, target=playMusicBackgroundTask, args=(finalRequest,))
                                musicDaemon.start()
                                TTSEngine.say("Now playing " + finalRequest)
                                TTSEngine.runAndWait()
                                pass
                        else:
                                musicDaemon = Process(daemon=True, target=playMusicBackgroundTask, args=(musicIdentifier,))
                            
                                musicDaemon.start()
                                TTSEngine.say("Now playing " + musicIdentifier)
                                TTSEngine.runAndWait()
                                pass
                    
                    elif intent == "NEWS":
                        newsDaemon = Process(daemon=True, target=playNewsBackgroundTask)
                        newsDaemon.start()
                        #code to ask for message and number
                        pass
                    elif intent == "STOPNEWSANDMUSIC":
                        cancelAllProcesses()
                        #code to ask for message and number
                        pass
                    elif intent == "FINDPHONE":
                        TTSEngine.say("Ringing Phone")
                        TTSEngine.runAndWait()
                        os.system("python3 /home/auxilium/findMyPhone.py")
                    elif intent == "REBOOT":
                        os.system("echo Password | sudo -S reboot")
                    elif intent == "VOLUMEUP":
                        volumeup.main()
                    elif intent == "VOLUMEDOWN":
                        volumedown.main()
                    elif intent == "VOLUMEUPBY":
                        commandArr = Input.split(" ")
                        commandConverted = ""
                        for word in commandArr:
                                try:
                                    commandConverted = commandConverted + str(w2n.word_to_num(word))
                                except:
                                    commandConverted = commandConverted + word
                        print(commandConverted)
                        number = re.search(r"(?:[1-9]|0[1-9]|10)$",commandConverted).group(0)
                        print(number)
                        volumeup.main(int(number))
                    elif intent == "VOLUMEDOWNBY":
                        commandArr = Input.split(" ")
                        commandConverted = ""
                        for word in commandArr:
                                try:
                                    commandConverted = commandConverted + str(w2n.word_to_num(word))
                                except:
                                    commandConverted = commandConverted + word
                        print(commandConverted)
                        number = re.search(r"(?:[1-9]|0[1-9]|10)$",commandConverted).group(0)
                        print(number)
                        volumedown.main(int(number))
                    elif intent == "TimeQuery":
                        TTSEngine.say(getTime.main())
                        TTSEngine.runAndWait()
                    elif intent == "DATE":
                        TTSEngine.say(getDate.main())
                        TTSEngine.runAndWait()
                    elif intent == "NOTHING":
                        pass
                    elif intent == "WEATHER":
                        locationFile = open("/home/auxilium/web-interface/src/assets/zipcode.txt", "r")
                        location = locationFile.readline()
                        inputarr = Input.lower().split(" ")
                        weatherString =""
                        if "tomorrow" in inputarr:
                            weatherString = getForecast.main(location, "tomorrow")
                        else:
                            weatherString = getForecast.main(location)
                        TTSEngine.say(weatherString)
                        TTSEngine.runAndWait()
                    elif intent == "IP":
                        TTSEngine.say("The I P addess is " + getHostIP.main())
                        TTSEngine.runAndWait()
                        
                else:
                    responses = tg["responses"]
                
                    TTSEngine.say( f"{random.choice(responses)}")
                    TTSEngine.runAndWait()
    else:
        #say dont understand
        TTSEngine.say(f"{random.choice(invalid_responses)}")
        TTSEngine.runAndWait()

