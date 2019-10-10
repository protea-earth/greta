# Greta
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Are%20you%20a%20climate%20enthusiast%20looking%20to%20learn%20how%20to%20be%20a%20better%20climate%20citizen?%20Check%20out%20Greta,%20a%20climate-based%20voice%20assistant%20@%20https://github.com/jim-schwoebel/greta.&hashtags=protea,greta,voice,assistant)

Greta is an agile voice assistant to help reduce your carbon footprint. She is built on top of the [Nala framework](https://github.com/jim-schwoebel/nala) for prototyping voice assistant apps. 

![](https://media.giphy.com/media/ZbH9DaFU2dZ4F6M4OI/giphy.gif)

Greta was built as a demo project for the [Climate-KIC Climathon](https://climathon.climate-kic.org/en/san-francisco-the-event-page-2019) in the SF Bay Area October 25th, 2019.

## Getting started

To get started, clone the repository and install the dependencies:

```
git clone git@github.com:protea-earth/greta.git
cd greta 
python3 -m venv env
source env/bin/activate
python3 setup.py 
```

Now, set up some environment variables in your ./~ directory:

```
cd ~
open .bash_profile
```

These are some environment variables that you should set here: 

```
export SUDO_PASSWORD=**********
export GOOGLE_APPLICATION_CREDENTIALS=/Users/jimschwoebel/Desktop/appcreds/APPNAME-basdfcnas3el98a8sd5.json
```

Note the sudo_password is your password for your Mac computer to help shut down computer and GOOGLE_APPLICATION_CREDENTIALS is the .json key location for the Google API to allow for Google transcription.

Now you can run:

```
python3 greta.py
```

This will start Greta up for you to now query her for some actions.

## How to query Greta

It's quite easy to query Greta. All you need to do is say "Hey Greta" and she'll wake up listening for an action. See below for more information.

![](https://github.com/jim-schwoebel/greta/blob/master/data/other/Gif-2019-56-06-18-56-43.gif)

To active Greta, all you need to do is query her with 'Hey Greta!' (1) - which then triggers a response from Greta - (3) in this case, “How can I help you?.” Then, a user provides another query (usually after some beeping sound) - such as (4) “get events.” Greta transcribes this query to understand it, and parses the query for keyword intents; for example, if the response is “get events” the only word that really matters is “events” and that would be used to provoke a response (5). Then, after this keyword maps onto an action dictionary (or a map of responses to keywords), the action is executed (6). Then, the intent loop repeats itself, looking for another wakeword (“Hey Greta”) before triggering another action.

## Actions: what Greta can do

Listed here are a description of these actions along with the query intents needed to activate them. 

If you have any other ideas, let us know on the [GitHub issues tab](https://github.com/jim-schwoebel/nala/issues) (as an enhancement)! 

### General actions 

| Action  | Description | Example query intent | 
| ------------- | ------------- | ------------- |
|🌎 calculate_carbon_footprint.py | Guides user through a list of questions then calculates the users carbon footprint (outputs in .PDF form). | “calculate", "carbon", "footprint" | 
|📅 events.py | Pulls up a meetup.com event related to climate change in your local area. | “events", "meetup" | 
|📠 facts.py | Grabs one quick fact from a random list of facts about climate change. | “get facts", "grab a fact" | 
|🥗 food.py | Based on the query, searches yelp for vegetarian-friendly restaurants. |"grab food"| 
|🎧 music.py | Pulls up a YouTube video that is inspired by climate change and global warming. | "open music", "play me a climate change song"| 
|📰 news.py | Searches some basic news sites related to climate change. | “grab the news” | 
|✈️ plan_trip.py | Schedules a trip based on an origin and destination city; suggests some ways to reduce your footprint while traveling. | “plan trip” | 
|💸 purchase_product.py | Selects a random green vendor and an item that you could purchase to be a good environmental citizen (energy, tech, home, and fashion categories). | “purchase”, "grab me a green product" |
|♻️ recycle.py | Opens up a voice-guided earth911.com  search for your nearest recycling facility (plastics). | "recycle", "find me the nearest recycling facility" | 
|💻 shut_down.py | Shuts down your computer, assuming your SUDO password is in the environment variables (helps to save energy). | "shut", "shut down", "down" | 
|🗣️ speech.py | Read Greta's speech from the [UN Climate Action Summit](https://www.npr.org/2019/09/23/763452863/transcript-greta-thunbergs-speech-at-the-u-n-climate-action-summit) | "recite speech", "speech" | 
|😴 sleep (no script) |  Puts the computer to sleep for a designated time period. | "go to sleep"|
|🌡️ weather.py | Searches weather.com for the current weather at your location. | "get the weather"|

... more to come into the future! 

## License
This repository is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). 

## Getting involved
Here are some ways you can get more involved:

* register an account @ [Protea.Earth](http://protea.earth), a social network community designed to reduce your carbon footprint.
* learn more about voice computing and buy the [Voice Computing in Python](https://github.com/jim-schwoebel/voicebook) textbook.
* be mentored by someone on our team @ [NeuroLex](https://neurolex.ai) through the [Innovation Fellows Program](http://neurolex.ai/research).
* give some feedback on this repository by opening up a [GitHub issue](https://github.com/jim-schwoebel/greta/issues).
* send me an email @ jim@protea.earth; I'm always interested to chat about voice computing and/or climate change!

## References

* [Nala](https://github.com/jim-schwoebel/nala)
* [Voicebook repository](https://github.com/jim-schwoebel/voicebook)
