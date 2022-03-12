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
class ShareSkinSettings:

    def share(self):
        try:
            f = open('/tmp/kraven_share_%s.skin' % version, 'w')
            self.debug("Open /tmp/kraven_share_%s.skin" % version)
            for configEntrie in myConfigList:
                f.write(configEntrie + '\n')
            f.close()
            self.debug("Youre Share Skin Config is saved. ;-)")
            return True
        except:
            self.debug("Anything goes wrong")
            return False
            
    def load(self):
        try:
           new_config = []
           new_skin = open('/tmp/kraven_share_%s.skin' % version).readlines()
           self.debug("Open /tmp/kraven_share_%s.skin" % version)
           for entrie in new_skin:
               if entrie != "":
                  self.debug('Entrie: ' + str(entrie))
                  try:
                     exec(entrie)
                     exec(entrie.replace('.value', '.save()').split(' ')[0])
                     self.debug('Entrie: ' + str(entrie.replace('.value', '.save()').split(' ')[0]))
                  except:
                     self.debug('\nError by: ' + str(entrie) + '\n')
           configfile.save()
           self.debug("New Skin Config is saved. ;-)")
           return True
        except:
           self.debug("Skin Config is wrong")
           return False
           
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           os.system("wget -q -c 'http://127.0.0.1/api/message?text=[ShareSkinSettings]\n%20%s%20&type=1' > /dev/null 2>&1 -O /tmp/muell &" % str(what))
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[ShareSkinSettings] ' + str(what) + '\n')
           f.close() 