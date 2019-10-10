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
##                             MUSIC_SONG.PY                                ##
##############################################################################

This script selects a random song that is inspired by climate change. This list 
of songs came from: https://conbio.org/images/content_groups/SSWG/climatechangesongs.pdf
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
songs={'https://www.youtube.com/watch?v=s3aVTJZ5ZWQ':'Sharon Abreu - Change in the Climate',
       'https://www.youtube.com/watch?v=4PpGdztrhWU':'Agnostic Front – “Toxic Shock”',
       'https://www.youtube.com/watch?v=iiHX2653XPE':'Alabama – “Pass It On Down”',
       'https://www.youtube.com/watch?v=gW1gwOriUKQ':'Linda Allen – “We Are the Rainbow Sign”',
       'https://www.youtube.com/watch?v=aBfxSxAfdPQ':'https://www.youtube.com/watch?v=aBfxSxAfdPQ',
       'https://www.youtube.com/watch?v=ovXUmXaxgN4':'Arrested Development – “Children Play With Earth”',
       'https://www.youtube.com/watch?v=4mslj4wVS3g':'Bad Religion – “Kyoto Now!”',
       'https://www.youtube.com/watch?v=xuk0z3bdYBU':'Ann Bailey – “Excuse Me Sir, That’s My Aquifer”',
       'https://www.youtube.com/watch?v=YpJ-pLYmDHU':'The Beach Boys – “Don’t Go Near the Water”',
       'https://www.youtube.com/watch?v=Ha1OS04YgGw':'Adrian Belew – “Burned By the Fire We Make”',
       'https://www.youtube.com/watch?v=fNfwZ64I3cw':'Adrian Belew – “Hot Zoo”',
       'https://www.youtube.com/watch?v=yBV3XnOAua8':'Adrian Belew – “House of Cards”',
       'https://www.youtube.com/watch?v=YqotFbF6sEE':'Adrian Belew – “The Lone Rhinoceros”  ',
       'https://www.youtube.com/watch?v=iiFdrepnhX4':'Adrian Belew – “Men in Helicopters”',
       'https://www.youtube.com/watch?v=pLIQ5jU2JXo':'Adrian Belew – “Modern Man Hurricane Blues”',
       'https://www.youtube.com/watch?v=DD_0vheB0b8':'Adrian Belew – “Only a Dream”',
       'https://www.youtube.com/watch?v=3ocdvVooZGk':'The Bears – “Save Me”',
       'https://www.youtube.com/watch?v=FYXJ6XAP7UY':'Dan Berggren – “The Power from Above”',
       'https://www.youtube.com/watch?v=muUZjovOFRg':'Blue Oyster Cult – “Godzilla”',
       'https://www.youtube.com/watch?v=7uxrHO9_66g':'Ken Boothe – “The Earth Dies Screaming”',
       'https://www.youtube.com/watch?v=tjAhlh23zPM':'Billy Bragg – “The Price of Oil”',
       'https://www.youtube.com/watch?v=-Glf1Hi-OMo':'Jon Braman – “The Weather”',
       'https://www.youtube.com/watch?v=JTAMPbRE8ZQ':'Jon Braman – “Time Has Come”  ',
       'https://www.youtube.com/watch?v=StKac3O2VMg':'Breaking Laces – “Global Warming Day”',
       'https://www.youtube.com/watch?v=bfF0x8e38Kg':'Jackson Browne – “Before the Deluge”',
       'https://www.youtube.com/watch?v=qKGTaplzmV4':'Jackson Browne – “Doctor My Eyes”',
       'https://www.youtube.com/watch?v=IjGHwGkFIFw':'Jimmy Buffett ‐ “Volcano”',
       'https://www.youtube.com/watch?v=Ypb54RBGzqE':'T Bone Burnett – “Humans from Earth”',
       'https://www.youtube.com/watch?v=aGLOh3ZHofk':'The Byrds – “Hungry Planet”',
       'https://www.youtube.com/watch?v=K3DRkVjuqmc':'Cake – “Carbon Monoxide”',
       'https://www.youtube.com/watch?v=-3wFxuuG-y0':'Cake – “Long Line of Cars”',
       'https://www.youtube.com/watch?v=IyPhakY1mX0':'Capitol Steps - God Bless My SUV',
       'https://www.youtube.com/watch?v=X0rzxVgqShU':'Johnny Cash - Dont Go Near the Water',
       'https://www.youtube.com/watch?v=cJ5V3OZdIZM':'Cerrone – “Supernature”',
       'https://www.youtube.com/watch?v=KeqDHppFwHE':'Tom Chapin – Various songs from the albums “This Pretty Planet”',
       'https://www.youtube.com/watch?v=iTnv4cXQNEw&list=PLJaxwXpk86i4LiOJd0A_Y5Ryj8-bBHPf2':'Darryl Cherney',
       'https://www.youtube.com/watch?v=63aLrOkTN7c':'Jimmy Cliff – “Save Our Planet Earth”',
       'https://www.youtube.com/watch?v=iwZZf5oB4l4':'Bruce Cockburn – “Beautiful Creatures”',
       'https://www.youtube.com/watch?v=SztTrfVqiG8':'Bruce Cockburn – “If a Tree Falls”',
       'https://www.youtube.com/watch?v=02TUsZzF6es':'Bruce Cockburn – “Last Night of the World”',
       'https://www.youtube.com/watch?v=kybkiiAKMOY':'Bruce Cockburn – “The Trouble with Normal”',
       'https://www.youtube.com/watch?v=L6Lpx6JIMmk':'Bruce Cockburn – “Wondering Where the Lions Are”',
       'https://www.youtube.com/watch?v=5-wl7Xk5FoY':'Coldcut – “Timber”',
       'https://www.youtube.com/watch?v=66W0D7HMD0E':'Cousteau – “Last Good Day of the Year”',
       'https://www.youtube.com/watch?v=5BmEGm-mraE':'Creedence Clearwater Revival – “Bad Moon Rising”',
       'https://www.youtube.com/watch?v=qoek1e8t2K4':'David Crosby and Graham Nash – “To the Last Whale”',
       'https://www.youtube.com/watch?v=juUufyYNKNM':'Crosby, Stills, and Nash – “Barrel of Pain”',
       'https://www.youtube.com/watch?v=w-EgtzodyeE':'Crosby, Stills, Nash, and Young  – “Clear Blue Skies”',
       'https://www.youtube.com/watch?v=6M-IRux3M_A':'Miley Cyrus – “Wake Up America”',
       'https://www.youtube.com/watch?v=roDXSHSEuoo':'Daughtry – “What About Now?”',
       'https://www.youtube.com/watch?v=9ewDZd2Heac':'Dead Kennedys – “Cesspools in Eden”',
       'https://www.youtube.com/watch?v=WDG8AojhnVs':'Dead Kennedys – “Hop With the Jet Set”',
       'https://www.youtube.com/watch?v=etHXCIhCWQM':'Dead Kennedys – “Kepone Factory”  ',
       'https://www.youtube.com/watch?v=8iYMtyy8kEo':'Dead Kennedys – “Moon Over Marin”',
       'https://www.youtube.com/watch?v=whgQ_HDnfXw':'Death Cab for Cutie – “Why You’d Want To Live Here”',
       'https://www.youtube.com/watch?v=G1XEYZEU0Tg':'Deee‐Lite – “I Had a Dream I Was Falling Through a Hole In the Ozone Layer”',
       'https://www.youtube.com/watch?v=q3EE83q6tzw':'John Denver – “Calypso”',
       'https://www.youtube.com/watch?v=LGnWuwAJ6bM':'John Denver – “Earth Day Every Day”',
       'https://www.youtube.com/watch?v=utHRwPYtkwE':'John Denver – “To the Wild Country”',
       'https://www.youtube.com/watch?v=1QR9cz7IdW0':'Depeche Mode – “The Landscape is Changing”',
       'https://www.youtube.com/watch?v=vZwac1lqOGI':'Bo Diddley – “Pollution”',
       'https://www.youtube.com/watch?v=sS0d6M112Ow':'Ani DiFranco – “Tamboritza Lingua”',
       'https://www.youtube.com/watch?v=Xra7sDcdOMI':'Dire Straits – “My Parties”',
       'https://www.youtube.com/watch?v=wy_cFHs5xb4':'The Doors – “Ship of Fools”',
       'https://www.youtube.com/watch?v=MSP-l9Szu5M':'Donavon Frankenreiter – “The Way it Is”',
       'https://www.youtube.com/watch?v=JVsdmYAYiD0':'Dramarama – “What Are We Gonna Do?”',
       'https://www.youtube.com/watch?v=0QoN7a3rSK4':'Jorge Drexler – “Disneylandia”',
       'https://www.youtube.com/watch?v=8NF6Qa84mno':'Duran Duran – “Planet Earth”',
       'https://www.youtube.com/watch?v=T5al0HmR4to':'Bob Dylan – “A Hard Rain’s A‐Gonna Fall”',
       'https://www.youtube.com/watch?v=Wpb2ISYWenk':'Bob Dylan – “Dark Eyes”',
       'https://www.youtube.com/watch?v=egSoj3g99gY':'Bob Dylan – “Everything is Broken”',
       'https://www.youtube.com/watch?v=7fdqF4XIUsE':'Bob Dylan – “High Water”',
       'https://www.youtube.com/watch?v=Bkw8-QtiM1k':'Bob Dylan – “License to Kill”',
       'https://www.youtube.com/watch?v=YQC_UnTPhho':'Bob Dylan – “Talkin’ Bear Mountain Picnic Massacre Blues”',
       'https://www.youtube.com/watch?v=L9EKqQWPjyo':'Bob Dylan – “Things Have Changed”',
       'https://www.youtube.com/watch?v=DHCnT5PT-ew':'Earth Mama – various songs (www.earthmama.org)  ',
       'https://www.youtube.com/watch?v=t4PnH3_WNTY':'Eddie – “Sentado na Beira do Rio”',
       'https://www.youtube.com/watch?v=wCczPpmX-zA':'Emerson, Lake, and Palmer – “Black Moon”',
       'https://www.youtube.com/watch?v=JUVqUz8m2PQ':'Melissa Etheridge – “I Need To Wake Up”',
       'https://www.youtube.com/watch?v=ouQiTstEpZQ':'Flipper – “Love Canal”',
       'https://www.youtube.com/watch?v=5HhUBdQzEqU':'Steve Forbert – “The Oil Song”',
       'https://www.youtube.com/watch?v=GEc7nQZi2Og':'Peter Gabriel – “Down to Earth”',
       'https://www.youtube.com/watch?v=vb7htoJAK7g':'Peter Gabriel – “Here Comes the Flood”',
       'https://www.youtube.com/watch?v=FkLTwX0duY4':'Peter Gabriel – “Red Rain”',
       'https://www.youtube.com/watch?v=Eqfm3KPwd14':'Marvin Gaye – “Mercy Mercy Me (The Ecology Song)”',
       'https://www.youtube.com/watch?v=F9NNawUy7Do':'Gilberto Gil – “A Novidade”',
       'https://www.youtube.com/watch?v=tcj6FtEbFhw':'Girlyman – “Amaze Me”',
       'https://www.youtube.com/watch?v=uSer4wdHvm8':'Grandaddy – “Nature Anthem”',
       'https://www.youtube.com/watch?v=NFSSqCxXpGg':'Grateful Dead – “Throwing Stones”',
       'https://www.youtube.com/watch?v=r5EXKDlf44M':'Green Day – “Boulevard of Broken Dreams”',
       'https://www.youtube.com/watch?v=jQYKJaWuj0Y':'Woody Guthrie – “Dust Bowl Blues”',
       'https://www.youtube.com/watch?v=zZEGhcekgHw':'Ben Harper – “Excuse Me Mr.”',
       'https://www.youtube.com/watch?v=I9TMesYlseY':'Cory Harris – “Fish Ain’t Bitin’”',
       'https://www.youtube.com/watch?v=M3Txzkb_xz4':'Jimi Hendrix – “Earth Blues”',
       'https://www.youtube.com/watch?v=VNSBj8yu0ZI':'Don Henley – “Goodbye to a River”',
       'https://www.youtube.com/watch?v=cBSeEcFiTWA':'Bruce Hornsby – “Look Out Any Window”',
       'https://www.youtube.com/watch?v=MB21q1MTDjA':'Hot Buttered Rum – (various songs, albums)',
       'https://www.youtube.com/watch?v=TAe1N33bM0U':'The Instigators – “Clean Air”',
       'https://www.youtube.com/watch?v=VQPrufzyd1I':'Iron Butterfly – “Slower Than Guns”',
       'https://www.youtube.com/watch?v=mj3MfUR35CM':'Michael Jackson – “Cry”',
       'https://www.youtube.com/watch?v=XAi3VTSdTxU':'Michael Jackson – “Earth Song”',
       'https://www.youtube.com/watch?v=BWf-eARnf6U':'Michael Jackson – “Heal the World”',
       'https://www.youtube.com/watch?v=PivWY9wn5ps':'Michael Jackson – “The Man in the Mirror”',
       'https://www.youtube.com/watch?v=cxcjA01oGyw':'Joe Jackson – “Obvious Song”',
       'https://www.youtube.com/watch?v=pBWW04xF_84':'James – “Greenpeace”',
       'https://www.youtube.com/watch?v=q9IdNYGRigk':'James – “What For?”',
       'https://www.youtube.com/watch?v=eo7iwlMFPrM':'Jamiroquai – “When You Gonna Learn”',
       'https://www.youtube.com/watch?v=Kjp1vPLkBBQ':'Jamiroquai – “Emergency on Planet Earth”',
       'https://www.youtube.com/watch?v=d7epbdQ4YYI':'Jefferson Airplane – “Eskimo Blue Day”',
       'https://www.youtube.com/watch?v=vCR4_985wq4':'Jethro Tull – “Jack‐in‐the‐Green”',
       'https://www.youtube.com/watch?v=qZxaH8SQgs8':'Jethro Tull – “North Sea Oil”',
       'https://www.youtube.com/watch?v=baM62gOuqg8':'Jethro Tull – “The Whaler’s Dues”',
       'https://www.youtube.com/watch?v=YmIbJ81MbKI':'Jethro Tull – “Wond’ring Again”',
       'https://www.youtube.com/watch?v=7rItHumCNNQ':'Jack Johnson – “Gone”',
       'https://www.youtube.com/watch?v=TTCaZVIUNp0':'Jack Johnson – “The Horizon Has Been Defeated”',
       'https://www.youtube.com/watch?v=USo_vH1Jz7E':'Jack Johnson – “The 3 Rs”',
       'https://www.youtube.com/watch?v=TtJIu0Tylb0':'Jack Johnson – “Traffic in the Sky”',
       'https://www.youtube.com/watch?v=zxqEIhyQvwA':'Jorge Ben Jor – “Luz Polarizada”  ',
       'https://www.youtube.com/watch?v=SbAdIFr2wJY':'Kansas – “Death of Mother Nature Suite”',
       'https://www.youtube.com/watch?v=mNPTBdNSPjc':'The Aaron Katz Band – “Chlorine Christmas”',
       'https://www.youtube.com/watch?v=ehRHFTu5xi4':'The Kingston Trio – “Coal Tattoo”',
       'https://www.youtube.com/watch?v=aRHqs8SffDo':'The Kinks – “Apeman”',
       'https://www.youtube.com/watch?v=R8BT44GgbLw':'The Kinks – “Demolition”',
       'https://www.youtube.com/watch?v=OJjai_pxCrQ':'The Kinks – “Gallon of Gas”',
       'https://www.youtube.com/watch?v=d7CzHFWsXQQ':'The Kinks – “Mountain Woman”',
       'https://www.youtube.com/watch?v=wGZtlNZl780':'The Kinks – “Preservation”',
       'https://www.youtube.com/watch?v=320yV68ab5c':'The Kinks – “Village Green”',
       'https://www.youtube.com/watch?v=rjym7r4GGrs':'The Kinks – “Wall of Fire”',
       'https://www.youtube.com/watch?v=nz_-KNNl-no':'Tom Lehrer – “Pollution”',
       'https://www.youtube.com/watch?v=ZSQVM9fCV7c':'Julian Lennon – “How Many Times?”',
       'https://www.youtube.com/watch?v=oGQiqq9N1jo':'Julian Lennon – “Salt Water”',
       'https://www.youtube.com/watch?v=eEwmfKhW5jk':'Liquid Blue – “Supernova”',
       'https://www.youtube.com/watch?v=5SPp1BLcBak':'Little Village (John Hiatt, Ry Cooder, et al.) – “Do You Want My Job”',
       'https://www.youtube.com/watch?v=rQZbB5CUXFI':'Kenny Loggins – “Conviction of the Heart”',
       'https://www.youtube.com/watch?v=LsYV0gkTUC4':'Kenny Loggins – “This Island Earth”  ',
       'https://www.youtube.com/watch?v=VChiKsQo534':'Jeff Lynne – “Save Me Now”',
       'https://www.youtube.com/watch?v=IQvizOhUWvw':'Dana Lyons – various songs from the album “I’d Go Anywhere to Fight For Oil To Lubricate the Red,',
       'https://www.youtube.com/watch?v=hmewV5iKnYU':'White, and Blue” (and other works, too).',
       'https://www.youtube.com/watch?v=S5-DC0NUY2w':'Joel Mabus – “Warmer Every Day”',
       'https://www.youtube.com/watch?v=i0TaOi7mQNo':'The Mammals – “Industrial Park”',
       'https://www.youtube.com/watch?v=HqFfA1rZ7XU':'Manfred Mann’s Earth Band – “Give Me the Good Earth”',
       'https://www.youtube.com/watch?v=NwDcf1PJXGI':'Manu Chao – “La Vacaloca”',
       'https://www.youtube.com/watch?v=eaVxcpefX-0':'Ziggy Marley – “Dragonfly”',
       'https://www.youtube.com/watch?v=0TrishCMmpc':'Massive Attack – “Hymn of the Big Wheel”',
       'https://www.youtube.com/watch?v=psIuidkkLjI':'Dave Matthews Band – “Don’t Drink the Water”',
       'https://www.youtube.com/watch?v=pvJZ2u5Za94':'Dave Matthews Band – “One Sweet World”',
       'https://www.youtube.com/watch?v=HQdphbEMmbY':'Dave Matthews Band – “Proudest  Monkey”https://www.youtube.com/watch?v=HQdphbEMmbY',
       'https://www.youtube.com/watch?v=pSPECzpKn4U':'Dave Matthews Band – “Too Much”',
       'https://www.youtube.com/watch?v=d1x7lDxHd-o':'John Mayall’s Bluesbreakers – “Nature’s Disappearing”',
       'https://www.youtube.com/watch?v=A1U4cnUxhK0':'Peter Mayer – various songs (http://www.petermayer.net/music/)',
       'https://www.youtube.com/watch?v=VMGOg8vB4Dc':'MC5 – “Over and Over”',
       'https://www.youtube.com/watch?v=knVq-rHzTyQ':'Kirsty McColl – “Maybe It’s Imaginary”',
       'https://www.youtube.com/watch?v=q_Co7JljBbE':'Country Joe McDonald – “Living in the Future in a Plastic Dome”',
       'https://www.youtube.com/watch?v=q_Co7JljBbE':'Country Joe McDonald – “Save the Whales”',
       'https://www.youtube.com/watch?v=GRKHTXCoJOk':'Roger McGuinn – “The Trees Are All Gone”',
       'https://www.youtube.com/watch?v=-WGcyRcqx2A':'Megadeath – “Countdown to Extinction”',
       'https://www.youtube.com/watch?v=joNzRzZhR2Y':'John Cougar Mellencamp – “Rain on the Scarecrow”',
       'https://www.youtube.com/watch?v=keLIiMi7ttI':'Midnight Oil – “Antarctica”',
       'https://www.youtube.com/watch?v=K4Tqf4xwPDg':'Midnight Oil – “Arctic World”',
       'https://www.youtube.com/watch?v=MjXa-wA180k':'Midnight Oil – “A Crocodile Cries”',
       'https://www.youtube.com/watch?v=OcKcjpSWmm0':'Midnight Oil – “Dreamworld”',
       'https://www.youtube.com/watch?v=owy1iAwToQw':'Midnight Oil – “Earth and Sun and Moon”',
       'https://www.youtube.com/watch?v=SjtxuMCdD1M':'Midnight Oil – “Feeding Frenzy”',
       'https://www.youtube.com/watch?v=dKLa6tFZeb8':'Midnight Oil – “Now or Never Land”',
       'https://www.youtube.com/watch?v=2LQXp7MLJ_A':'Midnight Oil – “Progress”',
       'https://www.youtube.com/watch?v=ljZW6V7GXiM':'Midnight Oil – “Renaissance Man”',
       'https://www.youtube.com/watch?v=IH5hBtgDVEs':'Midnight Oil – “River Runs Red”  ',
       'https://www.youtube.com/watch?v=m8CYDJ7kab8':'Midnight Oil – “Too Much Sunshine”',
       'https://www.youtube.com/watch?v=LcxdbZ5chcc':'Midnight Oil – “Truganini”',
       'https://www.youtube.com/watch?v=BS99cdhzWGo':'Bill Miller – “Sacred Ground”',
       'https://www.youtube.com/watch?v=VO0nfoV771s':'Ministry – “Breathe”',
       'https://www.youtube.com/watch?v=sZXQCs3rZtU':'Ministry – “Isle of Man”',
       'https://www.youtube.com/watch?v=GFB-d-8_bvY':'Joni Mitchell – “Big Yellow Taxi”',
       'https://www.youtube.com/watch?v=6i73a_6vUMQ':'Joni Mitchell – various songs from the album “Shine”',
       'https://www.youtube.com/watch?v=PR0ohbxwCcs':'Modest Mouse – “Convenient Parking”',
       'https://www.youtube.com/watch?v=ACfzcbS_0Qc':'Marilyn Monroe – “Heat Wave”',
       'https://www.youtube.com/watch?v=nh3EsEzVvws':'The Moody Blues – “How Is It”',
       'https://www.youtube.com/watch?v=3YwpG-dEQ0g':'The Moody Blues – “The Sun Is Still Shining”',
       'https://www.youtube.com/watch?v=ld4PL-HieLc':'Mundo Livre S/A – “Destruindo a Camada de Ozônio”',
       'https://www.youtube.com/watch?v=YNxr5-uFyY0':'Mundo Livre S/A – “Caiu a Ficha”',
       'https://www.youtube.com/watch?v=U3PTQ0Gi-_4':'The Prince Myshkin – “Ministry of Oil”',
       'https://www.youtube.com/watch?v=VtW8RkI3-c4':'Randy Newman – “Burn On”',
       'https://www.youtube.com/watch?v=CKy_XJIPUkA':'Olivia Newton‐John – “Gaia”',
       'https://www.youtube.com/watch?v=R6zOnMpLYxE':'New Riders of the Purple Sage – “Garden of Eden”',
       'https://www.youtube.com/watch?v=kwiAUQ7EpqE':'Niyorah – “Global Warming”',
       'https://www.youtube.com/watch?v=JKDl66XIEFM':'Orbital – “Impact (The Earth is Burning)”',
       'https://www.youtube.com/watch?v=Y43XLVqjytQ':'Orchestral Manoeuvres In the Dark – “Electricity”',
       'https://www.youtube.com/watch?v=LCCiwPEdEpg':'Ozzy Osborne – “Dreamer”https://www.youtube.com/watch?v=LCCiwPEdEpg',
       'https://www.youtube.com/watch?v=JImuJbc0hQA':'Ozzy Osborne – “Revelation (Mother Earth)”',
       'https://www.youtube.com/watch?v=FiaTINzP2nA':'Tom Paxton – “Let the Sunshine”',
       'https://www.youtube.com/watch?v=msKYLHwqvW4':'Tom Paxton – “Whose Garden Was This?”',
       'https://www.youtube.com/watch?v=XycBLF6kWuY':'The Pixies – “Monkey Gone to Heaven”',
       'https://www.youtube.com/watch?v=N3eb5g9NH30':'The Postal Service – “Sleeping In”',
       'https://www.youtube.com/watch?v=DEy6EuZp9IY':'John Prine – “Paradise”',
       'https://www.youtube.com/watch?v=thu8DWsirJo':'The Pretenders – “My City Was Gone”',
       'https://www.youtube.com/watch?v=_rVu2781fXk':'Pulp – “The Trees”',
       'https://www.youtube.com/watch?v=JskRVoI3PFM':'Queensryche – “Resistance”',
       'https://www.youtube.com/watch?v=AWtn4Kt05_Y':'Radiohead – “Idioteque”',
       'https://www.youtube.com/watch?v=0El3Dqk0wfU':'Rainbow – “Can’t Happen Here”',
       'https://www.youtube.com/watch?v=gUUdQfnshJ4':'Chris Rea – “The Road to Hell”',
       'https://www.youtube.com/watch?v=ZEDxDrhzYJc':'Lou Reed – “The Last Great American Whale”',
       'https://www.youtube.com/watch?v=XsKwqr2SKwo':'Lou Reed – “Sick of You”',
       'https://www.youtube.com/watch?v=lf6vCjtaV1k':'REM – “Fall on Me”',
       'https://www.youtube.com/watch?v=7izgjRJThds':'REM – “I Remember California”',
       'https://www.youtube.com/watch?v=8OyBtMPqpNY':'REM – “It’s the End of the World As We Know It (And I Feel Fine)”',
       'https://www.youtube.com/watch?v=glSHhC-KL30':'Malvina Reynolds – “DDT On My Brain”',
       'https://www.youtube.com/watch?v=9IIJoWiqZF0':'Malvina Reynolds – “Skagit Valley Forever”',
       'https://www.youtube.com/watch?v=DramVG4AL2c':'Malvina Reynolds – “What Have They Done to the Rain?”',
       'https://www.youtube.com/watch?v=GQdFNMB7DbA':'Jonathan Richman – “Man Walks Among Us”',
       'https://www.youtube.com/watch?v=b1DUjBYBESE':'Sally Rogers – “Over in the Endangered Meadow”',
       'https://www.youtube.com/watch?v=Jnlo_YTJ8Qc':'Xavier Rudd – “The Mother”',
       'https://www.youtube.com/watch?v=EYYdQB0mkEU':'Rush – “Subdivisions”',
       'https://www.youtube.com/watch?v=EYYdQB0mkEU':'Rush – “Trees”',
       'https://www.youtube.com/watch?v=eiDvUKDsP1g':'Rush – “Vapor Trails”',
       'https://www.youtube.com/watch?v=BRa4N0ABXQY':'Pete Seeger – “Cement Octopus”',
       'https://www.youtube.com/watch?v=0ZesRAo5PBg':'Pete Seeger – “Garbage”',
       'https://www.youtube.com/watch?v=FRZ739wbh68':'Pete Seeger – “God Bless the Grass”',
       'https://www.youtube.com/watch?v=FzyYCuY161E':'Pete Seeger – “My Dirty Stream (The Hudson River Song)”',
       'https://www.youtube.com/watch?v=LybxPjj0sbg':'Pete Seeger – “To My Old Brown Earth”',
       'https://www.youtube.com/watch?v=6bMM61Y5CEU':'Shriekback – “Nemesis”',
       'https://www.youtube.com/watch?v=SN1qkG6Da58':'ichard Sinclair – “Plan It Earth”',
       'https://www.youtube.com/watch?v=LYBv0bQb8ew':'Fred Small – “Warlords”',
       'https://www.youtube.com/watch?v=haVQC0KffPk':'Hurricane Smith – “Don’t Let It Die”',
       'https://www.youtube.com/watch?v=K_xgH-tbROg':'Jill Sobule – “Manhattan in January”',
       'https://www.youtube.com/watch?v=sQOOgQtLI4M':'Soundgarden – “Hands All Over”',
       'https://www.youtube.com/watch?v=k7MQ5rxUZsc':'Spirit – “Fresh Garbage”',
       'https://www.youtube.com/watch?v=YsTK2LHZKPQ':'Spirit – “Nature’s Way”',
       'https://www.youtube.com/watch?v=17YuScyo9v4':'Spirit – “Prelude/Nothing to Hide”',
       'https://www.youtube.com/watch?v=YHDnQO7B-PI':'Steel Pulse – “Earth Crisis”',
       'https://www.youtube.com/watch?v=xCrWjDK4hng':'Steel Pulse – “Global Warning”',
       'https://www.youtube.com/watch?v=F_vy-eWGKSk':'Cat Stevens – “Where Do the Children Play?”',
       'https://www.youtube.com/watch?v=gYtpOj8yw4c':'Stephen Stills – “Ecology Song”',
       'https://www.youtube.com/watch?v=jbXAlITCoeQ':'Sting – “Fragile Planet”',
       'https://www.youtube.com/watch?v=jbXAlITCoeQ':'Stress – “Il ny a qune terre',
       'https://www.youtube.com/watch?v=4IbMiqIdeME':'Joe Strummer – “Johnny Appleseed”',
       'https://www.youtube.com/watch?v=B2T7wmUDd5E':'Sweetbriars – “Get Down Into It”',
       'https://www.youtube.com/watch?v=kDAv8uLuZiU':'10,000 Maniacs – “Campfire Song”',
       'https://www.youtube.com/watch?v=OB0C2g7851U':'10,000 Maniacs – “Eden”',
       'https://www.youtube.com/watch?v=I9Fh5f2iG-M':'10,000 Maniacs – “Poison In the Well”',
       'https://www.youtube.com/watch?v=2twY8YQYDBE':'Talking Heads – “Nothing But Flowers”',
       'https://www.youtube.com/watch?v=Ynttgx6lNL4':'James Taylor – “Gaia”',
       'https://www.youtube.com/watch?v=EtnJhGupgnA':'James Taylor – “Traffic Jam”',
       'https://www.youtube.com/watch?v=a8ayMmM4mmo':'James Taylor – “Up Er Mei”',
       'https://www.youtube.com/watch?v=ySZ2P_io3v4':'James Taylor – “Yellow and Rose”  ',
       'https://www.youtube.com/watch?v=vq1dXaNHJQ0':'Thin Lizzy – “Mama Nature Said”',
       'https://www.youtube.com/watch?v=s3gGn6t8Bog':'Three Dog Night – “Out in the Country”',
       'https://www.youtube.com/watch?v=l_njmC9YLxw':'Timbuk 3 – “Acid Rain”',
       'https://www.youtube.com/watch?v=B5S-q1gRxvw':'Time Zone featuring John Lydon & Afrika Bambaataa – “World Destruction”',
       'https://www.youtube.com/watch?v=oMpGu9jw8Yc':'David Todd – “Where We Going To Go?”',
       'https://www.youtube.com/watch?v=UrxRJ9HlfZk':'Tower of Power – “There’s Only So Much Oil in the Ground”',
       'https://www.youtube.com/watch?v=NGuDkOzCclI':'Tribo de Jah – “El Niño”',
       'https://www.youtube.com/watch?v=wwAJdZ6x8I4':'The Turtles – “Earth Anthem”',
       'https://www.youtube.com/watch?v=Sg9l2419HKw':'UFO – “Martian Landscape”',
       'https://www.youtube.com/watch?v=o9htLZr7DcU':'Loudon Wainwright III – “Hard Day on the Planet”',
       'https://www.youtube.com/watch?v=hX8XZBxhHXQ':'Joe Walsh – “Song for a Dying Planet”',
       'https://www.youtube.com/watch?v=4BGe5dT0-v4':'The Waterboys – “World Party”',
       'https://www.youtube.com/watch?v=dH0FcFZSXrg':'Dar Williams – “Blue Light of the Flame”',
       'https://www.youtube.com/watch?v=Gfz_Telvv50':'Dar Williams – “Go To the Woods”',
       'https://www.youtube.com/watch?v=d-0jerE7ZY8':'Dar Williams – “The Hudson”',
       'https://www.youtube.com/watch?v=uDG3GHuW6bw':'Dar Williams – “Who Do You Love More Than Love?”',
       'https://www.youtube.com/watch?v=qsWqa-nfYDc':'Hank Williams, Jr. – “Kiss Mother Nature Goodbye”',
       'https://www.youtube.com/watch?v=LHiOb1toqGc':'World Party – “Give it All Away”',
       'https://www.youtube.com/watch?v=0tyLGi2LtlU':'World Party – “Is It Like Today?”',
       'https://www.youtube.com/watch?v=JaYcJQej5Uw':'World Party – “Private Revolution”',
       'https://www.youtube.com/watch?v=DXDJbqws3MY':'World Party – “Put the Message In the Box”',
       'https://www.youtube.com/watch?v=ZHh0V7UjVXI':'World Party – “Ship of Fools”',
       'https://www.youtube.com/watch?v=ZZrIdbumFiI':'World Party – “Way Down Now”',
       'https://www.youtube.com/watch?v=qB_xka50sME':'World Party – “World Party”',
       'https://www.youtube.com/watch?v=xjVVhJ-INWQ':'X‐Ray Spex – “The Day the World Turned Day‐Glo”',
       'https://www.youtube.com/watch?v=Jc17DqcA6Qc':'The Yardbirds – “Shapes of Things”',
       'https://www.youtube.com/watch?v=pdNWTT0mcmY':'Yes – “Don’t Kill the Whale”',
       'https://www.youtube.com/watch?v=wrtEyed7so8':'Neil Young – “After the Garden”',
       'https://www.youtube.com/watch?v=z9C2NxO_dJs':'Neil Young – “After the Gold Rush”',
       'https://www.youtube.com/user/MrMootdogg':'Neil Young – the entire “Greendale” album',
       'https://www.youtube.com/watch?v=XjC_eczKi4c':'Neil Young – “Like an Inca”',
       'https://www.youtube.com/watch?v=80TZ8t38gI4':'Neil Young – “Mother Earth (Natural Anthem)”',
       'https://www.youtube.com/watch?v=fmCCpzW7AFU':'Neil Young – “Natural Beauty”',
       'https://www.youtube.com/watch?v=Ovum-GjYWKQ':'Neil Young – “Piece of Crap”',
       'https://www.youtube.com/watch?v=yesyhQkYrQM':'Zager and Evans – “In the Year 2525”',
       'https://www.youtube.com/watch?v=X7ZWu0l2Xok':'Warren Zevon – “Run Straight Down”',
       'https://www.youtube.com/watch?v=k67GgvqLyJU':'Joel Zifkin – “High Water Rising”'}

# tell a random joke 
songlist=list(songs)
randomint=random.randint(0,len(songlist)-1)
songlink = songlist[randomint]
description = songs[songlink]

speaktext(hostdir,'listen to ' + description)
os.system('open %s'%(songlink))

# update database
database=json.load(open('actions.json'))
action_log=database['action log']

action={
    'action':'facts.py',
    'date': get_date(),
    'meta': [songlink, description],
}

action_log.append(action)
jsonfile=open('actions.json','w')
json.dump(database,jsonfile)
jsonfile.close()


