# -*- coding: utf-8 -*-
from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from urllib2 import urlopen
from enigma import eTimer

url = "http://www.gigablue-support.org/skins/SevenHD/update/version.txt"

class SevenHDUpdate(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		
                if type == 'Update':
                   self.type = 1
                else:
                   self.type = -1
		
                self.check_timer = eTimer()
                self.check_timer.callback.append(self.getText)
                self.check_timer.start(60000)
					
	@cached
	def getText(self):
	    version = config.plugins.SevenHD.version.value
            box_version = version
            if self.type == 1:
               try:
                   new_version = urlopen(url).read()
                   online_version = new_version
               except:
                   new_version = '0.0.0'
                   online_version = 'N/A'
               
               version = ''.join(version.replace('.',''))
               new_version = ''.join(new_version.replace('.',''))
                 
               if str(len(version)) <= str('3'): 
                   version = version + str('0')
                   if str(len(version)) < str('4'): 
                      version = version + str('0')
               if str(len(new_version)) <= str('3'): 
                   new_version = new_version + str('0')
                   if str(len(new_version)) < str('4'): 
                      new_version = new_version + str('0')
                      
               if int(version) < int(new_version):
                   self.update_available = 'Last Version on Server ' + str(online_version)
               else:
                   self.update_available = 'Last Version on Server ' + str(box_version)
                   
               return self.update_available
            else:
               return version
	text = property(getText)
################################################################################
        @cached
	def getValue(self):
	    version = config.plugins.SevenHD.version.value
            if self.type == 1:
               try:
                   new_version = urlopen(url).read()
               except:
                   new_version = '0.0.0'
                
               version = ''.join(version.replace('.',''))
               new_version = ''.join(new_version.replace('.',''))
                 
               if str(len(version)) <= str('3'): 
                   version = version + str('0')
                   if str(len(version)) < str('4'): 
                      version = version + str('0')
               if str(len(new_version)) <= str('3'): 
                   new_version = new_version + str('0')
                   if str(len(new_version)) < str('4'): 
                      new_version = new_version + str('0')
               
               if int(version) < int(new_version):
                   self.update_available = 1
               else:
                   self.update_available = -1
	
               return self.update_available
            else:
               return -1
	value = property(getValue)
################################################################################
        @cached
	def getBoolean(self):
	    version = config.plugins.SevenHD.version.value
            if self.type == 1:
               try:
                   new_version = urlopen(url).read()
               except:
                   new_version = '0.0.0'
                
               version = ''.join(version.replace('.',''))
               new_version = ''.join(new_version.replace('.',''))
               
               if int(version) < int(new_version):
                   return True
               else:
                   return False
	
            else:
               return False
	boolean = property(getBoolean)
################################################################################
	def changed(self, what):
	    Converter.changed(self, (self.CHANGED_POLL,))
