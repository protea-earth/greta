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
##                              FACT_FACTS.PY                               ##
##############################################################################

This script reads a random fact from a set of facts related to climate change.
'''
##############################################################################
##                           IMPORT STATEMENTS                              ##
##############################################################################

import random, os, sys, json, datetime

##############################################################################
##                            HELPER FUNCTIONS                              ##
##############################################################################

def get_date():
    return str(datetime.datetime.now())

def speaktext(hostdir,text):
    # speak to user from a text sample (tts system)  
    curdir=os.getcwd()
    os.chdir(hostdir+'/actions') 
    os.system("python3 speak.py '%s'"%(str(text)))
    os.chdir(curdir)

##############################################################################
##                            MAIN SCRIPT                                   ##
##############################################################################
    
hostdir=sys.argv[1]
os.chdir(hostdir)

# website source below
# https://www.conserve-energy-future.com/various-climate-change-facts-php.php
facts=['The global temperature on an average has increased by 0.6 to 1 degree Celsius till the 20th century.',
       'The United States constitutes 5 percent of the world population and contributes to 22 percent of world’s carbon emission.',
       'Around 15 percent of the carbon released in the environment is due to deforestation and change in use of land.',
       'The golden Toad is the first species to go extinct due to climate change.',
       'Vehicles like cars and truck contribute to 20 percent of carbon emissions in the United States.',
       'Air conditions and heating elements consume 50 percent of electricity in America.',
       'Hurricanes, droughts and coral deaths are few of the natural disasters  caused due to climate change.',
       'Climate change enhances the spread of pests that causes life threatening diseases like dengue, malaria, Lyme disease etc.',
       'The hottest years have been experienced since 1990 till 1997. The warmest years have been from 2005-2010.',
       'The number of climate change related incidents have increase four fold between 1980 and 2010.',
       'Land use change and deforestation contributes to 15 percent of carbon emission every year.',
       'The climate change scenario was much stable before the industrial revolution and has been rapidly changing since then. Today the reality is that climate change is going to get worse than yesterday.',
       'A separate budget of US$ 40 million has been allotted for climate change research since 1990.',
       'Due to the greenhouse effect, the average temperature of the earth is 15 degrees rather than -18 degrees without the greenhouse effect.',
       'Carbon dioxide constitutes only 3.6 percent of total greenhouse gases out of which 0.12 percent is attributed to human activities.',
       'Carbon dioxide is not the only contributing gas towards climate change. Other gases like methane and nitrous oxide are far more dangerous than carbon dioxide alone.',
       'The UN Intergovernmental Panel on Climate Change (IPCC) is a leading body fighting against climate change. This body is a political organization however and not a scientific body.',
       'The Kyoto Protocol, an organization formed to analyze and fight against climate change will cost more than 100 trillion dollars thus making developing and underdeveloped communities to participate.',
       'According to World Food Program (WPF.org), by 2015, the number of people affected by climate change disasters could reach 375 million per year.',
       'Over the last 50 years, the concentration of carbon dioxide in the atmosphere has increase by 30%  due to burning of fossil fuels and greenhouse gas emissions like carbon dioxide, nitrous oxide and other gases, trapping more heat in the lower atmosphere.',
       'The rising temperatures will cause more deaths not due to natural reasons but as a result of overheating and rapid spread of deadly diseases.',
       'Classic examples of climate change can be seen by the damages causes due to heavy rains and disasters like Hurricane Katrina in 2005.',
       'Above six hundred thousand deaths occur worldwide every year due to climate change. 95 percent of these deaths take place in developing countries.',
       'Climate change can have serious health impacts such as heat stress, extreme cold which can cause major deaths due to heart diseases.',
       'In two thosand three, around seventy thousand deaths have occurred in Europe alone due to diseases caused by rising temperatures.',
       'Pollen and aeroallergen high levels also lead to rising temperature. This can cause asthma which effects 300 million people worldwide.',
       'Climate change is rapidly causing coastal flooding and displacement of people. Floods further cause major damages by injuring and killing people. They can even cause deadly diseases by spreading infection and vector borne diseases.',
       'Due to water shortages, the transportation of water will cause it to contaminate and make it even more deadly by spreading diseases.',
       'Malaria, diarrhoea and malnutrition are diseases are water borne diseases that have caused more than three million deaths since 2005, one third of these deaths are in Africa.',
       'Steps to reduce greenhouse gases can help save the negative health impacts. Promoting safe public transportation and active activities like walking or use public transport can help reduce carbon emissions. This can also help to cut down traffic, air pollution and thereby reducing cardiovascular diseases.',
       'Various countries have taken steps to reduce greenhouse gas emissions. This has led to positive health effects. Promoting green transportation and car pooling can help to reduce carbon emissions and improve public health.',
       'Depending upon the carbon emissions, a rise in temperature from one point one degree up to six point four degrees is expected by the end of this century.',
       'Over the next twenty years, global warming is expected to increase by zero point two degrees per decade.',
       'The effects of climate change can have a disastrous impact on our planet Earth. High temperatures, loss of wildlife species, increase in sea level, changes in rainfall patterns, heat waves, stronger storms, wildfires and shrinking of arctic ice are few of the dangerous effects of climate change.',
       'According to a recent report by Oxfam, climate change could push food prices by 50-60 percent more by twenty thirty.',
       'Only about nine percent of all plastic ever made has likely been recycled with 12 percent of all plastic waste having been incinerated. The remaining 79 percent has accumulated in either landfill or the natural environment if not still in use.',
       'One million seabirds and one hundred thousand marine mammals die each year from plastic pollution in our oceans.',
       'In one study by the U.S. Centres for Disease Control, nearly ninety-three percent of people tested positive for BPA (a potentially harmful chemical present in plastic products).',
       'Every time you use a dryer, you add about 5 pounds of carbon dioxide to the atmosphere. While hanging up your clothes takes a little more time, the savings for both your wallet and the environment are well worth it.']

# tell a random joke 
randomint=random.randint(0,len(facts)-1)
fact = facts[randomint]
speaktext(hostdir, 'Did you know that ' + fact)

# update database
database=json.load(open('actions.json'))
action_log=database['action log']

action={
    'action':'facts.py',
    'date': get_date(),
    'meta': [fact],
}

action_log.append(action)
jsonfile=open('actions.json','w')
json.dump(database,jsonfile)
jsonfile.close()


