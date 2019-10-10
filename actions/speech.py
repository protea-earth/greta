'''
############################################################################
##                         GRETA REPOSITORY                               ##
############################################################################

repository name: Greta
repository version: 1.0 
repository link: https://github.com/jim-schwoebel/greta
author: Jim Schwoebel 
author contact: jim@protea.earth
description: Greta is an open-source voice assistant to help reduce your carbon footprint.
license category: opensource 
license: Apache 2.0 license 
organization name: Protea.earth 
location: Boston, MA
website: http://protea.earth 
release date: 2019-09-26

This code is hereby released under a Apache 2.0 license license. 

For more information, check out the license terms below. 

##############################################################################
##                            LICENSE TERMS                                 ##
##############################################################################

Copyright 2019 Protea.Earth

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

     http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 

##############################################################################
##                              SPEECH.PY                                   ##
##############################################################################

This script reads Greta's speech from the UN Climate Action Summit:
https://www.npr.org/2019/09/23/763452863/transcript-greta-thunbergs-speech-at-the-u-n-climate-action-summit
'''
##############################################################################
##                           IMPORT STATEMENTS                              ##
##############################################################################

import requests, time, random, webbrowser, datetime, platform, sys, feedparser, wave 
import pyautogui, platform, pygame, pyaudio, cv2, uuid, zipfile 
import speech_recognition as sr_audio
from fuzzywuzzy import fuzz
import ftplib, getpass, os, json 
from bs4 import BeautifulSoup
import pyttsx3 as pyttsx

##############################################################################
##                            HELPER FUNCTIONS                              ##
##############################################################################

def speak(text):
    # speak to a user from a text sample
    engine=pyttsx.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.fiona')
    engine.say(text)
    engine.runAndWait()

def get_date():
    return str(datetime.datetime.now())

def curloc():

    # get current location, limit 1000 requests/day
    r=requests.get('http://ipinfo.io')
    location=r.json()
    
    return location

def typekeys(keystring):
        for i in range(len(keystring)):
                pyautogui.press(keystring[i])
                time.sleep(0.025)

def record_to_file(path,filename,recordtime):

    # record 3 second voice file 
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 1 
    RATE = 16000 #sample rate
    RECORD_SECONDS = recordtime
    WAVE_OUTPUT_FILENAME = filename

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def playbackaudio(filename):
    # takes in a question and a filename to open and plays back the audio
    # file and prints on the screen the question for the user 
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(0.5)
    return "playback completed"

def transcribe_audio(filename,hostdir,transcript_type):
    # transcribe the audio according to transcript type 
    # google or sphinx (custom model) 
    try:
        if transcript_type == 'sphinx':
            transcript=pst.transcribe(hostdir,filename)
            print('pocket: '+transcript)

        elif transcript_type == 'google':
            try:
                # try google if you can, otherwise use sphinx 
                r=sr_audio.Recognizer()
                with sr_audio.AudioFile(filename) as source:
                    audio = r.record(source) 
                transcript=r.recognize_google_cloud(audio)
                print('google: '+transcript)
            except:
                print('error using google transcription, need to put API key in environment vars')
                print('defaulting to pocketsphinx...')
                r=sr_audio.Recognizer()
                with sr_audio.AudioFile(filename) as source:
                    audio = r.record(source) 
                transcript=r.recognize_sphinx(audio)
                print('sphinx (failed google): '+transcript)

        else:
            # default to sphinx if not sphinx or google inputs 
            transcript=pst.transcribe(hostdir,filename)
            print('pocket: '+transcript)

    except:
        transcript=''


    return transcript 

##############################################################################
##                               MAIN SCRIPT                                ##
##############################################################################

# host directory 
hostdir=sys.argv[1]
location=curloc()
city=location['city']
postal=location['postal']

# get screen size and do path if certain size 
screensize=pyautogui.size() 
protea_username=os.environ['PROTEA_USERNAME']
protea_password=os.environ['PROTEA_USERPASSWORD']
register=True
filenames=list()

if screensize == (1440, 900) and platform.system() == 'Darwin':
    # this is for the mac laptop 
    os.system('open -a safari https://media.giphy.com/media/hS3BVKSDpJOfFykOqI/giphy.gif')
    speech=open('speech.txt').read()
    pyautogui.moveTo(217, 0)
    pyautogui.click()
    pyautogui.moveTo(308, 480)
    pyautogui.click()
    speak(speech)
    speak('This concludes my speech')
    speak('Have a great rest of your day.')

    
