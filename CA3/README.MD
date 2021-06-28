# Controlled Assessment 3 - Coronavirus Smart Alarm Clock
This is a smart system that allows for the scheduling of daily briefing. This allows for the news, weather and covid19 specific infomation to be spoken to them at a desired time.
This project can be found on github
     https://github.com/js1294/CA3
## Motivation
I have had first hand experiance of the worry that the covid19 pandemic has caused, so making this might make it easier for some people. Plus, it is 50% of the module.
## Build Status
This is currently working.
## Code Style
This project uses python 3.8.
## Installation
To install this project correctly, you will need to add your own API keys to the config.json file.
This can be done by firstly going to https://openweathermap.org/api and https://newsapi.org/. Follow the website instruction to obtain a personal API key for each. 
To find the config.json file go to CA3/controlled assessment 3/config.json. Open up the config file with a text editor like notepad and put your API keys next to the "weather": and "news":.
Make sure the API keys are inside speech marks and that the correct API key is for the specific one.
## Tests
A basic testing routine is being used and should be run to check everything is working.
linter.py will also be used to check for problems with pep 8.
To test linter.py for main python files, use linter.py in controlled_assessment_main.
## License
   Copyright 2020 Jack Shaw

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
