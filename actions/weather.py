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
##                              WEATHER.PY                                  ##
##############################################################################

Gets the weather. This is intended to be run as an action upon boot process. 

This is following the tutorial found here: https://www.dataquest.io/blog/web-scraping-tutorial-python/

Thus, it depends on the weather.gov website being up and running for it to pull forecast and that internet
connection exists.
'''

##############################################################################
##                           IMPORT STATEMENTS                              ##
##############################################################################

import requests, time, datetime, ftplib, platform, json, getpass, os, sys
from bs4 import BeautifulSoup
import pyttsx3 as pyttsx

##############################################################################
##                            HELPER FUNCTIONS                              ##
##############################################################################


def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def speaktext(text):
    # speak to user from a text sample (tts system)
    engine = pyttsx.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.fiona')
    engine.say(text)
    engine.runAndWait()

def curloc():
    
    # get current location, limit 1000 requests/day
    
    r=requests.get('http://ipinfo.io')
    location=r.json()
    
    return location

def get_date():
    return str(datetime.datetime.now())

##############################################################################
##                            MAIN SCRIPT                                   ##
##############################################################################

internet_access=connected_to_internet()

if internet_access==True:

    # get location to know what URL to pull
    location=curloc()
    all_loc_data=location
    city=location['city']
    coords=location['loc'].split(',')
    latitude=coords[0]
    longitude=coords[1]

    # get current conditions 
    url="http://forecast.weather.gov/MapClick.php?lat=%s&lon=%s"%(latitude,longitude)
    page=requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    h=soup.find_all('div',class_='panel panel-default',id='current-conditions')
    text=h[0].get_text()
    text=text.split('\n\n\n\n')

    # get current weather results 
    location=text[1].split('\n')[1]
    cur_conditions=text[2].split('\n')[3].lower()
    cur_temp=text[2].split('\n')[4].replace('°F',' degrees Fahrenheit')

    # get forecast rest of day 
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")
    tonight = forecast_items[0]
    img = tonight.find("img")
    desc = img['title']

    # now speak current temperature and conditions
    speak_text='It is %s and %s in %s'%(cur_temp, cur_conditions,city)
    print(speak_text)
    speaktext(speak_text)
    #time.sleep(0.5)
    print(desc)
    speaktext(desc)
    
    #if desc.find('showers')!= -1:
        #speaktext('You may want to bring an umbrella with you. It may rain.')

    # update database 
    hostdir=sys.argv[1]
    os.chdir(hostdir)
    database=json.load(open('actions.json'))
    action_log=database['action log']

    action={
        'action': 'weather.py',
        'date': get_date(),
        'meta': [all_loc_data, speak_text],
    }

    action_log.append(action)
    database['action log']=action_log

    jsonfile=open('actions.json','w')
    json.dump(database,jsonfile)
    jsonfile.close()


else:
    # don't get the weather if not connected to the internet 
    speak_text='no internet access, cannot get weather from the national weather service'
    print(speak_text)
    speaktext(speak_text)

    # update database 
    hostdir=sys.argv[1]
    os.chdir(hostdir)
    database=json.load(open('actions.json'))
    action_log=database['action log']

    action={
        'action': 'weather.py',
        'date': get_date(),
        'meta': [[], speak_text, ''],
    }

    action_log.append(action)
    database['action log']=action_log

    jsonfile=open('actions.json','w')
    json.dump(database,jsonfile)
    jsonfile.close()

