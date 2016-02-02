# -*- coding: utf-8 -*-
# Written by .:TBX:.
# This Plugin is free Software!!!
# General imports

from GlobalImport import *

class Update():
        
        def __init__(self, session):
		self.session = session
		self.onClose = [ ]
		self.msgBox = None                                                    
                self.do_update()   

        
        def do_update(self):
                self.version = version
                self.debug(self.version)
                
                try:
                   self.new_version = urlopen(DOWNLOAD_UPDATE_URL + 'version.txt').read()
                   self.dl_version = self.new_version
                   self.ipk_url = DOWNLOAD_UPDATE_URL + 'enigma2-plugin-skins-sevenhd_%s_all.ipk' % str(self.dl_version)
                   self.filename = '/tmp/enigma2-plugin-skins-sevenhd_%s_all.ipk' % str(self.dl_version)
                   self.debug('Found new Version -> enigma2-plugin-skins-sevenhd_%s_all.ipk' % str(self.dl_version))
                   self.debug(self.ipk_url)

                except:
                   self.new_version = '0.0.0'
                   self.debug('URL/Server Error!!')

                self.version = ''.join(self.version.replace('.',''))
                self.new_version = ''.join(self.new_version.replace('.',''))

                self.debug('%s - %s' % (str(len(self.version)), str(len(self.new_version))))

                self.version = self.change_to_int(self.version)
                self.new_version = self.change_to_int(self.new_version)
                
                self.debug('%s - %s' % (str(self.version), str(self.new_version)))

                if int(self.version) < int(self.new_version):

                   if config.plugins.SevenHD.AutoUpdate.value:

                      if not self.session.in_exec:
                         self.download_ipk(True)
                         Notifications.AddNotification(MessageBox, _("GUI needs a restart after download Plugin.\n"), MessageBox.TYPE_INFO, timeout=5) 
                         
                      else:
                         self.download_ipk(True)
                         self.msgBox = self.session.open(MessageBox, _("GUI needs a restart after download Plugin.\n"), MessageBox.TYPE_INFO, timeout=5)
                         
                   else:

                      if not self.session.in_exec:
                         message = 'Found new Version -> enigma2-plugin-skins-sevenhd_%s_all.ipk\nDownload, Install and Reboot?' % str(self.dl_version)
                         Notifications.AddNotificationWithCallback(self.download_ipk, MessageBox, message, MessageBox.TYPE_YESNO, timeout=15)

                      else:
                         message = 'Found new Version -> enigma2-plugin-skins-sevenhd_%s_all.ipk\nDownload, Install and Reboot?' % str(self.dl_version)
                         self.msgBox = self.session.openWithCallback(self.download_ipk, MessageBox, message, MessageBox.TYPE_YESNO, timeout=15)

                else:
                   self.debug('No new Version found')
        
        
        def change_to_int(self, versionnumber):
            versionnumber = versionnumber.split('+')[0]
            if str(len(versionnumber)) <= str('3'): 
                   versionnumber = versionnumber + str('0')
                   if str(len(versionnumber)) < str('4'): 
                      versionnumber = versionnumber + str('0')
            return versionnumber
            
            
        def save_old_dirs(self):
            if os.path.exists("/tmp/SevenHDdirsbackup"):
               rmtree("/tmp/SevenHDdirsbackup")
               
            if os.path.exists('/usr/share/enigma2/SevenHD'):
               copytree('/usr/share/enigma2/SevenHD', '/tmp/SevenHDdirsbackup', symlinks=False, ignore=None)
        
        
        def copy_old_dirs_back(self):
            if os.path.exists('/tmp/SevenHDdirsbackup'):
               if not os.path.exists('/usr/share/enigma2/SevenHD'):
                  copytree('/tmp/SevenHDdirsbackup', '/usr/share/enigma2/SevenHD', symlinks=False, ignore=None)
            
                
        def download_ipk(self, answer):
            if answer is True:
               os.system('opkg update')
               self.save_old_dirs()
               self.debug('Try to download and install new Version')
               downloadPage(self.ipk_url, self.filename).addCallback(self.on_finish).addErrback(self.Error)
               self.msgBox = self.session.open(MessageBox, _("Please Wait ..."), MessageBox.TYPE_INFO, enable_input = False)
               

        def on_finish(self, fake): 
               self.debug('Install new Version finished')
               os.system('opkg install %s' % str(self.filename))
               self.debug('copy back')
               self.copy_old_dirs_back()
               self.debug('Download and Install new Version finished')
               self.msgBox = self.session.openWithCallback(self.reboot, MessageBox, _("GUI needs a restart after download Plugin."), MessageBox.TYPE_YESNO, timeout=30)
               
               
        def reboot(self, answer):
               if answer is True:
                  try:
                     self.session.open(TryQuitMainloop, 3)	
                  except:
                     os.system('reboot -f')

        def Error(self, error):
                if not self.session.in_exec:
                   Notifications.AddNotification(MessageBox, _("Download failed"), MessageBox.TYPE_ERROR)          
                else:
                   self.msgBox = self.session.open(MessageBox, _("Download failed"), MessageBox.TYPE_ERROR)
                self.debug(error)               
        
        
        def debug(self, what):        
                if config.plugins.SevenHD.debug.value:
                   f = open('/tmp/kraven_debug.txt', 'a+')
                   f.write('[AutoUpdate]' + str(what) + '\n')
                   f.close()
