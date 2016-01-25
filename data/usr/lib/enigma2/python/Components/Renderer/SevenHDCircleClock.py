# CircleClock
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
from enigma import ePixmap, eTimer
from Components.config import config
from PIL import Image, ImageDraw
import os

Clock_Path = '/usr/share/enigma2/SevenHD/clock'

class SevenHDCircleClock(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        if not os.path.isdir(Clock_Path):
           os.mkdir(Clock_Path)
        self.timer = eTimer()
        self.timer.callback.append(self.pollme)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if not self.suspended:
            
            value = self.source.text
            attrib = dict(self.skinAttributes)
            size = attrib['size'][0]

            hour_value = value.split(' ')[0]
            minute_value = value.split(' ')[1]
            seconde_value = value.split(' ')[2]

            a = int(size)
            b = int(a * 5 / 100)
            c = int(a - b)
            d = int(b * 2)
            e = int(a - d)
            f = int(b * 3)
            g = int(a - f)

            color_hour = self.generate(config.plugins.SevenHD.ClockTimeh.value)
            color_minute = self.generate(config.plugins.SevenHD.ClockTimem.value)
            color_seconde = self.generate(config.plugins.SevenHD.ClockTimes.value)

            image = Image.new('RGBA', (a,a), (255,0,0))
            image.putalpha(0)
            draw = ImageDraw.Draw(image)

            start = 270
            hour_end = 360 / 12 * int(hour_value) - 90
            minute_end = 360 / 60 * int(minute_value) - 90
            seconde_end = 360 / 60 * int(seconde_value) - 90

            draw.pieslice((0,0,a,a), start, hour_end, fill = (color_hour), outline=None)
            draw.ellipse((b,b,c,c), fill=0, outline = None)
            draw.pieslice((b,b,c,c), start, minute_end, fill = (color_minute), outline=None)
            draw.ellipse((d,d,e,e), fill=0, outline = None)
            if config.plugins.SevenHD.ClockStyle.value == 'clock-circle-second': 
               draw.pieslice((d,d,e,e), start, seconde_end, fill = (color_seconde), outline=None)
               draw.ellipse((f,f,g,g), fill=0, outline = None)

            image.save(Clock_Path + "/circle_clock.png")

            self.instance.setPixmapFromFile(Clock_Path + '/circle_clock.png')

    def generate(self,color):    
        if color.startswith('00'):
           r = int(color[2:4], 16)
           g = int(color[4:6], 16)
           b = int(color[6:], 16)
           return r,g,b

    def pollme(self):
        self.changed(None)
        return

    def onShow(self):
        self.suspended = False
        self.timer.start(200)

    def onHide(self):
        self.suspended = True
        self.timer.stop()
        
    def debug(self, what):
        if config.plugins.SevenHD.debug.value:
               f = open('/tmp/kraven_debug.txt', 'a+')
               f.write('[SevenHDCircleClockRender] ' + str(what) + '\n')
               f.close() 