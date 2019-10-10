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
##                       CARBON_CALCULATOR.PY                               ##
##############################################################################

Calculate your carbon footprint with your voice. This will make it easy to 
baseline users and calculate their own carbon footprints. 
'''

##############################################################################
##                           IMPORT STATEMENTS                              ##
##############################################################################

import requests, time, random, webbrowser, datetime, platform, sys, pygame, shutil
import ftplib, getpass, os, json, pyaudio, wave, smtplib, random, socket
import speech_recognition as sr_audio
from bs4 import BeautifulSoup
import pyttsx3 as pyttsx
import os, re, matplotlib
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.platypus import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.patches import Shadow
import numpy as np
from textblob import TextBlob
from PyPDF2 import PdfFileMerger, PdfFileReader
import numpy as np 
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email import encoders
import pandas as pd 

##############################################################################
##                            HELPER FUNCTIONS                              ##
##############################################################################

def send_email(username, password, to, subject, text, files=[]):

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Jim Schwoebel <signup@protea.earth>'
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text, 'html'))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        server = smtplib.SMTP("mail.protea.earth", 587)
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(username, to, msg.as_string())
        print('sent email!')
        server.quit()
        
    except:
        print('ERROR - sending email')


def create_message(html_message, description, target_email):

    ''' 
    Create a custom message based on % complete to incent a user to complete the surveys.
    This will be used in emails and will help to drive awareness of the incentives to 
    drive completion from week 0 to week 4.
    '''
    survey_title="Protea"
    survey_title_subtext="Connecting climate enthusiasts"
    survey_button_text='sign up now'
    current_link_url='http://protea.earth'
    unsubscribe_link='https://app.surveylex.com/surveys/47a8b060-ddfe-11e9-8872-a318f8d4f5fd'
    logo_url='http://protea.earth/sites/default/files/small_logo_1.png'

    # print(survey_title, survey_title_subtext, survey_button_text, current_link_url, unsubscribe_link)
    newmsg=html_message.replace('[SURVEY_MESSAGE_HTML]',description)
    newmsg=newmsg.replace('[SURVEY_TITLE]', survey_title)
    newmsg=newmsg.replace('[SURVEY_TITLE_SUBTEXT]', survey_title_subtext)
    newmsg=newmsg.replace('[SURVEY_BUTTON_TEXT]',survey_button_text)
    newmsg=newmsg.replace('[SURVEY_BUTTON_LINK]',current_link_url)
    newmsg=newmsg.replace('[UNSUBSCRIBE_LINK]',unsubscribe_link)
    newmsg=newmsg.replace('[REPLACE_WITH_REAL_LOGO]',logo_url)
    newmsg=newmsg.replace('[TARGET_EMAIL_ADDRESS]', target_email)
    newmsg=newmsg.replace('[EMAIL_PREVIEW_TEXT]', '')

    return newmsg

def speaktext(text):
    # speak to a user from a text sample
    engine=pyttsx.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.fiona')
    engine.say(text)
    engine.runAndWait()

def get_date():
    return str(datetime.datetime.now())

def playbackaudio(filename):
    # takes in a question and a filename to open and plays back the audio
    # file and prints on the screen the question for the user 
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

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

def clean_answer(answer):
    answer=answer.replace(' ','').replace('$','')
    # this is for intent querying 
    return answer

def ask(question, hostdir):
    speaktext(question)
    playbackaudio(hostdir+'/data/tone.wav')
    time.sleep(0.25)
    unique_sample='carbon_sample.wav'
    transcript_type = 'google'
    query_time=2
    sufficient=False
    record_to_file(os.getcwd(),unique_sample, query_time)
    transcript=transcribe_audio(unique_sample, hostdir, transcript_type)
    transcript=clean_answer(transcript)

    while sufficient==False:
        # just need yes/no answers and whether a number 
        # answers=['2', '50', '5', 'no', '1', 'yes', 'yes', '5', 'no', 'yes', '50']
        try:
            if transcript in ['yes','no']:
                sufficient=True
            elif int(transcript) == int(transcript):
                sufficient=True
        except:
            sufficient=False
            speaktext('Sorry, I did not get that. %s'%(question))
            playbackaudio(hostdir+'/data/tone.wav')
            time.sleep(0.25)
            record_to_file(os.getcwd(),unique_sample, query_time)
            transcript=transcribe_audio(unique_sample, hostdir, transcript_type)
            transcript=clean_answer(transcript)

    os.remove(unique_sample)
    print(transcript)
    return transcript

def make_report(footprint, footprintdelta):
    # load the data here 
    g=open('report.txt').read()

    if footprintdelta < 0:
        footprintdelta = str(footprintdelta) + ' less than'
    else:
        footprintdelta = str(footprintdelta) + ' greater than'

    footprint=str(footprint) + ' tons of CO2/year'

    g=g.replace('[INSERT_FOOTPRINT_HERE]', footprint)
    g=g.replace('[INSERT_FOOTPRINTDELTA_HERE]', footprintdelta)

    return report

# create a pdf 
def calculate_footprint(answers):
    # create carbon calculator 

    # initialize answers 
    answer_1 = answers[0]
    answer_2 = answers[1]
    answer_3 = answers[2]
    answer_4 = answers[3]
    answer_5 = answers[4]
    answer_6 = answers[5]
    answer_7 = answers[6]
    answer_8 = answers[7]
    answer_9 = answers[8]
    answer_10 = answers[9]
    answer_11 = answers[10]

    # Electric bill = 7,252.76 kg CO2/year 
    # $0.1327/kwh/0.62 kg CO2/kwh = $0.214/kg CO2  - all we need to do is divide montly bill by this.
    # electric bill = (electric bill / people in household) / ($0.214/kgCo2)     
    
    try:
        answer_1=answer_1.replace('$','')
        electric_=(int(answer_2)/int(answer_1))*12/0.214
    except:
        print('--> error on electric CO2 calculation')

    # Flights = 602.448 kg CO2/year (if yes)
    # 286.88 kg CO2/flight 
    try:
        flight_= float(answer_3)*286.88 
    except:
        print('--> error on flight CO2 calculation')
        flight_=602.448

    # Transportation = 0.
    # 6,525.0 kg CO2/year (if drive only), 4,470.0 kg CO2/year (if mixed), 2,415.0 kg/year (if public)
    # 0.435 kg CO2/mile driving, 0.298 kg CO2/mile 50%/50% public transport and driving, and 0.161 kg CO2/mile (if public)
    # assume 220 working days/year (w/ vacation)
    try:
        if answer_4 == 'yes' and answer_6 == 'no':
            transportation_=float(answer_5)*1.61* 0.435*2*220

        elif answer_4 == 'yes' and answer_6 == 'yes':
            transportation_=float(answer_5)*1.61*0.298*2*220

        elif answer_4 == 'no' and answer_6 == 'yes':
            transportation_=float(answer_5)*1.61*0.161*2*220

        # Uber trips 
        # 45.27 kg CO2/year (average) 
        # 6 miles * 0.435 kg Co2/ mile = 2.61 kg CO2/trip 
        transportation_=transportation_+float(answer_8)*2.61*12

    except:
        print('--> error on transportation CO2 caclulation')
        transportation=4515.27

    # Vegetarian - assume footprint from food 
    try:
        if answer_9 == 'yes':
            food_=1542.21406
        # meat lover 
        elif answer_10 == 'yes':
            food_=2993.70964
        else:
            food_=2267.96185
    except:
        print('--> error on food CO2 calculation')
        food_=2267.96185

    # do you use amazon? --> retail, etc. 
    answer_11=answer_11.replace('$','').replace(' ','')
    retail_=0.1289*float(answer_11)

    footprint=electric_+flight_+transportation_+food_+retail_
    footprintbytype=[electric_, flight_, transportation_, food_, retail_]

    # compared to averages (kg Co2/year)
    footprint_avg = 14660.85
    footprintbytype_avg = [7252.76, 602.45, 4515.27, 2267.96, 22.41]

    footprint_delta=footprint-footprint_avg
    footprintbytype_delta=list(np.array(footprintbytype)-np.array(footprintbytype_avg))

    labels_footprint=['electric (kg Co2/year)', 'flight (kg Co2/year)', 'transportation (kg Co2/year)', 'food (kg Co2/year)', 'retail (kg Co2/year)']
    labels_footprintbytype = 'total kg Co2/year'

    return footprint, footprintbytype, footprint_delta, footprintbytype_delta, labels_footprint, labels_footprintbytype

# helper function to sort names
def sortnames(filelist):
    filelist.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
    return filelist 

def delete_pdfs():
    listdir=os.listdir()
    for i in range(len(listdir)):
        if listdir[i][-4:]=='.pdf':
            os.remove(listdir[i])
def cover_page(pdfname, surveyname, company, date, sampleid):
    c=canvas.Canvas(pdfname, pagesize=portrait(letter))

    logo='logo.png'
    c.drawImage(logo, 200, 500, width=200,height=100, preserveAspectRatio=True)

    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,460,"Carbon footprint report")
    c.setFont('Helvetica', 16, leading=None)
    c.drawCentredString(300,430,"%s"%(surveyname))
    c.drawCentredString(300,400,"%s"%(date[0:10]))

    # get .PNG from GDRIVE for text
    c.drawImage('cover_text.png', 50,200,width=510,height=200,preserveAspectRatio=True)
    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()

    return pdfname

def combine_pdfs():
    return ''

def make_graphs(individual_means, individual_means_2):

    # bar graph compared to average in each category (2 phase bar graph)
    labels = ['Electricity consumption (kwh * 1000)', '# of flights per year', '# commute miles per year (thousands)', '# of uber trips per year', 'food choice (tons of CO2 emissions/year)']
    population_means = [11.698, 2.1, 15, 7.86, 2.5]
    population_means=list(map(int,population_means))

    print(labels)
    print(individual_means)
    print(population_means)

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, individual_means, width, label='Your score', color='#5dcf60')
    rects2 = ax.bar(x + width/2, population_means, width, label='Average score', color='#595959')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by label')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical') #rotation='vertical', fontsize='x-small',
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    # plt.show()
    plt.savefig('bar.png', format="png")


    # bar 2 
    labels = ['electricity', 'flights', 'transportation', 'food', 'retail']
    population_means = [7252.76, 602.45, 4515.27, 2267.96, 22.41]
    population_means=list(map(int,population_means))
    individual_means_2=list(map(int, individual_means_2))

    print(labels)
    print(individual_means_2)
    print(population_means)

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, individual_means_2, width, label='Your score', color='#5dcf60')
    rects2 = ax.bar(x + width/2, population_means, width, label='Average score', color='#595959')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('kg Co2/year')
    ax.set_title('Scores by label')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical') #rotation='vertical', fontsize='x-small',
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    # plt.show()
    plt.savefig('bar_2.png', format="png")

    # % of contributions to your carbon footpint
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    labels = ['electricitiy', 'flights', 'transport', 'food', 'retail']
    fracs = [individual_means_2[0], individual_means_2[1], individual_means_2[2], individual_means_2[3], individual_means_2[4]]
    colors = ['#5dcf60', '#999999', '#A4efa4', '#595959', '#c3dbc3', '#70b170']
    explode = (0, 0, 0, 0, 0)

    # We want to draw the shadow for each pie but we will not use "shadow"
    # option as it does'n save the references to the shadow patches.
    pies = ax.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors)

    for w in pies[0]:
        # set the id with the label.
        w.set_gid(w.get_label())

        # we don't want to draw the edge of the pie
        w.set_edgecolor("none")

    for w in pies[0]:
        # create shadow patch
        s = Shadow(w, -0.01, -0.01)
        s.set_gid(w.get_gid() + "_shadow")
        s.set_zorder(w.get_zorder() - 0.1)
        ax.add_patch(s)

    # save
    plt.savefig('pi.png', format="png")


def make_bar_pdf(pdfname, logo):

    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,600,"Your carbon consumption relative to the average American (units)")
    c.drawImage(logo, 0, 200, width=600,height=300, preserveAspectRatio=True)
    #powered by.. for branding 
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(300,100,"Powered by:")
    c.drawImage('logo.png', 250, 30, width=100,height=100, preserveAspectRatio=True)
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,50,"http://www.protea.earth")

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()

def make_bar_2_pdf(pdfname, logo, footprint_delta):

    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,600,"Your carbon consumption relative to the average American (kg CO2)")
    c.drawImage(logo, 0, 250, width=600,height=300, preserveAspectRatio=True)

    # now draw the delta 
    c.setFont('Helvetica', 11, leading=None)
    if float(footprint_delta) <= 0:
        c.drawCentredString(300, 200, "Your carbon consumption is %s kg CO2 less than the average American."%(footprint_delta))
    else:
        c.drawCentredString(300, 200, "Your carbon consumption is %s kg CO2 over the average American."%(footprint_delta))

    #powered by.. for branding 
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(300,100,"Powered by:")
    c.drawImage('logo.png', 250, 30, width=100,height=100, preserveAspectRatio=True)
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,50,"http://www.protea.earth")

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()

def make_pie_pdf(pdfname):
    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    logo='pi.png'
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,600,"Your carbon consumption: by category")
    c.drawImage(logo, 0, 200, width=600,height=300, preserveAspectRatio=True)
    #powered by.. for branding 
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(300,100,"Powered by:")
    c.drawImage('logo.png', 250, 30, width=100,height=100, preserveAspectRatio=True)
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,50,"http://www.protea.earth")

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()


def make_getinvolved(pdfname):
    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,600,"Get involved")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,500,"● Global Warming of 1.5 degrees C || https://www.ipcc.ch/sr15/")
    c.drawCentredString(300,480,"● Empowering everyday people to become activists || https://www.climaterealityproject.org/")
    c.drawCentredString(300,460,"● EU Climate Knowledge and Innovation Community --> https://www.climate-kic.org/")
    c.drawCentredString(300,440,"● Measure Ecological Footprint || https://www.footprintnetwork.org/")
    c.drawCentredString(300,420,"● Technical climate solutions || https://www.drawdown.org/")
    c.drawCentredString(300,400,"● Sustainable textile supply chain || https://textileexchange.org/")
    c.drawCentredString(300,380,"● Student strike on Fridays || https://globalclimatestrike.net/")
    c.drawCentredString(300,360,"● Breakthrough Energy Coalition and Ventures || http://www.b-t.energy/")
    c.drawCentredString(300,340,"● Machine Learning for Climate Change || https://www.climatechange.ai/")
    c.drawCentredString(300,320,"● NASA: Facts around Climate Change || https://climate.nasa.gov/evidence/")

    #powered by.. for branding 
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(300,100,"Powered by:")
    c.drawImage('logo.png', 250, 30, width=100,height=100, preserveAspectRatio=True)
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,50,"http://www.protea.earth")

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()    


def make_lastpage(pdfname):
    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    # Protea signup
    c.drawImage('protea_signup.png', 100, 200, width=400,height=400, preserveAspectRatio=True)

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)
    c.save()    

def merge_pdfs():
    # get file list 
    listdir=os.listdir()
    # get only pdfs 
    pdflist=list()
    for i in range(len(listdir)):
        if listdir[i][-4:]=='.pdf':
            pdflist.append(listdir[i])
    # sort pdfs by number 
    pdflist=sortnames(pdflist)
    print(pdflist)

    merger = PdfFileMerger()
    for pdf in pdflist:
       merger.append(PdfFileReader(open(pdf, 'rb')))
    merger.write('merged.pdf')

def improvement_pdf(pdfname, truthlist):
    # areas of improvement (recommend areas of improvement)
    # how to be more involved

    c=canvas.Canvas(pdfname, pagesize=portrait(letter))
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(300,600,"Here are some recommendations to become a better climate citizen:")
    recommendation_list=['ask questions to learn more about climate issues',
                       'carpool with friends to/from work',
                       'collect climate data in the scientific community',
                       'take efforts to clean nature (e.g. like recycling off the street)',
                       'reflect upon being a better climate citizen',
                       'collect and use clean energy (e.g. wind or solar power)',
                       'eat less meat when you can going out',
                       'buy local produce from farmers markets on weekends',
                       'exercise instead of uber to work',
                       'make eco-friendly purchases (e.g. Allbirds shoes instead of Nike shoes)',
                       'participate in climate-related events',
                       'post articles about climate change on social media platforms',
                       'plant trees or take care of plants in your house',
                       'try to recycle and reduce waste when you can',
                       'take fewer flights and/or reduce your own transportation',
                       'turn off your air conditioning unit and use less electricity when you can',
                       'write scientific papers and/or blog posts on climate change issues',
                       'take showers for 5 minutes or less']

    recommendations=list()
    for i in range(len(truthlist)):
        if truthlist[i] == False:
            recommendations.append(recommendation_list[i])

    c.setFont('Helvetica', 11, leading=None)
    height=550
    for i in range(len(recommendations)):
        c.drawCentredString(300,height,recommendations[i])
        height=height-20

    #powered by.. for branding 
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(300,100,"Powered by:")
    c.drawImage('logo.png', 250, 30, width=100,height=100, preserveAspectRatio=True)
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(300,50,"http://www.protea.earth")

    #wave looking thing on front page
    c.drawImage('footer.png', -100,-35,width=800,height=100,preserveAspectRatio=True)

    c.save()

##############################################################################
##                            MAIN SCRIPT                                   ##
##############################################################################

# # update database 
hostdir=sys.argv[1]

##############################################################################
###                       CARBON FOOTPRINT Q/A                              ##
##############################################################################

speaktext('please enter your email on the screen so we can send you a report')
email=input('what is your email? \n')

# example = 2 
question_1 = 'How many people are in your household?'
answer_1=ask(question_1, hostdir)
# example = 50 
question_2 = 'What is your electric bill (in dollars) monthly?'
answer_2=ask(question_2, hostdir)
# example = 5 
question_3 = 'How many flights do you take per year?'
answer_3=ask(question_3, hostdir)
# example = no 
question_4 = 'Do you own a car?'
answer_4=ask(question_4, hostdir)
# example = 1 
question_5 = 'What is your average distance to commute to/from work in miles - for example 21?'
answer_5=ask(question_5, hostdir)
# example = yes
question_6= 'Do you use public transportation?'
answer_6=ask(question_6, hostdir)
# example = yes 
question_7 = 'Do you use uber or another ride sharing platform like Lyft?'
answer_7=ask(question_7, hostdir)
if answer_7 == 'yes':
    # example = 5
    question_8 = "How many ride-sharing trips do you complete per month?"
    answer_8 =ask(question_8, hostdir)
else:
    answer_8 = '0'

# example = yes
question_9 = 'Are you a vegetarian?'
answer_9=ask(question_9, hostdir)
# example = no
question_10= 'Do you eat meat more than 3 times each week?'
answer_10=ask(question_10, hostdir)
# example = 50
question_11 = 'How much money do you spend on Amazon per month in US dollars - for example, fifty dollars?'
answer_11 =ask(question_11, hostdir)

# now consolidate and calculate carbon footprint
questions=[question_1, question_2, question_3, question_4, question_5, 
           question_6, question_7, question_8, question_9, question_10, question_11]

answers=[answer_1, answer_2, answer_3, answer_4, answer_5,
         answer_6, answer_7, answer_8, answer_9, answer_10, answer_11]

# -----------------
# FOR TESTING ONLY 
# email='js@neurolex.co'
# answers=['2', '50', '5', 'no', '1', 'yes', 'yes', '5', 'no', 'yes', '50']
# answer_1='2'
# answer_2='50'
# answer_3='5'
# answer_4='no'
# answer_5='1'
# answer_6='yes'
# answer_7='yes'
# answer_8='5'
# answer_9='no'
# answer_10='yes'
# answer_11='50'
# -----------------

## report on recommendations pop up + saved in directory
footprint, footprintbytype, footprint_delta, footprintbytype_delta, labels_footprint, labels_footprintbytype =calculate_footprint(answers)

data = {'email': email,
        #'questions': questions,
        'answers': answers,
        'footprint': footprint,
        'footprintbytype': footprintbytype,
        'footprint_delta': footprint_delta,
        'footprintbytype_delta': footprintbytype_delta,
        'labels_footprint': labels_footprint,
        'labels_footprintbytype': labels_footprintbytype}

print(data)

# compared to averages 
# footprint_avg = 14642.40 kg Co2/year 
# footprintbytype_avg = [7252.76, 602.45, 4,4515.27, 2267.96]

########################################################
##              Now create the PDF                    ##
########################################################

curdir=os.getcwd()
os.chdir('assets')
html_message=open('msg.html').read()
description=open('description.txt').read()
os.chdir(curdir)

tempdir='tempdir'
try:
    os.mkdir(tempdir)
    os.chdir(tempdir)
except:
    shutil.rmtree(tempdir)
    os.mkdir(tempdir)
    os.chdir(tempdir)

# copy required assets
shutil.copy(curdir+'/assets/protea_signup.png', os.getcwd()+'/protea_signup.png')
shutil.copy(curdir+'/assets/cover_text.png', os.getcwd()+'/cover_text.png')
shutil.copy(curdir+'/assets/footer.png', os.getcwd()+'/footer.png')
shutil.copy(curdir+'/assets/logo.png', os.getcwd()+'/logo.png')
shutil.copy(curdir+'/assets/main_contributors.png', os.getcwd()+'/main_contributors.png')

# Now make all the .PDF pages 
print(footprintbytype[3])
# individual_means = ['Electricity consumption (kwh * 1000)', '# of flights per year', '# of driven miles/year (thousands)', '# of uber trips/year', 'food choice (tons of CO2 emissions/year)']
if answer_4 == 'yes' and answer_6 == 'no':
    individual_means = [(int(answer_2)/0.1327)*12/1000, int(answer_3), int(answer_5)*220*2/1000, int(answer_8)*12, footprintbytype[3]/1000]
elif answer_4 == 'yes' and answer_6 == 'yes':
    individual_means = [(int(answer_2)/0.1327)*12/1000, int(answer_3), int(answer_5)*220*2/1000, int(answer_8)*12,  footprintbytype[3]/1000]
elif answer_4 == 'no' and answer_6 == 'yes':
    individual_means = [(int(answer_2)/0.1327)*12/1000, int(answer_3), int(answer_5)*220*2/1000, int(answer_8)*12, footprintbytype[3]/1000]
else:
    individual_means = [(int(answer_2)/0.1327)*12/1000, int(answer_3), 0, int(answer_8)*12, footprintbytype[3]/1000]

individual_means=list(map(int,individual_means))

#['electric (kg Co2/year)', 'flight (kg Co2/year)', 'transportation (kg Co2/year)', 'food (kg Co2/year)', 'retail (kg Co2/year)']
truthlist=[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
delete_pdfs()
cover_page('1.pdf', email, 'User', str(datetime.datetime.now()), '100')
make_graphs(individual_means, footprintbytype)
make_bar_pdf('2.pdf', 'bar.png')
make_bar_2_pdf('3.pdf', 'bar_2.png', str(footprint_delta))
make_pie_pdf('4.pdf')
improvement_pdf('5.pdf', truthlist)
make_getinvolved('6.pdf')
shutil.copy(curdir+'/assets/7.pdf', os.getcwd()+'/7.pdf')
make_lastpage('8.pdf')
merge_pdfs()
filename='footprint_report.pdf'
os.rename('merged.pdf', filename)
os.system('open %s'%(filename))

#########################################
##             SEND EMAILS              ##
##########################################
# username and password 
username=os.environ['PROTEA_EMAIL_ADDRESS']
password=os.environ['PROTEA_EMAIL_PASSWORD']

# read html message 
message=create_message(html_message, description, username)
subject='Protea: connecting climate enthusiasts'
os.chdir(curdir+'/tempdir/')
send_email(username, password, [email], subject, message, [os.getcwd()+'/'+filename])

# update database 
os.chdir(hostdir)
database=json.load(open('actions.json'))
action_log=database['action log']

action={
    'action': 'carbon_footprint.py',
    'date': get_date(),
    'meta': data,
}

action_log.append(action)
database['action log']=action_log

jsonfile=open('actions.json','w')
json.dump(database,jsonfile)
jsonfile.close()

speaktext('Here is your report. I also just emailed this to you. Cheers!')

#####################################################
###         ARCHIVED FOR FUTURE DEVELOPMENT        ## 
#####################################################

# question_3 = 'How much is your water bill each month?'
# answer_3=ask(question_3, hostdir)

#####################################################
###     ACTIONS ### (suggested to take)            ## 
#####################################################

# speaktext('please answer yes or no to the following questions.')
# time.sleep(1)
# question_9 = 'Do you ask questions to learn more about climate issues?'
# answer_9=ask(question_9, hostdir)
# question_10 = 'Do you carpool with friends to/from work?'
# answer_10=ask(question_10, hostdir)
# question_11 = 'Do you collect climate data in the scientific community?'
# answer_11=ask(question_11, hostdir)
# question_11 = 'Do you take efforts to clean nature; for example, removing trash off the street?'
# answer_11=ask(question_11, hostdir)
# question_12 = 'Do you reflect upon how how you can be a better climate citizen?'
# answer_12=ask(question_12, hostdir)
# question_13 = 'Do you collect and use clean energy like solar or wind power?'
# answer_13=ask(question_13, hostdir)
# question_14 = 'Do you eat less meat when you can?'
# answer_14=ask(question_14, hostdir)
# question_15 = 'Do you buy local produce; for example, at the farmers market on weekends?'
# answer_15=ask(question_15, hostdir)
# question_16 = 'Do you exercise instead of uber to work?'
# answer_16=ask(question_16, hostdir)
# question_17 = 'Do you make eco-friendly purchases - for example, buying Allbirds shoes versus Nike shoes?'
# answer_17=ask(question_17, hostdir)
# question_18 = 'Do you participate in climate-related events?'
# answer_18=ask(question_18, hostdir)
# question_19 = 'Do you post articles about climate change on social media platforms?'
# answer_19=ask(question_19, hostdir)
# question_20 = 'Do you plant trees or take care of plants in your house?'
# answer_20=speaktext(question_20, hostdir)
# question_21 = 'Do you try to recycle and reduce waste?'
# answer_21=ask(question_21, hostdir)
# question_22 = 'Do you try to take less flights and/or reduce your own transportation?'
# answer_22=ask(question_22, hostdir)
# question_23 = 'Do you turn off your air conditioning unit and use less electricity when you can?'
# answer_23=ask(question_23, hostdir)
# question_24 = 'Do you write scientific papers or blog posts on climate change issues?'
# answer_24=ask(question_24, hostdir)
# question_25 = 'Do you take showers for less than 5 minutes?'
# answer_25=ask(question_25, hostdir)
