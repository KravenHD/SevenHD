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
                         <widget name="colorthump" position="891,220" size="372,30" zPosition="1" backgroundColor="#00000000" alphatest="blend" />
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
        self.ColorLoad = ePicLoad()
        self["colorthump"] = Pixmap()
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
        list.append(getConfigListEntry(_('_____________________________global system settings________________________________________'), ))
        list.append(getConfigListEntry(_("image"),                     config.plugins.SevenHD.Image,                     'Diese Einstellung spezifiziert dein Image.',                                                         '4',                'IMAGE'))
        list.append(getConfigListEntry(_("skinmode"),                  config.plugins.SevenHD.skin_mode,                 'Hier kannst du die Aufl\xc3\xb6sung zwischen HD, FHD und UHD wechseln.',                             '4',                'SKIN_MODE'))
        if config.plugins.SevenHD.skin_mode.value == '7':
           list.append(getConfigListEntry(_("X Resolution"),           config.plugins.SevenHD.skin_mode_x,               'Stell hier die Breite ein.',                                                                         '4',                'x_resolution'))
           list.append(getConfigListEntry(_("Y Resolution"),           config.plugins.SevenHD.skin_mode_y,               'Stell hier die H\xc3\xb6he ein.',                                                                    '4',                'y_resolution'))
        list.append(getConfigListEntry(_("buttons"),                   config.plugins.SevenHD.ButtonStyle,               'Stellt die Farbe der Icons in der Infobar und Menu ein.',                                            '4',                'Button'))
        list.append(getConfigListEntry(_("plugin icons"),              config.plugins.SevenHD.IconStyle,                 'Stellt die Farbe der [+] und | im PluginBrowser sowie NetzwerkBrowser ein.',                         '4',                'Icons'))
        list.append(getConfigListEntry(_("volume style"),              config.plugins.SevenHD.VolumeStyle,               '\xc3\x84ndert die Darstellung der Lautst\xc3\xa4rkeanzeige.',                                        '1',                ''))
        list.append(getConfigListEntry(_("volumebar"),                 config.plugins.SevenHD.ProgressVol,               'Stellt die Farbe der Lautst\xc3\xa4rkeanzeige ein.',                                                 '4',                'progressvol'))
        list.append(getConfigListEntry(_('_____________________________________font__________________________________________________'), ))
        if config.plugins.SevenHD.systemfonts.value:
           list.append(getConfigListEntry(_("use systemfonts"),        config.plugins.SevenHD.systemfonts,               'Wenn JA, dann kannst du alle SystemFonts beim n\xc3\xa4chsten PluginStart nutzen.',                  '4',                'True'))
        else:
           list.append(getConfigListEntry(_("use systemfonts"),        config.plugins.SevenHD.systemfonts,               'Wenn JA, dann kannst du alle Systemschriften beim n\xc3\xa4chsten Pluginstart nutzen.',              '4',                'none'))
        list.append(getConfigListEntry(_("primary font style"),        config.plugins.SevenHD.FontStyle_1,               'W\xc3\xa4hle hier die prim\xc3\xa4re Schrift aus.',                                                  '4',                'fontpreview'))
        list.append(getConfigListEntry(_("primary font height in %"),  config.plugins.SevenHD.FontStyleHeight_1,         'Stellt die Gr\xc3\xb6\xc3\x9fe der prim\xc3\xa4ren Schrift ein.',                                    '4',                'fontheight'))
        list.append(getConfigListEntry(_("secondary font style"),      config.plugins.SevenHD.FontStyle_2,               'W\xc3\xa4hle hier die sekund\xc3\xa4re Schrift aus.',                                                '4',                'fontpreview'))
        list.append(getConfigListEntry(_("secondary font height in %"),config.plugins.SevenHD.FontStyleHeight_2,         'Stellt die Gr\xc3\xb6\xc3\x9fe der sekund\xc3\xa4ren Schrift ein.',                                  '4',                'fontheight'))
        list.append(getConfigListEntry(_('__________________________________running text____________________________________________'), ))
        list.append(getConfigListEntry(_("activate"),                  config.plugins.SevenHD.RunningText,               'L\xc3\xa4sst die Schrift scrollen oder schreiben.',                                                  '1',                'RunningText'))
        if config.plugins.SevenHD.RunningText.value == 'running':
           list.append(getConfigListEntry(_("startdelay"),             config.plugins.SevenHD.Startdelay,                'Stellt die Startzeit ein, nach wieviel Sek. der Text anfangen soll sich zu bewegen.',                '4',                'Delay'))
           list.append(getConfigListEntry(_("steptime"),               config.plugins.SevenHD.Steptime,                  'Stellt die Laufgeschwindigkeit ein. Je h\xc3\xb6her der Wert, desto langsamer die Geschwindigkeit', '4',                'Delay'))
        list.append(getConfigListEntry(_('__________________________________transparency_____________________________________________'), ))
        list.append(getConfigListEntry(_("main window"),               config.plugins.SevenHD.BackgroundColorTrans,      'Stellt die Transparenz des linken Fenster ein.',                                                     '4',                'transparency'))
        list.append(getConfigListEntry(_("right window"),              config.plugins.SevenHD.BackgroundRightColorTrans, 'Stellt die Transparenz des rechten Fenster ein.',                                                    '4',                'transparency'))
        
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
        if returnValue == config.plugins.SevenHD.ProgressVol:
              preview = self.generate(config.plugins.SevenHD.ProgressVol.value)
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
        
        elif 'progress' in color:
           return str(MAIN_IMAGE_PATH) + "progress.png"
        elif 'carbon' in color:
           return str(MAIN_IMAGE_PATH) + "carbon.png"
        elif 'lightwood' in color:
           return str(MAIN_IMAGE_PATH) + "lightwood.png"
        elif 'redwood' in color:
           return str(MAIN_IMAGE_PATH) + "redwood.png"
        elif 'slate' in color:
           return str(MAIN_IMAGE_PATH) + "slate.png"
        elif 'brownleather' in color:
           return str(MAIN_IMAGE_PATH) + "brownleather.png"


    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.preview_font()
        self.ShowPicture()
        self.ShowColor()
        
    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.preview_font()
        self.ShowPicture()
        self.ShowColor()
        
    def preview_font(self):
        returnValue = self["config"].getCurrent()[1].value
        try:
           path = None
           if '?systemfont' in returnValue:
              path = MAIN_SKIN_PATH + 'fonts/' + returnValue.split('?')[0]
           elif returnValue == 'noto':
              path = MAIN_SKIN_PATH + 'fonts/NotoSans-Regular.ttf'
           elif returnValue == 'handel':
              path = MAIN_SKIN_PATH + 'fonts/HandelGotD.ttf'
           elif returnValue == 'campton':
              path = MAIN_SKIN_PATH + 'fonts/Campton Medium.otf'
           elif returnValue == 'proxima':
              path = MAIN_SKIN_PATH + 'fonts/Proxima Nova Regular.otf'
           elif returnValue == 'opensans':
              path = MAIN_SKIN_PATH + 'fonts/OpenSans-Regular.ttf'
           
           if path:            
              img = Image.open(MAIN_IMAGE_PATH + str("fontpreview_in.jpg"))
              draw = ImageDraw.Draw(img)
              try:
                 font = ImageFont.truetype(path, 30)
                 draw.text((30, 85),"Sample Text",255,font=font)
              except:
                 draw.text((30, 85),"No Preview for youre Box Update PIL Package!",255)
                 self.debug('No Preview for youre Box Update PIL Package!')
              finally:
                 img.save(MAIN_IMAGE_PATH + str("fontpreview.jpg"))
              
        except TypeError:
           pass

    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.preview_font()
        self.ShowPicture()
        self.ShowColor()
        
    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.preview_font()
        self.ShowPicture()
        self.ShowColor()
        
    def grab_png(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
                                               
    def defaults(self):
        self.setInputToDefault(config.plugins.SevenHD.skin_mode)
        self.setInputToDefault(config.plugins.SevenHD.skin_mode_x)
        self.setInputToDefault(config.plugins.SevenHD.skin_mode_y)
        self.setInputToDefault(config.plugins.SevenHD.FontStyle_1)
        self.setInputToDefault(config.plugins.SevenHD.FontStyleHeight_1)
        self.setInputToDefault(config.plugins.SevenHD.FontStyle_2)
        self.setInputToDefault(config.plugins.SevenHD.FontStyleHeight_2)
        self.setInputToDefault(config.plugins.SevenHD.Image)
        self.setInputToDefault(config.plugins.SevenHD.ButtonStyle)
        self.setInputToDefault(config.plugins.SevenHD.IconStyle)
        self.setInputToDefault(config.plugins.SevenHD.RunningText)
        self.setInputToDefault(config.plugins.SevenHD.Startdelay)
        self.setInputToDefault(config.plugins.SevenHD.Steptime)
        self.setInputToDefault(config.plugins.SevenHD.Volume)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundRightColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.ProgressVol)
        self.setInputToDefault(config.plugins.SevenHD.SelectionBackground)
        self.setInputToDefault(config.plugins.SevenHD.SelectionBorder)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def save(self):
        
        if config.plugins.SevenHD.systemfonts.value == True:
           if not fileExists("/etc/enigma2/SystemFont"):
              self.session.open(MessageBox, _('Please look in "Extra" and do "Import SystemFonts"'), MessageBox.TYPE_INFO)
        else:
           if fileExists("/etc/enigma2/SystemFont"):
              remove("/etc/enigma2/SystemFont")
        
        if CREATOR != 'OpenMips':
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
