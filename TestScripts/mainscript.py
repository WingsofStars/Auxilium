import sounddevice as sd
import numpy as np
import pyaudio
import wave
import os
from scipy.io.wavfile import write

fs = 16000 
sd.default.samplerate = fs
sd.default.channels = 2

def audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   print(volume_norm)
   if(volume_norm > 50):
     iHeardYou()
    #  startRecording()
     startRecordingNew()
     os.system('sudo aplay /home/auxilium/important_sound_files/output.wav')
     

def startRecordingNew():
   file = sd.rec(int(2.5*16000))
   sd.wait()
   write("/home/auxilium/important_sound_files/output.wav",fs, file)
   


def iHeardYou():
   print("I heard You")

#start processing the audio


# too slow
# def startRecording():
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 2
#     RATE = 16000
#     RECORD_SECONDS = 2.5
#     WAVE_OUTPUT_FILENAME = "/home/auxilium/important_sound_files/output.wav"

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)



#     print("* recording")

#     frames = []

#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK,exception_on_overflow = False)
#         frames.append(data)

#     print("* done recording")


#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
#     os.system('sudo aplay /home/auxilium/important_sound_files/output.wav')

duration = 120

stream = sd.InputStream(callback=audio_callback)
with stream:
   sd.sleep(duration * 1000)