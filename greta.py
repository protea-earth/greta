'''
############################################################################
##                         GRETA REPOSITORY                               ##
############################################################################

repository name: Greta
repository version: 1.0 
repository link: https://github.com/jim-schwoebel/greta 
author: Jim Schwoebel 
author contact: jim@protea.earth
description: Greta is an open source voice assistant to help reduce your carbon footprint.
license category: opensource 
license: Apache 2.0 license 
organization name: Protea.Earth
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
##                           RELEASE NOTES                                  ##
##############################################################################

Greta is a verastile open-source voice assistant to improve the workflow of 
your daily life. Nala uses actions which can be triggered by user voice queries. 

All the user needs to do is say 'hey Greta' and it will spark Greta to listen 
and respond to requests.

Greta uses machine learning to parse through user intents. If a request is not 
understood or is an anomaly, a web search is performed to give th user an answer.

FOR NEW USERS:
--> be sure to include google application credentials as a .json file 
e.g. export GOOGLE_APPLICATION_CREDENTIALS='/Users/jimschwoebel/Desktop/appcreds/NLX-infrastructure-b9201d884ea5.json'
'''


##############################################################################
##                          IMPORT STATEMENT                                ##
##############################################################################

import smtplib, os, glob, time, getpass, socket, pyaudio, pygame, wave
import shutil, importlib, geocoder, librosa, json, re, platform, urllib, contextlib
import requests, random, webbrowser, pickle, pyperclip, sys, struct, collections
from pydub import AudioSegment
from datetime import datetime
from sys import byteorder
from array import array
from struct import pack
import soundfile as sf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import speech_recognition as sr_audio
import pyttsx3 as pyttsx
import soundfile as sf 
from data.models import ps_transcribe as pst

##############################################################################
##                           HELPER FUNCTIONS                               ##
##############################################################################

def speaktext(hostdir,text):
    # speak to user from a text sample (tts system)  
    curdir=os.getcwd()
    os.chdir(hostdir+'/actions') 
    os.system("python3 speak.py '%s'"%(str(text)))
    os.chdir(curdir)

def wakeup(wake_type):
    if wake_type == 'porcupine':
        os.system('python3 wake_porcupine.py')
    elif wake_type == 'snowboy':
        os.system('python3 wake_snow.py')
    elif wake_type == 'sphinx':
        os.system('python3 wake_pocket.py')
    else:
        # default to porcupine if don't know 
        os.system('python3 wake_porcupine.py')

def curloc():
    # get current location, limit 1000 requests/day
    r=requests.get('http://ipinfo.io')
    location=r.json()
    return location

def get_date():
    return str(datetime.now())

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

def playbackaudio(filename):
    # takes in a question and a filename to open and plays back the audio
    # file and prints on the screen the question for the user 
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(0.5)
    return "playback completed"

def get_clipboard():
    # gets the results from the current clipboard 
    text=pyperclip.paste()

    return text 

def get_seconds(transcript):
    # assume minutes are coming in
    # assume max of 10 mintues 
    minute=60
    transcript=transcript.lower()

    if transcript.find('one')>=0:
        seconds=minute
    elif transcript.find('two')>=0:
        seconds=2*minute
    elif transcript.find('three')>=0:
        seconds=3*minute
    elif transcript.find('four')>=0:
        seconds=4*minute
    elif transcript.find('five')>=0:
        seconds=5*minute
    elif transcript.find('six')>=0:
        seconds=6*minute
    elif transcript.find('seven')>=0:
        seconds=7*minute
    elif transcript.find('eight')>=0:
        seconds=8*minute
    elif transcript.find('nine')>=0:
        seconds=9*minute
    elif transcript.find('ten')>=0:
        seconds=10*minute
    else:
        # get back numbers by removing characters if not typed out  
        chars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                'q','r','s','t','u','v','w','x','y','z',' ','.',"'",'<','>','"',
                '[',']','-','=','+','(',')','*','&','^','%','$','#','@','!','~',
                '`']

        mins=transcript

        for i in range(len(chars)):
            mins=mins.replace(chars[i],'')

        try: 
            seconds=int(mins)*60
            minutes=int(mins)
        except:
            print('error converting')
            # default to 1 minute 
            seconds=60
            minutes=1

    print(minutes)
    print(seconds)

    return seconds, minutes

def capture_video(filename, timesplit):
    video=cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    a=0
    start=time.time()

    while True:
        a=a+1
        check, frame=video.read()
        #print(check)
        #print(frame)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        out.write(frame)
        #cv2.imshow("frame",gray)
        end=time.time()
        if end-start>timesplit:
            break 
        #print(end-start)

    print(a)
    video.release()
    out.release() 
    cv2.destroyAllWindows()

    return filename 

def cut_faces(modeldir,filename):
    # import data later 
    hostdir=os.getcwd()
    capture_video(filename, 10)
    face_cascade = cv2.CascadeClassifier(modeldir+'/data/models/haarcascade_frontalface_default.xml')
    foldername=filename[0:-4]+'_faces'

    try:
        os.mkdir(foldername)
    except:
        shutil.rmtree(foldername)
        os.mkdir(foldername)

    shutil.move(hostdir+'/'+filename, hostdir+'/'+foldername+'/'+filename)
    os.chdir(foldername)

    videodata=skvideo.io.vread(filename)
    frames, rows, cols, channels = videodata.shape
    metadata=skvideo.io.ffprobe(filename)
    frame=videodata[0]
    r,c,ch=frame.shape

    for i in range(0,len(videodata),25):
        #row, col, channels
        skvideo.io.vwrite("output"+str(i)+".png", videodata[i])

    listdir=os.listdir()
    facenums=0

    for i in range(len(listdir)):
        if listdir[i][-4:]=='.png':

            try:

                image_file = listdir[i]

                img = cv2.imread(hostdir+'/'+foldername+'/'+image_file)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                increment=0
                print(len(faces))

                if len(faces) == 0:
                    pass
                else:
                    for (x,y,w,h) in faces:
                        os.chdir(hostdir+'/'+foldername)
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        newimg=img[y:y+h,x:x+w]
                        new_image_file=image_file[0:-4] + '_face_' + str(increment) + '.png'
                        cv2.imwrite(new_image_file, newimg)
                        facenums=facenums+1

            except:
                print('error')

    os.chdir(hostdir+'/'+foldername)
    listdir=os.listdir()
    # print(listdir)
    
    for i in range(len(listdir)):
        if listdir[i][-4:]=='.png':
            if listdir[i].find('face') < 0:
                os.remove(listdir[i])

    return facenums

def save_query_json(wavfile, query, hostdir):
    # save queries in .json format in the queries folder 
    curdir=os.getcwd()
    os.chdir(hostdir)
    jsonfilename=wavfile[0:-4]+'.json'
    jsonfile=open(jsonfilename, 'w')
    json.dump(query,jsonfile)
    jsonfile.close()
    shutil.move(hostdir+'/'+jsonfilename,hostdir+'/data/queries/'+jsonfilename)
    os.chdir(curdir)

def register_user(action_list, hostdir):

    # hostdir
    os.chdir(hostdir)
    hostdir=os.getcwd()

    # assume default directory is hostdir 
    # if any folders exist delete them
    try:
        os.mkdir(hostdir+'/data/wakewords')
    except:
        shutil.rmtree(hostdir+'/data/wakewords')
        os.mkdir(hostdir+'/data/wakewords')
    try:
        os.mkdir(hostdir+'/data/actions')
    except:
        shutil.rmtree(hostdir+'/data/actions')
        os.mkdir(hostdir+'/data/actions')
    try:
        os.mkdir(hostdir+'/data/queries')
    except:
        shutil.rmtree(hostdir+'/data/queries')
        os.mkdir(hostdir+'/data/queries')
    try:
        os.mkdir(hostdir+'/data/baseline')
    except:
        shutil.rmtree(hostdir+'/data/baseline')
        os.mkdir(hostdir+'/data/baseline')

    os.chdir(hostdir+'/data/baseline')

    # get name from user profile name, if not record it 
    speaktext(hostdir, 'To begin, you must register with us. I have a few quick questions for you. Please type in the answers to the following questions.')
    email=input('what is your email? \n')
    name=input('what is your name (leave blank for %s)? \n'%(getpass.getuser()))

    # now get some wakewords to authenticate the user's identity 
    os.chdir(hostdir+'/data/wakewords')
    speaktext(hostdir, 'Okay, can you say Hey Gret ta for me?')
    playbackaudio(hostdir+'/data/tone.wav')
    record_to_file(os.getcwd(),'hey_greta_1.wav', 3)
    speaktext(hostdir, 'Can you say Hey Gret ta again?')
    playbackaudio(hostdir+'/data/tone.wav')
    record_to_file(os.getcwd(),'hey_greta_2.wav', 3)
    speaktext(hostdir, 'One more time.')
    playbackaudio(hostdir+'/data/tone.wav')
    record_to_file(os.getcwd(),'hey_Greta_3.wav', 3)

    # go back to baseline directory to save databases 
    os.chdir(hostdir+'/data/baseline')

    if name == '':
        name=getpass.getuser()

    speaktext(hostdir, 'Now give us a few seconds to make an account for you.')

    facenums=cut_faces(hostdir, name+'.avi')
    os.chdir(hostdir+'/data/baseline')

    jsonfile=open('settings.json','w')

    data = {
        # alarm True = on, False = off at designated time 
        'alarm': False,
        # the time the alarm would go off at (in 24 hour time, 8 = 8AM, 13 = 1 PM) 
        # if the alarm action is turned on.
        'alarm time': 8,
        # if True, then Nala will greet you every time you login and get the weather (default). 
        # If False, she will not do this.
        'greeting': True,
        # the last time that you updated the database (this is useful for understanding sessions).
        'end': time.time(),
        # options are ‘sphinx’, ‘google’ (recommended to use sphinx to not waste money )
        # if using google, make sure you have the right environment variables (e.g. 
        # export GOOGLE_APPLICATION_CREDENTIALS='/Users/NLX-infrastructure-b9201d884ea5.json')
        'transcript type': 'google',
        # Wakeword detector used to detect user queries. 
        # Default is ‘porcupine’ as it is the most accurate wakeword detector.
        # options are 'sphinx', 'snowboy', 'porcupine' (default)
        'wake type': 'snowboy',
        #Time in seconds of each query when Nala is activated. The default query time is 
        # 2 seconds (from trial-and-error).
        'query time':3,
        # Multi-query capability allows you to separate queries with AND in the transcript, 
        # so it doesn’t stop after one query. Default is True.
        'multi query':True,
        # Ability to save queries once they have been propagated. Otherwise, they are deleted. 
        # This is useful if you want to cache query data or build a dataset. Default is True.
        'query save':True,
        # Store face when user registers to authenticate later with facial recognition. Default is True.
        'register face': True,
        # The time (in minutes) that Nala will sleep if you trigger the “Go to sleep” action query. Default is 30 minutes.
        'sleep time': 30,
        # save .json queries as well in the data/queries folder to match audio (e.g. sample.wav --> sample.json with query info)
        # if True, does this. If not, does not save .json in the folder. 
        'query json': True,
        # budget (user query above)
        'budget': '30', 
        # genre (user query above)
        'genre': 'rock',
    }

    jsonfile=open('settings.json','w')
    json.dump(data,jsonfile)
    jsonfile.close()

    jsonfile=open('registration.json','w')
    data = {
        'name': name, 
        'email': email,
        'userID': 0,
        'hostdir': os.getcwd(),
        'location': curloc(),
        'rest time': 0.10,
        'facenums': facenums,
        'registration date': get_date(),
        'tts': 'com.apple.speech.synthesis.voice.fiona',
        }

    json.dump(data,jsonfile)
    jsonfile.close()

    jsonfile=open('actions.json','w')
    data = {
        'logins': [], # login datetime
        'logouts': [], # logout datetime (last time before login)
        'active session': [],
        'sessions': [],
        'query count': 0,
        'queries': [],
        'noise': [],
        'action count': 0,
        'action log': [], #action, datetime, other stuff 
        'loopnum': 0,
        'available actions': action_list,
    }
    json.dump(data, jsonfile)
    jsonfile.close()

    # store 2 copies in case of deletion
    shutil.copy(os.getcwd()+'/registration.json', hostdir+'/registration.json')
    shutil.copy(os.getcwd()+'/settings.json', hostdir+'/settings.json')
    shutil.copy(os.getcwd()+'/actions.json', hostdir+'/actions.json')

    speaktext(hostdir, 'Thank you, you are now registered.')


def update_database(hostdir,logins,logouts,session,sessions,query_count,queries,noise,action_count,loopnum, alarm, end):

    curdir=os.getcwd()
    os.chdir(hostdir)

    # update only the fields that matter
    data=json.load(open('actions.json'))

    data['logins']=logins
    data['logouts']=logouts
    data['active session']=session
    data['sessions']=sessions
    data['query count']=query_count
    data['queries']=queries
    data['noise']=noise
    data['action count']=action_count
    data['loopnum']=loopnum

    jsonfile=open('actions.json','w')
    json.dump(data,jsonfile)
    jsonfile.close()

    data=json.load(open('settings.json'))

    data['alarm']=alarm
    data['end']=end

    jsonfile=open('settings.json','w')
    json.dump(data,jsonfile)
    jsonfile.close()

    # store backup copy just in case of either database being corrupted 
    os.chdir(hostdir+'/data/baseline')
    os.remove('actions.json')
    os.remove('settings.json')
    shutil.copy(hostdir+'/actions.json',os.getcwd()+'/actions.json')
    shutil.copy(hostdir+'/settings.json',os.getcwd()+'/settings.json')

    os.chdir(curdir)

def wav_cleanup():
    # remove .wav files in current directory to clean it up
    # before next query 
    listdir=os.listdir()
    for i in range(len(listdir)):
        if listdir[i][-4:]=='.wav':
            os.remove(listdir[i])


##############################################################################
##                          ACTIONS LOADED                                  ##
##############################################################################

hostdir = os.getcwd()
os.chdir(hostdir+'/actions')
listdir=os.listdir()

action_list=list()
for i in range(len(listdir)):
    if listdir[i][-3:]=='.py':
        action_list.append(listdir[i])

# first get all the actions in the actions folder
action_keywords=list()
for i in range(len(action_list)):
    action=action_list[i][0:-3]
    action_keyword=action.split('_')
    action_keywords.append(action_keyword)

# print(action_keywords)
os.chdir(hostdir)

##############################################################################
##                           LOAD DATABASE                                  ##
##############################################################################

# try to load vars in baseline.json file or register a user 
os.chdir(hostdir)
if 'actions.json' not in os.listdir():
    # you only use these modules if you register, so put them here
    import cv2 
    import skvideo.io, skvideo.motion, skvideo.measure
    from moviepy.editor import VideoFileClip
    from PIL import Image
    
    register_user(action_list, hostdir)

try:
    # load database 
    os.chdir(hostdir)

    # registration.json data 
    try:
        database=json.load(open('registration.json'))
    except:
        # restore database if corrupted
        print('registration database corrupted, restoring...')
        os.chdir(hostdir+'/data/baseline/')
        database=json.load(open('registration.json'))
        os.chdir(hostdir)
        os.remove('registration.json')
        shutil.copy(hostdir+'/data/baseline/registration.json',hostdir+'/registration.json')

    name=database['name']
    regdate=database['registration date']
    rest_time=database['rest time']

    # actions.json data 
    try:
        database=json.load(open('actions.json'))
    except:
        # restore database if corrupted
        print('actions database corrupted, restoring...')
        os.chdir(hostdir+'/data/baseline/')
        database=json.load(open('actions.json'))
        os.chdir(hostdir)
        os.remove('actions.json')
        shutil.copy(hostdir+'/data/baseline/actions.json',hostdir+'/actions.json')
        
    logins=database['logins']
    logouts=database['logouts']
    session=database['active session']
    sessions=database['sessions']
    query_count=database['query count']
    queries=database['queries']
    noise=database['noise']
    action_count=database['action count']
    action_log=database['action log']
    loopnum=database['loopnum']
    avail_actions = database['available actions']
    #print(database)

    # settings.json data
    try:
        database=json.load(open('settings.json'))
    except:
        # restore database if corrupted
        print('settings database corrupted, restoring...')
        os.chdir(hostdir+'/data/baseline/')
        database=json.load(open('settings.json'))
        os.chdir(hostdir)
        os.remove('settings.json')
        shutil.copy(hostdir+'/data/baseline/settings.json',hostdir+'/settings.json')
        
    alarm=database['alarm']
    alarm_time=database['alarm time']
    greeting=database['greeting']
    end=database['end']
    transcript_type=database['transcript type']
    wake_type=database['wake type']
    query_time=database['query time']
    multi_query=database['multi query']
    query_save=database['query save']
    register_face=database['register face']
    sleep_time=database['sleep time']
    query_json=database['query json']

    # instantiate variables 
    logins.append(get_date())
    t=1
    query_request=False 
    turn_off = False

except:
    # register user if no user exists
    print('registering new user!')
    # you only use these modules if you register, so put them here
    import cv2 
    import skvideo.io, skvideo.motion, skvideo.measure
    from moviepy.editor import VideoFileClip
    from PIL import Image
    register_user(action_list, hostdir)

    # load database
    os.chdir(hostdir)

    # registration data 
    database=json.load(open('registration.json'))
    name=database['name']
    regdate=database['registration date']
    rest_time=database['rest time']

    # action data 
    database=json.load(open('actions.json'))
    logins=database['logins']
    logouts=database['logouts']
    session=database['active session']
    sessions=database['sessions']
    query_count=database['query count']
    queries=database['queries']
    noise=database['noise']
    action_count=database['action count']
    action_log=database['action log']
    loopnum=database['loopnum']
    avail_actions = database['available actions']
    
    # settings.json
    database=json.load(open('settings.json'))
    alarm=database['alarm']
    alarm_time=database['alarm time']
    greeting=database['greeting']
    end=database['end']
    transcript_type=database['transcript type']
    wake_type=database['wake type']
    query_time=database['query time']
    multi_query=database['multi query']
    query_save=database['query save']
    register_face=database['register face']
    sleep_time=database['sleep time']
    query_json=database['query json']

    # instantiate variables
    logins.append(get_date())
    t=1
    query_request=False 
    turn_off = False

##############################################################################
##                           MAIN SCRIPT                                    ##
##############################################################################

while turn_off == False:
    # record a 3.0 second voice sample
    # use try statement to avoid errors 
    try:

        # welcome user back if it's been over an hour since login 
        start=time.time()

        # set alarm and make false after you trigger alarm 
        if alarm == True and alarm_time == datetime.now().hour:
            os.chdir(hostdir+'/actions')
            os.system('python3 alarm.py %s'%(hostdir))
            alarm == False
            os.chdir(hostdir)

        if abs(end-start) > 60*60:

            end=time.time()

            if greeting == True:
               speaktext(hostdir,'welcome back, %s'%(name.split()[0]))
               os.chdir(hostdir+'/actions')
               os.system('python3 weather.py %s'%(hostdir))
               os.system('python3 news.py %s'%(hostdir))
               os.system('python3 events.py %s'%(hostdir))
               os.chdir(hostdir)

            # log session if the time of activity is greater than 60 minutes
            sessions.append(session)
            # start a new session 
            session=list()

        # change to host directory 
        os.chdir(hostdir)

        # wakeup according to wake_type then activate the query 
        os.chdir(hostdir+'/data/models/')
        wakeup(wake_type)
        query_num=0
        query_request=False

        while query_request==False and query_num <= 3: 

            os.chdir(hostdir)
            if query_num==0:
                # if the first query, ask how you can help 
                speaktext(hostdir,'how can I help you?')
                playbackaudio(hostdir+'/data/tone.wav')
            else:
                # the prior sample was noise, so we must add it as such 
                message="Sorry, I didn't get that. How can I help?"
                query={
                    'date':get_date(),
                    'audio': unique_sample,
                    'transcript type': transcript_type,
                    'query transcript': query_transcript,
                    'transcript': transcript,
                    'response': [],
                    'meta': [message],
                }
                noise.append(query)
                session.append(query)
                # now ask user for another sample because previous sample was noise 
                speaktext(hostdir,"Sorry, I did not get that. How can I help?")
                playbackaudio(hostdir+'/data/tone.wav')

            # record audio and initiate query 
            time.sleep(0.50)
            unique_sample='sample'+str(loopnum)+'_'+str(query_num)+'.wav'
            record_to_file(os.getcwd(),unique_sample, query_time)

            # transcribe audio according to transcript_type (in settings.json)
            transcript=transcribe_audio(unique_sample, hostdir, transcript_type)

            # only save the query if you'd like to with query_save variable (in settings.json)
            if query_save == True:
                shutil.move(hostdir+'/'+unique_sample,hostdir+'/data/queries/'+unique_sample)
            else:
                os.remove(unique_sample)

            query_transcript=transcript.lower().split()

            # enable multiple queries if it is activated 
            if multi_query == True:
                and_num = query_transcript.count('and')
            else:
                and_num = 0

            # break if it finds a query 
            for i in range(len(query_transcript)):

                # iterate through transcript 
                os.chdir(hostdir+'/actions')
                print(query_transcript[i])

                for k in range(len(action_keywords)):

                    if query_transcript[i] in action_keywords[k]:
                        # per the design patterns of the 'actions'
                        command='python3 %s %s'%(action_list[k], hostdir)
                        os.system(command)

                        query={
                            'date':get_date(),
                            'audio': unique_sample,
                            'transcript type': transcript_type,
                            'query transcript': query_transcript[i],
                            'transcript': transcript,
                            'response': command,
                            'meta': list(),
                        }

                        # save query to json 
                        try:
                            if query_json == True:
                                save_query_json(unique_sample, query, hostdir)
                        except:
                            print('error')

                        query_count=query_count+1 
                        queries.append(query)
                        session.append(query)
                        action_count=action_count+1
                        query_request=True 
                        if and_num == 0:
                            break 
                        else: 
                            and_num=and_num-1





                ## ############################################ ##
                ## ALL SLEEP AND TERMINATING ACTIONS BELOW HERE ##
                ## ############################################ ##

                if query_transcript[i] in ['sleep']:

                    speaktext(hostdir,"Okay, %s. I will sleep for 30 minutes."%(name.split()[0]))

                    query={
                        'date':get_date(),
                        'audio': unique_sample,
                        'transcript type': transcript_type,
                        'query transcript': query_transcript[i],
                        'transcript': transcript,
                        'response': '',
                        'meta': ['sleep for 30 minutes'],
                    }
                    # save query to json 
                    try:
                        if query_json == True:
                            save_query_json(unique_sample, query, hostdir)
                    except:
                        print('error')
                    # controlled by variable sleep_time (in settings.json )
                    time.sleep(60*sleep_time)
                    query_request=True 
                    speaktext(hostdir,"Okay, I am back %s. I am here if you need me."%(name.split()[0]))
                    if and_num == 0:
                        break 
                    else: 
                        and_num=and_num-1

                elif transcript.find('log out')>=0:

                    speaktext(hostdir,'Okay, %s. I will turn myself off. See you next time!'%(name.split()[0]))
                    
                    query={
                        'date':get_date(),
                        'audio': unique_sample,
                        'transcript type': transcript_type,
                        'query transcript': query_transcript[i],
                        'transcript': transcript,
                        'response': '',
                        'meta': 'logged off with turn_off = True',
                    }
                    # save query to json 
                    try:
                        if query_json == True:
                            save_query_json(unique_sample, query, hostdir)
                    except:
                        print('error')
                    query_count=query_count+1 
                    queries.append(query)
                    session.append(query)
                    logouts.append(get_date())
                    action_count=action_count+1
                    query_request=True  
                    end=time.time()
                    session.append('updated database @ %s'%(get_date()))
                    update_database(hostdir,logins,logouts,session,sessions,query_count,queries,noise,action_count,loopnum, alarm, end)
                    turn_off=True 
                    if and_num == 0:
                        break 
                    else: 
                        and_num=and_num-1

                elif query_transcript[i] in ['shut', 'down', 'restart']:

                    if query_transcript.index('shut')>=0 and query_transcript.index('down')>=0:
                        # only shutdown if both shut and down are present in google transcript 
                        speaktext(hostdir,'Okay, %s. I will shutdown the computer in ten seconds. See you next time!'%(name.split()[0]))
                       
                        query={
                            'date':get_date(),
                            'audio': unique_sample,
                            'transcript type': transcript_type,
                            'query transcript': query_transcript[i],
                            'transcript': transcript,
                            'response': "python3 shutdown.py %s"%(hostdir),
                        }
                        # save query to json 
                        try:
                            if query_json == True:
                                save_query_json(unique_sample, query, hostdir)
                        except:
                            print('error')
                        query_count=query_count+1 
                        queries.append(query)
                        session.append(query)
                        logouts.append(get_date())
                        action_count=action_count+1
                        query_request=True  
                        end=time.time()
                        print(query_request)
                        session.append('updated database @ %s'%(get_date()))
                        update_database(hostdir,logins,logouts,session,sessions,query_count,queries,noise,action_count,loopnum, alarm, end)
                        time.sleep(10)
                        os.system('python3 shutdown.py %s'%(hostdir))
                        if and_num == 0:
                            break 
                        else: 
                            and_num=and_num-1

                    elif query_transcript[i] == 'restart':
                        # restart computer using a forced reboot 
                        speaktext(hostdir,'Okay, %s. I will restart the computer in ten seconds. See you next time!'%(name.split()[0]))
                        
                        query={
                            'date':get_date(),
                            'audio': unique_sample,
                            'transcript type': transcript_type,
                            'query transcript': query_transcript[i],
                            'transcript': transcript,
                            'response': "python3 reboot.py %s"%(hostdir),
                        }
                        # save query to json 
                        try:
                            if query_json == True:
                                save_query_json(unique_sample, query, hostdir)
                        except:
                            print('error')
                        query_count=query_count+1 
                        queries.append(query)
                        session.append(query)
                        logouts.append(get_date())
                        action_count=action_count+1
                        query_request=True  
                        end=time.time()
                        print(query_request)
                        session.append('updated database @ %s'%(get_date()))
                        update_database(hostdir,logins,logouts,session,sessions,query_count,queries,noise,action_count,loopnum, alarm, end)
                        time.sleep(10)
                        os.system('python3 reboot.py %s'%(hostdir))
                        if and_num == 0:
                            break 
                        else: 
                            and_num=and_num-1

                else:
                    # pass if it does not satify any of the other conditions 
                    # eventually, if not a query that is valid, will ask the user 
                    # again becasue it does not satisfy query_request=True 
                    pass 

            query_num=query_num+1 
            os.chdir(hostdir)

        # update database 
        end=time.time()
        # can include this info in session, but I have left out because it can get a bit messy
        # session.append('updated database @ %s'%(get_date()))
        try:
            update_database(hostdir,logins,logouts,session,sessions,query_count,queries,noise,action_count,loopnum, alarm, end)

        except:
            print('error updating database')

        # clean up wav files in host directory 
        try:
            os.chdir(hostdir)
            wav_cleanup()
        except:
            pass

    except:
        pass 
    
    # sleep appropriately before each query to not harm the processor and suck battery 
    time.sleep(rest_time)
    loopnum=loopnum+1 

# say goodbye if loop breaks and is turned off 
speaktext(hostdir,'Goodbye')
    
