#! /usr/bin/env python2

# Android Music Sync
# Python 2.7
# Modules Required - mutagen

# Source - https://github.com/wilspi/AndroidMusicSync
# Author - Sourabh Deokar

# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
import os
import re
import shutil

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import mutagen.flac
import mutagen.mp3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Destination path of copying media
basePath="/run/user/1000/gvfs"
destAddress="/home/batman/myZone/temp"

#load MTP Device 
def loadDevice():
    dir = os.listdir(basePath)
    if not dir:
        print (bcolors.FAIL + "ERROR : NO DEVICE DETECTED" + bcolors.ENDC )
    else:
        global destAddress
        destAddress = os.path.join(os.path.join(basePath,dir[0]),"Internal storage/Music/Songs/English/Artiste")

#create the same playlist with different media paths in it
def createPlaylist():
    pass
        

#copy Playlist = copy songs + create playlist
def copyPlaylist():
    createPlaylist()
    

#copy Music ie mp3/flac files to destAddress and arrange it by Artist/SongName
def copyMusicFiles(filePath):
    filePath = filePath
    
    with open(filePath) as f:
        content = f.readlines()
    f.close()

    for file in content:
        file=file.strip()
        if os.path.exists(file):
            
            audioMeta={}
            if(file.lower().endswith('.flac')):
                try:
                    audioMeta=mutagen.flac.Open(file)
                except:
                    pass
            elif(file.lower().endswith('.mp3')):
                try:
                    audioMeta=EasyID3(file)
                except ID3NoHeaderError:
                    pass
            #if file doesnt exist check 
            try:
                print ("COPYING " + bcolors.OKBLUE + str(audioMeta["title"][0].encode('ascii','ignore')) + bcolors.ENDC )
                tempDir=os.path.join(destAddress,(str(audioMeta["Artist"][0].encode('ascii','ignore'))))              
                
                if not os.path.exists(tempDir):
                    os.makedirs(tempDir)

                if(file.lower().endswith('.flac')):
                    destFile=os.path.join(tempDir,(str(audioMeta["Title"][0].encode('ascii','ignore'))))+".flac"
                elif(file.lower().endswith('.mp3')):
                    destFile=os.path.join(tempDir,(str(audioMeta["Title"][0].encode('ascii','ignore'))))+".mp3"
                if not os.path.exists(destFile):
                    shutil.copyfile(file, destFile)
                    
            except KeyError:
                print (bcolors.FAIL + "ERROR : FILE DIDNT COPY" + bcolors.ENDC )    


#driver function
def main():
    print "\n" + bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE + "ANDROID MUSIC SYNC" + bcolors.ENDC
    mypath = "."
    mypath = raw_input("\nEnter the path of location of the playlist :");
    
    if(len(mypath)==0):
		mypath = "."
    if(os.path.exists(mypath)):
        loadDevice()
        copyMusicFiles(mypath)
    else:
        print (bcolors.FAIL + "ERROR : NO SUCH FILE FOUND" + bcolors.ENDC )    
    
if __name__ == '__main__':
   main()


#To infinity and beyond...
# \m/ W!LSP! \m/ 

'''
TO do
* KeyError : No meta found, copy with file name
* Identify android Device
* Identify Songs Location on Internal Storage as well as SD Card
* Make it Platform independent
* Make it universal for all devices
* option to copy all songs to one folder or by artist
* More playlist types other than .m3u

'''