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
##                       RECYCLE_RECYCLING.PY                               ##
##############################################################################

Guides the user to recycle using https://search.earth911.com
'''

##############################################################################
##                           IMPORT STATEMENTS                              ##
##############################################################################

import requests, time, random, webbrowser, datetime, platform, sys, feedparser 
import ftplib, getpass, os, json 
from bs4 import BeautifulSoup
import pyttsx3 as pyttsx

##############################################################################
##                            HELPER FUNCTIONS                              ##
##############################################################################

def speaktext(text):
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


##############################################################################
##                            MAIN SCRIPT                                   ##
##############################################################################
# search recycling facilities using https://search.earth911.com
location=curloc()
city=location['city']
postal=location['postal']
speaktext('Thanks for making the effort to recycle.')
os.system('open https://search.earth911.com/?what=plastics')
speaktext('Now search your zip code - %s.'%(postal))
speaktext('You can also search your city - %s')
speaktext('Have a great rest of your day!')

# update database 
hostdir=sys.argv[1]
os.chdir(hostdir)
database=json.load(open('actions.json'))
action_log=database['action log']

action={
    'action': 'recycle.py',
    'date': get_date(),
    'meta': [location],
}

action_log.append(action)
database['action log']=action_log

jsonfile=open('actions.json','w')
json.dump(database,jsonfile)
jsonfile.close()


