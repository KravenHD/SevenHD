version = '3.6.00'
import os
import re
import time
import socket
import gettext
import urllib
import subprocess
from Plugins.Plugin import PluginDescriptor
try:
  from Plugins.SystemPlugins.OSDPositionSetup.plugin import OSDScreenPosition
  OSDScreenPosition_plugin = True
except ImportError:
  from Screens.UserInterfacePositioner import UserInterfacePositioner
  OSDScreenPosition_plugin = False
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
from skin import parseColor
from urllib import urlencode
from urllib2 import urlopen, URLError
from twisted.web.client import downloadPage
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eListboxPythonMultiContent, gFont
from Tools.BoundFunction import boundFunction
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
################################################################################################################################################################
MAIN_IMAGE_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/'
MAIN_DATA_PATH = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/data/"
MAIN_SKIN_PATH = "/usr/share/enigma2/SevenHD/"
PLUGIN_PATH = "/usr/lib/enigma2/python/Plugins/"
FILE = "/usr/share/enigma2/SevenHD/skin.xml"
TMPFILE = FILE + ".tmp"
XML = ".xml"
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
   mem = entrie.split('bmem=')
   for info in mem:
     if 'M@' in info:
       mem_info.append((info.split('M@')[0]))
    
   if len(mem_info) > 1:
      bmem = int(mem_info[0]) + int(mem_info[1])  
   else:
      bmem = int(mem_info[0])
      
SkinModeList = []
SkinModeList.append(("1", _("HD Skin 1280 x 720")))
if bmem > 250:
   SkinModeList.append(("2", _("FullHD Skin 1920 x 1080")))
if bmem > 440:
   SkinModeList.append(("3", _("UHD Skin 3840 x 2160")))
   SkinModeList.append(("4", _("4K Skin 4096 x 2160")))
if bmem > 880:
   SkinModeList.append(("5", _("FullUHD Skin 7680 x 4320")))
   SkinModeList.append(("6", _("8K Skin 8192 x 4320")))
#SkinModeList.append(("7", _("User Selection")))

config.plugins.SevenHD.skin_mode = ConfigSelection(default="1", choices = SkinModeList)
config.plugins.SevenHD.skin_mode_x = ConfigInteger(default = 1280, limits=(720, 9999))
config.plugins.SevenHD.skin_mode_y = ConfigInteger(default = 720, limits=(720, 9999))
config.plugins.SevenHD.old_skin_mode = ConfigText(default = '1') 
###########################################
config.plugins.SevenHD.FontStyle = ConfigSelection(default="noto", choices = [
				("Noto", _("NotoSans-Regular"))
				])

config.plugins.SevenHD.Header = ConfigSelection(default="header-seven", choices = [
				("header-seven", _("SevenHD"))
				])

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
ColorList.append(("00FFBE00", _("yellow dark")))
ColorList.append(("00FFF006", _("yellow")))

TransList = []
TransList.append(("00", _("off")))
TransList.append(("0a", _("low")))
TransList.append(("4a", _("medium")))
TransList.append(("8a", _("high")))
TransList.append(("ff", _("full")))

BackList = ['brownleather', 'brick', 'checkerplate', 'lapis', 'metal', 
            'redwood', 'slate', 'scratchedmetal', 'stone']

################################################################################################################################################################
# GlobalScreen

config.plugins.SevenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS")),
				("main-custom-opennfr", _("openNFR")),
				("main-custom-atemio4you", _("Atemio4You"))
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
config.plugins.SevenHD.Startdelay = ConfigSelection(default="startdelay=2000", choices = [
				("startdelay=2000", _("2 sec")),
				("startdelay=4000", _("4 sec")),
				("startdelay=6000", _("6 sec")),
				("startdelay=8000", _("8 sec")),
				("startdelay=10000", _("10 sec"))
				])
config.plugins.SevenHD.Steptime = ConfigSelection(default="steptime=90", choices = [
				("steptime=150", _("low")),
				("steptime=90", _("standard")),
				("steptime=30", _("high"))
				])
config.plugins.SevenHD.VolumeStyle = ConfigSelection(default="volumestyle-original", choices = [
				("volumestyle-original", _("original")),
				("volumestyle-left-side", _("left")),
				("volumestyle-right-side", _("right")),
				("volumestyle-top-side", _("top")),
				("volumestyle-number", _("number")),
				("volumestyle-center", _("center"))
				])

config.plugins.SevenHD.Volume = ConfigSelection(default="00000000", choices = ColorList)
				
config.plugins.SevenHD.NumberZapExt = ConfigSelection(default="numberzapext-none", choices = [
				("numberzapext-none", _("off")),
				("numberzapext-zpicon", _("ZPicons")),
				("numberzapext-xpicon", _("XPicons")),
				("numberzapext-zzpicon", _("ZZPicons")),
				("numberzapext-zzzpicon", _("ZZZPicons"))
				])

config.plugins.SevenHD.PrimeTimeTime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))

ProgressVolList = [("progressvol", _("bunt"))]
ProgressVolList = ColorList + ProgressVolList
config.plugins.SevenHD.ProgressVol = ConfigSelection(default="00ffffff", choices = ProgressVolList)

config.plugins.SevenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("miniTV")),
				("cooltv-picon", _("picon"))
				])
				
config.plugins.SevenHD.EMCStyle = ConfigSelection(default="emcnocover", choices = [
				("emcnocover", _("no cover")),
				("emcsmallcover", _("small cover")),
				("emcbigcover", _("big cover")),
				("emcverybigcover", _("very big cover")),
				("emcminitv", _("miniTV"))
				])
				
config.plugins.SevenHD.MovieSelectionStyle = ConfigSelection(default="movieselectionnocover", choices = [
				("movieselectionnocover", _("no cover")),
				("movieselectionsmallcover", _("small cover")),
				("movieselectionbigcover", _("big cover")),
				("movieselectionminitv", _("miniTV"))
				])
################################################################################################################################################################
# MenuPluginScreen

BackgroundList = []
for x in BackList:
    BackgroundList.append(("back_%s_main" % x, _("%s" % x)))

#if config.plugins.SevenHD.skin_mode.value == '1':
BackgroundList = ColorList + BackgroundList
#else:
#   BackgroundList = ColorList
config.plugins.SevenHD.Background = ConfigSelection(default="00000000", choices = BackgroundList)

config.plugins.SevenHD.BackgroundColorTrans = ConfigSelection(default="0a", choices = TransList)

BackgroundRightList = []
for x in BackList:
    BackgroundRightList.append(("back_%s_right" % x, _("%s" % x)))                       
#if config.plugins.SevenHD.skin_mode.value == '1':
BackgroundRightList = ColorList + BackgroundRightList
#else:
#   BackgroundRightList = ColorList
config.plugins.SevenHD.BackgroundRight = ConfigSelection(default="00000000", choices = BackgroundRightList)
				
config.plugins.SevenHD.BackgroundRightColorTrans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.Line = ConfigSelection(default="00ffffff", choices = ColorList)
				
BorderList = [("ff000000", _("off"))]
BorderList = ColorList + BorderList
config.plugins.SevenHD.Border = ConfigSelection(default="00ffffff", choices = BorderList)

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
				("infobar-style-original", _("Original 1")),
				("infobar-style-original2", _("Original 2")),
				("infobar-style-original3", _("Original 3")),
				("infobar-style-original4", _("Original 4")),
				("infobar-style-original5", _("Original 5")),
				("infobar-style-original6", _("Original 6")),
				("infobar-style-zpicon", _("ZPicon 1")),
				("infobar-style-zpicon2", _("ZPicon 2")),
				("infobar-style-zpicon3", _("ZPicon 3")),
				("infobar-style-zpicon4", _("ZPicon 4")),
				("infobar-style-zpicon5", _("ZPicon 5")),
				("infobar-style-zpicon6", _("ZPicon 6")),
				("infobar-style-xpicon", _("XPicon 1")),
				("infobar-style-xpicon2", _("XPicon 2")),
				("infobar-style-xpicon3", _("XPicon 3")),
				("infobar-style-xpicon4", _("XPicon 4")),
				("infobar-style-xpicon5", _("XPicon 5")),
				("infobar-style-xpicon6", _("XPicon 6")),
				("infobar-style-zzpicon", _("ZZPicon 1")),
				("infobar-style-zzpicon2", _("ZZPicon 2")),
				("infobar-style-zzpicon3", _("ZZPicon 3")),
				("infobar-style-zzpicon4", _("ZZPicon 4")),
				("infobar-style-zzpicon5", _("ZZPicon 5")),
				("infobar-style-zzpicon6", _("ZZPicon 6")),
				("infobar-style-zzzpicon", _("ZZZPicon 1")),
				("infobar-style-zzzpicon2", _("ZZZPicon 2")),
				("infobar-style-zzzpicon3", _("ZZZPicon 3")),
				("infobar-style-zzzpicon4", _("ZZZPicon 4")),
				("infobar-style-zzzpicon5", _("ZZZPicon 5")),
				("infobar-style-zzzpicon6", _("ZZZPicon 6"))
				])
				
config.plugins.SevenHD.SIB = ConfigSelection(default="-top", choices = [
				("-top", _("top/bottom")),
				("-left", _("left/right")),
				("-full", _("full")),
				("-minitv", _("miniTV"))
				])				

BackgroundIB1List = []
for x in BackList:
    BackgroundIB1List.append(("back_%s_ib1" % x, _("%s" % x)))                     
#if config.plugins.SevenHD.skin_mode.value == '1':
BackgroundIB1List = ColorList + BackgroundIB1List
#else:
#   BackgroundIB1List = ColorList
config.plugins.SevenHD.BackgroundIB1 = ConfigSelection(default="00000000", choices = BackgroundIB1List)

config.plugins.SevenHD.BackgroundIB1Trans = ConfigSelection(default="0a", choices = TransList)

config.plugins.SevenHD.BackgroundIB2Trans = ConfigSelection(default="0a", choices = TransList)

BackgroundIB2List = []
for x in BackList:
    BackgroundIB2List.append(("back_%s_ib2" % x, _("%s" % x)))
#if config.plugins.SevenHD.skin_mode.value == '1':
BackgroundIB2List = ColorList + BackgroundIB2List
#else:
#   BackgroundIB2List = ColorList
config.plugins.SevenHD.BackgroundIB2 = ConfigSelection(default="00000000", choices = BackgroundIB2List)

config.plugins.SevenHD.InfobarLine = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.InfobarBorder = ConfigSelection(default="00ffffff", choices = ColorList)

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

################################################################################################################################################################
# InfobarExtraScreen

config.plugins.SevenHD.ClockStyle = ConfigSelection(default="clock-standard", choices = [
				("clock-standard", _("standard")),
				("clock-seconds", _("with seconds")),
				("clock-weekday", _("with weekday")),
				("clock-analog", _("analog")),
				("clock-weather", _("weather")),
				("clock-android", _("android"))
				])

config.plugins.SevenHD.AnalogStyle = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockDate = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimeh = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimem = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTimes = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockTime = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.ClockWeek = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.WeatherStyle = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-big", _("big")),
				("weather-slim", _("slim")),
				("weather-left-side", _("left")),
				("weather-small", _("small"))
				])
				
config.plugins.SevenHD.refreshInterval = ConfigSelectionNumber(10, 60, 10, default = 10, wraparound = True)

config.plugins.SevenHD.AutoWoeID = ConfigYesNo(default= True)

config.plugins.SevenHD.ClockWeather = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.SevenHD.weather_city = ConfigNumber(default="671072")

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
				("sysinfo-on", _("on"))
				])
				
config.plugins.SevenHD.ECMInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ecminfo2-on", _("on")),
				("ecminfo-on", _("infobar"))
				])


################################################################################################################################################################
# ChannelScreen

config.plugins.SevenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices = [
				("channelselection-twocolumns", _("two columns 1")),
				("channelselection-twocolumns2", _("two columns 2")),
				("channelselection-twocolumns3", _("two columns 3")),
				("channelselection-twocolumns4", _("two columns 4")),
				("channelselection-threecolumns", _("three columns")),
				("channelselection-threecolumnsminitv", _("three columns miniTV")),
				("channelselection-zpicon", _("ZPicon")),
				("channelselection-minitvz", _("ZPicon/miniTV")),
				("channelselection-xpicon", _("XPicon")),
				("channelselection-minitvx", _("XPicon/miniTV")),
				("channelselection-zzpicon", _("ZZPicon")),
				("channelselection-minitvzz", _("ZZPicon/miniTV")),
				("channelselection-zzzpicon", _("ZZZPicon")),
				("channelselection-minitvzzz", _("ZZZPicon/miniTV")),
				("channelselection-minitv1", _("miniTV")),
				("channelselection-pip", _("miniTV/PiP"))
				])

ChannelBack1List = []
for x in BackList:
    ChannelBack1List.append(("back_%s_csleft" % x, _("%s" % x)))                    
#if config.plugins.SevenHD.skin_mode.value == '1':
ChannelBack1List = ColorList + ChannelBack1List
#else:
#   ChannelBack1List = ColorList
config.plugins.SevenHD.ChannelBack1 = ConfigSelection(default="00000000", choices = ChannelBack1List)


ChannelBack2List = []
for x in BackList:
    ChannelBack2List.append(("back_%s_csright" % x, _("%s" % x)))                     
#if config.plugins.SevenHD.skin_mode.value == '1':
ChannelBack2List = ColorList + ChannelBack2List
#else:
#   ChannelBack2List = ColorList
config.plugins.SevenHD.ChannelBack2 = ConfigSelection(default="00000000", choices = ChannelBack2List)
                   

ChannelBack3List = []
for x in BackList:
    ChannelBack3List.append(("back_%s_csmiddle" % x, _("%s" % x)))                    
#if config.plugins.SevenHD.skin_mode.value == '1':
ChannelBack3List = ColorList + ChannelBack3List
#else:
#   ChannelBack3List = ColorList
config.plugins.SevenHD.ChannelBack3 = ConfigSelection(default="00000000", choices = ChannelBack3List)

config.plugins.SevenHD.ChannelLine = ConfigSelection(default="00ffffff", choices = ColorList)

ChannelBorderList = [("ff000000", _("off"))]
ChannelBorderList = ColorList + ChannelBorderList
config.plugins.SevenHD.ChannelBorder = ConfigSelection(default="00ffffff", choices = ChannelBorderList)

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

################################################################################################################################################################
# SonstigesScreen
				
config.plugins.SevenHD.debug = ConfigYesNo(default = False)

config.plugins.SevenHD.debug_screen_names = ConfigYesNo(default = False)

config.plugins.SevenHD.msgdebug = ConfigYesNo(default = False)

config.plugins.SevenHD.grabdebug = ConfigYesNo(default= False)	
			
################################################################################################################################################################
# ConfigList

myConfigList = [('config.plugins.SevenHD.Image.value = "' + str(config.plugins.SevenHD.Image.value) + '"'),
                ('config.plugins.SevenHD.ButtonStyle.value = "' + str(config.plugins.SevenHD.ButtonStyle.value) + '"'),
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
                ('config.plugins.SevenHD.Line.value = "' + str(config.plugins.SevenHD.Line.value) + '"'),
                ('config.plugins.SevenHD.Border.value = "' + str(config.plugins.SevenHD.Border.value) + '"'),
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
                ('config.plugins.SevenHD.BackgroundIB1Trans.value = "' + str(config.plugins.SevenHD.BackgroundIB1Trans.value) + '"'),
                ('config.plugins.SevenHD.BackgroundIB1Trans.value = "' + str(config.plugins.SevenHD.BackgroundIB1Trans.value) + '"'),
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
                ('config.plugins.SevenHD.WeatherStyle.value = "' + str(config.plugins.SevenHD.WeatherStyle.value) + '"'),
                ('config.plugins.SevenHD.WeatherView.value = "' + str(config.plugins.SevenHD.WeatherView.value) + '"'),
                ('config.plugins.SevenHD.MeteoColor.value = "' + str(config.plugins.SevenHD.MeteoColor.value) + '"'),
                ('config.plugins.SevenHD.ClockWeather.value = "' + str(config.plugins.SevenHD.ClockWeather.value) + '"'),
                ('config.plugins.SevenHD.SatInfo.value = "' + str(config.plugins.SevenHD.SatInfo.value) + '"'),
                ('config.plugins.SevenHD.SysInfo.value = "' + str(config.plugins.SevenHD.SysInfo.value) + '"'),
                ('config.plugins.SevenHD.ECMInfo.value = "' + str(config.plugins.SevenHD.ECMInfo.value) + '"'),
                ('config.plugins.SevenHD.ChannelSelectionStyle.value = "' + str(config.plugins.SevenHD.ChannelSelectionStyle.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack1.value = "' + str(config.plugins.SevenHD.ChannelBack1.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack2.value = "' + str(config.plugins.SevenHD.ChannelBack2.value) + '"'),
                ('config.plugins.SevenHD.ChannelBack3.value = "' + str(config.plugins.SevenHD.ChannelBack3.value) + '"'),
                ('config.plugins.SevenHD.ChannelLine.value = "' + str(config.plugins.SevenHD.ChannelLine.value) + '"'),
                ('config.plugins.SevenHD.ChannelBorder.value = "' + str(config.plugins.SevenHD.ChannelBorder.value) + '"'),
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
                ('config.plugins.SevenHD.MovieSelectionStyle.value = "' + str(config.plugins.SevenHD.MovieSelectionStyle.value) + '"'),
                ('config.plugins.SevenHD.ProgressLinePlug.value = "' + str(config.plugins.SevenHD.ProgressLinePlug.value) + '"'),
                ('config.plugins.SevenHD.ProgressLineIB.value = "' + str(config.plugins.SevenHD.ProgressLineIB.value) + '"'),
                ('config.plugins.SevenHD.ProgressLineCS.value = "' + str(config.plugins.SevenHD.ProgressLineCS.value) + '"'),
                ('config.plugins.SevenHD.ProgressBorderCS.value = "' + str(config.plugins.SevenHD.ProgressBorderCS.value) + '"')]