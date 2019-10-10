'''
############################################################################
##                         NALA REPOSITORY                                ##
############################################################################

repository name: nala 
repository version: 1.0 
repository link: https://github.com/jim-schwoebel/nala 
author: Jim Schwoebel 
author contact: js@neurolex.co 
description: Nala is an open source voice assistant. 
license category: opensource 
license: Apache 2.0 license 
organization name: NeuroLex Laboratories, Inc. 
location: Seattle, WA 
website: https://neurolex.ai 
release date: 2018-09-28 

This code (nala) is hereby released under a Apache 2.0 license license. 

For more information, check out the license terms below. 

##############################################################################
##                            LICENSE TERMS                                 ##
##############################################################################

Copyright 2018 NeuroLex Laboratories, Inc. 

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
##                            SERVICE STATEMENT                             ##
##############################################################################

If you are using the code written for a larger project, we are 
happy to consult with you and help you with deployment. Our team 
has >10 world experts in kafka distributed architectures, microservices 
built on top of Node.JS / Python / Docker, and applying machine learning to 
model speech and text data. 

We have helped a wide variety of enterprises - small businesses, 
researchers, enterprises, and/or independent developers. 

If you would like to work with us let us know @ js@neurolex.co. 

##############################################################################
##                            SETUP.PY                                      ##
##############################################################################

Run this script to install all dependencies for nala.
'''
import os, shutil

hostdir=os.getcwd()
# need to fix pocketsphinx for custom language model 
# https://github.com/watsonbox/homebrew-cmu-sphinx
os.system('brew uninstall pocketsphinx')
os.system('brew tap watsonbox/cmu-sphinx')
os.system('brew install --HEAD watsonbox/cmu-sphinx/cmu-sphinxbase')
os.system('brew install --HEAD watsonbox/cmu-sphinx/cmu-pocketsphinx')

# prompt user if they want to integrate with google? / open up docs to setup env vars 
# set up env var for host password 

def pip3_install(modules):
    for i in range(len(modules)):
        os.system('pip3 install %s'%(modules[i]))
          
def pip_install(modules):
    for i in range(len(modules)):
        os.system('pip3 install %s'%(modules[i]))
          
def brew_install(modules):
    for i in range(len(modules)):
        os.system('brew install %s'%(modules[i]))

brew_modules=['portaudio', 'ffmpeg', 'sox', 'shpotify', 'swig']

# for all actions and main script 
pip3_modules=['ftplib', 'smtplib', 'getpass', 'pyaudio','pygame'
             'wave','shutil','importlib','geocoder','librosa',
             'urrllib','random','webbrowser','pyperclip','pydub',
             'array','struct','soundfile','pandas','numpy',
             'bs4','cryptography','pyscreenshot','pyautogui',
             'cv2','readchar','psutil','SpeechRecognition',
             'pyttsx3','soundfile','moviepy','PIL',
             'pytube', 'email', 'nltk','textblob','pdf2image',
            'pytesseract','tempfile','pdfkit', 'pygame', 'pocketsphinx',
            'opencv-python','scikit-video', 'reportlab', 'matplotlib', 'pypdf2',
             'google-api-python-client', 'oauth2client', 'feedparser',  
             'chatterbot==0.7.4', 'chatterbot_corpus', 'fuzzywuzzy']

pip_modules=['pyttsx3', 'pyaudio']

brew_install(brew_modules)
os.system('pip3 install -U pyobjc')
os.system('pip install -U pyobjc')
pip3_install(pip3_modules)
pip_install(pip_modules)
os.system('/Applications/Python\ 3.6/Install\ Certificates.command')

# now we need to customize the Snowboy wakeword detector 
os.chdir('data/models')
rename_1=open('rename.txt').read()
rename_2=open('rename2.txt').read()
curdir=os.getcwd()
os.system('git clone https://github.com/Kitt-AI/snowboy.git')
os.chdir('snowboy')
snow_dir=os.getcwd()
shutil.copy(curdir+'/Greta.pmdl', os.getcwd()+'/examples/python3/Greta.pmdl')
os.remove(os.getcwd()+'/examples/python3/snowboydetect.py')
os.chdir('swig/python3')
os.system('make')
shutil.copy(os.getcwd()+'/snowboydetect.py', snow_dir+'/examples/python3/snowboydetect.py')
os.chdir(snow_dir+'/examples/python3/')
g=open('snowboydecoder.py').read()
text=g.replace('from . import snowboydetect', 'import snowboydetect')
text=text.replace(rename_1, rename_2)
g=open('snowboydecoder.py','w')
g.write(text)
g.close()

def speaktext(hostdir,text):
    # speak to user from a text sample (tts system)  
    curdir=os.getcwd()
    os.chdir(hostdir+'/actions') 
    os.system("python3 speak.py '%s'"%(str(text)))
    os.chdir(curdir)

os.system('open ~/.bash_profile')
speaktext(hostdir, 'Please configure your environment variables per this readme')
os.system('open https://github.com/jim-schwoebel/greta/blob/master/README.md')
speaktext(hostdir, 'Okay, setup is complete. Gret ta is ready for you to start.')
