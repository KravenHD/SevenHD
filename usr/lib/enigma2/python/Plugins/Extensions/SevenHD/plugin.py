#######################################################################
#
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#    SevenHD by Kraven
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad, getDesktop, eConsoleAppContainer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
#############################################################

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


#############################################################

config.plugins.SevenHD = ConfigSubsection()
config.plugins.SevenHD.weather_city = ConfigNumber(default="924938")

config.plugins.SevenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-atemio4you", _("Atemio4You")),
				("main-custom-hdmu", _("HDMU")),
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS")),
				("main-custom-opennfr", _("openNFR"))
				])
				
config.plugins.SevenHD.Header = ConfigSelection(default="header-seven", choices = [
				("header-seven", _("SevenHD"))
				])
				
config.plugins.SevenHD.Volume = ConfigSelection(default="volume-original", choices = [
				("volume-original", _("original")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-number", _("number")),
				("volume-center", _("center"))
				])
				
config.plugins.SevenHD.BackgroundColorTrans = ConfigSelection(default="0A", choices = [
				("0A", _("low")),
				("4A", _("medium")),
				("8A", _("high"))
				])
				
config.plugins.SevenHD.BackgroundRightColorTrans = ConfigSelection(default="0D", choices = [
				("0D", _("low")),
				("4D", _("medium")),
				("8C", _("high"))
				])
				
config.plugins.SevenHD.Background = ConfigSelection(default="000000", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("000000", _("black")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
				])
				
config.plugins.SevenHD.BackgroundRight = ConfigSelection(default="000001", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("000001", _("black")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
				])
				
config.plugins.SevenHD.BackgroundIB1 = ConfigSelection(default="000002", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("000002", _("black")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
				])
				
config.plugins.SevenHD.BackgroundIB2 = ConfigSelection(default="000003", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("000003", _("black")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
				])
				
config.plugins.SevenHD.SelectionBackground = ConfigSelection(default="000050EF", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.SevenHD.Font1 = ConfigSelection(default="00fffff3", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff3", _("white"))
				])
				
config.plugins.SevenHD.Font2 = ConfigSelection(default="00fffff4", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff4", _("white"))
				])
				
config.plugins.SevenHD.SelectionFont = ConfigSelection(default="00fffff7", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff7", _("white"))
				])
				
config.plugins.SevenHD.ButtonText = ConfigSelection(default="00fffff2", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff2", _("white"))
				])
				
config.plugins.SevenHD.Border = ConfigSelection(default="00fffff1", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff1", _("white")),
				("ff000000", _("off"))
				])
				
config.plugins.SevenHD.Progress = ConfigSelection(default="00fffff6", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff6", _("white"))
				])
				
config.plugins.SevenHD.Line = ConfigSelection(default="00fffff5", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00fffff5", _("white"))
				])
				
config.plugins.SevenHD.SelectionBorder = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.SevenHD.AnalogStyle = ConfigSelection(default="00999999", choices = [
				("00F0A30A", _("amber")),
				("00000000", _("black")),
				("001B1775", _("blue")),
				("007D5929", _("brown")),
				("000050EF", _("cobalt")),
				("001BA1E2", _("cyan")),
				("00999999", _("grey")),
				("0070AD11", _("green")),
				("00C3461B", _("orange")),
				("00F472D0", _("pink")),
				("00E51400", _("red")),
				("00647687", _("steel")),
				("006C0AAB", _("violet")),
				("00ffffff", _("white"))
				])
				
config.plugins.SevenHD.InfobarStyle = ConfigSelection(default="infobar-style-original", choices = [
				("infobar-style-original", _("Original")),
				("infobar-style-original2", _("Original 2")),
				("infobar-style-original3", _("Original 3")),
				("infobar-style-zpicon", _("ZPicon")),
				("infobar-style-zpicon2", _("ZPicon 2")),
				("infobar-style-zpicon3", _("ZPicon 3")),
				("infobar-style-xpicon", _("XPicon")),
				("infobar-style-xpicon2", _("XPicon 2")),
				("infobar-style-xpicon3", _("XPicon 3")),
				("infobar-style-zzpicon", _("ZZPicon")),
				("infobar-style-zzpicon2", _("ZZPicon 2")),
				("infobar-style-zzpicon3", _("ZZPicon 3")),
				("infobar-style-zzzpicon", _("ZZZPicon")),
				("infobar-style-zzzpicon2", _("ZZZPicon 2"))
				])
				
config.plugins.SevenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices = [
				("channelselection-twocolumns", _("two columns")),
				("channelselection-threecolumns", _("three columns")),
				("channelselection-zpicon", _("ZPicon")),
				("channelselection-xpicon", _("XPicon")),
				("channelselection-zzpicon", _("ZZPicon")),
				("channelselection-zzzpicon", _("ZZZPicon")),
				("channelselection-minitv", _("miniTV"))
				])
				
config.plugins.SevenHD.NumberZapExt = ConfigSelection(default="numberzapext-none", choices = [
				("numberzapext-none", _("off")),
				("numberzapext-zpicon", _("ZPicons")),
				("numberzapext-xpicon", _("XPicons")),
				("numberzapext-zzpicon", _("ZZPicons")),
				("numberzapext-zzzpicon", _("ZZZPicons"))
				])
				
config.plugins.SevenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("miniTV")),
				("cooltv-picon", _("picon"))
				])
				
config.plugins.SevenHD.EMCStyle = ConfigSelection(default="emc-bigcover", choices = [
				("emc-nocover", _("no cover")),
				("emc-smallcover", _("small cover")),
				("emc-bigcover", _("big cover")),
				("emc-verybigcover", _("very big cover"))
				])
				
config.plugins.SevenHD.RunningText = ConfigSelection(default="movetype=running", choices = [
				("movetype=running", _("on")),
				("movetype=none", _("off"))
				])
				
config.plugins.SevenHD.ButtonStyle = ConfigSelection(default="buttons_seven_white", choices = [
				("buttons_seven_white", _("white")),
				("buttons_seven_black", _("black"))
				])
config.plugins.SevenHD.ClockStyle = ConfigSelection(default="clock-standard", choices = [
				("clock-standard", _("standard")),
				("clock-seconds", _("with seconds")),
				("clock-weekday", _("with weekday")),
				("clock-analog", _("analog")),
				("clock-weather", _("weather")),
				("clock-android", _("android"))
				])
				
config.plugins.SevenHD.WeatherStyle = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-big", _("big")),
				("weather-small", _("small"))
				])
				
config.plugins.SevenHD.FontStyle = ConfigSelection(default="noto", choices = [
				("Noto", _("NotoSans-Regular"))
				])
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
				("ecminfo-on", _("on"))
				])
				
config.plugins.SevenHD.SIB1 = ConfigSelection(default="infobar-style-original_end", choices = [
				("infobar-style-original_end", _("top/bottom")),
				("infobar-style-original_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB2 = ConfigSelection(default="infobar-style-xpicon_end", choices = [
				("infobar-style-xpicon_end", _("top/bottom")),
				("infobar-style-xpicon_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB3 = ConfigSelection(default="infobar-style-zpicon_end", choices = [
				("infobar-style-zpicon_end", _("top/bottom")),
				("infobar-style-zpicon_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB4 = ConfigSelection(default="infobar-style-zzpicon_end", choices = [
				("infobar-style-zzpicon_end", _("top/bottom")),
				("infobar-style-zzpicon_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB5 = ConfigSelection(default="infobar-style-zzzpicon_end", choices = [
				("infobar-style-zzzpicon_end", _("top/bottom")),
				("infobar-style-zzzpicon_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB10 = ConfigSelection(default="infobar-style-original2_end", choices = [
				("infobar-style-original2_end", _("top/bottom")),
				("infobar-style-original2_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB20 = ConfigSelection(default="infobar-style-xpicon2_end", choices = [
				("infobar-style-xpicon2_end", _("top/bottom")),
				("infobar-style-xpicon2_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB30 = ConfigSelection(default="infobar-style-zpicon2_end", choices = [
				("infobar-style-zpicon2_end", _("top/bottom")),
				("infobar-style-zpicon2_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB40 = ConfigSelection(default="infobar-style-zzpicon2_end", choices = [
				("infobar-style-zzpicon2_end", _("top/bottom")),
				("infobar-style-zzpicon2_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB50 = ConfigSelection(default="infobar-style-zzzpicon2_end", choices = [
				("infobar-style-zzzpicon2_end", _("top/bottom")),
				("infobar-style-zzzpicon2_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB100 = ConfigSelection(default="infobar-style-original3_end", choices = [
				("infobar-style-original3_end", _("top/bottom")),
				("infobar-style-original3_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB200 = ConfigSelection(default="infobar-style-xpicon3_end", choices = [
				("infobar-style-xpicon3_end", _("top/bottom")),
				("infobar-style-xpicon3_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB300 = ConfigSelection(default="infobar-style-zpicon3_end", choices = [
				("infobar-style-zpicon3_end", _("top/bottom")),
				("infobar-style-zpicon3_end2", _("left/right"))
				])
				
config.plugins.SevenHD.SIB400 = ConfigSelection(default="infobar-style-zzpicon3_end", choices = [
				("infobar-style-zzpicon3_end", _("top/bottom")),
				("infobar-style-zzpicon3_end2", _("left/right"))
				])
				
config.plugins.SevenHD.InfobarChannelName1 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-original", _("on"))
				])
				
config.plugins.SevenHD.InfobarChannelName2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-original2", _("on"))
				])
				
config.plugins.SevenHD.InfobarChannelName3 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-zxpicon", _("on"))
				])
				
config.plugins.SevenHD.InfobarChannelName4 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-zxpicon2", _("on"))
				])
				
config.plugins.SevenHD.InfobarChannelName5 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-zzpicon", _("on"))
				])
				
config.plugins.SevenHD.InfobarChannelName6 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("name-zzpicon2", _("on"))
				])
				
#######################################################################

class SevenHD(ConfigListScreen, Screen):
	skin = """
<screen name="SevenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
   <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Reboot" transparent="1" />
  <widget name="config" position="18,72" size="816,575" transparent="1" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,12" size="708,46" text="SevenHD - Konfigurationstool" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
<eLabel position="891,657" size="372,46" text="Thanks to http://www.gigablue-support.org/" font="Regular; 12" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <widget name="helperimage" position="891,178" size="372,328" zPosition="1" backgroundColor="#00000000" />
  <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
    <eLabel backgroundColor="#00000000" position="6,6" size="842,708" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
    <eLabel backgroundColor="#00ffffff" position="6,6" size="842,2" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="6,714" size="842,2" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="6,6" size="2,708" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="848,6" size="2,708" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="18,64" size="816,2" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="18,656" size="816,2" zPosition="2" />
    <ePixmap pixmap="SevenHD/buttons/key_red1.png" position="22,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
    <ePixmap pixmap="SevenHD/buttons/key_green1.png" position="222,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
    <ePixmap pixmap="SevenHD/buttons/key_yellow1.png" position="422,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
    <ePixmap pixmap="SevenHD/buttons/key_blue1.png" position="622,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
 <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
      <convert type="ClockToText">Default</convert>
    </widget>
    <eLabel backgroundColor="#00000000" position="878,6" size="396,708" transparent="0" zPosition="-9" />
    <eLabel backgroundColor="#00ffffff" position="878,6" size="396,2" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="878,714" size="396,2" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="878,6" size="2,708" zPosition="2" />
    <eLabel backgroundColor="#00ffffff" position="1274,6" size="2,708" zPosition="2" />
<eLabel position="891,88" size="372,46" text="Version: 2.3" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/SevenHD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/comp/"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		
		list = []
		ConfigListScreen.__init__(self, list)
		
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.UpdatePicture()
		self.onLayoutFinish.append(self.mylist)

	def mylist(self):
		list = []
		list.append(getConfigListEntry(_("______________________ system __________________________________"), ))
		list.append(getConfigListEntry(_("image"), config.plugins.SevenHD.Image))
		list.append(getConfigListEntry(_("button style"), config.plugins.SevenHD.ButtonStyle))
		list.append(getConfigListEntry(_("running text"), config.plugins.SevenHD.RunningText))
		list.append(getConfigListEntry(_("Weather ID"), config.plugins.SevenHD.weather_city))
		list.append(getConfigListEntry(_("______________________ background __________________________________"), ))
		list.append(getConfigListEntry(_("color layer main"), config.plugins.SevenHD.Background))
		list.append(getConfigListEntry(_("transparency"), config.plugins.SevenHD.BackgroundColorTrans))
		list.append(getConfigListEntry(_("color layer right"), config.plugins.SevenHD.BackgroundRight))
		list.append(getConfigListEntry(_("transparency"), config.plugins.SevenHD.BackgroundRightColorTrans))
		list.append(getConfigListEntry(_("______________________ colors __________________________________"), ))
		list.append(getConfigListEntry(_("line"), config.plugins.SevenHD.Line))
		list.append(getConfigListEntry(_("border"), config.plugins.SevenHD.Border))
		list.append(getConfigListEntry(_("listselection"), config.plugins.SevenHD.SelectionBackground))
		list.append(getConfigListEntry(_("listselection border"), config.plugins.SevenHD.SelectionBorder))
		list.append(getConfigListEntry(_("progress-/volumebar"), config.plugins.SevenHD.Progress))
		list.append(getConfigListEntry(_("font 1"), config.plugins.SevenHD.Font1))
		list.append(getConfigListEntry(_("font 2"), config.plugins.SevenHD.Font2))
		list.append(getConfigListEntry(_("selection font"), config.plugins.SevenHD.SelectionFont))
		list.append(getConfigListEntry(_("button text"), config.plugins.SevenHD.ButtonText))
		list.append(getConfigListEntry(_("______________________ infobar __________________________________"), ))
		list.append(getConfigListEntry(_("style"), config.plugins.SevenHD.InfobarStyle))
		list.append(getConfigListEntry(_("color 1"), config.plugins.SevenHD.BackgroundIB1))
		list.append(getConfigListEntry(_("color 2"), config.plugins.SevenHD.BackgroundIB2))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName1))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original3":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName2))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName3))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon3" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon3":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName4))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName5))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon3":
			list.append(getConfigListEntry(_("channelname"), config.plugins.SevenHD.InfobarChannelName6))
		list.append(getConfigListEntry(_("clock"), config.plugins.SevenHD.ClockStyle))
		if config.plugins.SevenHD.ClockStyle.value == "clock-analog":
			list.append(getConfigListEntry(_("color clock analog"), config.plugins.SevenHD.AnalogStyle))
		list.append(getConfigListEntry(_("weather"), config.plugins.SevenHD.WeatherStyle))
		list.append(getConfigListEntry(_("satellite information"), config.plugins.SevenHD.SatInfo))
		list.append(getConfigListEntry(_("system information"), config.plugins.SevenHD.SysInfo))
		list.append(getConfigListEntry(_("ecm information"), config.plugins.SevenHD.ECMInfo))
		list.append(getConfigListEntry(_("______________________ general __________________________________"), ))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB1))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB2))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB3))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB4))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzzpicon":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB5))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original2":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB10))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon2":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB20))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon2":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB30))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon2":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB40))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzzpicon2":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB50))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original3":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB100))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon3":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB200))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon3":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB300))
		if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon3":
			list.append(getConfigListEntry(_("second infobar"), config.plugins.SevenHD.SIB400))
		list.append(getConfigListEntry(_("channel selection"), config.plugins.SevenHD.ChannelSelectionStyle))
		list.append(getConfigListEntry(_("EMC"), config.plugins.SevenHD.EMCStyle))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.SevenHD.NumberZapExt))
		list.append(getConfigListEntry(_("volume style"), config.plugins.SevenHD.Volume))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.SevenHD.CoolTVGuide))
		
		self["config"].list = list
		self["config"].l.setList(list)
		
		self.ShowPicture()

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			if returnValue == "infobar-style-original_end" or returnValue == "infobar-style-original2_end" or returnValue == "infobar-style-original3_end" or returnValue == "infobar-style-zpicon_end" or returnValue == "infobar-style-zpicon2_end" or returnValue == "infobar-style-zpicon3_end" or returnValue == "infobar-style-xpicon_end" or returnValue == "infobar-style-xpicon2_end" or returnValue == "infobar-style-xpicon3_end" or returnValue == "infobar-style-zzpicon_end" or returnValue == "infobar-style-zzpicon2_end" or returnValue == "infobar-style-zzpicon3_end" or returnValue == "infobar-style-zzzpicon_end" or returnValue == "infobar-style-zzzpicon2_end":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/SIB1.jpg"
			elif returnValue == "infobar-style-original_end2" or returnValue == "infobar-style-original2_end2" or returnValue == "infobar-style-original3_end2" or returnValue == "infobar-style-zpicon_end2" or returnValue == "infobar-style-zpicon2_end2" or returnValue == "infobar-style-zpicon3_end2" or returnValue == "infobar-style-xpicon_end2" or returnValue == "infobar-style-xpicon2_end2" or returnValue == "infobar-style-xpicon3_end2" or returnValue == "infobar-style-zzpicon_end2" or returnValue == "infobar-style-zzpicon2_end2" or returnValue == "infobar-style-zzpicon3_end2" or returnValue == "infobar-style-zzzpicon_end2" or returnValue == "infobar-style-zzzpicon2_end2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/SIB2.jpg"
			if returnValue == "name-original" or returnValue == "name-original2" or returnValue == "name-original3" or returnValue == "name-zxpicon" or returnValue == "name-zxpicon2" or returnValue == "name-zxpicon3" or returnValue == "name-zzpicon" or returnValue == "name-zzpicon2" or returnValue == "name-zzpicon3" or returnValue == "name-zzzpicon" or returnValue == "name-zzzpicon2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/name.jpg"
			else:
				path = "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/" + returnValue + ".jpg"
			if fileExists(path):
				return path
			else:
				## colors
				return "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/colors.jpg"
		except:
			## weather
			return "/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/924938.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)
	
	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.mylist()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.mylist()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

	def getDataByKey(self, list, key):
		for item in list:
			if item["key"] == key:
				return item
		return list[0]

	def getFontStyleData(self, key):
		return self.getDataByKey(channelselFontStyles, key)

	def getFontSizeData(self, key):
		return self.getDataByKey(channelInfoFontSizes, key)

	def save(self):
		if fileExists("/tmp/SevenHDweather.xml"):
			remove('/tmp/SevenHDweather.xml')

		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.set_font()
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(["0A", config.plugins.SevenHD.BackgroundColorTrans.value])
			self.skinSearchAndReplace.append(["0D", config.plugins.SevenHD.BackgroundRightColorTrans.value])
			self.skinSearchAndReplace.append(["000000", config.plugins.SevenHD.Background.value])
			self.skinSearchAndReplace.append(["000002", config.plugins.SevenHD.BackgroundIB1.value])
			self.skinSearchAndReplace.append(["000003", config.plugins.SevenHD.BackgroundIB2.value])
			self.skinSearchAndReplace.append(["000001", config.plugins.SevenHD.BackgroundRight.value])
			self.skinSearchAndReplace.append(["000050EF", config.plugins.SevenHD.SelectionBackground.value])
			self.skinSearchAndReplace.append(["00fffff3", config.plugins.SevenHD.Font1.value])
			self.skinSearchAndReplace.append(["00fffff4", config.plugins.SevenHD.Font2.value])
			self.skinSearchAndReplace.append(["00fffff7", config.plugins.SevenHD.SelectionFont.value])
			self.skinSearchAndReplace.append(["00fffff2", config.plugins.SevenHD.ButtonText.value])
			self.skinSearchAndReplace.append(["00fffff6", config.plugins.SevenHD.Progress.value])
			self.skinSearchAndReplace.append(["00fffff1", config.plugins.SevenHD.Border.value])
			self.skinSearchAndReplace.append(["00fffff5", config.plugins.SevenHD.Line.value])
			self.skinSearchAndReplace.append(["buttons_seven_white", config.plugins.SevenHD.ButtonStyle.value])
			self.skinSearchAndReplace.append(["movetype=running", config.plugins.SevenHD.RunningText.value])
			
			self.selectionbordercolor = config.plugins.SevenHD.SelectionBorder.value
			self.borset = ("borset_" + self.selectionbordercolor + ".png")
			self.skinSearchAndReplace.append(["borset.png", self.borset])
			
			self.analogstylecolor = config.plugins.SevenHD.AnalogStyle.value
			self.analog = ("analog_" + self.analogstylecolor + ".png")
			self.skinSearchAndReplace.append(["analog.png", self.analog])
			
			### Header
			self.appendSkinFile(self.daten + config.plugins.SevenHD.Header.value + ".xml")
			
			### Volume
			self.appendSkinFile(self.daten + config.plugins.SevenHD.Volume.value + ".xml")
			
			###ChannelSelection
			self.appendSkinFile(self.daten + config.plugins.SevenHD.ChannelSelectionStyle.value + ".xml")

			###Infobar_main
			self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarStyle.value + "_main.xml")

			###Channelname
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName1.value + ".xml")
			elif config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName2.value + ".xml")
			elif config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName3.value + ".xml")
			elif config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon3" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName4.value + ".xml")
			elif config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName5.value + ".xml")
			elif config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon2" or config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarChannelName6.value + ".xml")

			###ecm-info
			self.appendSkinFile(self.daten + config.plugins.SevenHD.ECMInfo.value + ".xml")

			###clock-style xml
			self.appendSkinFile(self.daten + config.plugins.SevenHD.ClockStyle.value + ".xml")

			###sat-info
			self.appendSkinFile(self.daten + config.plugins.SevenHD.SatInfo.value + ".xml")

			###sys-info
			self.appendSkinFile(self.daten + config.plugins.SevenHD.SysInfo.value + ".xml")

			###weather-style
			self.appendSkinFile(self.daten + config.plugins.SevenHD.WeatherStyle.value + ".xml")

			###Infobar_middle
			self.appendSkinFile(self.daten + config.plugins.SevenHD.InfobarStyle.value + "_middle.xml")

			###clock-style xml
			self.appendSkinFile(self.daten + config.plugins.SevenHD.ClockStyle.value + ".xml")

			###Infobar_end
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB1.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB2.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB3.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB4.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzzpicon":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB5.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original2":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB10.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon2":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB20.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon2":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB30.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon2":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB40.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzzpicon2":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB50.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-original3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB100.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-xpicon3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB200.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zpicon3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB300.value + ".xml")
			if config.plugins.SevenHD.InfobarStyle.value == "infobar-style-zzpicon3":
				self.appendSkinFile(self.daten + config.plugins.SevenHD.SIB400.value + ".xml")

			###Main XML
			self.appendSkinFile(self.daten + "main.xml")

			###Plugins XML
			self.appendSkinFile(self.daten + "plugins.xml")

			#EMCSTYLE
			self.appendSkinFile(self.daten + config.plugins.SevenHD.EMCStyle.value +".xml")

			#NumberZapExtStyle
			self.appendSkinFile(self.daten + config.plugins.SevenHD.NumberZapExt.value + ".xml")

			###custom-main XML
			self.appendSkinFile(self.daten + config.plugins.SevenHD.Image.value + ".xml")

			###cooltv XML
			self.appendSkinFile(self.daten + config.plugins.SevenHD.CoolTVGuide.value + ".xml")

			###skin-user
			try:
				self.appendSkinFile(self.daten + "skin-user.xml")
			except:
				pass
			###skin-end
			self.appendSkinFile(self.daten + "skin-end.xml")

			xFile = open(self.dateiTMP, "w")
			for xx in self.skin_lines:
				xFile.writelines(xx)
			xFile.close()

			move(self.dateiTMP, self.datei)

			#system('rm -rf ' + self.dateiTMP)
			
			console1 = eConsoleAppContainer()
			console2 = eConsoleAppContainer()
			console3 = eConsoleAppContainer()
			console4 = eConsoleAppContainer()
			
			#buttons
			console1.execute("rm -rf /usr/share/enigma2/SevenHD/buttons/*.*; rm -rf /usr/share/enigma2/SevenHD/buttons; wget -q http://www.gigablue-support.org/skins/SevenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ButtonStyle.value), str(config.plugins.SevenHD.ButtonStyle.value), str(config.plugins.SevenHD.ButtonStyle.value)))
			#weather
			console2.execute("rm -rf /usr/share/enigma2/SevenHD/WetterIcons/*.*; rm -rf /usr/share/enigma2/SevenHD/WetterIcons; wget -q http://www.gigablue-support.org/skins/SevenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.WeatherStyle.value), str(config.plugins.SevenHD.WeatherStyle.value), str(config.plugins.SevenHD.WeatherStyle.value)))
			#clock
			console3.execute("rm -rf /usr/share/enigma2/SevenHD/clock/*.*; rm -rf /usr/share/enigma2/SevenHD/clock; wget -q http://www.gigablue-support.org/skins/SevenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.ClockStyle.value), str(config.plugins.SevenHD.ClockStyle.value), str(config.plugins.SevenHD.ClockStyle.value)))
			#volume
			console4.execute("rm -rf /usr/share/enigma2/SevenHD/volume/*.*; rm -rf /usr/share/enigma2/SevenHD/volume; wget -q http://www.gigablue-support.org/skins/SevenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/SevenHD/" % (str(config.plugins.SevenHD.Volume.value), str(config.plugins.SevenHD.Volume.value), str(config.plugins.SevenHD.Volume.value)))
						
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to download files and apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		"""
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def set_font(self):
		'''header-kraven.xml; header-seven; header-zero
		handel = 97
		noto= 95
		opensans= 93
		proxima = 103'''
		#config.plugins.SevenHD.Header.value
		new_font = config.plugins.SevenHD.FontStyle.value
		if new_font == "noto":
			new_scale = 'scale="95"'
			new_font_name1 = 'NotoSans-Regular.ttf'
			new_font_name2 = 'NotoSans-Bold.ttf'
		elif new_font == "handel":
			new_scale = 'scale="97"'
			new_font_name1 = 'HandelGotD.ttf'
			new_font_name2 = 'HandelGotDBol.ttf'
		elif new_font == "proxima":
			new_scale = 'scale="103"'
			new_font_name1 = 'Proxima Nova Regular.otf'
			new_font_name2 = 'Proxima Nova Bold.otf'
		elif new_font == "opensans":
			new_scale = 'scale="93"'
			new_font_name1 = 'setrixHD.ttf'
			new_font_name2 = 'OpenSans-Regular.ttf'
			
		old_xml = self.daten + config.plugins.SevenHD.Header.value + ".xml"
		new_xml = self.daten + config.plugins.SevenHD.Header.value + ".xml_new"
		
		fin = open(old_xml)
		fout = open(new_xml, "wt")
		
		for line in fin.readlines():
			if line.find('NotoSans-Regular.ttf')>= 0:
				fout.write( line.replace('NotoSans-Regular.ttf', new_font_name1).replace('scale="95"', new_scale))
			elif line.find('NotoSans-Bold.ttf')>= 0:
				fout.write( line.replace('NotoSans-Bold.ttf', new_font_name2).replace('scale="95"', new_scale))
			elif line.find('HandelGotD.ttf')>= 0:
				fout.write( line.replace('HandelGotD.ttf', new_font_name1).replace('scale="97"', new_scale))
			elif line.find('HandelGotDBol.ttf')>= 0:
				fout.write( line.replace('HandelGotDBol.ttf', new_font_name2).replace('scale="97"', new_scale))
			elif line.find('Proxima Nova Regular.otf')>= 0:
				fout.write( line.replace('Proxima Nova Regular.otf', new_font_name1).replace('scale="103"', new_scale))
			elif line.find('Proxima Nova Bold.otf')>= 0: 
				fout.write( line.replace('Proxima Nova Bold.otf', new_font_name2).replace('scale="103"', new_scale)) 
			elif line.find('setrixHD.ttf')>= 0:
				fout.write( line.replace('setrixHD.ttf', new_font_name1).replace('scale="93"', new_scale))
			elif line.find('OpenSans-Regular.ttf')>= 0: 
				fout.write( line.replace('OpenSans-Regular.ttf', new_font_name2).replace('scale="93"', new_scale))
			else:
				fout.write( line )
		
		fin.close()
		fout.close()
		
		remove(old_xml)
		rename(new_xml, old_xml)
		

	def restartGUI(self, answer):
		if answer is True:
			config.skin.primary_skin.setValue("SevenHD/skin.xml")
			config.skin.save()
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()

#############################################################

def main(session, **kwargs):
	session.open(SevenHD,"/usr/lib/enigma2/python/Plugins/Extensions/SevenHD/images/kravencolors.jpg")

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [PluginDescriptor(name="SevenHD", description=_("Configuration tool for SevenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
	else:
		return [PluginDescriptor(name="SevenHD", description=_("Configuration tool for SevenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]