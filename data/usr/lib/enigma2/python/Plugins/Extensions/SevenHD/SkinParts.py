# -*- coding: utf-8 -*-
#######################################################################
#
# SkinPartManager by .:TBX:.
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
class SkinParts(Screen):
    skin =  """
                  <screen name="SkinParts" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <widget name="buttonRed" font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" transparent="1" />
                         <widget name="buttonGreen" font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" transparent="1" />
                         <widget name="buttonYellow" font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" transparent="1" />
                         <widget name="buttonBlue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="menuList" position="18,72" size="816,575" font="Regular; 19" itemHeight="30" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,278" size="372,200" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget name="titel" position="70,12" size="708,46" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
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
        self["buttonRed"] = Label()
        self["buttonGreen"] = Label()
        self["buttonYellow"] = Label()
        self["buttonBlue"] = Label()
        self["titel"] = Label()
        self["buttonRed"].setText(_("Cancel"))
        self["buttonGreen"].setText(_("Delete Screen"))
        self["buttonYellow"].setText(_("Extract Screen"))
        self["buttonBlue"].setText(_("Show Preview"))
        self["titel"].setText(_("Skin Parts"))
        
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
        self.root_backup = root

        for screen in root.findall('screen'):   
            screenname = screen.attrib['name']
            list.append((_(str(screenname)), str(screenname)))

        list.sort()
        self.debug(len(list))
        self["menuList"].setList(list)

    def keyGreen(self):
        options = []
        d = os.listdir(MAIN_USER_PATH)
        try:
           for xml in d:
              if xml.endswith('.part'):
                 options.extend(((_(str(xml)), boundFunction(self.delete_screen, str(xml))),))
           self.session.openWithCallback(self.menuCallback, ChoiceBox, list = options, title = "L\xc3\xb6sche part.Datei")
        except:
           self.session.open(MessageBox, _("Keine part.Dateien gefunden"), MessageBox.TYPE_INFO, timeout=5)

    def keyYellow(self):
        self.curSN = self["menuList"].getCurrent()[1]    
        for screen in self.root_backup.findall('screen'):   
            screenname = screen.attrib['name']
            if screenname.startswith(str(self.curSN)):
               self.screen_part = etree.tostring(screen, encoding='utf-8', pretty_print=True)
               break
        
        self.skin_part_file = MAIN_USER_PATH + 'screen_' + str(self.curSN) + '.part'
        if fileExists(self.skin_part_file):
           message = str(self.skin_part_file) + '\nist schon vorhanden soll die vorhandene ersetzt werden?'
           self.session.openWithCallback(self.ask_for_extract, MessageBox, message, MessageBox.TYPE_YESNO)
        else:
           self.extract_screen_part()

    def keyBlue(self):
        self.curSN = self["menuList"].getCurrent()[1]
        options = []
        d = os.listdir(MAIN_USER_PATH)
        try:
           for xml in d:
              if xml.endswith('.part'):
                 options.extend(((_(str(xml)), boundFunction(self.show_screen, str(xml))),))
           self.session.openWithCallback(self.menuCallback, ChoiceBox, list = options, title = "Zeige part.Datei")
        except:
           self.session.open(MessageBox, _("Keine part.Dateien gefunden"), MessageBox.TYPE_INFO, timeout=5)
           
    def menuCallback(self, ret):
        ret and ret[1]()    

    def delete_screen(self, what):
        os.remove(MAIN_USER_PATH + str(what))
        self.session.open(MessageBox, _(str(what) + " wurde entfernt."), MessageBox.TYPE_INFO, timeout=5)
    
    def show_screen(self, what):
        self.session.open(PartPreview, str(what))
        
    def ask_for_extract(self, answer):
        if answer is True:
            self.extract_screen_part()
        else:
            pass       
    
    def extract_screen_part(self):       
        f = open(self.skin_part_file,'w')
        f.write(str(self.screen_part))
        f.close 
        self.session.open(MessageBox, _("Der " + str(self.curSN) + " Screen wurde als Screen Part in /user erstellt."), MessageBox.TYPE_INFO, timeout=5)
        
    def exit(self):
        self["menuList"].onSelectionChanged.remove(self.__selectionChanged)
        self.close()

    def __selectionChanged(self):
        pass
        
    def debug(self, what, error=None):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[SkinParts]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
           
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           if error != None:
              f.write('[SkinParts]' + str(what) + ' error: ' + str(error) + '\n')
           else:
              f.write('[SkinParts]' + str(what) + '\n')
           f.close()
           
class PartPreview(Screen):
    def __init__(self, session, what):
        self.session = session
        f = open(MAIN_USER_PATH + str(what), 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self["actions"] = ActionMap(
            [
                "OkCancelActions"
            ],
            {
                "cancel": self.close
            }, -1)
        self.onLayoutFinish.append(self.hello)
        
    def hello(self):
        print('here i am')