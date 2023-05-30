import os
import sys


def main(multiplier=1):
    volumeControlFile = open("/home/auxilium/important_text_files/volumecontrol.txt", "r+")
    volumeargs = volumeControlFile.readlines()

    if(float(volumeargs[0]) < 6 ):
        volumeargs[0] = str(float(volumeargs[0]) + 2*multiplier)
        if float(volumeargs[0]) > 6:
            volumeargs[0] = "6"
        os.system('amixer -c 1 -- set Speaker ' + str(volumeargs[0])+'dB')
        with open("/home/auxilium/important_text_files/volumecontrol.txt", "w") as file:
            file.writelines([volumeargs[0], "\n"+volumeargs[1]])
    #make signal noise


    volumeControlFile.close()