# -*- coding: utf-8 -*-
import os
import requests
from enigma import eTimer
from Components.config import config
from Components.Element import cached
from Components.Converter.Converter import Converter

URL = 'https://raw.githubusercontent.com/KravenHD/SevenHD-Daten/master/update/version.txt'

class SevenHDUpdate(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
                
                if type == 'Update':
                   self.type = 'Update'
                elif type == 'Version':
                   self.type = 'Version'
                
                self.git_version = '0.0.0.0'   
                self.check_timer = eTimer()
                self.check_timer.callback.append(self.get)
                self.check_timer.start(30000)
	
	@cached
	def getText(self):
            if self.type == 'Update':
               self.info = self.look('1')
            if self.type == 'Version':
               self.info = self.get_version()
            return str(self.info)

	text = property(getText)

        @cached
	def getBoolean(self):
	    if self.type == 'Update':
               self.info = self.look('2')
            if self.type == 'Version':
               self.info = True
            return self.info

	boolean = property(getBoolean)

        def get(self):
            try:
                res = requests.request('get', URL)
                self.git_version = str(res.text)
            except:
            	print 'SevenHD Update Request Fails'
        
        def look(self, what):
            if self.git_version == '0.0.0.0':
               self.get()
            box_version = config.plugins.SevenHD.version.value
            online_version = self.git_version
	            
	    version_on_box = self.change_to_int(box_version)
	    version_on_line = self.change_to_int(online_version)
	    
            if int(version_on_box) < int(version_on_line):
                if str(what) == str('1'):   
                   self.update_available = 'Last Version on Server ' + str(online_version)
                else:
                   self.update_available = True
            else:
                if str(what) == str('1'):   
                   self.update_available = 'Last Version on Server ' + str(box_version)
                else:
                   self.update_available = False

            return self.update_available
        
        def change_to_int(self, versionnumber):
            versionnumber = versionnumber.replace('.','').split('+')[0]
            if str(len(versionnumber)) <= str('3'): 
                   versionnumber = versionnumber + str('0')
                   if str(len(versionnumber)) < str('4'): 
                      versionnumber = versionnumber + str('0')
            return versionnumber

        def get_version(self):
            opkg_info = os.popen("opkg list-installed enigma2-plugin-skins-sevenhd | cut -d ' ' -f3").read()
            version = 'Version: ' + str(opkg_info.strip())
            return version
            
        def changed(self, what):
	    Converter.changed(self, (self.CHANGED_POLL,))
