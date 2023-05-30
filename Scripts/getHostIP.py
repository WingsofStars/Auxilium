import subprocess

def main():
    process = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
    IP = (process.stdout).decode() 
    newIP = ""
    for i in IP:
        if i == ".":
            newIP += " dot "
        newIP += i + " "
    return(newIP)
