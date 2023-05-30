import os
import threading

def startKDEConnectDaemon():
    os.system("/usr/lib/aarch64-linux-gnu/libexec/kdeconnectd -platform offscreen")
try:
    thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()
    thread1.raise_exception()
    thread1.join()
except:
    pass
def start():
    thread1 = threading.Thread(target=startKDEConnectDaemon, daemon=True).start()
    thread1.raise_exception()
    thread1.join()