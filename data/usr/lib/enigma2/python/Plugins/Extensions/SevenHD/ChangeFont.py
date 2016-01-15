# -*- coding: utf-8 -*-
#######################################################################
#
# FontHeightManager by .:TBX:.
#   for KravenSkin (c) 2016
#
#######################################################################
import re
import sys
from lxml import etree
from shutil import copy

copy('/usr/share/enigma2/SevenHD/skin.xml', '/usr/share/enigma2/SevenHD/skin.xml.tmp')

tree = etree.parse('/usr/share/enigma2/SevenHD/skin.xml.tmp')
root = tree.getroot()

with open('/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/user/user_font.txt', 'r') as font_file:
     lines = font_file.readlines()
                
for fontheight in lines:
    height_entrie = re.search("'(.+?)', '(.+?)', '(.+?)', '(.+?)', '(.+?)', '(.+?)'", str(fontheight)).groups(1)
    new_height = round(float(height_entrie[5]) * float(sys.argv[1]))
   
   
    for screen in root.findall('screen'):   
        if screen.get('name') == str(height_entrie[1]):
           for child in screen:
              try:
                 font = child.get('font')
                 if ';' in font:
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
                             name = 'NICHTS'
                        
                    if name == str(height_entrie[2]):
                       fontheight = font.split(';')
                       new_font = fontheight[0] + ';' + str(int(new_height))
                       child.set('font', new_font)
              except:
                 pass
             
tree.write('/usr/share/enigma2/SevenHD/skin.xml')