#version = '3.6.64'
import os
try:
   opkg_info = os.popen("opkg list-installed enigma2-plugin-skins-sevenhd | cut -d ' ' -f3").read()
   version = str(opkg_info.strip().split('+')[0])
except:
   version = '3.6.64'
import re
import time
import math
import urllib
import socket
import gettext
import requests
import subprocess
from Plugins.Plugin import PluginDescriptor
try:
  from Plugins.SystemPlugins.OSDPositionSetup.plugin import OSDScreenPosition
  OSDScreenPosition_plugin = True
except ImportError:
  from Screens.UserInterfacePositioner import UserInterfacePositioner
  OSDScreenPosition_plugin = False
try:
  from boxbranding import getBoxType
  brand = True
except ImportError:
  brand = False
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Setup import Setup
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigSelectionNumber, ConfigNumber, ConfigText, ConfigInteger, ConfigClock
from Components.NimManager import nimmanager
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Console import Console as eConsole
from Components.Language import language
from os import environ, listdir, remove, rename, system, popen
from shutil import move, copy, rmtree, copytree
from lxml import etree
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from skin import parseColor
from tempfile import mkstemp
from urllib import urlencode
from urllib2 import urlopen, URLError
from xml.etree.cElementTree import fromstring
from twisted.web.client import downloadPage, getPage
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eListboxPythonMultiContent, gFont
from Tools import Notifications
from Tools.BoundFunction import boundFunction
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
################################################################################################################################################################
DOWNLOAD_URL = 'https://raw.githubusercontent.com/KravenHD/SevenHD-Daten/master/'
DOWNLOAD_UPDATE_URL = DOWNLOAD_URL + 'update/'
MAIN_PLUGIN_PATH = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/"
MAIN_IMAGE_PATH = MAIN_PLUGIN_PATH + "images/"
MAIN_DATA_PATH = MAIN_PLUGIN_PATH + "data/"
MAIN_USER_PATH = MAIN_PLUGIN_PATH + "user/"
MAIN_SKIN_PATH = "/usr/share/enigma2/SevenHD/"
USER_FONT_FILE = MAIN_USER_PATH + 'user_font.txt'
USER_COLOR_FILE = MAIN_USER_PATH + 'user_color.txt'
PLUGIN_PATH = "/usr/lib/enigma2/python/Plugins/"
FILE = MAIN_SKIN_PATH + "skin.xml"
DEV_MODE = MAIN_PLUGIN_PATH + "dev_mode"
TMPFILE = FILE + ".tmp"
XML = ".xml"
CREATOR = 'openATV'
try:
   image = os.popen('cat /etc/image-version').read()
   if 'creator=OpenMips' in image: 
      CREATOR = 'OpenMips'
except:
   try:
      image = os.popen('cat /etc/motd').read()
      if 'HDMU' in image: 
         CREATOR = 'OpenMips'
   except:
         CREATOR = 'unknow'
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
################################################################################################################################################################
# GobalConfigEntries
config.plugins.SevenHD = ConfigSubsection()
###########################################
# try Importe
config.plugins.SevenHD.NumberZapExtImport = ConfigYesNo(default= False)
try:
   from Plugins.SystemPlugins.NumberZapExt.plugin import ACTIONLIST, NumberZapExtSetupScreen
   config.plugins.SevenHD.NumberZapExtImport.value = True
except ImportError:
   config.plugins.SevenHD.NumberZapExtImport.value = False

config.plugins.SevenHD.version = ConfigText(default=version, fixed_size=False)
config.plugins.SevenHD.AutoUpdate = ConfigYesNo(default = False)
config.plugins.SevenHD.AutoUpdateInfo = ConfigYesNo(default = False)
config.plugins.SevenHD.AutoUpdatePluginStart = ConfigYesNo(default = False)
################# bmeminfo ##############################
if fileExists('/proc/bmeminfo'):
   entrie = os.popen('cat /proc/bmeminfo').read()
   mem = entrie.split(':', 1)[1].split('k')[0]
   bmem = int(mem)/1024
else:
   mem_info = []
   entrie = os.popen('cat /proc/cmdline').read()
   
   if brand:
      if getBoxType() == 'vusolo4k':
         mem = re.findall('_cma=(.*?)M', entrie)
      else:   
         mem = re.findall('bmem=(.*?)M', entrie)
   else:   
      mem = re.findall('bmem=(.*?)M', entrie)
      
   for info in mem:
      mem_info.append((info))
       
   bmem = 0
   for x in range(len(mem_info)):
       bmem += int(mem_info[x])   
       
SkinModeList = []
SkinModeList.append(("1", _("HD Skin 1280 x 720")))
if bmem > 180:
   SkinModeList.append(("2", _("FullHD Skin 1920 x 1080")))
if bmem > 440:
   SkinModeList.append(("3", _("UHD Skin 3840 x 2160")))
   #SkinModeList.append(("4", _("4K Skin 4096 x 2160")))
#if bmem > 880:
   #SkinModeList.append(("5", _("FullUHD Skin 7680 x 4320")))
   #SkinModeList.append(("6", _("8K Skin 8192 x 4320")))
#SkinModeList.append(("7", _("User Selection")))

config.plugins.SevenHD.skin_mode = ConfigSelection(default="1", choices = SkinModeList)
config.plugins.SevenHD.skin_mode_x = ConfigInteger(default = 1280, limits=(720, 9999))
config.plugins.SevenHD.skin_mode_y = ConfigInteger(default = 720, limits=(720, 9999))
config.plugins.SevenHD.old_skin_mode = ConfigText(default = '1') 
###########################################
config.plugins.SevenHD.systemfonts = ConfigYesNo(default = False) 
FontList = []
FontList.append(("noto", _("NotoSans (Standard)")))
FontList.append(("handel", _("HandelGotD")))
FontList.append(("campton", _("Campton")))
FontList.append(("proxima", _("Proxima Nova")))
FontList.append(("opensans", _("OpenSans")))
# todo skip Fonts from above
USE_FONT = 0
if fileExists("/etc/enigma2/SystemFont"):
   USE_FONT = 1
   if os.path.exists(MAIN_SKIN_PATH + 'fonts'):
      USE_FONT = 2
      FontsDir = os.listdir(MAIN_SKIN_PATH + 'fonts')
      for font in FontsDir:
          if font.endswith('.otf') or font.endswith('.ttf'):
             FontList.append(("%s?systemfont" % font, _("%s (SystemFont)" % font))) 
config.plugins.SevenHD.FontStyle_1 = ConfigSelection(default="noto", choices = FontList)
config.plugins.SevenHD.FontStyle_2 = ConfigSelection(default="noto", choices = FontList)

config.plugins.SevenHD.FontStyleHeight_1 = ConfigSelectionNumber(default = 95, stepwidth = 1, min = 0, max = 120, wraparound = True)
config.plugins.SevenHD.FontStyleHeight_2 = ConfigSelectionNumber(default = 95, stepwidth = 1, min = 0, max = 120, wraparound = True)

config.plugins.SevenHD.Header = ConfigSelection(default="header-seven", choices = [
				("header-seven", _("SevenHD"))
				])

UserList = []
if fileExists(MAIN_USER_PATH + "user_color.txt"):
   with open(MAIN_USER_PATH + "user_color.txt", 'r') as xFile:
        lines = xFile.readlines()
   for line in lines:
        if ',' in line and not line.startswith('#'):
           ColorHexCode, ColorName = re.split(',', str(line))
           UserList.append(("%s" % str(ColorHexCode.strip()), _("%s" % str(ColorName.strip()))))

ColorList = []
ColorList.append(("00000000", _("black")))
ColorList.append(("00ffffff", _("white")))
ColorList.append(("00F0A30A", _("amber")))
ColorList.append(("00B27708", _("amber dark")))
ColorList.append(("001B1775", _("blue")))
ColorList.append(("000E0C3F", _("blue dark")))
ColorList.append(("007D5929", _("brown")))
ColorList.append(("003F2D15", _("brown dark")))
ColorList.append(("000050EF", _("cobalt")))
ColorList.append(("00001F59", _("cobalt dark")))
ColorList.append(("001BA1E2", _("cyan")))
ColorList.append(("000F5B7F", _("cyan dark")))
ColorList.append(("00999999", _("grey")))
ColorList.append(("003F3F3F", _("grey dark")))
ColorList.append(("0070AD11", _("green")))
ColorList.append(("00213305", _("green dark")))
ColorList.append(("006D8764", _("olive")))
ColorList.append(("00313D2D", _("olive dark")))
ColorList.append(("00C3461B", _("orange")))
ColorList.append(("00892E13", _("orange dark")))
ColorList.append(("00F472D0", _("pink")))
ColorList.append(("00723562", _("pink dark")))
ColorList.append(("00E51400", _("red")))
ColorList.append(("00330400", _("red dark")))
ColorList.append(("00647687", _("steel")))
ColorList.append(("00262C33", _("steel dark")))
ColorList.append(("006C0AAB", _("violet")))
ColorList.append(("001F0333", _("violet dark")))
ColorList.append(("00FFF006", _("yellow")))
ColorList.append(("00FFBE00", _("yellow dark")))
ColorList.append(("00A19181", _("Kraven")))
ColorList.append(("0028150B", _("Kraven dark")))
ColorList += UserList
   
TransList = [] 
for x in range(101):
    tc = hex(int(round(float(255 * x / 100))))[2:]
    if len(tc) == 1:
       tc = '0' + str(tc)
    TransList.append(("%s" % str(tc), "%s" % str(str(x) + ' %')))              

BackList = ['brownleather', 'carbon', 'lightwood', 'redwood', 'slate']

LanguageList = []
LanguageList.append(("de", _("Deutsch")))
LanguageList.append(("en", _("English")))
LanguageList.append(("ru", _("Russian")))
LanguageList.append(("it", _("Italian")))
LanguageList.append(("es", _("Spanish (es)")))
LanguageList.append(("sp", _("Spanish (sp)")))
LanguageList.append(("uk", _("Ukrainian (uk)")))
LanguageList.append(("ua", _("Ukrainian (ua)")))
LanguageList.append(("pt", _("Portuguese")))
LanguageList.append(("ro", _("Romanian")))
LanguageList.append(("pl", _("Polish")))
LanguageList.append(("fi", _("Finnish")))
LanguageList.append(("nl", _("Dutch")))
LanguageList.append(("fr", _("French")))
LanguageList.append(("bg", _("Bulgarian")))
LanguageList.append(("sv", _("Swedish (sv)")))
LanguageList.append(("se", _("Swedish (se)")))
LanguageList.append(("zh_tw", _("Chinese Traditional")))
LanguageList.append(("zh", _("Chinese Simplified (zh)")))
LanguageList.append(("zh_cn", _("Chinese Simplified (zh_cn)")))
LanguageList.append(("tr", _("Turkish")))
LanguageList.append(("hr", _("Croatian")))
LanguageList.append(("ca", _("Catalan")))
################################################################################################################################################################
# GlobalScreen

config.plugins.SevenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS")),
				("main-custom-opennfr", _("openNFR"))
				])

config.plugins.SevenHD.ButtonStyle = ConfigSelection(default="buttons_seven_white", choices = [
				("buttons_seven_white", _("white")),
				("buttons_seven_black", _("black")),
				("buttons_seven_blue", _("blue")),
				("buttons_seven_green", _("green")),
				("buttons_seven_grey", _("grey")),
				("buttons_seven_orange", _("orange")),
				("buttons_seven_red", _("red")),
				("buttons_seven_violet", _("violet")),
				("buttons_seven_yellow", _("yellow")),
				("buttons_seven_black_blue", _("black/blue")),
				("buttons_seven_black_green", _("black/green")),
				("buttons_seven_black_orange", _("black/orange")),
				("buttons_seven_black_red", _("black/red")),
				("buttons_seven_black_silver", _("black/silver")),
				("buttons_seven_black_violet", _("black/violet")),
				("buttons_seven_black_yellow", _("black/yellow"))
				])
                                				
config.plugins.SevenHD.IconStyle = ConfigSelection(default="icons_seven_white", choices = [
				("icons_seven_amber", _("amber")),
				("icons_seven_white", _("white")),
				("icons_seven_black", _("black")),
				("icons_seven_blue", _("blue")),
				("icons_seven_brown", _("brown")),
				("icons_seven_cobalt", _("cobalt")),
				("icons_seven_cyan", _("cyan")),
				("icons_seven_green", _("green")),
				("icons_seven_grey", _("grey")),
				("icons_seven_olive", _("olive")),
				("icons_seven_orange", _("orange")),
				("icons_seven_pink", _("pink")),
				("icons_seven_red", _("red")),
				("icons_seven_steel", _("steel")),
				("icons_seven_violet", _("violet")),
				("icons_seven_yellow", _("yellow"))
				])
config.plugins.SevenHD.RunningText = ConfigSelection(default="running", choices = [
				("running", _("running")),
				("writing", _("writing")),
				("none", _("off"))
				])
				
config.plugins.SevenHD.Startdelay = ConfigSelectionNumber(default = 20, stepwidth = 1, min = 1, max = 20, wraparound = True)

config.plugins.SevenHD.Steptime = ConfigSelectionNumber(default = 100, stepwidth = 25, min = 25, max = 325, wraparound = True)

config.plugins.SevenHD.VolumeStyle = ConfigSelection(default="volumestyle-original", choices = [
				("volumestyle-original", _("Style 1")),
				("volumestyle-left-side", _("Style 2")),
				("volumestyle-right-side", _("Style 3")),
				("volumestyle-top-side", _("Style 4")),
				("volumestyle-number", _("Style 5")),
				("volumestyle-center", _("Style 6"))
				])

config.plugins.SevenHD.Volume = ConfigSelection(default="00000000", choices = ColorList)
				
config.plugins.SevenHD.NumberZapExt = ConfigSelection(default="numberzapext-none", choices = [
				("numberzapext-none", _("off")),
				("numberzapext-xpicon", _("Style 1")),
				("numberzapext-xpicon2", _("Style 2")),
				("numberzapext-xpicon3", _("Style 3")),
				("numberzapext-xpicon4", _("Style 4"))
				])

config.plugins.SevenHD.PrimeTimeTime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))

ProgressVolList = [("progressvol", _("bunt"))]
ProgressVolList = ColorList + ProgressVolList
config.plugins.SevenHD.ProgressVol = ConfigSelection(default="00ffffff", choices = ProgressVolList)

################################################################################################################################################################
# PluginScreen
config.plugins.SevenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("Style 1")),
				("cooltv-picon", _("Style 2"))
				])
				
config.plugins.SevenHD.EMCStyle = ConfigSelection(default="emcnocover", choices = [
				("emcnocover", _("Style 1")),
				("emcsmallcover", _("Style 2")),
				("emcsmallcover2", _("Style 3")),
				("emcbigcover", _("Style 4")),
				("emcverybigcover", _("Style 5")),
				("emcminitv", _("Style 6")),
				("emcminitv2", _("Style 7"))
				])
				
config.plugins.SevenHD.MovieSelectionStyle = ConfigSelection(default="movieselectionnocover", choices = [
				("movieselectionnocover", _("Style 1")),
				("movieselectionsmallcover", _("Style 2")),
				("movieselectionsmallcover2", _("Style 3")),
				("movieselectionbigcover", _("Style 4")),
				("movieselectionminitv", _("Style 5"))
				])
				
config.plugins.SevenHD.MSNWeather = ConfigSelection(default="msn-standard", choices = [
				("msn-standard", _("standard")),
				("msn-icon", _("alternative icons"))
				])
				
config.plugins.SevenHD.EventView = ConfigSelection(default="eventviewnopicon", choices = [
				("eventviewnopicon", _("Style 1")),
				("eventviewpicon", _("Style 2")),
				("eventviewthumb", _("Style 3")),
				("eventviewminitv", _("Style 4"))
				])
				
config.plugins.SevenHD.EPGSelection = ConfigSelection(default="epgselectionnopicon", choices = [
				("epgselectionnopicon", _("Style 1")),
				("epgselectionpicon", _("Style 2")),
				("epgselectionthumb", _("Style 3")),
				("epgselectionminitv", _("Style 4"))
				])
				
config.plugins.SevenHD.TimerEdit = ConfigSelection(default="timereditleft", choices = [
				("timereditleft", _("Style 1")),
				("timereditright", _("Style 2")),
				("timereditminitv", _("Style 3"))
				])
				
config.plugins.SevenHD.use_alba_skin = ConfigYesNo(default = False)

config.plugins.SevenHD.use_mp_skin = ConfigYesNo(default= False)				
################################################################################################################################################################
# MenuScreen

BackgroundList = []
for x in BackList:
    BackgroundList.append(("back_%s_main" % x, _("%s" % x)))

BackgroundList = ColorList + BackgroundList
config.plugins.SevenHD.Background = ConfigSelection(default="00000000", choices = BackgroundList)

config.plugins.SevenHD.BackgroundColorTrans = ConfigSelection(default="0a", choices = TransList)

BackgroundRightList = []
for x in BackList:
    BackgroundRightList.append(("back_%s_right" % x, _("%s" % x)))                       
BackgroundRightList = ColorList + BackgroundRightList
config.plugins.SevenHD.BackgroundRight = ConfigSelection(default="00000000", choices = BackgroundRightList)
				
config.plugins.SevenHD.BackgroundRightColorTrans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.Line = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.SevenHD.LineRight = ConfigSelection(default="00ffffff", choices = ColorList)

BorderList = [("ff000000", _("off"))]
BorderList = ColorList + BorderList
config.plugins.SevenHD.Border = ConfigSelection(default="00ffffff", choices = BorderList)

BorderRightList = [("ff000000", _("off"))]
BorderRightList = ColorList + BorderRightList
config.plugins.SevenHD.BorderRight = ConfigSelection(default="00ffffff", choices = BorderRightList)

config.plugins.SevenHD.SelectionBackground = ConfigSelection(default="000050EF", choices = ColorList)
				
SelectionBorderList = [("none", _("off"))]
SelectionBorderList = ColorList + SelectionBorderList
config.plugins.SevenHD.SelectionBorder = ConfigSelection(default="00ffffff", choices = SelectionBorderList)

ProgressList = [("progress", _("bunt"))]
ProgressList = ColorList + ProgressList
config.plugins.SevenHD.Progress = ConfigSelection(default="00ffffff", choices = ProgressList)

config.plugins.SevenHD.Font1 = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.Font2 = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.SelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ButtonText = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ProgressLinePlug = ConfigSelection(default="00ffffff", choices = ColorList)


################################################################################################################################################################
# InfobarScreen

config.plugins.SevenHD.InfobarStyle = ConfigSelection(default="infobar-style-original", choices = [
				("infobar-style-original", _("Style 1")),
				("infobar-style-original2", _("Style 2")),
				("infobar-style-xpicon", _("Style 3")),
				("infobar-style-xpicon1", _("Style 4")),
				("infobar-style-xpicon2", _("Style 5")),
				("infobar-style-xpicon3", _("Style 6")),
				("infobar-style-xpicon4", _("Style 7")),
				("infobar-style-xpicon5", _("Style 8")),
				("infobar-style-xpicon6", _("Style 9")),
				("infobar-style-xpicon7", _("Style 10")),
				("infobar-style-xpicon8", _("Style 11")),
				("infobar-style-xpicon9", _("Style 12"))
				])
				
config.plugins.SevenHD.SIB = ConfigSelection(default="-top", choices = [
				("-top", _("Style 1")),
				("-left", _("Style 2")),
				("-full", _("Style 3")),
				("-minitv", _("Style 4")),
				("-right", _("Style 5")),
				("-minitv2", _("Style 6")),
				("-double", _("Style 7")),
				("-picon", _("Style 8"))
				])				

BackgroundIB1List = []
for x in BackList:
    BackgroundIB1List.append(("back_%s_ib1" % x, _("%s" % x)))                     
BackgroundIB1List = ColorList + BackgroundIB1List
config.plugins.SevenHD.BackgroundIB1 = ConfigSelection(default="00000000", choices = BackgroundIB1List)

BackgroundIB2List = []
for x in BackList:
    BackgroundIB2List.append(("back_%s_ib2" % x, _("%s" % x)))
BackgroundIB2List = ColorList + BackgroundIB2List
config.plugins.SevenHD.BackgroundIB2 = ConfigSelection(default="00000000", choices = BackgroundIB2List)

config.plugins.SevenHD.InfobarLine = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.InfobarLine2 = ConfigSelection(default="00ffffff", choices = ColorList)

BorderList = [("ff000000", _("off"))]
BorderList = ColorList + BorderList
config.plugins.SevenHD.InfobarBorder = ConfigSelection(default="00ffffff", choices = BorderList)

BorderList = [("ff000000", _("off"))]
BorderList = ColorList + BorderList
config.plugins.SevenHD.InfobarBorder2 = ConfigSelection(default="00ffffff", choices = BorderList)

config.plugins.SevenHD.InfobarChannelName = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("-ICN", _("name")),
				("-ICNumber", _("number")),
				("-ICNameandNumber", _("number and name"))
				])

config.plugins.SevenHD.FontCN = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.NextEvent = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.NowEvent = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.SNR = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ProgressLineIB = ConfigSelection(default="00ffffff", choices = ColorList)

ProgressIBList = [("progressib", _("bunt"))]
ProgressIBList = ColorList + ProgressIBList
config.plugins.SevenHD.ProgressIB = ConfigSelection(default="00ffffff", choices = ProgressIBList)

config.plugins.SevenHD.IB1ColorTrans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.IB2ColorTrans = ConfigSelection(default="0a", choices = TransList)

################################################################################################################################################################
# InfobarExtraScreen

config.plugins.SevenHD.ClockStyle = ConfigSelection(default="clock-standard", choices = [
				("clock-standard", _("standard")),
				("clock-seconds", _("with seconds")),
				("clock-weekday", _("with weekday")),
				("clock-analog", _("analog")),
				("clock-weather", _("weather icon")),
				("clock-weather-meteo", _("weather meteo")),
				("clock-android", _("android")),
				("clock-flip", _("flip")),
				("clock-circle", _("circle")),
				("clock-circle-second", _("circle seconds"))
				])

config.plugins.SevenHD.AnalogStyle = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockDate = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimeh = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimem = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimes = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTime = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockWeek = ConfigSelection(default="00ffffff", choices = ColorList)

WeatherList_1 = []
WeatherList_1.append(("none", _("off")))
WeatherList_1.append(("weather-big", _("big")))
WeatherList_1.append(("weather-small", _("small")))
WeatherList_1.append(("weather-slim", _("slim")))
WeatherList_1.append(("weather-left-side", _("left")))

WeatherList_2 = []
WeatherList_2.append(("none", _("off")))
WeatherList_2.append(("weather-tiny", _("on")))                              

config.plugins.SevenHD.WeatherStyle_1 = ConfigSelection(default="none", choices = WeatherList_1)

config.plugins.SevenHD.WeatherStyle_2 = ConfigSelection(default="none", choices = WeatherList_2)
                                
config.plugins.SevenHD.faq_language = ConfigSelection(default="de", choices = LanguageList)
				
config.plugins.SevenHD.refreshInterval = ConfigSelectionNumber(0, 480, 15, default = 15, wraparound = True)

config.plugins.SevenHD.ClockWeather = ConfigSelection(default="00ffffff", choices = ColorList)

##################################
# weahter
config.plugins.SevenHD.weather_owm_latlon = ConfigText(default = 'lat=51.3452&lon=12.38594&units=metric&lang=de', fixed_size = False) 
config.plugins.SevenHD.weather_accu_latlon = ConfigText(default = 'lat=51.3452&lon=12.38594&metric=1&language=de', fixed_size = False)
config.plugins.SevenHD.weather_realtek_latlon = ConfigText(default = 'lat=51.3452&lon=12.38594&metric=1&language=de', fixed_size = False)
config.plugins.SevenHD.weather_woe_id = ConfigNumber(default="671072") 
config.plugins.SevenHD.weather_accu_id = ConfigNumber(default="171240")
config.plugins.SevenHD.weather_msn_id = ConfigNumber(default="18374")
config.plugins.SevenHD.weather_lat = ConfigText(default = '51.3452', fixed_size = False) 
config.plugins.SevenHD.weather_lon = ConfigText(default = '12.38594', fixed_size = False) 
config.plugins.SevenHD.weather_gmcode = ConfigText(default="GMXX0072", fixed_size = False)
config.plugins.SevenHD.weather_cityname = ConfigText(default = 'Leipzig', fixed_size = False)
config.plugins.SevenHD.weather_language = ConfigSelection(default="de", choices = LanguageList)
config.plugins.SevenHD.weather_server = ConfigSelection(default="_owm", choices = [
				("_yahoo", _("Yahoo")),
				("_owm", _("OpenWeatherMap")),
				("_msn", _("MSN")),
				("_accu", _("Accuweather")),
				("_realtek", _("RealTek"))
                                ])
config.plugins.SevenHD.weather_search_over = ConfigSelection(default="auto", choices = [
				("auto", _("Auto")),
				("ip", _("IP")),
				("name", _("Name")),
				("woeid", _("WoeID")),
				("gmcode", _("GM Code")),
				("latlon", _("Lat/Long"))
                                ])
#############################
config.plugins.SevenHD.WeatherView = ConfigSelection(default="icon", choices = [
				("icon", _("Icon")),
				("meteo", _("Meteo"))
				])

config.plugins.SevenHD.MeteoColor = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.SatInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("satinfo-on", _("on"))
				])
				

config.plugins.SevenHD.SysInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("systeminfo-small", _("small")),
				("systeminfo-big", _("big"))
				])
				
config.plugins.SevenHD.ECMInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ecminfo-on", _("on"))
				])

config.plugins.SevenHD.FrontInfo = ConfigSelection(default="snr", choices = [
				("snr", _("SNR")),
				("db", _("dB"))
				])


################################################################################################################################################################
# ChannelScreen

config.plugins.SevenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices = [
				("channelselection-twocolumns", _("two columns 1")),
				("channelselection-twocolumns2", _("two columns 2")),
				("channelselection-twocolumns3", _("two columns 3")),
				("channelselection-twocolumns4", _("two columns 4")),
				("channelselection-twocolumns5", _("two columns 5")),
				("channelselection-twocolumns6", _("two columns 6")),
				("channelselection-twocolumns7", _("two columns 7")),
				("channelselection-twocolumns8", _("two columns 8")),
				("channelselection-twocolumns9", _("two columns 9")),
				("channelselection-minitv1", _("two columns 10")),
				("channelselection-minitvx", _("two columns 11")),
				("channelselection-pip", _("two columns 12")),
				("channelselection-preview", _("two columns 13 (preview)")),
				("channelselection-threecolumns", _("three columns 1")),
				("channelselection-threecolumnsminitv", _("three columns 2"))
				])

ChannelBack1List = []
for x in BackList:
    ChannelBack1List.append(("back_%s_csleft" % x, _("%s" % x)))                    
ChannelBack1List = ColorList + ChannelBack1List
config.plugins.SevenHD.ChannelBack1 = ConfigSelection(default="00000000", choices = ChannelBack1List)


ChannelBack2List = []
for x in BackList:
    ChannelBack2List.append(("back_%s_csright" % x, _("%s" % x)))                     
ChannelBack2List = ColorList + ChannelBack2List
config.plugins.SevenHD.ChannelBack2 = ConfigSelection(default="00000000", choices = ChannelBack2List)
                   

ChannelBack3List = []
for x in BackList:
    ChannelBack3List.append(("back_%s_csmiddle" % x, _("%s" % x)))                    
ChannelBack3List = ColorList + ChannelBack3List
config.plugins.SevenHD.ChannelBack3 = ConfigSelection(default="00000000", choices = ChannelBack3List)

config.plugins.SevenHD.ChannelLine = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelLineRight = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelLineMiddle = ConfigSelection(default="00ffffff", choices = ColorList)

ChannelBorderList = [("ff000000", _("off"))]
ChannelBorderList = ColorList + ChannelBorderList
config.plugins.SevenHD.ChannelBorder = ConfigSelection(default="00ffffff", choices = ChannelBorderList)

ChannelBorderRightList = [("ff000000", _("off"))]
ChannelBorderRightList = ColorList + ChannelBorderRightList
config.plugins.SevenHD.ChannelBorderRight = ConfigSelection(default="00ffffff", choices = ChannelBorderRightList)

ChannelBorderMiddleList = [("ff000000", _("off"))]
ChannelBorderMiddleList = ColorList + ChannelBorderMiddleList
config.plugins.SevenHD.ChannelBorderMiddle = ConfigSelection(default="00ffffff", choices = ChannelBorderMiddleList)

config.plugins.SevenHD.ChannelColorButton = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorBouquet = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorChannel = ConfigSelection(default="00ffffff", choices = ColorList)
                                                                                                        
config.plugins.SevenHD.ChannelColorNext = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorNow = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorPrimeTime = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorDesciption = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorDesciptionNext = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorDesciptionLater = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorRuntime = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorProgram = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorTimeCS = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorChannelName = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorChannelNumber = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ChannelColorEvent = ConfigSelection(default="00ffffff", choices = ColorList)

ProgressBorderCSList = [("ff000000", _("off"))]
ProgressBorderCSList = ColorList + ProgressBorderCSList
config.plugins.SevenHD.ProgressBorderCS = ConfigSelection(default="00ffffff", choices = ProgressBorderCSList)

config.plugins.SevenHD.ProgressLineCS = ConfigSelection(default="00ffffff", choices = ColorList)

ProgressCSList = [("progresscs", _("bunt"))]
ProgressCSList = ColorList + ProgressCSList
config.plugins.SevenHD.ProgressCS = ConfigSelection(default="00ffffff", choices = ProgressCSList)

ProgressListCSList = [("progresslistcs", _("bunt"))]
ProgressListCSList = ColorList + ProgressListCSList
config.plugins.SevenHD.ProgressListCS = ConfigSelection(default="00ffffff", choices = ProgressListCSList)

config.plugins.SevenHD.CSLeftColorTrans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.CSMiddleColorTrans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.CSRightColorTrans = ConfigSelection(default="0a", choices = TransList)
################################################################################################################################################################
# SkinParts
config.plugins.SevenHD.use_skin_parts = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("skin_user", _("skin-user.xml")),
				("skinparts", _("screen_xxxxx.part"))
				])
################################################################################################################################################################
# SonstigesScreen
				
config.plugins.SevenHD.debug = ConfigYesNo(default = True)

config.plugins.SevenHD.debug_screen_names = ConfigYesNo(default = False)

config.plugins.SevenHD.msgdebug = ConfigYesNo(default = False)

config.plugins.SevenHD.grabdebug = ConfigYesNo(default= False)	

config.plugins.SevenHD.use_epg_thumb = ConfigYesNo(default= False)

PathList = []
if os.path.isdir("/media/hdd"):
   PathList.append(("/media/hdd", _("/media/hdd")))
if os.path.isdir("/media/usb"):
   PathList.append(("/media/usb", _("/media/usb")))
if os.path.isdir("/media/cf"):
   PathList.append(("/media/cf", _("/media/cf")))
PathList.append(("/tmp", _("/tmp")))

config.plugins.SevenHD.epg_thumb_cache = ConfigSelection(default="/tmp", choices = PathList)			
################################################################################################################################################################
# ConfigList

myConfigList = [('config.plugins.SevenHD.Image.value = "' + str(config.plugins.SevenHD.Image.value) + '"'),
                ('config.plugins.SevenHD.ButtonStyle.value = "' + str(config.plugins.SevenHD.ButtonStyle.value) + '"'),
                ('config.plugins.SevenHD.FontStyle_1.value = "' + str(config.plugins.SevenHD.FontStyle_1.value) + '"'),
                ('config.plugins.SevenHD.FontStyle_2.value = "' + str(config.plugins.SevenHD.FontStyle_2.value) + '"'),
                ('config.plugins.SevenHD.RunningText.value = "' + str(config.plugins.SevenHD.RunningText.value) + '"'),
                ('config.plugins.SevenHD.Startdelay.value = "' + str(config.plugins.SevenHD.Startdelay.value) + '"'),
                ('config.plugins.SevenHD.Steptime.value = "' + str(config.plugins.SevenHD.Steptime.value) + '"'),
                ('config.plugins.SevenHD.VolumeStyle.value = "' + str(config.plugins.SevenHD.VolumeStyle.value) + '"'),
                ('config.plugins.SevenHD.Volume.value = "' + str(config.plugins.SevenHD.Volume.value) + '"'),
                ('config.plugins.SevenHD.NumberZapExt.value = "' + str(config.plugins.SevenHD.NumberZapExt.value) + '"'),
                ('config.plugins.SevenHD.Background.value = "' + str(config.plugins.SevenHD.Background.value) + '"'),
                ('config.plugins.SevenHD.BackgroundColorTrans.value = "' + str(config.plugins.SevenHD.BackgroundColorTrans.value) + '"'),
                ('config.plugins.SevenHD.BackgroundRight.value = "' + str(config.plugins.SevenHD.BackgroundRight.value) + '"'),
                ('config.plugins.SevenHD.BackgroundRightColorTrans.value = "' + str(config.plugins.SevenHD.BackgroundRightColorTrans.value) + '"'),
                ('config.plugins.SevenHD.IB1ColorTrans.value = "' + str(config.plugins.SevenHD.IB1ColorTrans.value) + '"'),
                ('config.plugins.SevenHD.IB2ColorTrans.value = "' + str(config.plugins.SevenHD.IB2ColorTrans.value) + '"'),
                ('config.plugins.SevenHD.CSLeftColorTrans.value = "' + str(config.plugins.SevenHD.CSLeftColorTrans.value) + '"'),
                ('config.plugins.SevenHD.CSMiddleColorTrans.value = "' + str(config.plugins.SevenHD.CSMiddleColorTrans.value) + '"'),
                ('config.plugins.SevenHD.CSRightColorTrans.value = "' + str(config.plugins.SevenHD.CSRightColorTrans.value) + '"'),
                ('config.plugins.SevenHD.Line.value = "' + str(config.plugins.SevenHD.Line.value) + '"'),
                ('config.plugins.SevenHD.Border.value = "' + str(config.plugins.SevenHD.Border.value) + '"'),
                ('config.plugins.SevenHD.LineRight.value = "' + str(config.plugins.SevenHD.LineRight.value) + '"'),
                ('config.plugins.SevenHD.BorderRight.value = "' + str(config.plugins.SevenHD.BorderRight.value) + '"'),
                ('config.plugins.SevenHD.SelectionBackground.value = "' + str(config.plugins.SevenHD.SelectionBackground.value) + '"'),
                ('config.plugins.SevenHD.SelectionBorder.value = "' + str(config.plugins.SevenHD.SelectionBorder.value) + '"'),
                ('config.plugins.SevenHD.Progress.value = "' + str(config.plugins.SevenHD.Progress.value) + '"'),
                ('config.plugins.SevenHD.ProgressVol.value = "' + str(config.plugins.SevenHD.ProgressVol.value) + '"'),
                ('config.plugins.SevenHD.ProgressIB.value = "' + str(config.plugins.SevenHD.ProgressIB.value) + '"'),
                ('config.plugins.SevenHD.ProgressCS.value = "' + str(config.plugins.SevenHD.ProgressCS.value) + '"'),
                ('config.plugins.SevenHD.ProgressListCS.value = "' + str(config.plugins.SevenHD.ProgressListCS.value) + '"'),
                ('config.plugins.SevenHD.Font1.value = "' + str(config.plugins.SevenHD.Font1.value) + '"'),
                ('config.plugins.SevenHD.Font2.value = "' + str(config.plugins.SevenHD.Font2.value) + '"'),
                ('config.plugins.SevenHD.SelectionFont.value = "' + str(config.plugins.SevenHD.SelectionFont.value) + '"'),
                ('config.plugins.SevenHD.ButtonText.value = "' + str(config.plugins.SevenHD.ButtonText.value) + '"'),
                ('config.plugins.SevenHD.InfobarStyle.value = "' + str(config.plugins.SevenHD.InfobarStyle.value) + '"'),
                ('config.plugins.SevenHD.SIB.value = "' + str(config.plugins.SevenHD.SIB.value) + '"'),
                ('config.plugins.SevenHD.BackgroundIB1.value = "' + str(config.plugins.SevenHD.BackgroundIB1.value) + '"'),
                ('config.plugins.SevenHD.BackgroundIB2.value = "' + str(config.plugins.SevenHD.BackgroundIB2.value) + '"'),
                ('config.plugins.SevenHD.InfobarLine.value = "' + str(config.plugins.SevenHD.InfobarLine.value) + '"'),
                ('config.plugins.SevenHD.InfobarBorder.value = "' + str(config.plugins.SevenHD.InfobarBorder.value) + '"'),
                ('config.plugins.SevenHD.InfobarChannelName.value = "' + str(config.plugins.SevenHD.InfobarChannelName.value) + '"'),
                ('config.plugins.SevenHD.FontCN.value = "' + str(config.plugins.SevenHD.FontCN.value) + '"'),
                ('config.plugins.SevenHD.NextEvent.value = "' + str(config.plugins.SevenHD.NextEvent.value) + '"'),
                ('config.plugins.SevenHD.NowEvent.value = "' + str(config.plugins.SevenHD.NowEvent.value) + '"'),
                ('config.plugins.SevenHD.SNR.value = "' + str(config.plugins.SevenHD.SNR.value) + '"'),
                ('config.plugins.SevenHD.ClockStyle.value = "' + str(config.plugins.SevenHD.ClockStyle.value) + '"'),
                ('config.plugins.SevenHD.AnalogStyle.value = "' + str(config.plugins.SevenHD.AnalogStyle.value) + '"'),
                ('config.plugins.SevenHD.ClockDate.value = "' + str(config.plugins.SevenHD.ClockDate.value) + '"'),
                ('config.plugins.SevenHD.ClockTimeh.value = "' + str(config.plugins.SevenHD.ClockTimeh.value) + '"'),
                ('config.plugins.SevenHD.ClockTimem.value = "' + str(config.plugins.SevenHD.ClockTimem.value) + '"'),
                ('config.plugins.SevenHD.ClockTimes.value = "' + str(config.plugins.SevenHD.ClockTimes.value) + '"'),
                ('config.plugins.SevenHD.ClockTime.value = "' + str(config.plugins.SevenHD.ClockTime.value) + '"'),
                ('config.plugins.SevenHD.ClockWeek.value = "' + str(config.plugins.SevenHD.ClockWeek.value) + '"'),
                ('config.plugins.SevenHD.WeatherStyle_1.value = "' + str(config.plugins.SevenHD.WeatherStyle_1.value) + '"'),
                ('config.plugins.SevenHD.WeatherStyle_2.value = "' + str(config.plugins.SevenHD.WeatherStyle_2.value) + '"'),
                ('config.plugins.SevenHD.WeatherView.value = "' + str(config.plugins.SevenHD.WeatherView.value) + '"'),
                ('config.plugins.SevenHD.MeteoColor.value = "' + str(config.plugins.SevenHD.MeteoColor.value) + '"'),
                ('config.plugins.SevenHD.ClockWeather.value = "' + str(config.plugins.SevenHD.ClockWeather.value) + '"'),
                ('config.plugins.SevenHD.SatInfo.value = "' + str(config.plugins.SevenHD.SatInfo.value) + '"'),
                ('config.plugins.SevenHD.SysInfo.value = "' + str(config.plugins.SevenHD.SysInfo.value) + '"'),
                ('config.plugins.SevenHD.ECMInfo.value = "' + str(config.plugins.SevenHD.ECMInfo.value) + '"'),
                ('config.plugins.SevenHD.FrontInfo.value = "' + str(config.plugins.SevenHD.FrontInfo.value) + '"'),
                ('config.plugins.SevenHD.ChannelSelectionStyle.value = "' + str(config.plugins.SevenHD.ChannelSelectionStyle.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack1.value = "' + str(config.plugins.SevenHD.ChannelBack1.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack2.value = "' + str(config.plugins.SevenHD.ChannelBack2.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack3.value = "' + str(config.plugins.SevenHD.ChannelBack3.value) + '"'),
                ('config.plugins.SevenHD.ChannelLine.value = "' + str(config.plugins.SevenHD.ChannelLine.value) + '"'),
                ('config.plugins.SevenHD.ChannelBorder.value = "' + str(config.plugins.SevenHD.ChannelBorder.value) + '"'),
                ('config.plugins.SevenHD.ChannelLineRight.value = "' + str(config.plugins.SevenHD.ChannelLineRight.value) + '"'),
                ('config.plugins.SevenHD.ChannelBorderRight.value = "' + str(config.plugins.SevenHD.ChannelBorderRight.value) + '"'),
                ('config.plugins.SevenHD.ChannelLineMiddle.value = "' + str(config.plugins.SevenHD.ChannelLineMiddle.value) + '"'),
                ('config.plugins.SevenHD.ChannelBorderMiddle.value = "' + str(config.plugins.SevenHD.ChannelBorderMiddle.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorButton.value = "' + str(config.plugins.SevenHD.ChannelColorButton.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorBouquet.value = "' + str(config.plugins.SevenHD.ChannelColorBouquet.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorChannel.value = "' + str(config.plugins.SevenHD.ChannelColorChannel.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorNext.value = "' + str(config.plugins.SevenHD.ChannelColorNext.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorNow.value = "' + str(config.plugins.SevenHD.ChannelColorNow.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorPrimeTime.value = "' + str(config.plugins.SevenHD.ChannelColorPrimeTime.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorDesciption.value = "' + str(config.plugins.SevenHD.ChannelColorDesciption.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorDesciptionNext.value = "' + str(config.plugins.SevenHD.ChannelColorDesciptionNext.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorDesciptionLater.value = "' + str(config.plugins.SevenHD.ChannelColorDesciptionLater.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorRuntime.value = "' + str(config.plugins.SevenHD.ChannelColorRuntime.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorProgram.value = "' + str(config.plugins.SevenHD.ChannelColorProgram.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorTimeCS.value = "' + str(config.plugins.SevenHD.ChannelColorTimeCS.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorChannelName.value = "' + str(config.plugins.SevenHD.ChannelColorChannelName.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorChannelNumber.value = "' + str(config.plugins.SevenHD.ChannelColorChannelNumber.value) + '"'),
                ('config.plugins.SevenHD.ChannelColorEvent.value = "' + str(config.plugins.SevenHD.ChannelColorEvent.value) + '"'),
                ('config.plugins.SevenHD.CoolTVGuide.value = "' + str(config.plugins.SevenHD.CoolTVGuide.value) + '"'),
                ('config.plugins.SevenHD.EMCStyle.value = "' + str(config.plugins.SevenHD.EMCStyle.value) + '"'),
                ('config.plugins.SevenHD.EventView.value = "' + str(config.plugins.SevenHD.EventView.value) + '"'),
                ('config.plugins.SevenHD.TimerEdit.value = "' + str(config.plugins.SevenHD.TimerEdit.value) + '"'),
                ('config.plugins.SevenHD.EPGSelection.value = "' + str(config.plugins.SevenHD.EPGSelection.value) + '"'),
                ('config.plugins.SevenHD.MovieSelectionStyle.value = "' + str(config.plugins.SevenHD.MovieSelectionStyle.value) + '"'),
                ('config.plugins.SevenHD.ProgressLinePlug.value = "' + str(config.plugins.SevenHD.ProgressLinePlug.value) + '"'),
                ('config.plugins.SevenHD.ProgressLineIB.value = "' + str(config.plugins.SevenHD.ProgressLineIB.value) + '"'),
                ('config.plugins.SevenHD.ProgressLineCS.value = "' + str(config.plugins.SevenHD.ProgressLineCS.value) + '"'),
                ('config.plugins.SevenHD.ProgressBorderCS.value = "' + str(config.plugins.SevenHD.ProgressBorderCS.value) + '"')]
