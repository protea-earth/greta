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
##                                NEWS.PY                                   ##
##############################################################################

This pulls up a news source related to climate change - be it a podcast, video,
or article. This thus can help you keep up-to-date on various climate change 
issues from RSS feeds, and can be expanded upon easily into the future.
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

##############################################################################
##                            MAIN SCRIPT                                   ##
##############################################################################

# get a random news outlet to not spam all sites 

newstype=4
# random.randint(0,3)

podcasts=['http://feeds.feedburner.com/Greenbiz350',
          'http://feeds.feedburner.com/TheEnergyTransitionShow',
          'http://feeds.soundcloud.com/users/soundcloud:users:244123832/sounds.rss',
          'http://feeds.soundcloud.com/users/soundcloud:users:235660424/sounds.rss',
          'http://mptypodcast.libsyn.com/rss',
          'http://audio.commonwealthclub.org/audio/podcast/climateone.xml']

RSS_feeds=['https://www.youtube.com/feeds/videos.xml?user=NASAClimate',
           'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/subject/global-warming-climate-change/rss.xml',
           'https://climate.mit.edu/rss.xml',
           'https://www.theguardian.com/environment/climate-change/rss']

if newstype == 0:
    g=feedparser.parse(RSS_feeds[0])
    source = 'NASA'
    mediatype= 'YouTube video'
elif newstype == 1:
    g=feedparser.parse(RSS_feeds[1])
    source = 'The New York Times'
    mediatype= 'article'
elif newstype == 2:
    g=feedparser.parse(RSS_feeds[2])
    source = 'The MIT Climate Initiative'
    mediatype= 'article'
elif newstype == 3:
    g=feedparser.parse(RSS_feeds[3])
    source = 'The Guardian'
    mediatype= 'article'
elif newstype == 4: 
    g=feedparser.parse(random.choice(podcasts))
    source = ''
    mediatype='podcast'

g=g['entries']
links = list()
titles = list()
for i in range(len(g)):
    try:
        links.append(g[i]['link'])
        titles.append(g[i]['title'])
    except:
        pass 

# get index, link, and title
index=random.randint(0,len(links)-1)
link=links[index]
title=titles[index]

speak_text='perhaps check out this %s posted by '%(mediatype) + source +'. '
speaktext(speak_text)
webbrowser.open(link)
speaktext(title)

# update database 
hostdir=sys.argv[1]
os.chdir(hostdir)
database=json.load(open('actions.json'))
action_log=database['action log']

action={
    'action': 'news.py',
    'date': get_date(),
    'meta': [speak_text, link],
}

action_log.append(action)
database['action log']=action_log

jsonfile=open('actions.json','w')
json.dump(database,jsonfile)
jsonfile.close()


