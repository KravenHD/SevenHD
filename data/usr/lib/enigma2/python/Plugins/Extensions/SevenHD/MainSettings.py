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
class MainSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <eLabel position="70,12" size="708,46" text="SevenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <eLabel position="891,657" size="372,46" text="Thanks to http://www.gigablue-support.org/" font="Regular; 12" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
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
                         <eLabel position="891,88" size="372,46" text="Version: """ + str(version) + """" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget source="session.CurrentService" render="Label" position="891,134" size="372,28" font="Regular;26" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                         </widget>
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
        self.creator = 'openATV'
        try:
           image = os.popen('cat /etc/image-version').read()
           if 'creator=OpenMips' in image: 
              self.creator = 'OpenMips'
        except:
           try:
              image = os.popen('cat /etc/motd').read()
              if 'HDMU' in image: 
                 self.creator = 'OpenMips'
           except:
              self.creator = 'unknow'
        self.debug('Image-Type: ' + str(self.creator) + '\n')
        
        self.onLayoutFinish.append(self.UpdatePicture)

    def getMenuItemList(self):
        list = [] 
        list.append(getConfigListEntry(_('_______________________________________ global system settings _______________________________________'), ))
        list.append(getConfigListEntry(_("image"), config.plugins.SevenHD.Image, 'IMAGE'))
        list.append(getConfigListEntry(_("skinmode"), config.plugins.SevenHD.skin_mode, 'SKIN_MODE'))
        if config.plugins.SevenHD.skin_mode.value == '7':
           list.append(getConfigListEntry(_("X Resolution"), config.plugins.SevenHD.skin_mode_x, 'x_resolution'))
           list.append(getConfigListEntry(_("Y Resolution"), config.plugins.SevenHD.skin_mode_y, 'y_resolution'))
        list.append(getConfigListEntry(_("buttons"), config.plugins.SevenHD.ButtonStyle, 'Button'))
        list.append(getConfigListEntry(_("plugin icons"), config.plugins.SevenHD.IconStyle, 'Icons'))
        list.append(getConfigListEntry(_("volume style"), config.plugins.SevenHD.VolumeStyle))
        list.append(getConfigListEntry(_("volumebar"), config.plugins.SevenHD.ProgressVol, 'progressvol'))
        list.append(getConfigListEntry(_('_____________________________________________running text ____________________________________________'), ))
        list.append(getConfigListEntry(_("activate"), config.plugins.SevenHD.RunningText, 'RunningText'))
        if config.plugins.SevenHD.RunningText.value == 'running':
           list.append(getConfigListEntry(_("startdelay"), config.plugins.SevenHD.Startdelay, 'Delay'))
           list.append(getConfigListEntry(_("steptime"), config.plugins.SevenHD.Steptime, 'Delay'))
        list.append(getConfigListEntry(_('_____________________________________________transparency ____________________________________________'), ))
        list.append(getConfigListEntry(_("main window"), config.plugins.SevenHD.BackgroundColorTrans))
        list.append(getConfigListEntry(_("right window"), config.plugins.SevenHD.BackgroundRightColorTrans))
        list.append(getConfigListEntry(_('_____________________________________________ autoupdate _____________________________________________'), ))
        list.append(getConfigListEntry(_("activate"), config.plugins.SevenHD.AutoUpdate))
        list.append(getConfigListEntry(_("autoupdate infobar info"), config.plugins.SevenHD.AutoUpdateInfo))
        list.append(getConfigListEntry(_("autoupdate plugin startinfo"), config.plugins.SevenHD.AutoUpdatePluginStart))
        list.append(getConfigListEntry(_('______________________________________________ plugins _______________________________________________'), ))
        list.append(getConfigListEntry(_("Movie Selection"), config.plugins.SevenHD.MovieSelectionStyle))
        if not fileExists(PLUGIN_PATH + "/Extensions/EnhancedMovieCenter/plugin.pyo"):
           list.append(getConfigListEntry(_('{:<114}{:>1}'.format('EnhancedMovieCenter','not installed')), ))
        else:   
           list.append(getConfigListEntry(_("EMC"), config.plugins.SevenHD.EMCStyle))
           config.EMC.skin_able.value = True
           config.EMC.skin_able.save()
        if config.plugins.SevenHD.NumberZapExtImport.value:
           if fileExists(PLUGIN_PATH + "/SystemPlugins/NumberZapExt/NumberZapExt.pyo"):
              list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.SevenHD.NumberZapExt))
           else:
              list.append(getConfigListEntry(_('{:<121}{:>1}'.format('ExtNumberZap','not installed')), ))                   
        else:
           list.append(getConfigListEntry(_('{:<121}{:>1}'.format('ExtNumberZap','not installed')), ))
           
        if not fileExists(PLUGIN_PATH + "/Extensions/CoolTVGuide/plugin.pyo"):
           list.append(getConfigListEntry(_('{:<124}{:>1}'.format('CoolTVGuide','not installed')), ))
        else:
           list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.SevenHD.CoolTVGuide))
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        try:
           returnValue = self["config"].getCurrent()[1].value
	   self.debug('\nRet_value[1]: ' + str(returnValue) + '\n')		
           		
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
           ## update
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
           
           if returnValue == 'activate' or returnValue == 'Aktivieren' and config.plugins.SevenHD.AutoUpdate.value == False:
              return MAIN_IMAGE_PATH + str("none.jpg")
           if returnValue == 'activate' or returnValue == 'Aktivieren' and config.plugins.SevenHD.AutoUpdate.value == True:
              return MAIN_IMAGE_PATH + str("True.jpg")
           if returnValue == 'autoupdate infobar info' or returnValue == 'Updateinformationen in Infobar' and config.plugins.SevenHD.AutoUpdateInfo.value == False:
              return MAIN_IMAGE_PATH + str("none.jpg")
           if returnValue == 'autoupdate infobar info' or returnValue == 'Updateinformationen in Infobar' and config.plugins.SevenHD.AutoUpdateInfo.value == True:
              return MAIN_IMAGE_PATH + str("True.jpg") 
           if returnValue == 'autoupdate plugin startinfo' or returnValue == 'Updateinformationen beim Pluginstart' and config.plugins.SevenHD.AutoUpdatePluginStart.value == False:
              return MAIN_IMAGE_PATH + str("none.jpg")
           if returnValue == 'autoupdate plugin startinfo' or returnValue == 'Updateinformationen beim Pluginstart' and config.plugins.SevenHD.AutoUpdatePluginStart.value == True:
              return MAIN_IMAGE_PATH + str("True.jpg")
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
        self.setInputToDefault(config.plugins.SevenHD.skin_mode)
        self.setInputToDefault(config.plugins.SevenHD.skin_mode_x)
        self.setInputToDefault(config.plugins.SevenHD.skin_mode_y)
        self.setInputToDefault(config.plugins.SevenHD.AutoUpdate)
        self.setInputToDefault(config.plugins.SevenHD.AutoUpdateInfo)
        self.setInputToDefault(config.plugins.SevenHD.AutoUpdatePluginStart)
        self.setInputToDefault(config.plugins.SevenHD.Image)
        self.setInputToDefault(config.plugins.SevenHD.ButtonStyle)
        self.setInputToDefault(config.plugins.SevenHD.IconStyle)
        self.setInputToDefault(config.plugins.SevenHD.RunningText)
        self.setInputToDefault(config.plugins.SevenHD.Startdelay)
        self.setInputToDefault(config.plugins.SevenHD.Steptime)
        self.setInputToDefault(config.plugins.SevenHD.Volume)
        self.setInputToDefault(config.plugins.SevenHD.NumberZapExt)
        self.setInputToDefault(config.plugins.SevenHD.EMCStyle)
        self.setInputToDefault(config.plugins.SevenHD.MovieSelectionStyle)
        self.setInputToDefault(config.plugins.SevenHD.CoolTVGuide)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundRightColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.ProgressVol)
        self.setInputToDefault(config.plugins.SevenHD.SelectionBackground)
        self.setInputToDefault(config.plugins.SevenHD.SelectionBorder)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def showInfo(self):
        self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

    def save(self):
        
        if self.creator != 'OpenMips':
           if config.plugins.SevenHD.skin_mode.value >= '2':
              config.epgselection.multi_itemsperpage.value = '10'
           else:
              self.setInputToDefault(config.epgselection.multi_itemsperpage)
           config.epgselection.multi_itemsperpage.save()
        
        if config.plugins.SevenHD.skin_mode.value >= '3':
           if config.plugins.SevenHD.skin_mode.value == '3': 
              msg_text = '3840x2160 for UHD'
           if config.plugins.SevenHD.skin_mode.value == '4':
              msg_text = '4096x2160 for 4k'
           if config.plugins.SevenHD.skin_mode.value == '5':
              msg_text = '7680x4320 for FUHD'
           if config.plugins.SevenHD.skin_mode.value == '6':
              msg_text = '8192x4320 for 8k'     
           if config.plugins.SevenHD.skin_mode.value == '7':
              msg_text = '%sx%s' % (str(int(config.plugins.SevenHD.skin_mode_x.value)), str(int(config.plugins.SevenHD.skin_mode_y.value)))
           
           self.session.open(MessageBox, _('Make sure that your Box support\nyour Resolution %s!!\n' % str(msg_text)), MessageBox.TYPE_INFO)   
        
        if fileExists(PLUGIN_PATH + "/Extensions/EnhancedMovieCenter/plugin.pyo"):
           if config.plugins.SevenHD.EMCStyle.value != 'emcnocover':
              config.EMC.movie_cover.value = True         
           else:
              config.EMC.movie_cover.value = False
           config.EMC.movie_cover.save()
        
        if self.creator != 'OpenMips':
           if config.plugins.SevenHD.MovieSelectionStyle.value == 'movieselectionbigcover':
              config.movielist.itemsperpage.value = '10'
           else:
              self.setInputToDefault(config.movielist.itemsperpage)
           config.movielist.itemsperpage.save()
              
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
              self.session.open(MessageBox, _('[MainSettingsScreen]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[MainSettingsScreen]' + str(what) + '\n')
           f.close() 
