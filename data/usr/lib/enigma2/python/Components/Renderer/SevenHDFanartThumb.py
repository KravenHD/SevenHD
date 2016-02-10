# FanArt Thumb
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

import os
import re
import requests
from PIL import Image
from Renderer import Renderer
from enigma import ePixmap, eTimer
from Components.config import config
from twisted.web.client import downloadPage

HEADERS = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': 'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'}
PATH = '/usr/share/enigma2/SevenHD/thumb'
TIMEOUT = 1

class SevenHDFanartThumb(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        if not os.path.isdir(PATH):
           os.mkdir(PATH)
        
        self.count = 0
        self.png_name = PATH + '/default.png'  
        
        self.timer = eTimer()
        self.timer.callback.append(self.poll_my_search)
    
        self.re_download_timer = eTimer()
        self.re_download_timer.callback.append(self.poll_my_thumb)
        
    GUI_WIDGET = ePixmap
    def changed(self, what):
        self.load = 1
        if not self.instance:
           config.plugins.SevenHD.fanart_url.value = '-'
           config.plugins.SevenHD.fanart_url.save()
           return

        try:
           event = str(self.source.text.split(' - ', 1)[1])
           self.new_event = str(event)
        except:
           self.new_event = ''
           
        if self.new_event == '':
           self.timer.start(2000, 1)
        
        if what[0] != self.CHANGED_DEFAULT:
           
            if self.count == 0:
               return
            
            try:
               self.url = None
               
               self.get_id_by_tvdb()
               if self.path_data == None:
                  self.get_id_by_imdb()
                  if self.path_data == None:
                     self.get_id()
               
               if self.path_data == None:   
                  self.Error('Nothing Found')
                  return
               else:   
                  
                  if self.path_data == 'shows':
                     if self.tvdb_id != None:
                        self.get_show_by_fanart()
                     if self.url == None:
                        self.get_movie_show_by_trak()
                  
                  if self.path_data == 'movies':
                     if self.imdb_id == None:
                        return
                     else:
                        self.get_movie_by_fanart()
                        if self.url == None:
                           self.get_movie_show_by_trak()

               if self.url != None:         
               ######################################
                  if str(config.plugins.SevenHD.fanart_url.value) != str(self.new_event):      
                     downloadPage(str(self.url), self.png_name).addCallback(self.on_finish).addErrback(self.Error)
                  else:
                     if os.path.isfile(self.png_name):
                        self.instance.setPixmapFromFile(self.png_name)
                        self.instance.show()
               else:
                  self.Error('Nothing Found')
               return

            except:
                if os.path.isfile(self.png_name):
                   self.instance.setPixmapFromFile(self.png_name)
                   self.instance.show()
            return

        else:

            if str(config.plugins.SevenHD.fanart_url.value) == str(self.new_event):
                if os.path.isfile(self.png_name):
                   self.instance.setPixmapFromFile(self.png_name)
                   self.instance.show()
                return
            else:
                self.count = 1
        return  
    
    def get_id(self):
        try:
            res = requests.request('get', 'https://api-v2launch.trakt.tv/search?query=%s&type=movie,show' % str(self.new_event), headers = HEADERS, timeout = TIMEOUT)
            data = res.json()
            
            self.imdb_id = None
            self.tvdb_id = None
            self.path_data = None
            
            for x in data:
                if x['type'] == 'show':
                   self.path_data = 'shows'
                   self.imdb_id = x['show']['ids']['imdb']
                   self.tvdb_id = x['show']['ids']['tvdb']
                   break
                if x['type'] == 'movie':
                   self.path_data = 'movies'
                   self.imdb_id = x['movie']['ids']['imdb']
                   break
            return
        except:
            self.Error('Nothing Found')
    
    def get_id_by_tvdb(self):
        self.tvdb_id = None
        self.path_data = None
        self.imdb_id = None
        
        res = requests.request('get','http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=de' % str(self.new_event.replace('&','+').replace(':',' : ')), timeout = TIMEOUT)
        status = str(res.status_code)
        
        if status.startswith('40'):
           return        
        else:
           try:
              self.tvdb_id = re.search('id>(.+?)</id', str(res.text)).groups(1)[0]
              try:
                 self.imdb_id = re.search('IMDB_ID>(.+?)</IMDB_ID', str(res.text)).groups(1)[0]
              except:
                 self.imdb_id = self.imdb_id
              self.path_data = 'shows'
           except:
              self.tvdb_id = None
              self.path_data = None
              self.imdb_id = None
    
    def get_id_by_imdb(self):
        
        res = requests.request('get','https://www.omdbapi.com/?s=' + str(self.new_event), timeout = TIMEOUT)
        status = str(res.status_code)
        
        if status.startswith('40'):
           return
        else:
           try:
              data = res.json()
              self.imdb_id = data['Search'][0]['imdbID']
              self.path_data = 'movies'
           except:
              self.tvdb_id = None
              self.path_data = None
              self.imdb_id = None    
                              
    def get_show_by_fanart(self):
        if not self.tvdb_id:
           self.url = None
        else:
           res = requests.request('get','http://webservice.fanart.tv/v3/tv/%s?api_key=ed4b784f97227358b31ca4dd966a04f1' % str(self.tvdb_id), timeout = TIMEOUT)
           status = str(res.status_code)
           
           if status.startswith('40'):
              return
              
           data = res.json()
           
           try:
               try:
                   try:
                       try:
                           self.url = data['clearart'][0]['url']
                       except KeyError:
                           self.url = data['hdclearart'][0]['url']
                   except:   
                       self.url = data['hdtvlogo'][0]['url']
               except:
                   self.url = data['clearlogo'][0]['url']
           except:
               self.url = None
 
    
    def get_movie_by_fanart(self):
        if not self.imdb_id:
           self.url = None
        else:
           res = requests.request('get','http://webservice.fanart.tv/v3/movies/%s?api_key=ed4b784f97227358b31ca4dd966a04f1' % str(self.imdb_id), timeout = TIMEOUT)
           status = str(res.status_code)
           
           if status.startswith('40'):
              return
              
           data = res.json()
           
           try:
               try:
                   try:
                       try:
                           self.url = data['movieart'][0]['url']
                       except KeyError:
                           self.url = data['hdmovieclearart'][0]['url']
                   except:
                       self.url = data['hdmovielogo'][0]['url']
               except:
                   self.url = data['movielogo'][0]['url']    
           except:
               self.url = None
        
    
    def get_movie_show_by_trak(self):
        if not self.imdb_id:
           self.url = None
        else:
           res = requests.request('get', 'https://api-v2launch.trakt.tv/%s/%s?extended=images' % (str(self.path_data),str(self.imdb_id)), headers = HEADERS, timeout = TIMEOUT)
           status = str(res.status_code)
           
           if status.startswith('40'):
              return
              
           data = res.json()
                   
           self.url = data['images']['clearart']['full']
           if self.url == None:
              self.url = data['images']['banner']['full']
              if self.url == None:
                 self.url = data['images']['logo']['full']
        
            
    def on_finish(self, what):

        if self.load != 1:
           return
           
        if os.path.isfile(self.png_name):
           self.load = 0
           size = self.instance.size()
           
           self.re_download_timer.start(2000, 1)
           
           thumb = Image.open(self.png_name)
           thumb.thumbnail((size.width(), size.height()))
           thumb.save(self.png_name, 'png')
           
           self.re_download_timer.stop()
           
           config.plugins.SevenHD.fanart_url.value = str(self.new_event)
           config.plugins.SevenHD.fanart_url.save()
           
           self.instance.setPixmapFromFile(self.png_name)
           self.instance.show()
           return
           
    def Error(self, errors):
        if str(config.plugins.SevenHD.fanart_url.value) != str(self.new_event):
           if os.path.isfile(self.png_name):
              if self.load != 0:
                 os.remove(self.png_name)
        if errors == 'Nothing Found':
              config.plugins.SevenHD.fanart_url.value = str(self.new_event)
              config.plugins.SevenHD.fanart_url.save()
              self.instance.hide()
        return

    def onHide(self):
        self.timer.stop()
        self.re_download_timer.stop()
        
    def onShow(self):
        if self.instance:
           self.instance.hide()
           self.do_try(False)

    def do_try(self, suspended):
        self.count = 0
        if not suspended:
           self.changed((self.CHANGED_DEFAULT,))
           if self.count == 1:
              self.changed((self.CHANGED_CLEAR,))

    def poll_my_search(self):
        self.timer.stop()
        self.do_try(False)

    def poll_my_thumb(self):
        self.re_download_timer.stop()
        if str(config.plugins.SevenHD.fanart_url.value) != str(self.new_event):      
              self.load = 1
              os.remove(self.png_name)
              downloadPage(str(self.url), self.png_name).addCallback(self.on_finish).addErrback(self.Error)