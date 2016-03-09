# -*- coding: UTF-8 -*-
#######################################################################
#
# SevenHD by Team Kraven
# 
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#######################################################################
from GlobalImport import *
#######################################################################
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
	t = gettext.dgettext("SevenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block
########################################################################
class InfobarExtraSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <widget name="buttonRed" font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" transparent="1" />
                         <widget name="buttonGreen" font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" transparent="1" />
                         <widget name="buttonYellow" font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" transparent="1" />
                         <widget name="buttonBlue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <widget name="titel" position="70,12" size="708,46" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget name="colorthump" position="891,220" size="372,30" zPosition="1" backgroundColor="#00000000" alphatest="blend" />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="preview" position="891,274" size="372,209" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" zPosition="2" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
                         <eLabel backgroundColor="#00000000" position="6,6" size="842,708" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="842,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,714" size="844,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="848,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,64" size="816,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,656" size="816,2" zPosition="2" />
                         <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="ClockToText">Default</convert>
                         </widget>
                         <eLabel backgroundColor="#00000000" position="878,6" size="396,708" transparent="0" zPosition="-9" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="396,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,714" size="398,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="1274,6" size="2,708" zPosition="2" />
                         <widget source="session.CurrentService" render="Label" position="891,88" size="372,46" font="Regular2;35" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="SevenHDUpdate">Version</convert>
                         </widget>
                         <widget source="session.CurrentService" render="Label" position="891,134" size="372,28" font="Regular;26" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                         </widget>
                         <eLabel position="891,274" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,481" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="1261,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                  </screen>
               """

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self.ColorLoad = ePicLoad()
        self["colorthump"] = Pixmap()
        self["helperimage"] = Pixmap()
        self["description"] = Label()
        self["preview"] = Label()
        self["buttonRed"] = Label()
        self["buttonGreen"] = Label()
        self["buttonYellow"] = Label()
        self["titel"] = Label()
        self["buttonRed"].setText(_("Cancel"))
        self["buttonGreen"].setText(_("Save"))
        self["buttonYellow"].setText(_("Defaults"))
        self["titel"].setText(_("Infobar Extra Settings"))
        self["buttonBlue"] = Label()
        
        if config.plugins.SevenHD.grabdebug.value:
           self["buttonBlue"].setText('Screenshot')
        else:
           self["buttonBlue"].setText('Preview Result')
        
        self.preview = False
        self["preview"].hide()      
        
        ConfigListScreen.__init__(
            self,
            self.getMenuItemList(),
            session = session,
            on_change = self.__selectionChanged
        )

        self["actions"] = ActionMap(
        [
            "OkCancelActions",
            "DirectionActions",
            "InputActions",
            "ColorActions"
        ],
        {
            "left": self.keyLeft,
            "down": self.keyDown,
            "up": self.keyUp,
            "right": self.keyRight,
            "red": self.exit,
            "yellow": self.defaults,
            "green": self.save,
            "blue": self.keyBlue,
            "cancel": self.exit
        }, -1)

        self.onLayoutFinish.append(self.UpdatePicture)
        
    def getMenuItemList(self):
        list = []
        list.append(getConfigListEntry(_('_____________________________infobar extras________________________________________'), ))
        list.append(getConfigListEntry(_("satellite information"),            config.plugins.SevenHD.SatInfo,         'Zeigt die Satelliten Informationen auf der rechten Seite.',                   '1',        ''))
        if config.plugins.SevenHD.SatInfo.value != 'none':
           list.append(getConfigListEntry(_("font color"),                    config.plugins.SevenHD.SevenSat,        'Stellt die Schriftfarbe ein.',                                                '4',       'satcolor'))
        list.append(getConfigListEntry(_("system information"),               config.plugins.SevenHD.SysInfo,         'Zeigt die System Informationen auf der rechten Seite.',                       '1',        ''))
        if config.plugins.SevenHD.SysInfo.value != 'none':
           list.append(getConfigListEntry(_("font 1"),                        config.plugins.SevenHD.SevenSys1,       'Stellt die Schriftfarbe ein.',                                                '4',       'syscolor1'))
           list.append(getConfigListEntry(_("font 2"),                        config.plugins.SevenHD.SevenSys2,       'Stellt die Schriftfarbe ein.',                                                '4',       'syscolor2'))
        if config.plugins.SevenHD.InfobarStyle.value != 'infobar-style-xpicon9':
           list.append(getConfigListEntry(_("ECM information"),                  config.plugins.SevenHD.ECMInfo,         'Zeigt die ECM Informationen im unteren Bereich der Infobar an.',              '1',        ''))
           if config.plugins.SevenHD.ECMInfo.value != 'none':
              list.append(getConfigListEntry(_("font color"),                    config.plugins.SevenHD.SevenECM,        'Stellt die Schriftfarbe ein.',                                                '4',       'ecmcolor'))
        list.append(getConfigListEntry(_("signal strengh"),                   config.plugins.SevenHD.FrontInfo,       'Zeigt die Anzeige in SNR oder dB an.',                                        '1',        'SNRdB'))
        list.append(getConfigListEntry(_('________________________________weather____________________________________________'), ))
        
        if config.plugins.SevenHD.InfobarStyle.value != 'infobar-style-xpicon8':
           if config.plugins.SevenHD.WeatherStyle_1.value == 'none':
              list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle_1,    'Zeigt das Wetter an.',                                                        '4',        'none'))
           else:
              list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle_1,    'Zeigt das Wetter an.',                                                        '1',        ''))
           config.plugins.SevenHD.WeatherStyle_2.setValue('none')
        else:
           if config.plugins.SevenHD.WeatherStyle_2.value == 'none':
              list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle_2,    'Zeigt das Wetter an.',                                                        '4',        'none'))
           else:
              list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle_2,    'Zeigt das Wetter an.',                                                        '1',        ''))
           config.plugins.SevenHD.WeatherStyle_1.setValue('none')
           
        if config.plugins.SevenHD.WeatherStyle_1.value != 'none' or config.plugins.SevenHD.WeatherStyle_2.value != 'none' or config.plugins.SevenHD.ClockStyle.value == "clock-android" or config.plugins.SevenHD.ClockStyle.value == "clock-weather":
           
           list.append(getConfigListEntry(_("Server"),                        config.plugins.SevenHD.weather_server,  'Stellt den Server ein, wor\xc3\xbcber die Wetterdaten gesucht werden sollen.','4',        'server'))
           list.append(getConfigListEntry(_("Search by"),                     config.plugins.SevenHD.weather_search_over,'Stell hier ein, wie gesucht werden sollen.',                               '4',        'server'))
           
           if config.plugins.SevenHD.weather_search_over.value == 'name':
              list.append(getConfigListEntry(_("Cityname"),                   config.plugins.SevenHD.weather_cityname,'Gib hier deinen Ort ein.',                                                    '4',        'search'))
           elif config.plugins.SevenHD.weather_search_over.value == 'woeid':
              list.append(getConfigListEntry(_("Woe ID"),                     config.plugins.SevenHD.weather_woe_id,  'Gib hier deine WoeID ein.',                                                   '4',        'search'))
           elif config.plugins.SevenHD.weather_search_over.value == 'gmcode':
              list.append(getConfigListEntry(_("GM Code"),                    config.plugins.SevenHD.weather_gmcode,  'Gib hier deinen GM Code ein.\neine Liste findet ihr auf http://weather.codes','4',        'search'))
           elif config.plugins.SevenHD.weather_search_over.value == 'latlon':
              list.append(getConfigListEntry(_("Latitude"),                   config.plugins.SevenHD.weather_lat,     'Gib hier deinen Latitude ein.\nBsp. 51.3452',                                 '4',        'search'))
              list.append(getConfigListEntry(_("Longitude"),                  config.plugins.SevenHD.weather_lon,     'Gib hier deinen Longitude ein.\nBsp. 12.38594',                               '4',        'search'))
           
           if config.plugins.SevenHD.weather_server.value != '_yahoo':
              list.append(getConfigListEntry(_("Language for Weather"),       config.plugins.SevenHD.weather_language,'Stellt die Ausgabesprache ein.',                                              '4',        'language'))
           
           list.append(getConfigListEntry(_("Weather Style"),                 config.plugins.SevenHD.WeatherView,     'W\xc3\xa4hle zwischen Wetter Icon oder Meteo.',                               '1',        ''))
           if config.plugins.SevenHD.WeatherView.value == 'meteo':
              list.append(getConfigListEntry(_("Meteo Color"),                config.plugins.SevenHD.MeteoColor,      'Stellt die Farbe des MeteoIcon ein.',                                         '4',        'MeteoColor'))
           list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.SevenHD.refreshInterval, 'Stellt die Abfragezeit des Wetter ein.',                                      '4',        'MeteoColor'))

        if config.plugins.SevenHD.WeatherStyle_1.value != 'none' or config.plugins.SevenHD.WeatherStyle_2.value != 'none':
           list.append(getConfigListEntry(_("font 1"),                        config.plugins.SevenHD.SevenWeather1,   'Stellt die Schriftfarbe ein.',                                                '4',       'weather1'))
           list.append(getConfigListEntry(_("font 2"),                        config.plugins.SevenHD.SevenWeather2,   'Stellt die Schriftfarbe ein.',                                                '4',       'weather2'))
        if config.plugins.SevenHD.WeatherStyle_1.value != 'none' or config.plugins.SevenHD.WeatherStyle_2.value != 'none':
           if config.plugins.SevenHD.WeatherStyle_1.value in ('weather-big','weather-left-side') or config.plugins.SevenHD.WeatherStyle_2.value in ('weather-big','weather-left-side'):
              list.append(getConfigListEntry(_("font 3"),                     config.plugins.SevenHD.SevenWeather3,   'Stellt die Schriftfarbe ein.',                                                '4',       'weather3'))
           
        return list

    def __selectionChanged(self):
        returnValue = self["config"].getCurrent()[4]
        #if not returnValue in 'woeid latlon gmcode cityname' or returnValue == '':
        if returnValue != 'search' or returnValue == '':
           self["config"].setList(self.getMenuItemList())
                 
    def GetPicturePath(self):
        returnValue = self["config"].getCurrent()[3]
           		
        if returnValue == '4':
           returnValue = self["config"].getCurrent()[int(returnValue)]
        else:
           returnValue = self["config"].getCurrent()[int(returnValue)].value
        
        path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
        
        self["description"].setText(self["config"].getCurrent()[2])
        
        if fileExists(path):
           return path
        else:
           self.debug('Missing Picture: ' + str(path) + '\n')
           return MAIN_IMAGE_PATH + str("924938.jpg")

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.UpdateColor()
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def UpdateColor(self):
        self.ColorLoad.PictureData.get().append(self.DecodeColor)
        self.onLayoutFinish.append(self.ShowColor)

    def ShowColor(self):
        self.ColorLoad.setPara([self["colorthump"].instance.size().width(),self["colorthump"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.ColorLoad.startDecode(self.getFontColor())

    def DecodeColor(self, PicInfo = ""):
        ptr = self.ColorLoad.getData()
        self["colorthump"].instance.setPixmap(ptr)
    
    def getFontColor(self):   
        returnValue = self["config"].getCurrent()[1]
        self["colorthump"].instance.show()
        preview = ''
        if returnValue == config.plugins.SevenHD.MeteoColor:
              preview = self.generate(config.plugins.SevenHD.MeteoColor.value)
        elif returnValue == config.plugins.SevenHD.SevenECM:
              preview = self.generate(config.plugins.SevenHD.SevenECM.value)
        elif returnValue == config.plugins.SevenHD.SevenSat:
              preview = self.generate(config.plugins.SevenHD.SevenSat.value)
        elif returnValue == config.plugins.SevenHD.SevenSys1:
              preview = self.generate(config.plugins.SevenHD.SevenSys1.value)
        elif returnValue == config.plugins.SevenHD.SevenSys2:
              preview = self.generate(config.plugins.SevenHD.SevenSys2.value)
        elif returnValue == config.plugins.SevenHD.SevenWeather1:
              preview = self.generate(config.plugins.SevenHD.SevenWeather1.value)
        elif returnValue == config.plugins.SevenHD.SevenWeather2:
              preview = self.generate(config.plugins.SevenHD.SevenWeather2.value)
        elif returnValue == config.plugins.SevenHD.SevenWeather3:
              preview = self.generate(config.plugins.SevenHD.SevenWeather3.value)
        else:
              self["colorthump"].instance.hide()
        return str(preview)
        
    def generate(self,color):    
        
        if color.startswith('00'):
           r = int(color[2:4], 16)
           g = int(color[4:6], 16)
           b = int(color[6:], 16)

           img = Image.new("RGB",(372,30),(r,g,b))
           img.save(str(MAIN_IMAGE_PATH) + "color.png")
           return str(MAIN_IMAGE_PATH) + "color.png"

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()
        self.ShowColor()
        
    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()
        self.ShowColor()
         
    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()
        self.ShowColor()
        
    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
        self.ShowColor()
        
    def keyBlue(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
        else:
           self.preview = True
           self.get_weather_data()
              
    def defaults(self):
        
        self.setInputToDefault(config.plugins.SevenHD.WeatherStyle_1)
        self.setInputToDefault(config.plugins.SevenHD.WeatherStyle_2)
        self.setInputToDefault(config.plugins.SevenHD.weather_owm_latlon)
        self.setInputToDefault(config.plugins.SevenHD.weather_accu_latlon)
        self.setInputToDefault(config.plugins.SevenHD.weather_realtek_latlon)
        self.setInputToDefault(config.plugins.SevenHD.weather_woe_id)
        self.setInputToDefault(config.plugins.SevenHD.weather_accu_id)
        self.setInputToDefault(config.plugins.SevenHD.weather_msn_id)
        self.setInputToDefault(config.plugins.SevenHD.weather_lat)
        self.setInputToDefault(config.plugins.SevenHD.weather_lon)
        self.setInputToDefault(config.plugins.SevenHD.weather_gmcode)
        self.setInputToDefault(config.plugins.SevenHD.weather_cityname)
        self.setInputToDefault(config.plugins.SevenHD.weather_server)
        self.setInputToDefault(config.plugins.SevenHD.weather_search_over)
        self.setInputToDefault(config.plugins.SevenHD.weather_language)
        self.setInputToDefault(config.plugins.SevenHD.WeatherView)
        self.setInputToDefault(config.plugins.SevenHD.MeteoColor)
        self.setInputToDefault(config.plugins.SevenHD.SatInfo)
        self.setInputToDefault(config.plugins.SevenHD.SysInfo)
        self.setInputToDefault(config.plugins.SevenHD.ECMInfo)
        self.setInputToDefault(config.plugins.SevenHD.FrontInfo)
        self.setInputToDefault(config.plugins.SevenHD.SevenECM)
        self.setInputToDefault(config.plugins.SevenHD.SevenSat)
        self.setInputToDefault(config.plugins.SevenHD.SevenSys1)
        self.setInputToDefault(config.plugins.SevenHD.SevenSys2)
        self.setInputToDefault(config.plugins.SevenHD.SevenWeather1)
        self.setInputToDefault(config.plugins.SevenHD.SevenWeather2)
        self.setInputToDefault(config.plugins.SevenHD.SevenWeather3)
        self.save()
        
    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)
    
    def save(self):
        
        if config.plugins.SevenHD.WeatherStyle_1.value != 'none' or config.plugins.SevenHD.WeatherStyle_2.value != 'none' or config.plugins.SevenHD.ClockStyle.value == "clock-android" or config.plugins.SevenHD.ClockStyle.value == "clock-weather":
           self.preview = False
           self.get_weather_data()
           
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
            else:
                pass

        configfile.save()
        self.exit()

    def exit(self):
        for x in self["config"].list:
            if len(x) > 1:
                    x[1].cancel()
            else:
                    pass
        self.close()
    
    def get_weather_data(self):
           
           self.city = ''
           self.lat = ''
           self.lon = ''
           self.zipcode = ''
           self.msn_id = ''
           self.accu_id = ''
           self.woe_id = ''
           self.gm_code = ''
           self.preview_text = ''
           
           if config.plugins.SevenHD.weather_search_over.value == 'ip':
              self.get_latlon_by_ip()
           elif config.plugins.SevenHD.weather_search_over.value == 'name':
              self.get_latlon_by_name()
           elif config.plugins.SevenHD.weather_search_over.value == 'woeid':
              self.get_latlon_by_woeid()
           elif config.plugins.SevenHD.weather_search_over.value == 'gmcode':
              self.get_latlon_by_gmcode()
           elif config.plugins.SevenHD.weather_search_over.value == 'latlon':
              self.get_latlon_by_latlon() 
           elif config.plugins.SevenHD.weather_search_over.value == 'auto':
              self.get_latlon_by_homepage()
           
           if config.plugins.SevenHD.weather_server.value == '_yahoo':
              self.get_woe_id_by_latlon()
           elif config.plugins.SevenHD.weather_server.value == '_owm':
              self.generate_owm_accu_realtek_string()
           elif config.plugins.SevenHD.weather_server.value == '_msn':
              self.get_msn_id_by_latlon()
           elif config.plugins.SevenHD.weather_server.value == '_accu':
              self.get_accu_id_by_latlon()
           elif config.plugins.SevenHD.weather_server.value == '_realtek':
              self.generate_owm_accu_realtek_string()
    
           # tomele
           # added
           config.plugins.SevenHD.weather_foundcity.value=self.city
           config.plugins.SevenHD.weather_foundcity.save()

           if self.preview:
              self["helperimage"].hide()
              self["preview"].show()
              self["preview"].setText(str(self.preview_text))
              self.preview = False
    
    def get_latlon_by_ip(self):
        try:
           res = requests.request('get', 'http://api.wunderground.com/api/2b0d6572c90d3e4a/geolookup/q/autoip.json')
           data = res.json()
           
           self.city = data['location']['city']
           self.lat = data['location']['lat'] 
           self.lon = data['location']['lon']
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:
           self.session.open(MessageBox, _('No Data for IP'), MessageBox.TYPE_INFO, timeout = 5)
           
    def get_latlon_by_name(self):
        try:
           name = config.plugins.SevenHD.weather_cityname.getValue()
           res = requests.request('get', 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % str(name))
           data = res.json()
           
           for info in data['results'][0]['address_components'][0]['types']:
              if 'locality' in info:
                 self.city = data['results'][0]['address_components'][0]['long_name']
           
           self.lat = data['results'][0]['geometry']['location']['lat']
           self.lon = data['results'][0]['geometry']['location']['lng']
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:
           self.get_latlon_by_ip()
           self.session.open(MessageBox, _('No Data on Name, fallback over IP'), MessageBox.TYPE_INFO, timeout = 5)
    
    def get_latlon_by_gmcode(self):
        try:        
           gmcode = config.plugins.SevenHD.weather_gmcode.value
           res = requests.request('get', 'http://wxdata.weather.com/wxdata/weather/local/%s?cc=*' % str(gmcode))
           data = fromstring(res.text)
           
           self.city = data[1][0].text.split(',')[0]
           self.lat = data[1][2].text
           self.lon = data[1][3].text
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:
           self.get_latlon_by_ip()
           self.session.open(MessageBox, _('No Data on GM Code, fallback over IP'), MessageBox.TYPE_INFO, timeout = 5)
       
    def get_latlon_by_woeid(self):
        try:
           res = requests.request('get', 'http://query.yahooapis.com/v1/public/yql?format=json&q=select * from geo.places where woeid = "%s"' % str(config.plugins.SevenHD.weather_woe_id.value))
           data = res.json()              
           
           self.city = data['query']['results']['place']['name']
           self.lat = data['query']['results']['place']['centroid']['latitude']
           self.lon = data['query']['results']['place']['centroid']['longitude']
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:    
           self.get_latlon_by_rss()
           self.session.open(MessageBox, _('No Data by WOEID, try RSS'), MessageBox.TYPE_INFO, timeout = 5)
           
    def get_latlon_by_rss(self):
        try:
           res = requests.request('get', 'http://weather.yahooapis.com/forecastrss?w=%s&u=c' % str(config.plugins.SevenHD.weather_woe_id.value))
           
           self.city = re.search('city="(.+?)" region', str(res.text)).groups(1)
           self.lat = re.search('geo:lat.+>(.+?)</geo:lat', str(res.text)).groups(1)
           self.lon = re.search('geo:long.+>(.+?)</geo:long', str(res.text)).groups(1)
           self.gm_code = re.search('/forecast/(.+?)_c.html', str(res.text)).groups(1)
           
           # tomele
           # save added
           config.plugins.SevenHD.weather_gmcode.value = str(self.gm_code)
           config.plugins.SevenHD.weather_gmcode.save()
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:
           self.get_latlon_by_ip()
           self.session.open(MessageBox, _('No Data on RSS, fallback over IP'), MessageBox.TYPE_INFO, timeout = 5)

    def get_latlon_by_latlon(self):
        try:
           lat = config.plugins.SevenHD.weather_lat.getValue()
           lon = config.plugins.SevenHD.weather_lon.getValue()
           
           res = requests.request('get', 'http://maps.googleapis.com/maps/api/geocode/json?address=' + str(lat) + ',' + str(lon) + '&sensor=true')
           data = res.json()
           
           for info in data['results'][0]['address_components']:
              if 'locality' in info['types']:
                 self.city = info['long_name']
           
           self.lat = data['results'][0]['geometry']['location']['lat']
           self.lon = data['results'][0]['geometry']['location']['lng']
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon)
        except:
           self.get_latlon_by_ip()
           self.session.open(MessageBox, _('No Data on Lat/Lon, fallback over IP'), MessageBox.TYPE_INFO, timeout = 5)
    
    def get_latlon_by_homepage(self):
        try:
           res = requests.request('get', 'https://de.yahoo.com')
           d = re.search('currentLoc":{"woeid":"(.+?)","city":"(.+?)"', str(res.text)).groups(1)
                        
           self.city = str(d[1])
           self.woe_id = str(d[0])
           
           # tomele
           # save added
           config.plugins.SevenHD.weather_woe_id.value = str(self.woe_id)
           config.plugins.SevenHD.weather_woe_id.save()
           
           self.get_latlon_by_woeid()
        except:
           self.get_latlon_by_ip()
           self.session.open(MessageBox, _('No Data on Homepage, fallback over IP'), MessageBox.TYPE_INFO, timeout = 5)
           
    def get_msn_id_by_latlon(self):
        try:
           res = requests.request('get', 'http://weather.service.msn.com/find.aspx?src=outlook&weadegreetype=C&culture=%s&weasearchstr=%s,%s' % (str(config.plugins.SevenHD.weather_language.value), str(self.lat), str(self.lon)))
           data = fromstring(res.text.encode('utf-8'))
           
           for child in data:
               self.city = child.attrib.get('weatherlocationname').split(',')[0]
               self.zipcode = child.attrib.get('zipcode')
               self.lat = child.attrib.get('lat').replace(',','.')
               self.lon = child.attrib.get('long').replace(',','.')
               self.msn_id = child.attrib.get('entityid')
           
           # tomele
           # save added
           config.plugins.SevenHD.weather_msn_id.value = str(self.msn_id)
           config.plugins.SevenHD.weather_msn_id.save()
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon) + '\nMSN ID: ' + str(self.msn_id)    
        except:
           self.session.open(MessageBox, _('No MSN Id found'), MessageBox.TYPE_INFO, timeout = 5)
           
    def get_accu_id_by_latlon(self):
        try:
           self.generate_owm_accu_realtek_string()    #htc2 androiddoes
           res = requests.request('get', 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp?%s' % config.plugins.SevenHD.weather_realtek_latlon.value)
           
           cityId = re.search('cityId>(.+?)</cityId', str(res.text)).groups(1)
           city = re.search('city>(.+?)</city', str(res.text)).groups(1)
           lat = re.search('lat>(.+?)</lat', str(res.text)).groups(1)
           lon = re.search('lon>(.+?)</lon', str(res.text)).groups(1)
           
           # tomele
           # only if needed, because of wrong encoding of umlauts at realtek
           if self.city=='':
               self.city = str(city[0])
           
           self.accu_id = str(cityId[0])
           self.lat = str(lat[0])
           self.lon = str(lon[0])
           
           # tomele
           # save added
           config.plugins.SevenHD.weather_accu_id.value = str(self.accu_id)
           config.plugins.SevenHD.weather_accu_id.save()
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon) + '\nAccu ID: ' + str(self.accu_id)
        except:
           self.session.open(MessageBox, _('No Accu Id found'), MessageBox.TYPE_INFO, timeout = 5)
    
    def get_woe_id_by_latlon(self):
        try:
           res = requests.request('get', 'http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where text = "%s,%s" and gflags = "R"&format=json' % (str(self.lat), str(self.lon)))
           data = res.json()
           
           self.woe_id = data['query']['results']['Result']['woeid']
           self.city = data['query']['results']['Result']['city']
           self.lat = data['query']['results']['Result']['latitude']
           self.lon = data['query']['results']['Result']['longitude']
           
           # tomele
           # save added
           config.plugins.SevenHD.weather_woe_id.value = str(self.woe_id)
           config.plugins.SevenHD.weather_woe_id.save()
           
           self.preview_text = 'City: ' + str(self.city) + '\nLati: ' + str(self.lat) + '\nLong: ' + str(self.lon) + '\nWOE ID: ' + str(self.woe_id)
        except:
           self.session.open(MessageBox, _('No WOE Id found'), MessageBox.TYPE_INFO, timeout = 5)
           
    def generate_owm_accu_realtek_string(self):
        config.plugins.SevenHD.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.SevenHD.weather_language.value))
        config.plugins.SevenHD.weather_owm_latlon.save()
        config.plugins.SevenHD.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.SevenHD.weather_language.value))
        config.plugins.SevenHD.weather_accu_latlon.save()
        config.plugins.SevenHD.weather_realtek_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.SevenHD.weather_language.value))
        config.plugins.SevenHD.weather_realtek_latlon.save()
               
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[InfobarExtraSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[InfobarExtraSettings]' + str(what) + '\n')
           f.close() 