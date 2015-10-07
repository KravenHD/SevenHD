# -*- coding: utf-8 -*-
#######################################################################
#
#    SevenHD by Kraven, TBX & örlgrey
#    based on
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################
from GlobalImport import *
from OnlineUpdate import *
from MainSettings import MainSettings
from MenuPluginSettings import MenuPluginSettings
from InfobarSettings import InfobarSettings
from InfobarExtraSettings import InfobarExtraSettings
from ChannelSettings import ChannelSettings
from SonstigeSettings import SonstigeSettings
from ShareSkinSettings import ShareSkinSettings

class MainMenuList(MenuList):
    def __init__(self, list, font0 = 24, font1 = 16, itemHeight = 50, enableWrapAround = True):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        screenwidth = getDesktop(0).size().width()
        if screenwidth and screenwidth == 1920:
            self.l.setFont(0, gFont("Regular", int(font0*1.5)))
            self.l.setFont(1, gFont("Regular", int(font1*1.5)))
            self.l.setItemHeight(int(itemHeight*1.5))
        else:
            self.l.setFont(0, gFont("Regular", font0))
            self.l.setFont(1, gFont("Regular", font1))
            self.l.setItemHeight(itemHeight)

#############################################################

def MenuEntryItem(itemDescription, key):
    res = [(itemDescription, key)]
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        res.append(MultiContentEntryText(pos=(15, 8), size=(660, 68), font=0, text=itemDescription))
    else:
        res.append(MultiContentEntryText(pos=(10, 5), size=(440, 45), font=0, text=itemDescription))
    return res

#############################################################
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
#############################################################
class SevenHD(Screen):
    skin =  """<screen name="SevenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent"> 
                     <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                     <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                     <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Reboot" transparent="1" />
                     <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" text="Extras" transparent="1" />
                     <widget name="menuList" position="18,72" size="816,575" backgroundColor="#00000000"  scrollbarMode="showOnDemand" transparent="1" />
                     <eLabel position="70,12" size="708,46" text="SevenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                     <eLabel position="891,657" size="372,46" text="Thanks to http://www.gigablue-support.org/" font="Regular; 12" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                     <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                     <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
                     <eLabel backgroundColor="#00000000" position="6,6" size="842,708" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
                     <eLabel backgroundColor="#00ffffff" position="6,6" size="842,2" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="6,714" size="842,2" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="6,6" size="2,708" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="848,6" size="2,708" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="18,64" size="816,2" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="18,656" size="816,2" zPosition="2" />
                     <ePixmap pixmap="SevenHD/buttons/key_red1.png" position="22,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
                     <ePixmap pixmap="SevenHD/buttons/key_green1.png" position="222,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
                     <ePixmap pixmap="SevenHD/buttons/key_yellow1.png" position="422,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
                     <ePixmap pixmap="SevenHD/buttons/key_blue1.png" position="622,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
                     <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                             <convert type="ClockToText">Default</convert>
                     </widget>
                     <eLabel backgroundColor="#00000000" position="878,6" size="396,708" transparent="0" zPosition="-9" />
                     <eLabel backgroundColor="#00ffffff" position="878,6" size="396,2" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="878,714" size="396,2" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="878,6" size="2,708" zPosition="2" />
                     <eLabel backgroundColor="#00ffffff" position="1274,6" size="2,708" zPosition="2" />
                     <eLabel position="891,88" size="415,46" text="Version: """ + str(version) + """" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                     <widget source="session.CurrentService" render="Label" position="891,134" size="415,28" font="Regular;26" halign="left" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                     </widget>
               </screen>"""
                  
    def __init__(self, session, args = None):
        self.session = session
        
        Screen.__init__(self, session)
        
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self["helperimage"] = Pixmap()

        self["actions"] = ActionMap(
            [
                "OkCancelActions",
                "DirectionActions",
                "InputActions",
                "ColorActions"
            ],
            {
                "ok": self.ok,
                "cancel": self.exit,
                "red": self.exit,
                "green": self.save,
                "yellow": self.reboot,
                "blue": self.showInfo
                
            }, -1)	
        creator = 'openATV'
        try:
           image = os.popen('cat /etc/image-version').read()
           if 'creator=OpenMips' in image: 
              creator = 'OpenMips'
        except:
           try:
              image = os.popen('cat /etc/motd').read()
              if 'HDMU' in image: 
                 creator = 'OpenMips'
           except:
              creator = 'unknow'
        self.debug('Image-Type: ' + str(creator) + '\n')   
           
        list = []
        list.append(MenuEntryItem(_("main setting"), "MainSettings"))
        list.append(MenuEntryItem(_("menu and plugins"), "MenuPluginSettings"))
        list.append(MenuEntryItem(_("infobar and second infobar"), "InfobarSettings"))
        list.append(MenuEntryItem(_("infobar extras"), "InfobarExtraSettings"))
        list.append(MenuEntryItem(_("channel selection"), "ChannelSettings"))
        list.append(MenuEntryItem(_("other settings"), "SonstigeSettings"))
        list.append(MenuEntryItem(_("system osd settings"), "SystemOSDSettings"))
        if creator != 'OpenMips':
           list.append(MenuEntryItem(_("system channel settings"), "SystemChannelSettings"))
        
        self["menuList"] = MainMenuList([], font0=24, font1=16, itemHeight=50)
        self["menuList"].l.setList(list)

        if not self.__selectionChanged in self["menuList"].onSelectionChanged:
            self["menuList"].onSelectionChanged.append(self.__selectionChanged)

        self.onChangedEntry = []

        self.onLayoutFinish.append(self.UpdatePicture)

    def __del__(self):
        self["menuList"].onSelectionChanged.remove(self.__selectionChanged)

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        if self["helperimage"] is None or self["helperimage"].instance is None:
            return

        cur = self["menuList"].getCurrent()

        if cur:
            selectedKey = cur[0][1]
            self.debug('def ShowPicture\nneed: ' + MAIN_IMAGE_PATH + str(selectedKey) + '.jpg\n')
            if selectedKey == "MainSettings":
               imageUrl = MAIN_IMAGE_PATH + str("MAINSETTINGS.jpg")
            elif selectedKey == "MenuPluginSettings":
               imageUrl = MAIN_IMAGE_PATH + str("MENU.jpg")
            elif selectedKey == "InfobarSettings":
               imageUrl = MAIN_IMAGE_PATH + str("IB.jpg")
            elif selectedKey == "InfobarExtraSettings":
               imageUrl = MAIN_IMAGE_PATH + str("EXTRA.jpg")
            elif selectedKey == "ChannelSettings":
               imageUrl = MAIN_IMAGE_PATH + str("CS.jpg")
            elif selectedKey == "SonstigeSettings":
               imageUrl = MAIN_IMAGE_PATH + str("OTHER.jpg")
            elif selectedKey == "SystemOSDSettings":
               imageUrl = MAIN_IMAGE_PATH + str("OSD.jpg")
            elif selectedKey == "SystemChannelSettings":
               imageUrl = MAIN_IMAGE_PATH + str("SCS.jpg")
                        
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(imageUrl)

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def ok(self):
        cur = self["menuList"].getCurrent()
        
        if cur:
            selectedKey = cur[0][1]
            self.debug('def ok\ntry open: "' + selectedKey + '" Screen\n')
            
            if selectedKey == "MainSettings":
                self.session.open(MainSettings)
            elif selectedKey == "MenuPluginSettings":
                self.session.open(MenuPluginSettings)
            elif selectedKey == "InfobarSettings":
                self.session.open(InfobarSettings)
            elif selectedKey == "InfobarExtraSettings":
                self.session.open(InfobarExtraSettings)
    	    elif selectedKey == "ChannelSettings":
                self.session.open(ChannelSettings)  
            elif selectedKey == "SonstigeSettings":
                self.session.open(SonstigeSettings)
            elif selectedKey == "SystemOSDSettings":
                self.session.open(Setup, "userinterface")
            elif selectedKey == "SystemChannelSettings":
                self.session.open(Setup, "channelselection")
                            
    def save(self):
        self.skin_lines = []        
        try:
                #global tag search and replace in all skin elements
		self.skinSearchAndReplace = []
                
                self.Background = config.plugins.SevenHD.Background.value
                if self.Background.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/menumain.png","SevenHD/back/menumain_1.png"])
                else:  
                   self.skinSearchAndReplace.append(['name="SevenBackground" value="#00000000"', 'name="SevenBackground" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.Background[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackground" value="#00000000"', 'name="SevenFontBackground" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.Background[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/menumain.png"',""])
                
                self.BackgroundIB1 = config.plugins.SevenHD.BackgroundIB1.value
                if self.BackgroundIB1.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/ibone.png","SevenHD/back/ibone_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackgroundIB1" value="#00000000"', 'name="SevenBackgroundIB1" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.BackgroundIB1[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackgroundIB1" value="#00000000"', 'name="SevenFontBackgroundIB1" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.BackgroundIB1[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/ibone.png"',""])
                
                self.BackgroundIB2 = config.plugins.SevenHD.BackgroundIB2.value
                if self.BackgroundIB2.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/ibtwo.png","SevenHD/back/ibtwo_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackgroundIB2" value="#00000000"', 'name="SevenBackgroundIB2" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.BackgroundIB2[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackgroundIB2" value="#00000000"', 'name="SevenFontBackgroundIB2" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.BackgroundIB2[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/ibtwo.png"',""])
                
                self.ChannelBack1 = config.plugins.SevenHD.ChannelBack1.value
                if self.ChannelBack1.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/csleft.png","SevenHD/back/csleft_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackCS" value="#00000000"', 'name="SevenBackCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.ChannelBack1[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackCS" value="#00000000"', 'name="SevenFontBackCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.ChannelBack1[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/csleft.png"',""])
                
                self.ChannelBack2 = config.plugins.SevenHD.ChannelBack2.value
                if self.ChannelBack2.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/csright.png","SevenHD/back/csright_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackRightCS" value="#00000000"', 'name="SevenBackRightCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundRightColorTrans.value, self.ChannelBack2[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackRightCS" value="#00000000"', 'name="SevenFontBackRightCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.ChannelBack2[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/csright.png"',""])
                
                self.ChannelBack3 = config.plugins.SevenHD.ChannelBack3.value
                if self.ChannelBack3.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/csmiddle.png","SevenHD/back/csmiddle_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackMiddleCS" value="#00000000"', 'name="SevenBackMiddleCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.ChannelBack3[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackMiddleCS" value="#00000000"', 'name="SevenFontBackMiddleCS" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.ChannelBack3[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/csmiddle.png"',""])
                
                self.BackgroundRight = config.plugins.SevenHD.BackgroundRight.value
                if self.BackgroundRight.startswith('back'):
                   self.skinSearchAndReplace.append(["SevenHD/back/menuright.png","SevenHD/back/menuright_1.png"])
                else:
                   self.skinSearchAndReplace.append(['name="SevenBackgroundRight" value="#00000000"', 'name="SevenBackgroundRight" value="#%s%s"' % (config.plugins.SevenHD.BackgroundRightColorTrans.value, self.BackgroundRight[2:8])])
                   self.skinSearchAndReplace.append(['name="SevenFontBackgroundRight" value="#00000000"', 'name="SevenFontBackgroundRight" value="#%s%s"' % (config.plugins.SevenHD.BackgroundColorTrans.value, self.BackgroundRight[2:8])])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/back/menuright.png"',""])
                
                self.skinSearchAndReplace.append(["PluginVersionString", "Version: %s" % str(version)])
                
		self.skinSearchAndReplace.append(["Seven_Selection", config.plugins.SevenHD.SelectionBackground.value])
		self.skinSearchAndReplace.append(["SevenFont_1", config.plugins.SevenHD.Font1.value])
		self.skinSearchAndReplace.append(["SevenFont_2", config.plugins.SevenHD.Font2.value])
		self.skinSearchAndReplace.append(["SevenSel_Font", config.plugins.SevenHD.SelectionFont.value])
		self.skinSearchAndReplace.append(["SevenButton_Text", config.plugins.SevenHD.ButtonText.value])
		self.skinSearchAndReplace.append(["Seven_Border", config.plugins.SevenHD.Border.value])
		self.skinSearchAndReplace.append(["Seven_Line", config.plugins.SevenHD.Line.value])


		self.skinSearchAndReplace.append(["SevenMeteo_Font", config.plugins.SevenHD.MeteoColor.value])


		self.skinSearchAndReplace.append(["SevenProgress_BorderCS", config.plugins.SevenHD.ProgressBorderCS.value])
		self.skinSearchAndReplace.append(["SevenProgress_LineCS", config.plugins.SevenHD.ProgressLineCS.value])
		self.skinSearchAndReplace.append(["SevenProgress_LineIB", config.plugins.SevenHD.ProgressLineIB.value])
		self.skinSearchAndReplace.append(["SevenProgress_LinePlug", config.plugins.SevenHD.ProgressLinePlug.value])


		self.skinSearchAndReplace.append(["SevenProgress_IB", config.plugins.SevenHD.ProgressIB.value])
		self.skinSearchAndReplace.append(["SevenProgress_Vol", config.plugins.SevenHD.ProgressVol.value])
		self.skinSearchAndReplace.append(["SevenProgress_CS", config.plugins.SevenHD.ProgressCS.value])
		self.skinSearchAndReplace.append(["SevenProgress_ListCS", config.plugins.SevenHD.ProgressListCS.value])


		self.skinSearchAndReplace.append(["SevenBorder_IB", config.plugins.SevenHD.InfobarBorder.value])
		self.skinSearchAndReplace.append(["SevenLine_IB", config.plugins.SevenHD.InfobarLine.value])
		self.skinSearchAndReplace.append(["SevenNext_IB", config.plugins.SevenHD.NextEvent.value])
		self.skinSearchAndReplace.append(["SevenNow_IB", config.plugins.SevenHD.NowEvent.value])
		self.skinSearchAndReplace.append(["SevenSNR_IB", config.plugins.SevenHD.SNR.value])
		self.skinSearchAndReplace.append(["SevenFont_CN", config.plugins.SevenHD.FontCN.value])


		self.skinSearchAndReplace.append(["SevenClock_Date", config.plugins.SevenHD.ClockDate.value])
		self.skinSearchAndReplace.append(["SevenClock_H", config.plugins.SevenHD.ClockTimeh.value])
		self.skinSearchAndReplace.append(["SevenClock_M", config.plugins.SevenHD.ClockTimem.value])
		self.skinSearchAndReplace.append(["SevenClock_S", config.plugins.SevenHD.ClockTimes.value])
		self.skinSearchAndReplace.append(["SevenClock_Time", config.plugins.SevenHD.ClockTime.value])
		self.skinSearchAndReplace.append(["SevenClock_Weather", config.plugins.SevenHD.ClockWeather.value])
		self.skinSearchAndReplace.append(["SevenClock_Weekday", config.plugins.SevenHD.ClockWeek.value])


		self.skinSearchAndReplace.append(["SevenLine_CS", config.plugins.SevenHD.ChannelLine.value])
		self.skinSearchAndReplace.append(["SevenBorder_CS", config.plugins.SevenHD.ChannelBorder.value])
		self.skinSearchAndReplace.append(["SevenButtons_CS", config.plugins.SevenHD.ChannelColorButton.value])
		self.skinSearchAndReplace.append(["SevenBouquet_CS", config.plugins.SevenHD.ChannelColorBouquet.value])
		self.skinSearchAndReplace.append(["SevenChannel_CS", config.plugins.SevenHD.ChannelColorChannel.value])
		self.skinSearchAndReplace.append(["SevenNext_CS", config.plugins.SevenHD.ChannelColorNext.value])
		self.skinSearchAndReplace.append(["SevenDestcriptionNext_CS", config.plugins.SevenHD.ChannelColorDesciptionNext.value])
		self.skinSearchAndReplace.append(["SevenDestcriptionLater_CS", config.plugins.SevenHD.ChannelColorDesciptionLater.value])
		self.skinSearchAndReplace.append(["SevenRuntime_CS", config.plugins.SevenHD.ChannelColorRuntime.value])
		self.skinSearchAndReplace.append(["SevenProgram_CS", config.plugins.SevenHD.ChannelColorProgram.value])
		self.skinSearchAndReplace.append(["SevenTime_CS", config.plugins.SevenHD.ChannelColorTimeCS.value])
		self.skinSearchAndReplace.append(["SevenPrime_CS", config.plugins.SevenHD.ChannelColorPrimeTime.value])
		self.skinSearchAndReplace.append(["SevenDestcription_CS", config.plugins.SevenHD.ChannelColorDesciption.value])
		self.skinSearchAndReplace.append(["SevenName_List", config.plugins.SevenHD.ChannelColorChannelName.value])
		self.skinSearchAndReplace.append(["SevenNumber_List", config.plugins.SevenHD.ChannelColorChannelNumber.value])
		self.skinSearchAndReplace.append(["SevenProgram_List", config.plugins.SevenHD.ChannelColorEvent.value])
		
		
                if config.plugins.SevenHD.WeatherView.value == "meteo":
                   self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="SevenHDPiconUni" alphatest="blend"', 'size="50,50" render="Label" font="Meteo; 45" halign="center" valign="center" foregroundColor="SevenMeteoFont" backgroundColor="SevenFontBackgroundIB1" noWrap="1"'])
                   self.skinSearchAndReplace.append(['size="70,70" render="SevenHDPiconUni" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo; 70" halign="center" valign="center" foregroundColor="SevenMeteoFont" backgroundColor="SevenFontBackgroundIB1" noWrap="1"'])
                   self.skinSearchAndReplace.append(['convert  type="SevenHDVWeather">currentWeatherPicon', 'convert  type="SevenHDVWeather">currentWeatherCode'])
                   self.skinSearchAndReplace.append(['convert  type="SevenHDVWeather">forecastTomorrowPicon', 'convert  type="SevenHDVWeather">forecastTomorrowCode'])
                   self.skinSearchAndReplace.append(['convert  type="SevenHDVWeather">forecastTomorrow1Picon', 'convert  type="SevenHDVWeather">forecastTomorrow1Code'])
                   self.skinSearchAndReplace.append(['convert  type="SevenHDVWeather">forecastTomorrow2Picon', 'convert  type="SevenHDVWeather">forecastTomorrow2Code'])
                   self.skinSearchAndReplace.append(['convert  type="SevenHDVWeather">forecastTomorrow3Picon', 'convert  type="SevenHDVWeather">forecastTomorrow3Code'])
                
                       
                ### Progress
                if config.plugins.SevenHD.Progress.value == "progress":
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress52.png","SevenHD/progress/progress52_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress300.png","SevenHD/progress/progress300_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress362.png","SevenHD/progress/progress362_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress535.png","SevenHD/progress/progress535_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress793.png","SevenHD/progress/progress793_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress858.png","SevenHD/progress/progress858_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress990.png","SevenHD/progress/progress990_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progress/progress1280.png","SevenHD/progress/progress1280_1.png"])
                else:
                   self.skinSearchAndReplace.append(["00fffff1", config.plugins.SevenHD.Progress.value])
                   self.skinSearchAndReplace.append(['picServiceEventProgressbar="SevenHD/progress/progress52.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress300.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress362.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress535.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress793.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress858.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress990.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progress/progress1280.png"',""])
                       
                ### ProgressIB
                if config.plugins.SevenHD.ProgressIB.value == "progressib":
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib621.png","SevenHD/progressib/progressib621_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib638.png","SevenHD/progressib/progressib638_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib770.png","SevenHD/progressib/progressib770_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib793.png","SevenHD/progressib/progressib793_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib812.png","SevenHD/progressib/progressib812_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib858.png","SevenHD/progressib/progressib858_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib1022.png","SevenHD/progressib/progressib1022_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib1045.png","SevenHD/progressib/progressib1045_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressib/progressib1280.png","SevenHD/progressib/progressib1280_1.png"])
                else:
                   self.skinSearchAndReplace.append(["00fffff2", config.plugins.SevenHD.ProgressIB.value])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib621.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib638.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib770.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib793.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib812.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib858.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib1022.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib1045.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressib/progressib1280.png"',""])
                       
                ### ProgressVol
                if config.plugins.SevenHD.ProgressVol.value == "progressvol":
                   self.skinSearchAndReplace.append(["SevenHD/progressvol/progressvol170.png","SevenHD/progressvol/progressvol170_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressvol/progressvol213.png","SevenHD/progressvol/progressvol213_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progressvol/progress213vvol.png","SevenHD/progressvol/progress213vvol_1.png"])
                else:
                   self.skinSearchAndReplace.append(["00fffff3", config.plugins.SevenHD.ProgressVol.value])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressvol/progressvol170.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressvol/progressvol213.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progressvol/progress213vvol.png"',""])
                       
                ### ProgressCS
                if config.plugins.SevenHD.ProgressCS.value == "progresscs":
                   self.skinSearchAndReplace.append(["SevenHD/progresscs/progresscs52.png","SevenHD/progresscs/progresscs52_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progresscs/progresscs362.png","SevenHD/progresscs/progresscs362_1.png"])
                   self.skinSearchAndReplace.append(["SevenHD/progresscs/progresscs426.png","SevenHD/progresscs/progresscs426_1.png"])
                else:
                   self.skinSearchAndReplace.append(["00fffff4", config.plugins.SevenHD.ProgressCS.value])
                   self.skinSearchAndReplace.append(['picServiceEventProgressbar="SevenHD/progresscs/progresscs52.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progresscs/progresscs362.png"',""])
                   self.skinSearchAndReplace.append(['pixmap="SevenHD/progresscs/progresscs426.png"',""])
                       
                ### ProgressListCS
                if config.plugins.SevenHD.ProgressListCS.value == "progresslistcs":
                   self.skinSearchAndReplace.append(["SevenHD/progresslistcs/progresslistcs52.png","SevenHD/progresslistcs/progresslistcs52_1.png"])
                else:
                   self.skinSearchAndReplace.append(["00fffff5", config.plugins.SevenHD.ProgressListCS.value])
                   self.skinSearchAndReplace.append(['picServiceEventProgressbar="SevenHD/progresslistcs/progresslistcs52.png"',""])

		self.skinSearchAndReplace.append(["buttons_seven_white", config.plugins.SevenHD.ButtonStyle.value])
		self.skinSearchAndReplace.append(["icons_seven_white", config.plugins.SevenHD.IconStyle.value])
		
		### Text (running, writing, none)
		if config.plugins.SevenHD.RunningText.value == "writing":
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,startpoint=0,startdelay=2000,steptime=90,wrap=1,always=0,repeat=2,oneshot=1"', 'render="SevenHDEmptyEpg"'])
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,direction=top,startpoint=0,startdelay=2000,steptime=90,wrap=1,always=0,repeat=2,oneshot=1"', 'render="SevenHDEmptyEpg"'])
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,startpoint=0,startdelay=2000,steptime=90,wrap=0,always=0,repeat=2,oneshot=1"', 'render="SevenHDEmptyEpg"'])
		elif config.plugins.SevenHD.RunningText.value == "none":
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,startpoint=0,startdelay=2000,steptime=90,wrap=1,always=0,repeat=2,oneshot=1"', 'render="Label"'])
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,direction=top,startpoint=0,startdelay=2000,steptime=90,wrap=1,always=0,repeat=2,oneshot=1"', 'render="Label"'])
			self.skinSearchAndReplace.append(['render="SevenHDRunningText" options="movetype=running,startpoint=0,startdelay=2000,steptime=90,wrap=0,always=0,repeat=2,oneshot=1"', 'render="Label"'])
		
		self.skinSearchAndReplace.append(["startdelay=2000", config.plugins.SevenHD.Startdelay.value])
			
		if not config.plugins.SevenHD.SelectionBorder.value == "none":
			self.selectionbordercolor = config.plugins.SevenHD.SelectionBorder.value
			self.borset = ("borset_" + self.selectionbordercolor + ".png")
			self.skinSearchAndReplace.append(["borset.png", self.borset])
		
		self.analogstylecolor = config.plugins.SevenHD.AnalogStyle.value
		self.analog = ("analog_" + self.analogstylecolor + ".png")
		self.skinSearchAndReplace.append(["analog.png", self.analog])
		
		self.tuner_Count = self.getTunerCount()
		self.debug("verbaute Tuner: " + str(self.tuner_Count))
		
                if str(self.tuner_Count) == str('1'):
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/b_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/b_off.png"'])
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/c_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/c_off.png"'])
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/d_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/d_off.png"'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerB -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerB -->'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerC -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerC -->'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerD -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerD -->'])
		if str(self.tuner_Count) == str('2'):
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/c_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/c_off.png"'])
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/d_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/d_off.png"'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerC -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerC -->'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerD -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerD -->'])
                if str(self.tuner_Count) == str('3'):
		   self.skinSearchAndReplace.append(['<ePixmap pixmap="SevenHD/buttons/d_off.png"', '<!-- ePixmap pixmap="SevenHD/buttons/d_off.png"'])
		   self.skinSearchAndReplace.append(['size="32,32" zPosition="1" alphatest="blend" /> <!-- TunerD -->', 'size="32,32" zPosition="1" alphatest="blend" / --> <!-- TunerD -->'])
			
                ### Header
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.Header.value + "-begin" + XML)
		if not config.plugins.SevenHD.SelectionBorder.value == "none":
			self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.Header.value + "-middle" + XML)
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.Header.value + "-end" + XML)
                
                ### Volume
                self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.VolumeStyle.value + XML)
		self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.VolumeStyle.value + XML)	
                
                ###ChannelSelection
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.ChannelSelectionStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.ChannelSelectionStyle.value + XML)    
                
                ###Infobar_main
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-main.xml")
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-main.xml")       
                
                ###Channelname
                if config.plugins.SevenHD.InfobarChannelName.value == "none":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarChannelName.value + XML)
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarChannelName.value + XML) 
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICN":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICN.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICN.xml")    
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICNumber":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNumber.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNumber.xml") 
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICNameandNumber":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNameandNumber.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNameandNumber.xml") 
		
                ###ecm-info
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.ECMInfo.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.ECMInfo.value + XML)        
                
                ###clock-style xml
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.ClockStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.ClockStyle.value + XML)               
                
                ###sat-info
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.SatInfo.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.SatInfo.value + XML)        
                
                ###sys-info
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.SysInfo.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.SysInfo.value + XML)        
                
                ###weather-style
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.WeatherStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.WeatherStyle.value + XML)        
                
                ###Infobar_middle
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-middle.xml")
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-middle.xml")         
                
                ###Channelname
                if config.plugins.SevenHD.InfobarChannelName.value == "none":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarChannelName.value + XML)
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarChannelName.value + XML) 
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICN":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICN.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICN.xml")    
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICNumber":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNumber.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNumber.xml") 
                if config.plugins.SevenHD.InfobarChannelName.value == "-ICNameandNumber":
                   self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNameandNumber.xml")
                   self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + "-ICNameandNumber.xml") 
                
                ###clock-style xml
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.ClockStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.ClockStyle.value + XML)       
                
                ###Infobar_end
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + config.plugins.SevenHD.SIB.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.InfobarStyle.value + config.plugins.SevenHD.SIB.value + XML)       
		
                ###Main XML
		self.appendSkinFile(MAIN_DATA_PATH + "main.xml")
                self.debug(MAIN_DATA_PATH + "main.xml")       
                
                ###Plugins XML
		self.appendSkinFile(MAIN_DATA_PATH + "plugins.xml")
                self.debug(MAIN_DATA_PATH + "plugins.xml")        
                
                #EMCSTYLE
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.EMCStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.EMCStyle.value + XML)        
                
                
                #MOVIESELECTIONSTYLE
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.MovieSelectionStyle.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.MovieSelectionStyle.value + XML)        
                
                #NumberZapExtStyle
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.NumberZapExt.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.NumberZapExt.value + XML)       
                
                ###custom-main XML
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.Image.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.Image.value + XML)        
                
                ###cooltv XML
		self.appendSkinFile(MAIN_DATA_PATH + config.plugins.SevenHD.CoolTVGuide.value + XML)
                self.debug(MAIN_DATA_PATH + config.plugins.SevenHD.CoolTVGuide.value + XML)      
                
                ###skin-user
		try:
		   self.appendSkinFile(MAIN_DATA_PATH + "skin-user.xml")
		except:
		   pass
		
                ###skin-end
		self.appendSkinFile(MAIN_DATA_PATH + "skin-end.xml")
                self.debug(MAIN_DATA_PATH + "skin-end.xml")       
                
                self.debug('try open: ' + TMPFILE + "\n")
                xFile = open(TMPFILE, "w")
                for xx in self.skin_lines:
                    xFile.writelines(xx)
                xFile.close()
                self.debug('close: ' + TMPFILE + "\n")
                move(TMPFILE, FILE)
                self.debug('mv : ' + TMPFILE + ' to ' + FILE + "\n")
		
                self.debug('Console\n')	
		
                #DOWNLOADS	
                #buttons
                eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/buttons/*.*; rm -rf /usr/share/enigma2/SevenHD/buttons; wget -q http://www.gigablue-support.org/skins/SevenHD/buttons/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ButtonStyle.value), str(config.plugins.SevenHD.ButtonStyle.value), str(config.plugins.SevenHD.ButtonStyle.value)))
                
                #weather
                eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/WetterIcons/*.*; rm -rf /usr/share/enigma2/SevenHD/WetterIcons; wget -q http://www.gigablue-support.org/skins/SevenHD/weather/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.WeatherStyle.value), str(config.plugins.SevenHD.WeatherStyle.value), str(config.plugins.SevenHD.WeatherStyle.value)))
                #clock
                eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/clock/*.*; rm -rf /usr/share/enigma2/SevenHD/clock; wget -q http://www.gigablue-support.org/skins/SevenHD/clock/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ClockStyle.value), str(config.plugins.SevenHD.ClockStyle.value), str(config.plugins.SevenHD.ClockStyle.value)))
                #volume
                eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/volume/*.*; rm -rf /usr/share/enigma2/SevenHD/volume; wget -q http://www.gigablue-support.org/skins/SevenHD/volume/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.VolumeStyle.value), str(config.plugins.SevenHD.VolumeStyle.value), str(config.plugins.SevenHD.VolumeStyle.value)))
                #progress
                if config.plugins.SevenHD.Progress.value == "progress":
                   eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/progress/*.*; rm -rf /usr/share/enigma2/SevenHD/progress/progress; wget -q http://www.gigablue-support.org/skins/SevenHD/progress/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.Progress.value), str(config.plugins.SevenHD.Progress.value), str(config.plugins.SevenHD.Progress.value)))
                #progressVol
                if config.plugins.SevenHD.ProgressVol.value == "progressvol":
                   eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/progressvol/*.*; rm -rf /usr/share/enigma2/SevenHD/progressvol; wget -q http://www.gigablue-support.org/skins/SevenHD/progress/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ProgressVol.value), str(config.plugins.SevenHD.ProgressVol.value), str(config.plugins.SevenHD.ProgressVol.value)))
                #progressIB
                if config.plugins.SevenHD.ProgressIB.value == "progressib":
                   eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/progressib/*.*; rm -rf /usr/share/enigma2/SevenHD/progressib; wget -q http://www.gigablue-support.org/skins/SevenHD/progress/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ProgressIB.value), str(config.plugins.SevenHD.ProgressIB.value), str(config.plugins.SevenHD.ProgressIB.value)))
                #progressCS
                if config.plugins.SevenHD.ProgressCS.value == "progresscs":
                   eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/progresscs/*.*; rm -rf /usr/share/enigma2/SevenHD/progresscs; wget -q http://www.gigablue-support.org/skins/SevenHD/progress/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ProgressCS.value), str(config.plugins.SevenHD.ProgressCS.value), str(config.plugins.SevenHD.ProgressCS.value)))
                #progressListCS
                if config.plugins.SevenHD.ProgressListCS.value == "progresslistcs":
                   eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/progresslistcs/*.*; rm -rf /usr/share/enigma2/SevenHD/progresslistcs; wget -q http://www.gigablue-support.org/skins/SevenHD/progress/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ProgressListCS.value), str(config.plugins.SevenHD.ProgressListCS.value), str(config.plugins.SevenHD.ProgressListCS.value)))
                #icons
                eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/icons/*.*; rm -rf /usr/share/enigma2/SevenHD/icons; wget -q http://www.gigablue-support.org/skins/SevenHD/icons/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.IconStyle.value), str(config.plugins.SevenHD.IconStyle.value), str(config.plugins.SevenHD.IconStyle.value)))
		
                #background
		eConsole().ePopen("rm -rf /usr/share/enigma2/SevenHD/back/*.*; rm -rf /usr/share/enigma2/SevenHD/back")
                
                if self.Background.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.Background), str(self.Background), str(self.Background)))
                if self.BackgroundRight.startswith('back'):
                   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.BackgroundRight), str(self.BackgroundRight), str(self.BackgroundRight)))
		if self.BackgroundIB1.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.BackgroundIB1), str(self.BackgroundIB1), str(self.BackgroundIB1)))
		if self.BackgroundIB2.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.BackgroundIB2), str(self.BackgroundIB2), str(self.BackgroundIB2)))
		if self.ChannelBack1.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.ChannelBack1), str(self.ChannelBack1), str(self.ChannelBack1)))
		if self.ChannelBack2.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.ChannelBack2), str(self.ChannelBack2), str(self.ChannelBack2)))
		if self.ChannelBack3.startswith('back'):
		   eConsole().ePopen("wget -q http://www.gigablue-support.org/skins/SevenHD/back/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(self.ChannelBack3), str(self.ChannelBack3), str(self.ChannelBack3)))
                
                self.debug('download tgz complett\n')	
        
        except:
           self.debug('error on "def save()"\n')
           self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

        self.reboot("GUI needs a restart to download files and apply a new skin.\nDo you want to Restart the GUI now?")

    def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
        """
        add skin file to main skin content

        appendFileName:
        xml skin-part to add

        skinPartSearchAndReplace:
        (optional) a list of search and replace arrays. first element, search, second for replace
        """
        
        skFile = open(appendFileName, "r")
        file_lines = skFile.readlines()
        skFile.close()

        tmpSearchAndReplace = []

        if skinPartSearchAndReplace is not None:
           tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
        else:
           tmpSearchAndReplace = self.skinSearchAndReplace

        for skinLine in file_lines:
            for item in tmpSearchAndReplace:
                skinLine = skinLine.replace(item[0], item[1])
            self.skin_lines.append(skinLine)
    
    def getTunerCount(self):
        '''
        get tuner count
        :return:
        '''
        tunerCount = nimmanager.getSlotCount()

        tunerCount = max(1, tunerCount)
        tunerCount = min(6, tunerCount)

        return tunerCount
          
    def showInfo(self):
        options = []
        options.extend(((_("Hier koennte ihre Werbung stehen ...."), boundFunction(self.send_to_msg_box, "Ehrlich jetzt?")),))
        if config.plugins.SevenHD.debug.value:
           options.extend(((_("Show Debug Log"), boundFunction(self.show_log)),))
        
        if not fileExists(PLUGIN_PATH + "/Extensions/EnhancedMovieCenter/plugin.pyo"):
           options.extend(((_("Install EnhancedMovieCenter?"), boundFunction(self.Open_Setup, "enigma2-plugin-extensions-enhancedmoviecenter")),))
        
        if config.plugins.SevenHD.NumberZapExtImport.value:
           if fileExists(PLUGIN_PATH + "/SystemPlugins/NumberZapExt/NumberZapExt.pyo"):
              options.extend(((_("Open NumberZapExt Setup"), boundFunction(self.Open_NumberExt)),))
           else:
              options.extend(((_("Install NumberZapExt?"), boundFunction(self.Open_Setup, "enigma2-plugin-systemplugins-extnumberzap")),))
        else:
           options.extend(((_("Install NumberZapExt?"), boundFunction(self.Open_Setup, "enigma2-plugin-systemplugins-extnumberzap")),))
        
        if not fileExists(PLUGIN_PATH + "/Extensions/CoolTVGuide/plugin.pyo"):
           options.extend(((_("Install CoolTVGuide?"), boundFunction(self.Open_Setup, "enigma2-plugin-extensions-cooltvguide")),))
        
        options.extend(((_("Share my Skin"), boundFunction(self.Share_Skin)),))
        options.extend(((_("ChangeLog"), boundFunction(self.ChangeLog)),))
        options.extend(((_("Information"), boundFunction(self.send_to_msg_box, "Thanks to\n\xc3\xb6rlgrey, TBX, stony272 and Philipswalther")),))
        self.session.openWithCallback(self.menuCallback, ChoiceBox,list = options)
            
    def menuCallback(self, ret):
        ret and ret[1]()
    
    def ChangeLog(self):
	os.popen("wget 'http://www.gigablue-support.org/skins/SevenHD/update/SevenHDChangeLog.txt' -O /tmp/SevenHDChangeLog.txt")
        if fileExists("/tmp/SevenHDChangeLog.txt"): 
           self.session.open(Console, _("Show Debug Log"), cmdlist=[("cat /tmp/SevenHDChangeLog.txt")])
	
    def send_to_msg_box(self, my_msg):
        self.session.open(MessageBox,_('%s' % str(my_msg)), MessageBox.TYPE_INFO)
    
    def show_log(self):
        if fileExists("/tmp/kraven_debug.txt"):
           self.session.open(Console, _("Show Debug Log"), cmdlist=[("cat /tmp/kraven_debug.txt")])
    
    def Share_Skin(self):
        answer = []
        answer.extend(((_("Share my Skin Config"), boundFunction(self.Open_Skin_Config, "share")),))
        answer.extend(((_("Load shared Skin Config"), boundFunction(self.Open_Skin_Config, "load")),))
        self.session.openWithCallback(self.menuCallback, ChoiceBox,list = answer)
    
    def Open_Skin_Config(self, what):
        do_skin = ShareSkinSettings()
        if what == 'share':
           answer = do_skin.share()
        else:
           answer = do_skin.load()
        
        self.debug(str(answer) + '\n')
        
        if what == 'share':
           if answer:
              self.session.open(MessageBox,_('Youre Skin Config is ready to share.\nLook in /tmp for youre Skin File.'), MessageBox.TYPE_INFO)
           else:
              self.session.open(MessageBox,_('Anything goes wrong.'), MessageBox.TYPE_INFO)
        else:
           if answer:
              self.save()
              self.session.open(MessageBox,_('New Skin Config is load.'), MessageBox.TYPE_INFO)
           else:
              self.session.open(MessageBox,_('Skin Config is wrong.'), MessageBox.TYPE_INFO)
              
    def Open_Setup(self, what):
        self.reboot("GUI needs a restart after download Plugin.\nDo you want to Restart the GUI now?")
        self.session.open(Console, _("Install Plugin") , cmdlist=[("opkg install %s" % what)])
    
    def Open_NumberExt(self): 
        self.session.open(NumberZapExtSetupScreen, ACTIONLIST)
    
    def reboot(self, message = None):
        self.debug('Reboot\n')
        if message is None:
           message = _("Do you really want to reboot now?")
        
        configfile.save()
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, message, MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Restart GUI"))

    def restartGUI(self, answer):
        if answer is True:
            config.skin.primary_skin.setValue("SevenHD/skin.xml")
            config.skin.save()
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def exit(self):
        self["menuList"].onSelectionChanged.remove(self.__selectionChanged)
        self.close()

    def __selectionChanged(self):
        self.ShowPicture()
        
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[PluginScreen]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
           
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[PluginScreen]' + str(what) + '\n')
           f.close()    
################################################################################        
def main(session, **kwargs):
        if fileExists("/tmp/kraven_debug.txt"):
           remove('/tmp/kraven_debug.txt')
        
        updateInstance = None
        session.open(SevenHD)
        
        if config.plugins.SevenHD.AutoUpdatePluginStart.value or config.plugins.SevenHD.AutoUpdate.value:
           global updateInstance
           if updateInstance is None:
              updateInstance = Update(session)

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [PluginDescriptor(name="SevenHD", description=_("Configuration tool for SevenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
	else:
		return [PluginDescriptor(name="SevenHD", description=_("Configuration tool for SevenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]
