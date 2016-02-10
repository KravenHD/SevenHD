# MovieThumb
# Copyright (c) .:TBX:. 2016
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from Renderer import Renderer
from enigma import ePixmap, eTimer, ePicLoad
from twisted.web.client import downloadPage
import requests
import os
from Components.AVSwitch import AVSwitch

PATH = '/usr/share/enigma2/SevenHD/thumb'

class SevenHDMovieThumb(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        if not os.path.isdir(PATH):
           os.mkdir(PATH)
        
        self.jpg_name = PATH + '/default.jpg'
        self.picload = ePicLoad()
        self.sc = AVSwitch().getFramebufferScale()
        
    def gotPic(self, picInfo = None):
        ptr = self.picload.getData()
        if ptr:
           self.instance.setPixmap(ptr.__deref__())
           os.remove(self.jpg_name)
    
    GUI_WIDGET = ePixmap
    def changed(self, what):
        if not self.instance:
           return
        try:
            size = self.instance.size()
            self.picload.setPara((size.width(), size.height(), self.sc[0], self.sc[1], 0, 0, '#ff000000'))
            self.picload.PictureData.get().append(self.gotPic)
            
            res = requests.request('get','http://ajax.googleapis.com/ajax/services/search/video?v=1.0&q=%s' % str(self.source.text))
            data = res.json()
            
            jpg_url = data['responseData']['results'][0]['tbUrl'].split('?')[0]
            downloadPage(str(jpg_url.replace('default','hqdefault')), self.jpg_name).addCallback(self.on_finish).addErrback(self.Error)
        
        except:
            self.instance.hide()
    
    def on_finish(self, what):
        print '[SevenHDMovieThumb] downlod complet'
        if os.path.isfile(self.jpg_name):
           print '[SevenHDMovieThumb] found Thumb'
           self.instance.show()
           self.picload.startDecode(self.jpg_name)
        
    def Error(self, errors):
        print '[SevenHDMovieThumb] found no Thumb'
        self.instance.hide()
        
    def onShow(self):
        self.changed(None)
        