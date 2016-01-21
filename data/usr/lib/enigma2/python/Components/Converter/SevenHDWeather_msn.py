# -*- coding: utf-8 -*-
#
#  MSN Weather Info
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
from xml.etree.cElementTree import fromstring
from enigma import eTimer
import os, gettext, requests

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

URL = 'http://weather.service.msn.com/data.aspx?src=outlook&culture=' + str(config.plugins.SevenHD.weather_language.value) + '&weadegreetype=C&wealocations=wc:' + str(config.plugins.SevenHD.weather_msn_id.value)
WEATHER_DATA = None

class SevenHDWeather_msn(Converter, object):
	def __init__(self, type):
                Converter.__init__(self, type)
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
            elif self.what == 'LongDay':
               self.info = self.getLongDay(int(day))
            elif self.what == 'WetterDate':
               self.info = self.getWeatherDate(int(day))
            elif self.what == 'Wind':
               self.info = self.getCompWind()	
            elif self.what == 'Humidity':
               self.info = self.getHumidity()
            elif self.what == 'RainPrecent':
               self.info = self.getRainPrecent(int(day))
            elif self.what == 'City':
               self.info = str(config.plugins.SevenHD.weather_cityname.getValue())
               
            return str(self.info)
	text = property(getText)
	
	def reset(self):
	    global WEATHER_DATA
            WEATHER_DATA = None
            
        def get_Data(self):
            global WEATHER_DATA
            if WEATHER_DATA is None:

               self.data = {}
               index = 0
            
               res = requests.request('get', URL)
               root = fromstring(res.text)
            
               for childs in root:
                   for items in childs:
                       if items.tag == 'current':
                          self.data['Day_%s' % str(index)] = {}
                          self.data['Day_%s' % str(index)]['temp'] = items.attrib.get('temperature').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['skytextday'] = items.attrib.get('skytext').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['humidity'] = items.attrib.get('humidity').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['winddisplay'] = items.attrib.get('winddisplay').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['feelslike'] = items.attrib.get('feelslike').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['skycodeday'] = items.attrib.get('skycode').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['shortday'] = items.attrib.get('shortday').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['longday'] = items.attrib.get('day').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['observationpoint'] = items.attrib.get('observationpoint').encode('utf-8', 'ignore')
                       elif items.tag == 'forecast':
                          index += 1
                          self.data['Day_%s' % str(index)] = {}
                          self.data['Day_%s' % str(index)]['low'] = items.attrib.get('low').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['high'] = items.attrib.get('high').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['skycodeday'] = items.attrib.get('skycodeday').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['skytextday'] = items.attrib.get('skytextday').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['shortday'] = items.attrib.get('shortday').encode('utf-8', 'ignore')          
                          self.data['Day_%s' % str(index)]['longday'] = items.attrib.get('day').encode('utf-8', 'ignore')
                          self.data['Day_%s' % str(index)]['precip'] = items.attrib.get('precip').encode('utf-8', 'ignore')
                          
               WEATHER_DATA = self.data
               timeout = int(config.plugins.SevenHD.refreshInterval.value) * 1000.0 * 60.0
               self.timer.start(int(timeout), True)
               
            else:
               self.data = WEATHER_DATA
               
        def getMinTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['low']
               if temp == '':
                  temp = 'N/A'
               return str(temp) + '°C'
            except:
               return 'N/A'
            
        def getMaxTemp(self, day):
            try:
               temp = self.data['Day_%s' % str(day)]['high']
               if temp == '':
                  temp = 'N/A'
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
            
        def getWeatherDes(self, day):
            try:
               weather = self.data['Day_%s' % str(day)]['skytextday']
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
            
        def getLongDay(self, day):
            try:
               weather_dayname = self.data['Day_%s' % str(day)]['longday']
               return str(weather_dayname)
            except:
               return 'N/A'
            
        def getCompWind(self):
            try:
               wind = self.data['Day_0']['winddisplay']
               return str(wind)
            except:
               return 'N/A'
        
        def getRainPrecent(self, day):
            try:
               rainprobability = self.data['Day_%s' % str(day)]['precip']
               return str(float(rainprobability)) + ' %'
            except:
               return 'N/A'    
        
        def getHumidity(self):
            try:
               humi = self.data['Day_0']['humidity']
               return str(humi) + _('% humidity')
            except:
               return 'N/A'
            
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