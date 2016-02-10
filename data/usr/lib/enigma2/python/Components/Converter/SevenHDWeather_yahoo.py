# -*- coding: utf-8 -*-
#
#  Yahoo Weather Info
#
#  Coded by TBX for Kraven Skins (c) 2015
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Converter.Converter import Converter
from Components.Language import language
from Components.Element import cached
from Components.config import config
from xml.dom.minidom import parseString
from enigma import eTimer
import os, gettext, requests
from Poll import Poll

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
	t = gettext.dgettext("SevenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t                              

URL = 'http://weather.yahooapis.com/forecastrss?w=' + str(config.plugins.SevenHD.weather_woe_id.value) + '&u=c'
WEATHER_DATA = None

class SevenHDWeather_yahoo(Poll, Converter, object):
	def __init__(self, type):
                Poll.__init__(self)
                Converter.__init__(self, type)
                self.poll_interval = 60000
                self.poll_enabled = True
                type = type.split(',')                
                self.day_value = type[0]
                self.what = type[1]
                self.data = {}
                self.timer = eTimer()
		self.timer.callback.append(self.reset)
                self.timer.callback.append(self.get_Data)
		self.get_Data()
		 
	@cached
	def getText(self):
	    global WEATHER_DATA
            self.data = WEATHER_DATA
	    day = self.day_value.split('_')[1]
            if self.what == 'DayTemp':
               self.info = self.getDayTemp()	
            elif self.what == 'FeelTemp':
               self.info = self.getFeelTemp()
            elif self.what == 'MinTemp':
               self.info = self.getMinTemp(int(day))
            elif self.what == 'MaxTemp':
               self.info = self.getMaxTemp(int(day))
            elif self.what == 'Description':
               self.info = self.getWeatherDes(int(day)) 
            elif self.what == 'MeteoIcon':
               self.info = self.getWeatherIcon(int(day))
            elif self.what == 'MeteoFont':
               self.info = self.getMeteoFont(int(day))
            elif self.what == 'ShortDay':
               self.info = self.getShortDay(int(day))
            elif self.what == 'WetterDate':
               self.info = self.getWeatherDate(int(day))
            elif self.what == 'Wind':
               self.info = self.getCompWind()	
            elif self.what == 'Humidity':
               self.info = self.getHumidity()
            elif self.what == 'City':
               self.info = str(config.plugins.SevenHD.weather_cityname.getValue())
               
            return str(self.info)
	text = property(getText)
	
	def reset(self):
	    global WEATHER_DATA
            WEATHER_DATA = None
	    self.timer.stop()
	    
        def get_Data(self):
            global WEATHER_DATA
            if WEATHER_DATA is None:
               
               self.data = {}
               index = 0
            
               try:
                 res = requests.request('get', URL)
                 root = parseString(res.text)
                 
                 self.data['Day_%s' % str(index)] = {}
                 self.data['Day_%s' % str(index)]['feelslike'] = root.getElementsByTagName('yweather:wind')[0].getAttributeNode('chill').nodeValue
                 self.data['Day_%s' % str(index)]['winddisplay'] = root.getElementsByTagName('yweather:wind')[0].getAttributeNode('direction').nodeValue
                 self.data['Day_%s' % str(index)]['windspeed'] = root.getElementsByTagName('yweather:wind')[0].getAttributeNode('speed').nodeValue
                 self.data['Day_%s' % str(index)]['humidity'] = root.getElementsByTagName('yweather:atmosphere')[0].getAttributeNode('humidity').nodeValue
                 self.data['Day_%s' % str(index)]['temp'] = root.getElementsByTagName('yweather:condition')[0].getAttributeNode('temp').nodeValue
                 self.data['Day_%s' % str(index)]['skytextday'] = root.getElementsByTagName('yweather:condition')[0].getAttributeNode('text').nodeValue
                 self.data['Day_%s' % str(index)]['skycodeday'] = root.getElementsByTagName('yweather:condition')[0].getAttributeNode('code').nodeValue
                 self.data['Day_%s' % str(index)]['shortday'] = _(root.getElementsByTagName('yweather:condition')[0].getAttributeNode('date').nodeValue.split(',')[0])
            
                 for x in range(5):
                     index += 1
                     self.data['Day_%s' % str(index)] = {}
                     self.data['Day_%s' % str(index)]['shortday'] = _(root.getElementsByTagName('yweather:forecast')[int(x)].getAttributeNode('day').nodeValue)
                     self.data['Day_%s' % str(index)]['low'] = root.getElementsByTagName('yweather:forecast')[int(x)].getAttributeNode('low').nodeValue
                     self.data['Day_%s' % str(index)]['high'] = root.getElementsByTagName('yweather:forecast')[int(x)].getAttributeNode('high').nodeValue
                     self.data['Day_%s' % str(index)]['skytextday'] = root.getElementsByTagName('yweather:forecast')[int(x)].getAttributeNode('text').nodeValue
                     self.data['Day_%s' % str(index)]['skycodeday'] = root.getElementsByTagName('yweather:forecast')[int(x)].getAttributeNode('code').nodeValue
               except:
                 WEATHER_DATA = self.data
                 return
               WEATHER_DATA = self.data            
               timeout = int(config.plugins.SevenHD.refreshInterval.value) * 1000.0 * 60.0
               self.timer.start(int(timeout), 1)

            else:
               self.data = WEATHER_DATA
               
        def getMinTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['low']
               return str(temp) + '°C'
            except:
               return 'N/A'
               
        def getMaxTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['high']
               return str(temp) + '°C'
            except:
               return 'N/A'
               
        def getFeelTemp(self):
            try:
               temp = self.data['Day_0']['temp']
               feels = self.data['Day_0']['feelslike']
               return str(temp) + '°C' + _(", feels ") + str(feels) + '°C'
            except:
               return 'N/A'
            
        def getDayTemp(self):
            try:
               temp = self.data['Day_0']['temp']
               return str(temp) + '°C'
            except:
               return 'N/A'
            
        def getWeatherDate(self, day):
            try:
               weather_dayname = self.data['Day_%s' % str(day)]['shortday']
               return str(weather_dayname)
            except:
               return 'N/A'
            
        def getWeatherDes(self, day):
            try:
               weather = self.description(self.data['Day_%s' % str(day)]['skycodeday'])
               return str(weather)
            except:
               return 'N/A'
            
        def getWeatherIcon(self, day):
            try:
               weathericon = self.data['Day_%s' % str(day)]['skycodeday']
               return str(weathericon)
            except:
               return 'N/A'
            
        def getShortDay(self, day):
            try:
               weather_dayname = self.data['Day_%s' % str(day)]['shortday']
               return str(weather_dayname)
            except:
               return 'N/A'
            
        def getCompWind(self):
            try:
               wind = self.getWind()
               speed = self.data['Day_0']['windspeed']
               return str(speed) + _(" km/h") + _(" from ") + str(wind)
            except:
               return 'N/A'
            
        def getHumidity(self):
            try:
               humi = self.data['Day_0']['humidity']
               return str(humi) + _('% humidity')
            except:
               return 'N/A'
            
        def getWind(self):
            direct = self.data['Day_0']['winddisplay']
            direct = int(direct)
            
            if direct >= 0 and direct <= 20:
               wdirect = _('N')
            elif direct >= 21 and direct <= 35:
               wdirect = _('N-NE')
            elif direct >= 36 and direct <= 55:
               wdirect = _('NE')
            elif direct >= 56 and direct <= 70:
               wdirect = _('E-NE')
            elif direct >= 71 and direct <= 110:
               wdirect = _('E')
            elif direct >= 111 and direct <= 125:
               wdirect = _('E-SE')
            elif direct >= 126 and direct <= 145:
               wdirect = _('SE')
            elif direct >= 146 and direct <= 160:
               wdirect = _('S-SE')
            elif direct >= 161 and direct <= 200:
               wdirect = _('S')
            elif direct >= 201 and direct <= 215:
               wdirect = _('S-SW')
            elif direct >= 216 and direct <= 235:
               wdirect = _('SW')
            elif direct >= 236 and direct <= 250:
               wdirect = _('W-SW')
            elif direct >= 251 and direct <= 290:
               wdirect = _('W')
            elif direct >= 291 and direct <= 305:
               wdirect = _('W-NW')
            elif direct >= 306 and direct <= 325:
               wdirect = _('NW')
            elif direct >= 326 and direct <= 340:
               wdirect = _('N-NW')
            elif direct >= 341 and direct <= 360:
               wdirect = _('N')
            else:
               wdirect = "N/A"
            return wdirect
        
        def getMeteoFont(self, day):
            weathercode = self.data['Day_%s' % str(day)]['skycodeday']
            weathercode = int(weathercode)
	    
            if weathercode == 0 or weathercode == 1 or weathercode == 2:
	                weatherfont = "S"
	    elif weathercode == 3 or weathercode == 4:
			weatherfont = "Z"
	    elif weathercode == 5  or weathercode == 6 or weathercode == 7 or weathercode == 18:
			weatherfont = "U"
	    elif weathercode == 8 or weathercode == 10 or weathercode == 25:
			weatherfont = "G"
	    elif weathercode == 9:
			weatherfont = "Q"
	    elif weathercode == 11 or weathercode == 12 or weathercode == 40:
			weatherfont = "R"
	    elif weathercode == 13 or weathercode == 14 or weathercode == 15 or weathercode == 16 or weathercode == 41 or weathercode == 46 or weathercode == 42 or weathercode == 43:
			weatherfont = "W"
	    elif weathercode == 17 or weathercode == 35:
			weatherfont = "X"
	    elif weathercode == 19:
			weatherfont = "F"
	    elif weathercode == 20 or weathercode == 21 or weathercode == 22:
			weatherfont = "L"
	    elif weathercode == 23 or weathercode == 24:
			weatherfont = "S"
	    elif weathercode == 26 or weathercode == 44:
			weatherfont = "N"
	    elif weathercode == 27 or weathercode == 29:
			weatherfont = "I"
	    elif weathercode == 28 or weathercode == 30:
			weatherfont = "H"
	    elif weathercode == 31 or weathercode == 33:
			weatherfont = "C"
	    elif weathercode == 32 or weathercode == 34 or weathercode == 36:
			weatherfont = "B"
            elif weathercode == 37 or weathercode == 38 or weathercode == 39 or weathercode == 45 or weathercode == 47:
			weatherfont = "0"
	    else:
			weatherfont = ")"
	    return str(weatherfont)
        
        def description(self, what):
            what = int(what)
            
            if what == 0:
               return _('Tornado')
	    elif what == 1:
	       return _('Tropical\n storm')
            elif what == 2:
	       return _('Hurricane')
	    elif what == 3:
	       return _('Severe\n thunderstorms')
	    elif what == 4:
	       return _('Thunderstorms')
	    elif what == 5:
	       return _('Mixed rain\n and snow')
	    elif what == 6:
	       return _('Mixed rain\n and sleet')
	    elif what == 7:
               return _('Mixed snow\n and sleet')
	    elif what == 8:
               return _('Freezing\n drizzle')
	    elif what == 9:
	       return _('Drizzle')
	    elif what == 10:
               return _('Freezing\n rain')
	    elif what == 11:
	       return _('Showers')
	    elif what == 12:
	       return _('Rain')
	    elif what == 13:
               return _('Snow\n flurries')
	    elif what == 14:
	       return _('Light\n snow showers')
	    elif what == 15:
               return _('Blowing\n snow')
	    elif what == 16:
	       return _('Snow')
	    elif what == 17:
	       return _('Hail')
	    elif what == 18:
	       return _('Sleet')
	    elif what == 19:
	       return _('Dust')
	    elif what == 20:
	       return _('Foggy')
	    elif what == 21:
	       return _('Haze')
	    elif what == 22:
    	       return _('Smoky')
	    elif what == 23:
	       return _('Blustery')
	    elif what == 24:
	       return _('Windy')
	    elif what == 25:
	       return _('Cold')
	    elif what == 26:
	       return _('Cloudy')
	    elif what == 27:
	       return _('Mostly\n cloudy')
	    elif what == 28:
	       return _('Mostly\n cloudy')
	    elif what == 29:
	       return _('Partly\n cloudy')
	    elif what == 30:
	       return _('Partly\n cloudy')
	    elif what == 31:
	       return _('Clear')
	    elif what == 32:
	       return _('Sunny')
	    elif what == 33:
	       return _('Fair')
	    elif what == 34:
	       return _('Fair')
	    elif what == 35:
	       return _('Mixed rain\n and hail')
	    elif what == 36:
               return _('Hot')
	    elif what == 37:
	       return _('Isolated\n thunderstorms')
	    elif what == 38:
	       return _('Scattered\n thunderstorms')
	    elif what == 39:
	       return _('Scattered\n thunderstorms')
	    elif what == 40:
	       return _('Scattered\n showers')
	    elif what == 41:
	       return _('Heavy snow')
	    elif what == 42:
	       return _('Scattered\n snow showers')
	    elif what == 43:
	       return _('Heavy snow')
	    elif what == 44:
	       return _('Partly\n cloudy')
	    elif what == 45:
	       return _('Thundershowers')
	    elif what == 46:
	       return _('Snow showers')
	    elif what == 47:
	       return _('Isolated\n thundershowers')
	    elif what == 3200:
	       return _('Not\n available')
	    else:
	       return 'N/A'