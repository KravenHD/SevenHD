# -*- coding: UTF-8 -*-
#######################################################################
#
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#    SevenHD by Kraven
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
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
#######################################################################
class ChannelSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" transparent="1" zPosition="1" backgroundColor="#00000000" />
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
                  </screen>
               """

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self["helperimage"] = Pixmap()
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
        list.append(getConfigListEntry(_('__________________________________________ channelselection __________________________________________'), ))
        list.append(getConfigListEntry(_("style"), config.plugins.SevenHD.ChannelSelectionStyle))
        ChannelSelectionStyle = config.plugins.SevenHD.ChannelSelectionStyle.value
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"), config.plugins.SevenHD.PrimeTimeTime, 'primetimetime'))
        list.append(getConfigListEntry(_('_____________________________________________ background _____________________________________________'), ))
        list.append(getConfigListEntry(_("color left"), config.plugins.SevenHD.ChannelBack1, 'colorleftcs'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("color middle"), config.plugins.SevenHD.ChannelBack3, 'colormiddlecs'))
        list.append(getConfigListEntry(_("color right"), config.plugins.SevenHD.ChannelBack2 ,'colorrightcs'))
        list.append(getConfigListEntry(_('_____________________________________________ color lines ____________________________________________'), ))
        list.append(getConfigListEntry(_("line"), config.plugins.SevenHD.ChannelLine, 'linecs'))
        list.append(getConfigListEntry(_("border"), config.plugins.SevenHD.ChannelBorder, 'bordercs'))
        list.append(getConfigListEntry(_('__________________________________________ color description _________________________________________'), ))
        list.append(getConfigListEntry(_("bouquet name"), config.plugins.SevenHD.ChannelColorBouquet, 'bouquetname'))
        list.append(getConfigListEntry(_("program name"), config.plugins.SevenHD.ChannelColorProgram, 'programname'))
        list.append(getConfigListEntry(_("next events"), config.plugins.SevenHD.ChannelColorNext, 'nextevents'))
        list.append(getConfigListEntry(_("runtime"), config.plugins.SevenHD.ChannelColorRuntime, 'runtime'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           list.append(getConfigListEntry(_("channel name"), config.plugins.SevenHD.ChannelColorChannel, 'channelnamecs'))
        if not ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("time"), config.plugins.SevenHD.ChannelColorTimeCS, 'time'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns') or ChannelSelectionStyle.endswith('2') or ChannelSelectionStyle.endswith('3'):
           pass
        else:
           list.append(getConfigListEntry(_("prime time"), config.plugins.SevenHD.ChannelColorPrimeTime, 'primetime'))
        list.append(getConfigListEntry(_("program description now"), config.plugins.SevenHD.ChannelColorDesciption, 'descriptionnow'))
        if ChannelSelectionStyle.startswith('channelselection-threecolumns'):
           list.append(getConfigListEntry(_("program description next"), config.plugins.SevenHD.ChannelColorDesciptionNext, 'descriptionnext'))
        list.append(getConfigListEntry(_("buttons"), config.plugins.SevenHD.ChannelColorButton, 'textbuttons'))
        list.append(getConfigListEntry(_('______________________________________________ color list ____________________________________________'), ))
        list.append(getConfigListEntry(_("channel name and number"), config.plugins.SevenHD.ChannelColorChannelName, 'channelnamelist'))
        list.append(getConfigListEntry(_("program"), config.plugins.SevenHD.ChannelColorEvent, 'programlist'))
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        try:
           returnValue = self["config"].getCurrent()[1].value
	   #self.debug('\nRet_value[1]: ' + str(returnValue) + '\n')		
           self.debug('\nvalue[1]: ' + str(int(config.plugins.SevenHD.PrimeTimeTime.value[0])) + '-' + str(int(config.plugins.SevenHD.PrimeTimeTime.value[1])) + '\n')
           if returnValue.endswith('-top'):
              path = MAIN_IMAGE_PATH + str("SIB1.jpg")
           elif returnValue.endswith('-left'):
              path = MAIN_IMAGE_PATH + str("SIB2.jpg")
           elif returnValue.endswith('-full'):
              path = MAIN_IMAGE_PATH + str("SIB3.jpg")
           elif returnValue.endswith('-minitv'):
              path = MAIN_IMAGE_PATH + str("SIB4.jpg")
           else:
              path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
	   		
           if fileExists(path):
              return path
           else:
           ## colors
              try:
                 returnValue = self["config"].getCurrent()[2]
                 path = MAIN_IMAGE_PATH + returnValue + str(".jpg")
                 if fileExists(path):
                    return path
                 
                 self.debug('1: Missing Picture: ' + str(path) + '\n')
              except:
                 self.debug('2: Missing Picture: ' + str(path) + '\n')

        except:
           returnValue = self["config"].getCurrent()[0]
           self.debug('3: Missing Picture: ' + MAIN_IMAGE_PATH + str(returnValue) + '.jpg\n')
           ## weather
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
        self.setInputToDefault(config.plugins.SevenHD.ChannelSelectionStyle)
        self.setInputToDefault(config.plugins.SevenHD.PrimeTimeTime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack1)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack2)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBack3)
        self.setInputToDefault(config.plugins.SevenHD.ChannelLine)
        self.setInputToDefault(config.plugins.SevenHD.ChannelBorder)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorButton)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorBouquet)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannel)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorNext)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorDesciptionNext)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorRuntime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorProgram)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorTimeCS)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorPrimeTime)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorDesciption)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannelName)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorChannelNumber)
        self.setInputToDefault(config.plugins.SevenHD.ChannelColorEvent)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def showInfo(self):
        self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

    def save(self):
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
              self.session.open(MessageBox, _('[ChannelSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[ChannelSettings]' + str(what) + '\n')
           f.close() 