import os
import time
OwnerNameFile = open("/home/auxilium/important_text_files/ownername.txt", "r")
volumeControlFile = open("/home/auxilium/important_text_files/volumecontrol.txt", "w")
ownerName = OwnerNameFile.readline()

time.sleep(10) # needed to ensure that all other services are functioning and currently running before executing the welcome sound

os.system('amixer -c 1 --set Playback 0dB')
os.system('amixer -c 1 -- set Speaker -14dB')
volumeControlFile.write("-14dB\nfalse")
os.system('gtts-cli "Hello ' + ownerName + '" | mpg123 -')
OwnerNameFile.close()
volumeControlFile.close()