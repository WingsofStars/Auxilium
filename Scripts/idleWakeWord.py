import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
from deepgram import Deepgram
import json
import pyttsx3
import time as timer
timer.sleep(7)

engine = pyttsx3.init()
#sets speech rate at a comfortable speed
engine.setProperty('rate', 125)

#make environ variable
API_KEY = '619838795b88f3e51cda87cdb4b7aa87ab35cdf2'

PATH_TO_FILE = '/home/auxilium/important_sound_files/output.wav'
MIMETYPE = 'audio/wav'



fs = 16000 
sd.default.samplerate = fs
sd.default.channels = 2
volume_norm = 0

def audio_callback(indata, frames, time, status):
   global count
   count = count + 1
   global volume_norm
   volume_norm = np.linalg.norm(indata) * 10
#    print(volume_norm)
   






def startRecording(time):
    file = sd.rec(int(time*16000))
    sd.wait()
    write(PATH_TO_FILE, fs, file)



def sendRequestandTranscribe(filepath):
    # Initializes the Deepgram SDK
    dg_client = Deepgram(API_KEY)
    
    with open(filepath, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": False, "model": "nova", "language": "en-US" }
    
        # print('Requesting transcript...')
        # print('Your file may take up to a couple minutes to process.')
        # print('While you wait, did you know that Deepgram accepts over 40 audio file formats? Even MP4s.')
        # print('To learn more about customizing your transcripts check out developers.deepgram.com')
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        r = (json.dumps(response, indent=4))
        responseJSON = json.loads(r)
        return responseJSON["results"]["channels"][0]["alternatives"][0]["transcript"]
    

# duration = 30


stream = sd.InputStream(samplerate=16000, callback=audio_callback, channels=2)
with stream:
    count = 0
    while True:
        if(volume_norm > 14 and count > 15):
                startRecording(3.5)
                # os.system('aplay ' + PATH_TO_FILE)
                try:
                    response = sendRequestandTranscribe(PATH_TO_FILE)
                    if response != '':
                        # print(transcription)
                        if "oxy" in response.lower() or "ilium" in response.lower() or "oxi" in response.lower():
                            stream.stop()
                            engine.say("What would you like me to do?")
                            engine.runAndWait()
                            startRecording(8)
                            command = sendRequestandTranscribe(PATH_TO_FILE)
                            if command != '':
                                os.system("python3 nlp.py \""+ command +"\"")
                            
                        
                    
                except:
                    pass

                timer.sleep(0.1)
                count = 0
                stream.start()
                