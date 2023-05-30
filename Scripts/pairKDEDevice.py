import subprocess
import threading
import os
import sys
import time


def startKDEConnectDaemon():
    subprocess = subprocess.run()
    os.system("/usr/lib/arm-linux-gnueabihf/libexec/kdeconnectd -platform offscreen")





popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd

# stop_threads = False

thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()



def sendSMS():
    os.system("kdeconnect-cli --name \"" + deviceName +"\" --send-sms \"" + sys.argv[1] +"\" --destination "+sys.argv[2])

time.sleep(5)

sendSMS()