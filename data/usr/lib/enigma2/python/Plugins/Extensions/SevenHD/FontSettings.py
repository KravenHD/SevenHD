# -*- coding: utf-8 -*-
#######################################################################
#
# FontHeightManager by .:TBX:.
#   for KravenSkin (c) 2016
#
#######################################################################
from GlobalImport import *
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
class FontSettings(Screen):
    skin =  """
                  <screen name="SevenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <eLabel font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text=" - " transparent="1" />
                         <eLabel font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" text=" + " transparent="1" />
                         <widget name="menuList" position="18,72" size="816,575" font="Regular; 19" itemHeight="30" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,278" size="372,200" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <eLabel position="70,12" size="708,46" text="Font Settings" font="Regular2; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
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
                         <widget source="session.CurrentService" render="Label" position="891,88" size="372,46" font="Regular2;35" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="SevenHDUpdate">Version</convert>
                         </widget>
                         <widget source="session.CurrentService" render="Label" position="891,134" size="372,28" font="Regular;26" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                         </widget>
                  </screen>
               """
                  
    def __init__(self, session, args = None):
        self.session = session
        
        Screen.__init__(self, session)
        
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self["helperimage"] = Pixmap()
        self["description"] = Label()
        
        self.has_change = False
        
        try:
           with open(FILE, 'r') as oldFile:
              old_skin = oldFile.readlines()
           for old_res in old_skin:
               if 'resolution bpp="32" xres="' in old_res:
                  old_skin_resolution = re.search('resolution bpp="32" xres="(.+?)" yres="(.+?)"', str(old_res)).groups(1)
                  break
           old_resolution = old_skin_resolution[0]
        except:
           old_resolution = '1280'
                
        if str(old_resolution) == str('1280'):
           self.value = float(1)
        elif str(old_resolution) == str('1920'):
           self.value = float(1.5)
        elif str(old_resolution) == str('3840'):
           self.value = float(3)
        elif str(old_resolution) == str('4096'):
           self.value = float(3)
        elif str(old_resolution) == str('7680'):
           self.value = float(4.5)
        elif str(old_resolution) == str('8192'):
           self.value = float(4.5)
        else:
           self.value = float(1)
                
        self["actions"] = ActionMap(
            [
                "OkCancelActions",
                "DirectionActions",
                "InputActions",
                "ColorActions"
            ],
            {
                "cancel": self.exit,
                "red": self.exit,
                "green": self.keyGreen,
                "yellow": self.keyYellow,
                "blue": self.keyBlue
                
            }, -1)	
           
        self["menuList"] = MenuList([])
        self.list_init()
        
        if not self.__selectionChanged in self["menuList"].onSelectionChanged:
            self["menuList"].onSelectionChanged.append(self.__selectionChanged)

        self.onChangedEntry = []
        self.onLayoutFinish.append(self.__selectionChanged)

    def __del__(self):
        self["menuList"].onSelectionChanged.remove(self.__selectionChanged)
        
    def list_init(self):
        list = []
        
        tree = etree.parse(FILE)
        root = tree.getroot()
        
        for screen in root.findall('screen'):   
            screenname = screen.attrib['name']
            if not screenname.startswith('template'):
               for child in screen:
                   try:
                     font = child.get('font')
                     if ';' in font:
                        # really tricky
                        # child dont except the "except"
                        try:
                           name = child.get('source')
                        except:
                           name = None
                        if name == None:   
                           try:
                             name = child.get('name')
                           except:
                             name = None
                        
                           if name == None:
                              try:
                                 name = child.get('text')
                              except:
                                 name = None
                        try:
                            for sub in child:
                                name = sub.text
                                break
                        except:
                            name = name
                            
                        if name != None:
                           fontheight = font.split(';')
                           
                           if len(screenname) >= 15:
                              self.screen_tab = '\t'
                           else:
                              self.screen_tab = '\t\t'
                           if len(name) >= 15:
                              self.name_tab = '\t'
                           else:
                              self.name_tab = '\t\t'
                           
                           list.append((_(str(screenname) + self.screen_tab + str(name) + self.name_tab + str(fontheight[1])), str(screenname), str(name), str(fontheight[1]), str(font)))
                   
                   except:
                      pass
        
        list.sort()
        self.debug(len(list))
        self["menuList"].setList(list)

    def keyBlue(self):
        self.curFH = int(self.curFH) + 1
        self.new_height = self.curFH
        self["description"].setText('Aktuelle Gr\xc3\xb6\xc3\x9fe: ' + str(self.new_height) + '\nzum anwenden Speichern')       
    
    def keyYellow(self):
        self.curFH = int(self.curFH) - 1
        self.new_height = self.curFH
        self["description"].setText('Aktuelle Gr\xc3\xb6\xc3\x9fe: ' + str(self.new_height) + '\nzum anwenden Speichern')
    
    def keyGreen(self):
        if fileExists(FILE):
           copy(FILE, TMPFILE)
           self.debug('cp : ' + FILE + ' to ' + TMPFILE + "\n")
        
        cur = self["menuList"].getCurrent()
        curSN = self["menuList"].getCurrent()[1]
        curCN = self["menuList"].getCurrent()[2]
        
        list_entrie = str(cur)
        self.hd_height = round(float(self.new_height) / float(self.value))
        
        if fileExists(USER_FONT_FILE):
           fh, tmp_file_path = mkstemp()
           search_string = "'" + curSN + "', '" + curCN + "',"
           with open(tmp_file_path, 'w') as tmp_file:
                with open(USER_FONT_FILE, 'r') as user_file:
                     for line in user_file:
                         if not search_string in line:
                         #   pass
                         #else:
                            tmp_file.write(line)
        
           remove(USER_FONT_FILE)
           move(tmp_file_path, USER_FONT_FILE)
        
        f = open(USER_FONT_FILE, 'a+')
        f.write(str(list_entrie.replace(")", ", '%s')" % int(self.hd_height))) + '\n')
        f.close()
        
        os.system('python /usr/lib/enigma2/python/Plugins/Extensions/SevenHD/ChangeFont.py %s' % str(self.value))
        
        self.has_change = True
        self.list_init()
        
    def exit(self):
        if self.has_change:
           self.session.open(MessageBox, _("Deine skin.xml wurde ge\xc3\xa4ndert.\nBitte einen GUI Neustart machen."), MessageBox.TYPE_INFO, timeout=5)
        
        self["menuList"].onSelectionChanged.remove(self.__selectionChanged)
        self.close()

    def __selectionChanged(self):
        self["description"].setText('Zum \xc3\xa4ndern GELB/BLAU dr\xc3\xbccken')
        curFH = self["menuList"].getCurrent()[3]
        self.curFH = self["menuList"].getCurrent()[3]
        self.new_height = int(curFH)
        
    def debug(self, what, error=None):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[FontSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
           
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           if error != None:
              f.write('[FontSettings]' + str(what) + ' error: ' + str(error) + '\n')
           else:
              f.write('[FontSettings]' + str(what) + '\n')
           f.close()