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
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <eLabel position="70,12" size="708,46" text="SevenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
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
        self["helperimage"] = Pixmap()
        self["description"] = Label()
        self["blue"] = Label()
        
        if config.plugins.SevenHD.grabdebug.value:
           self["blue"].setText('Screenshot')
           
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
            "blue": self.grab_png,
            "ok": self.rawinput,
            "cancel": self.exit
        }, -1)

        self.onLayoutFinish.append(self.UpdatePicture)
        
    def getMenuItemList(self):
        list = []
        list.append(getConfigListEntry(_('_____________________________infobar extras________________________________________'), ))
        list.append(getConfigListEntry(_("satellite information"),            config.plugins.SevenHD.SatInfo,         'Zeigt die Satelliten Informationen auf der rechten Seite.',                    '1',        ''))
        list.append(getConfigListEntry(_("system information"),               config.plugins.SevenHD.SysInfo,         'Zeigt die System Informationen auf der rechten Seite.',                 '1',        ''))
        list.append(getConfigListEntry(_("ECM information"),                  config.plugins.SevenHD.ECMInfo,         'Zeigt die ECM Informationen im unteren Bereich der Infobar an.',        '1',        ''))
        list.append(getConfigListEntry(_('________________________________weather____________________________________________'), ))
        if config.plugins.SevenHD.WeatherStyle.value == 'none':
           list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle,    'Zeigt das Wetter an.',                      '4',        'none'))
        else:
           list.append(getConfigListEntry(_("weather"),                       config.plugins.SevenHD.WeatherStyle,    'Zeigt das Wetter an.',                      '1',        ''))
        
        if config.plugins.SevenHD.WeatherStyle.value != 'none' or config.plugins.SevenHD.ClockStyle.value == "clock-android" or config.plugins.SevenHD.ClockStyle.value == "clock-weather":
           list.append(getConfigListEntry(_("Server"),                        config.plugins.SevenHD.AutoWoeIDServer, 'Stellt den Server ein, wor\xc3\xbcber die Wetterdaten gesucht werden sollen.','4','server'))
           if config.plugins.SevenHD.AutoWoeIDServer.value != 'yahoo':
              list.append(getConfigListEntry(_("Language for Weather"),       config.plugins.SevenHD.weather_language,'Stellt die Ausgabesprache ein.',                               '4',        'language'))
           
           list.append(getConfigListEntry(_("Weather Style"),                 config.plugins.SevenHD.WeatherView,     'W\xc3\xa4hle zwischen Wetter Icon oder Meteo.',                      '1',        ''))
           if config.plugins.SevenHD.WeatherView.value == 'meteo':
              list.append(getConfigListEntry(_("Meteo Color"),                config.plugins.SevenHD.MeteoColor,      'Stellt die Farbe des MeteoIcon ein.',                          '4',        'MeteoColor'))
           list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.SevenHD.refreshInterval, 'Stellt die Abfragezeit des Wetter ein.',                       '4',        'MeteoColor'))
           if config.plugins.SevenHD.AutoWoeID.value == True:
              list.append(getConfigListEntry(_("auto weather ID"),            config.plugins.SevenHD.AutoWoeID,       'Auf JA, wird deine Stadt automatisch gesucht und eingestellt.', '4',        'True'))
           else:
              list.append(getConfigListEntry(_("auto weather ID"),            config.plugins.SevenHD.AutoWoeID,       'Auf JA, wird deine Stadt automatisch gesucht und eingestellt.', '4',        'none'))
           if config.plugins.SevenHD.AutoWoeID.value == False:
              list.append(getConfigListEntry(_("weather ID"),                 config.plugins.SevenHD.weather_city,    'Gib hier deine WoeID ein.',                                    '4',        'WOEID'))
           
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        returnValue = self["config"].getCurrent()[3]
        self.debug('\nRet_value[3]: ' + str(returnValue))		
           		
        if returnValue == '4':
           returnValue = self["config"].getCurrent()[int(returnValue)]
        else:
           returnValue = self["config"].getCurrent()[int(returnValue)].value
        
        self.debug('Ret_value[4]: ' + str(returnValue))   
        path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
        
        self["description"].setText(self["config"].getCurrent()[2])
        
        if fileExists(path):
           return path
        else:
           self.debug('Missing Picture: ' + str(path) + '\n')
           return MAIN_IMAGE_PATH + str("924938.jpg")

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()
        returnValue = self["config"].getCurrent()[4]
        if returnValue == 'WOEID': 
           self.session.openWithCallback(self.do_search, VirtualKeyBoard, title = _("Enter youre WOEID"))
           
    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()
        returnValue = self["config"].getCurrent()[4]
        if returnValue == 'WOEID': 
           self.session.openWithCallback(self.do_search, VirtualKeyBoard, title = _("Enter youre WOEID"))
           
    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()

    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()

    def rawinput(self):
        returnValue = self["config"].getCurrent()[4]
        if returnValue == 'WOEID': 
           self.session.openWithCallback(self.do_search, VirtualKeyBoard, title = _("Enter youre WOEID"))
    
    def do_search(self, number = None):
        try:
           if int(number):
	      config.plugins.SevenHD.weather_city.value = str(number)
	except:
           config.plugins.SevenHD.weather_city.value = "924938"
           self.session.open(MessageBox, _('Only Numbers allowed!\n'), MessageBox.TYPE_INFO)
    
    def grab_png(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
           
    def defaults(self):
        self.setInputToDefault(config.plugins.SevenHD.WeatherStyle)
        self.setInputToDefault(config.plugins.SevenHD.AutoWoeIDServer)
        self.setInputToDefault(config.plugins.SevenHD.AutoWoeID)
        self.setInputToDefault(config.plugins.SevenHD.weather_city)
        self.setInputToDefault(config.plugins.SevenHD.weather_cityname)
        self.setInputToDefault(config.plugins.SevenHD.weather_language)
        self.setInputToDefault(config.plugins.SevenHD.weather_lat_lon)
        self.setInputToDefault(config.plugins.SevenHD.WeatherView)
        self.setInputToDefault(config.plugins.SevenHD.MeteoColor)
        self.setInputToDefault(config.plugins.SevenHD.SatInfo)
        self.setInputToDefault(config.plugins.SevenHD.SysInfo)
        self.setInputToDefault(config.plugins.SevenHD.ECMInfo)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def save(self):
        
        if config.plugins.SevenHD.WeatherStyle.value != 'none' or config.plugins.SevenHD.ClockStyle.value == "clock-android" or config.plugins.SevenHD.ClockStyle.value == "clock-weather":
           if config.plugins.SevenHD.AutoWoeID.value == True:
              self.getgeo()
        
           if config.plugins.SevenHD.AutoWoeIDServer.value != 'yahoo':
              self.getlatlon()
           
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
    
    def getgeo(self):
        #            Auto Weather ID Function by .:TBX:.
       	#               for MyMetrix or Kraven Skins
	        
        try:                
                        res = requests.request('get', 'https://de.yahoo.com')
                        d = re.search('currentLoc":{"woeid":"(.+?)","city":"(.+?)"', str(res.text)).groups(1)
                        
                        city = str(d[1])
                        woeid = d[0]
                        
                        self.debug('Founded WoeID: ' + str(woeid))
                        self.debug('Founded City: ' + str(city) + '\n')
                        
                        config.plugins.SevenHD.weather_cityname.value = str(city)
                        config.plugins.SevenHD.weather_cityname.save()
                        
                        config.plugins.SevenHD.weather_city.value = woeid
                        config.plugins.SevenHD.weather_city.save()
                        
                        self.session.open(MessageBox, _(str(city) + ' is detected and set as your Location.\nIf that should not be right then set\nAuto Weather ID Function to "OFF".'), MessageBox.TYPE_INFO)
      
        except:
                    self.debug('Anything goes wrong \n')
                    self.an_error()
                               
    def an_error(self):
        self.debug('ServerError WoeID')
        config.plugins.SevenHD.weather_city.value = "924938"
        config.plugins.SevenHD.AutoWoeID.value = False
    
    def getlatlon(self):
        res = requests.request('get', 'http://weather.yahooapis.com/forecastrss?w=%s&u=c' % str(config.plugins.SevenHD.weather_city.value))
        city = re.search('city="(.+?)" region', str(res.text)).groups(1)
        lat = re.search('geo:lat>(.+?)</geo:lat', str(res.text)).groups(1)
        lon = re.search('geo:long>(.+?)</geo:long', str(res.text)).groups(1)
        config.plugins.SevenHD.weather_cityname.value = str(city[0])
        config.plugins.SevenHD.weather_cityname.save()
        config.plugins.SevenHD.weather_lat_lon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(lat[0]),str(lon[0]),str(config.plugins.SevenHD.weather_language.value))
        config.plugins.SevenHD.weather_lat_lon.save()
        
        self.debug('lat/long :' + str(lat[0]) + ' - ' + str(lon[0]) + '\n%s' % config.plugins.SevenHD.weather_lat_lon.value)
        
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