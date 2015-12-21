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
class InfobarSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <eLabel position="70,12" size="708,46" text="SevenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 26" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
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
            "cancel": self.exit
        }, -1)

        self.onLayoutFinish.append(self.UpdatePicture)

    def getMenuItemList(self):
        list = []
        list.append(getConfigListEntry(_('_______________________________style___________________________________________'), ))
        list.append(getConfigListEntry(_("infobar"),                 config.plugins.SevenHD.InfobarStyle,         'W\xc3\xa4hle den Stil der Infobar.',                                                                          '1',       ''))
        if config.plugins.SevenHD.SIB.value == '-top':
           list.append(getConfigListEntry(_("second infobar"),          config.plugins.SevenHD.SIB,               'W\xc3\xa4hle den Stil der zweiten Infobar',                                                                    '4',       'SIB1'))
        if config.plugins.SevenHD.SIB.value == '-left':
           list.append(getConfigListEntry(_("second infobar"),          config.plugins.SevenHD.SIB,               'W\xc3\xa4hle den Stil der zweiten Infobar',                                                                    '4',       'SIB2'))
        if config.plugins.SevenHD.SIB.value == '-full':
           list.append(getConfigListEntry(_("second infobar"),          config.plugins.SevenHD.SIB,               'W\xc3\xa4hle den Stil der zweiten Infobar',                                                                    '4',       'SIB3'))
        if config.plugins.SevenHD.SIB.value == '-minitv':
           list.append(getConfigListEntry(_("second infobar"),          config.plugins.SevenHD.SIB,               'W\xc3\xa4hle den Stil der zweiten Infobar',                                                                    '4',       'SIB4'))
        if config.plugins.SevenHD.SIB.value == '-right':
           list.append(getConfigListEntry(_("second infobar"),          config.plugins.SevenHD.SIB,               'W\xc3\xa4hle den Stil der zweiten Infobar',                                                                    '4',       'SIB5'))
        #list.append(getConfigListEntry(_("progress-/volumebar"), config.plugins.SevenHD.ProgressInfobar, 'ProgressInfobar'))
        list.append(getConfigListEntry(_('_____________________________background________________________________________'), ))
        list.append(getConfigListEntry(_("primary font"),                 config.plugins.SevenHD.BackgroundIB1,        'Stellt die Farbe der linken Seite sowie den unteren Bereich der Infobar ein.',                         '4',       'Color1'))
        list.append(getConfigListEntry(_("secondary font"),                 config.plugins.SevenHD.BackgroundIB2,        'Stellt die Farbe der rechten Seite sowie den mittigen Bereich der Infobar ein.',                       '4',       'Color2'))
        list.append(getConfigListEntry(_('_____________________________color lines_______________________________________'), ))
        list.append(getConfigListEntry(_("line"),                    config.plugins.SevenHD.InfobarLine,          'Stellt die Farbe der Linie unter dem Fortschrittsbalken in der Infobar ein.',                          '4',       'InfobarLine'))
        list.append(getConfigListEntry(_("border"),                  config.plugins.SevenHD.InfobarBorder,        'Stellt die Rahmenfarbe der Infobar ein.',                                                              '4',       'InfobarBorder'))
        list.append(getConfigListEntry(_("progressbar"),             config.plugins.SevenHD.ProgressIB,           'Stellt die Farbe des Sendungsforschritt in der Infobar ein.',                                          '4',       'progressib'))
        list.append(getConfigListEntry(_("progressbar line"),        config.plugins.SevenHD.ProgressLineIB,       'Stellt die Farbe der Linie unter dem Fortschrittsbalken in der Infobar ein.',                          '4',       'progresslineib'))
        list.append(getConfigListEntry(_('______________________________color font________________________________________'), ))
        if config.plugins.SevenHD.InfobarChannelName.value == 'none':
           list.append(getConfigListEntry(_("channelname"),             config.plugins.SevenHD.InfobarChannelName,'Auswahl zwischen der Anzeige Name, Nummer, Name und Nummer oder Aus, wenn die Infobar angezeigt wird.','4',       'none'))
        else:
           list.append(getConfigListEntry(_("channelname"),             config.plugins.SevenHD.InfobarChannelName,'Auswahl zwischen der Anzeige Name, Nummer, Name und Nummer oder Aus, wenn die Infobar angezeigt wird.','4',       'channelname'))
        if config.plugins.SevenHD.InfobarChannelName.value != 'none':
           list.append(getConfigListEntry(_("color channelname"),    config.plugins.SevenHD.FontCN,               'Stellt die Farbe des Sendernamen ein.',                                                                '4',       'ColorCN'))
        list.append(getConfigListEntry(_("now event"),               config.plugins.SevenHD.NowEvent,             'Stellt die Farbe der aktuellen Programmbeschreibung ein.',                                             '4',       'NowEvent'))
        list.append(getConfigListEntry(_("next event"),              config.plugins.SevenHD.NextEvent,            'Stellt die Farbe der n\xc3\xa4chsten Programmbeschreibung ein.',                                             '4',       'NextEvent'))
        list.append(getConfigListEntry(_("indicate"),                config.plugins.SevenHD.SNR,                  'Stellt die Farbe der Zusatzinfos (SNR, Videogr\xc3\xb6\xc3\x9fe, ...) in der Infobar ein.',                        '4',       'snr'))
        list.append(getConfigListEntry(_('_______________________________clock___________________________________________'), ))
        list.append(getConfigListEntry(_("style"),                   config.plugins.SevenHD.ClockStyle,           'W\xc3\xa4hle den Stil der Uhr.',                                                                             '1',       ''))
        if config.plugins.SevenHD.ClockStyle.value == "clock-analog":
	   list.append(getConfigListEntry(_("color clock"),          config.plugins.SevenHD.AnalogStyle,          'Stellt die Farbe vom Ziffernblatt ein.',                                                               '4',       'Analog'))
           list.append(getConfigListEntry(_("color date"),           config.plugins.SevenHD.ClockDate,            'Stellt die Farbe des Datums ein.',                                                                     '4',       'ClockDate'))
           list.append(getConfigListEntry(_("color pointer hour"),   config.plugins.SevenHD.ClockTimeh,           'Stellt die Farbe des Stundenzeiger ein.',                                                             '4',       'ClockTimeh'))
	   list.append(getConfigListEntry(_("color pointer minute"), config.plugins.SevenHD.ClockTimem,           'Stellt die Farbe des Minutenzeiger ein.',                                                             '4',       'ClockTimem'))
	   list.append(getConfigListEntry(_("color pointer second"), config.plugins.SevenHD.ClockTimes,           'Stellt die Farbe des Sekundenzeiger ein.',                                                            '4',       'ClockTimes'))
        if config.plugins.SevenHD.ClockStyle.value == "clock-standard" or config.plugins.SevenHD.ClockStyle.value == "clock-seconds":
	   list.append(getConfigListEntry(_("color time"),           config.plugins.SevenHD.ClockTime,            'Stellt die Farbe der Zeit ein.',                                                                       '4',       'ClockTime'))
	   list.append(getConfigListEntry(_("color date"),           config.plugins.SevenHD.ClockDate,            'Stellt die Farbe des Datum ein.',                                                                      '4',       'ClockDate'))
        if config.plugins.SevenHD.ClockStyle.value == "clock-weekday":
	   list.append(getConfigListEntry(_("color time"),           config.plugins.SevenHD.ClockTime,            'Stellt die Farbe der Zeit ein.',                                                                       '4',       'ClockTime'))
	   list.append(getConfigListEntry(_("color date"),           config.plugins.SevenHD.ClockDate,            'Stellt die Farbe des Datum ein.',                                                                      '4',       'ClockDate'))
	   list.append(getConfigListEntry(_("color weekday"),        config.plugins.SevenHD.ClockWeek,            'Stellt die Farbe des Wochetages ein.',                                                                      '4',       'ClockWeek'))
        if config.plugins.SevenHD.ClockStyle.value == "clock-weather" or config.plugins.SevenHD.ClockStyle.value == "clock-weather-meteo":
	   list.append(getConfigListEntry(_("color time"),           config.plugins.SevenHD.ClockTime,            'Stellt die Farbe der Zeit ein.',                                                                       '4',       'ClockTime'))
	   list.append(getConfigListEntry(_("color date"),           config.plugins.SevenHD.ClockDate,            'Stellt die Farbe des Datum ein.',                                                                      '4',       'ClockDate'))
	   list.append(getConfigListEntry(_("color weather"),        config.plugins.SevenHD.ClockWeather,         'Stellt die Farbe von der Temperatur ein.',                                                             '4',       'ClockWeather'))
        if config.plugins.SevenHD.ClockStyle.value == "clock-android":
	   list.append(getConfigListEntry(_("color date"),           config.plugins.SevenHD.ClockDate,            'Stellt die Farbe des Datum ein.',                                                                      '4',       'ClockDate'))
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

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()

    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()

    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
    
    def grab_png(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
           
    def defaults(self):
        self.setInputToDefault(config.plugins.SevenHD.InfobarStyle)
        self.setInputToDefault(config.plugins.SevenHD.SIB)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundIB1)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundIB2)
        self.setInputToDefault(config.plugins.SevenHD.InfobarLine)
        self.setInputToDefault(config.plugins.SevenHD.InfobarBorder)
        self.setInputToDefault(config.plugins.SevenHD.InfobarChannelName)
        self.setInputToDefault(config.plugins.SevenHD.FontCN)
        self.setInputToDefault(config.plugins.SevenHD.NowEvent)
        self.setInputToDefault(config.plugins.SevenHD.NextEvent)
        self.setInputToDefault(config.plugins.SevenHD.SNR)
        self.setInputToDefault(config.plugins.SevenHD.ClockStyle)
        self.setInputToDefault(config.plugins.SevenHD.AnalogStyle)
        self.setInputToDefault(config.plugins.SevenHD.ClockDate)
        self.setInputToDefault(config.plugins.SevenHD.ClockTimeh)
        self.setInputToDefault(config.plugins.SevenHD.ClockTimem)
        self.setInputToDefault(config.plugins.SevenHD.ClockTimes)
        self.setInputToDefault(config.plugins.SevenHD.ClockTime)
        self.setInputToDefault(config.plugins.SevenHD.ClockWeek)
        self.setInputToDefault(config.plugins.SevenHD.ClockWeather)
        self.setInputToDefault(config.plugins.SevenHD.ProgressLineIB)
        self.setInputToDefault(config.plugins.SevenHD.ProgressIB)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def save(self):
        
        if config.plugins.SevenHD.skin_mode.value > '3':
           if 'back' in config.plugins.SevenHD.BackgroundIB1.value:
              self.setInputToDefault(config.plugins.SevenHD.BackgroundIB1)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
           if 'back' in config.plugins.SevenHD.BackgroundIB2.value:
              self.setInputToDefault(config.plugins.SevenHD.BackgroundIB2)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
        
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
    
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[InfobarSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[InfobarSettings]' + str(what) + '\n')
           f.close() 