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
class PluginSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Defaults" transparent="1" />
                         <widget name="blue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <eLabel position="70,12" size="708,46" text="Plugin Settings" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
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
        list.append(getConfigListEntry(_('_______________________________plugins__________________________________________'), ))                                           
        list.append(getConfigListEntry(_("Event View"),          config.plugins.SevenHD.EventView,              'Auswahl der Darstellung von Event View.',                    '1',     ''))
        list.append(getConfigListEntry(_("Movie Selection"),     config.plugins.SevenHD.MovieSelectionStyle,    'Auswahl der Covergr\xc3\xb6\xc3\x9fe.',                      '1',     ''))
        if not fileExists(PLUGIN_PATH + "/Extensions/EnhancedMovieCenter/plugin.pyo"):
           list.append(getConfigListEntry(_('{:<114}{:>1}'.format('EnhancedMovieCenter','not installed')), ))
        else:   
           list.append(getConfigListEntry(_("EMC"),              config.plugins.SevenHD.EMCStyle,               'Auswahl der Covergr\xc3\xb6\xc3\x9fe.',                      '1',     ''))
           config.EMC.skin_able.value = True
           config.EMC.skin_able.save()
        if os.path.isdir(PLUGIN_PATH + "Extensions/Albatros") :
           if config.plugins.SevenHD.use_alba_skin.value:
              list.append(getConfigListEntry(_("Use Albatros Skin"),   config.plugins.SevenHD.use_alba_skin,    'Wenn ja wird das SevenHD Skin für Albatros installiert.',    '1',     ''))
           else:
              list.append(getConfigListEntry(_("Use Albatros Skin"),   config.plugins.SevenHD.use_alba_skin,    'Wenn ja wird das SevenHD Skin für Albatros installiert.',    '4',     'none'))
        else:
           list.append(getConfigListEntry(_('{:<121}{:>1}'.format('Albatros','not installed')), )) 
        if os.path.isdir(PLUGIN_PATH + "Extensions/MediaPortal") :
           if config.plugins.SevenHD.use_mp_skin.value:
              list.append(getConfigListEntry(_("Use MediaPortal Skin"),config.plugins.SevenHD.use_mp_skin,      'Wenn ja wird das SevenHD Skin für MediaPortal installiert.', '1',     ''))
           else:
              list.append(getConfigListEntry(_("Use MediaPortal Skin"),config.plugins.SevenHD.use_mp_skin,      'Wenn ja wird das SevenHD Skin für MediaPortal installiert.', '4',     'none'))
        else:
           list.append(getConfigListEntry(_('{:<121}{:>1}'.format('MediaPortal','not installed')), )) 
        if config.plugins.SevenHD.NumberZapExtImport.value:
           if fileExists(PLUGIN_PATH + "/SystemPlugins/NumberZapExt/NumberZapExt.pyo"):
              list.append(getConfigListEntry(_("ExtNumberZap"),  config.plugins.SevenHD.NumberZapExt,           'Auswahl der Darstellung beim Senderwechsel per Nummertaste.','1',     ''))
           else:
              list.append(getConfigListEntry(_('{:<121}{:>1}'.format('ExtNumberZap','not installed')), ))                   
        else:
           list.append(getConfigListEntry(_('{:<121}{:>1}'.format('ExtNumberZap','not installed')), ))
           
        if not fileExists(PLUGIN_PATH + "/Extensions/CoolTVGuide/plugin.pyo"):
           list.append(getConfigListEntry(_('{:<124}{:>1}'.format('CoolTVGuide','not installed')), ))
        else:
           list.append(getConfigListEntry(_("CoolTVGuide"),      config.plugins.SevenHD.CoolTVGuide,            'Auswahl der Darstellung von CoolTVGuide.',                   '1',     ''))
        if not fileExists(PLUGIN_PATH + "/Extensions/WeatherPlugin/plugin.pyo"):
           list.append(getConfigListEntry(_('{:<124}{:>1}'.format('MSN Weather','not installed')), ))
        else:
           list.append(getConfigListEntry(_("MSN Weather"),      config.plugins.SevenHD.MSNWeather,             'Auswahl der Darstellung von MSN Weather Plugin.',            '1',     ''))
        return list

    def __selectionChanged(self):
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
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self["description"].setText(self["config"].getCurrent()[4])
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
        self.setInputToDefault(config.plugins.SevenHD.NumberZapExt)
        self.setInputToDefault(config.plugins.SevenHD.EMCStyle)
        self.setInputToDefault(config.plugins.SevenHD.MovieSelectionStyle)
        self.setInputToDefault(config.plugins.SevenHD.EventView)
        self.setInputToDefault(config.plugins.SevenHD.CoolTVGuide)
        self.setInputToDefault(config.plugins.SevenHD.use_alba_skin)
        self.setInputToDefault(config.plugins.SevenHD.use_mp_skin)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def showInfo(self):
        self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

    def save(self):
        
        if fileExists(PLUGIN_PATH + "/Extensions/EnhancedMovieCenter/plugin.pyo"):
           if config.plugins.SevenHD.EMCStyle.value != 'emcnocover':
              config.EMC.movie_cover.value = True         
           else:
              config.EMC.movie_cover.value = False
           config.EMC.movie_cover.save()
        
        if CREATOR != 'OpenMips':
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
              self.session.open(MessageBox, _('[PluginSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[PluginSettings]' + str(what) + '\n')
           f.close() 