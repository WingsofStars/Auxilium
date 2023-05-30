import os
import time
import pyttsx3
import threading

def startKDEConnectDaemon():
    os.system("echo Password | su -c \"/usr/lib/aarch64-linux-gnu/libexec/kdeconnectd -platform offscreen\" auxilium")


engine = pyttsx3.init()
#sets speech rate at a comfortable speed
engine.setProperty('rate', 150)
time.sleep(12) # needed to ensure that all other services are functioning and currently running before executing the welcome sound
OwnerNameFile = open("/home/auxilium/web-interface/src/assets/ownername.txt", "r")
volumeControlFile = open("/home/auxilium/important_text_files/volumecontrol.txt", "w")
ownerName = OwnerNameFile.readline()



os.system('amixer -c 1 -- set Playback 0dB')
os.system('amixer -c 1 -- set Speaker -14dB')
volumeControlFile.writelines(["-14", "\nfalse"])
engine.say("Hello " + ownerName)
engine.runAndWait()
os.system("echo Password | sudo -S systemctl start bluetooth.service")
OwnerNameFile.close()
volumeControlFile.close()
time.sleep(2)

def startWebServer():
    os.system('cd /home/auxilium/web-interface/ && echo Password |  sudo -S ng serve --host 0.0.0.0 --port 80')




thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()
webServerThread = threading.Thread(daemon=True, target= startWebServer).start()

try:
    thread1.raise_exception()
    thread1.join()
except:
    pass