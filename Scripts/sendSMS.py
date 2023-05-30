import threading
import os
import sys
import time

deviceNameFile = open("/home/auxilium/important_text_files/device_name.txt", "r")
deviceName = deviceNameFile.readline()


# def startKDEConnectDaemon():
#     os.system("echo Password | su -c \"/usr/lib/aarch64-linux-gnu/libexec/kdeconnectd -platform offscreen\" auxilium")



# # stop_threads = False

# thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()


def sendSMS():
    sys.argv[1]=sys.argv[1].replace("\'","")
    print(sys.argv[1])
    os.system('''echo Password | su -c 'kdeconnect-cli --name \"''' + deviceName +'''\" --send-sms \"''' + sys.argv[1] +'''\" --destination \"'''+sys.argv[2]+'''\"' auxilium''')

# time.sleep(7)

sendSMS()
# thread1.raise_exception()
# thread1.join()
# "echo <password> | su -c `kdeconnect-cli --name \"<deviceName>\" --send-sms \"<message>\" --destination \"<destination>\"` <user>"