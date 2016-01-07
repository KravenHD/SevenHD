# -*- coding: utf-8 -*-
#
#  Accuweather Weather Info
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
from enigma import eTimer
import requests, time, os, gettext

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

URL = 'http://api.accuweather.com/forecasts/v1/daily/5day/' + str(config.plugins.SevenHD.weather_locationcode.value) + '?apikey=srRLeAmTroxPinDG8Aus3Ikl6tLGJd94&metric=true&details=true&language=' + str(config.plugins.SevenHD.weather_language.value)
URL2 = 'http://api.accuweather.com/currentconditions/v1/' + str(config.plugins.SevenHD.weather_locationcode.value) + '?apikey=srRLeAmTroxPinDG8Aus3Ikl6tLGJd94&metric=true&details=true&language=' + str(config.plugins.SevenHD.weather_language.value)

class SevenHDWeather_accu(Converter, object):
	def __init__(self, type):
                Converter.__init__(self, type)
                type = type.split(',')                
                self.day_value = type[0]
                self.what = type[1]
                self.timer = eTimer()
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
	
        def get_Data(self):
            res = requests.request('get', URL)
            self.data = res.json()
            res2 = requests.request('get', URL2)
            self.data2 = res2.json()
            timeout = int(config.plugins.SevenHD.refreshInterval.value) * 1000.0 * 60.0
            self.timer.start(int(timeout), True)
            
        def getMinTemp(self, day):
            temp = self.data['DailyForecasts'][day]['Temperature']['Minimum']['Value']
            return str(float(temp)) + '°C'
            
        def getMaxTemp(self, day):
            temp = self.data['DailyForecasts'][day]['Temperature']['Maximum']['Value']
            return str(float(temp)) + '°C'
        
        def getDayTemp(self):
            temp = self.data2[0]['Temperature']['Metric']['Value']
            return str(float(temp)) + '°C'
            
        def getWeatherDes(self, day):
            weather = self.data['DailyForecasts'][day]['Day']['IconPhrase']
            return str(weather)
            
        def getWeatherIcon(self, day):
            weathericon = self.data['DailyForecasts'][day]['Day']['Icon']
            return str(weathericon)
            
        def getWeatherDate(self, day):
            weather_epoch_date = self.data['DailyForecasts'][day]['EpochDate']
            weather_dayname = time.strftime('%a', time.localtime(weather_epoch_date))
            return str(weather_dayname)
        
        def getCompWind(self):
            wind = self.data['DailyForecasts'][0]['Day']['Wind']['Direction']['Localized']
            speed = self.getSpeed()
            return str(speed) + _(" from ") + str(wind)
        
        def getSpeed(self):
            windspeed = self.data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
            return str(float(windspeed)) + ' km/h'
            
        def getHumidity(self):
            humi = self.data2[0]['RelativeHumidity']
            return str(humi) + _('% humidity')
        
        def getFeelTemp(self):
            temp = self.data2[0]['Temperature']['Metric']['Value']
            feels = self.data2[0]['RealFeelTemperature']['Metric']['Value']
            return str(temp) + '°C' + _(", feels ") + str(feels) + '°C'
        
        def getMeteoFont(self, day):
            font = self.data['DailyForecasts'][day]['Day']['Icon']
            font_icon = '0x' + str(20 + font)
            weather_font_icon = unichr(int(font_icon, 16)).encode('utf-8')
            return str(weather_font_icon)