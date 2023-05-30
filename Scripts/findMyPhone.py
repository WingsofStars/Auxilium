import threading
import os
import time

deviceNameFile = open("/home/auxilium/important_text_files/device_name.txt", "r")
deviceName = deviceNameFile.readline()


# def startKDEConnectDaemon():
#     os.system("echo Password | su -c \"/usr/lib/aarch64-linux-gnu/libexec/kdeconnectd -platform offscreen\" auxilium")



# stop_threads = False

# thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()


def ringPhone():
    os.system("echo Password | su -c 'kdeconnect-cli --ring --name " + deviceName +"' auxilium")


# time.sleep(5)
ringPhone()
# thread1.raise_exception()
# thread1.join()