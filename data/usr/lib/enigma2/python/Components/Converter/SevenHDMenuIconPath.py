#
#  Menu Icon Path Converter
#
#  Coded by tomele for Kraven Skins
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll

class SevenHDMenuIconPath(Poll,Converter,object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 1000
		self.poll_enabled = True
		self.logo = "/usr/share/enigma2/SevenHD/menu-icons/logo.png"
		self.path = "/usr/share/enigma2/SevenHD/menu-icons/"
		self.userpath = "/usr/share/enigma2/Seven-user-icons/"
		self.type = str(type)
		
		self.names=[
		########ATV########
		##menu_mainmenu##
		("vmc_init_startvmc","menu_mainmenu_vmc.png"),
		("Infopanel","menu_mainmenu_infopanel.pn"),
		("OpenStore","menu_mainmenu_openstore.png"),
		("timer_menu","menu_mainmenu_timer.png"),
		("scart_switch","menu_mainmenu_scart.png"),
		("info_screen","info.png"),
		("plugin_selection","menu_mainmenu_pluginmanager.png"),
		("setup_selection","setup.png"),
		("standby_restart_list","menu_mainmenu_shutdown.png"),
		("pvmc_mainmenu","pvmc.png"),
		("dmc_mainmenu","menu_mainmenu_dmc_mainmenu.png"),
		("googlemaps","google.png"),
		("media_player","media.png"),
		("dvd_player","dvd.png"),
		("subtitle_selection","sub.png"),
		("filecommand","filecom.png"),
		("multi_quick","remotecontrol.png"),
		("dreamplex","plex.png"),
		("merlin_music_player","music.png"),
		("moviebrowser","service_info.png"),
		("run_kodi","menu_kodi.png"),
		("start_kodi","menu_kodi.png"),
		("webradioFS","webradioFS.png"),
		##menu_information##
		("supportchannel_YTChannel","menu_information_supportchannel.png"),
		("about_screen","menu_information_about.png"),
		("device_screen","menu_information_device.png"),
		("service_info_screen","info.png"),
		##menu_timermenu##
		("autotimer_setup","menu_timermenu_autotimers.png"),
		("crontimer_edit","menu_timermenu_crontimers.png"),
		("timer_edit","menu_timermenu_timers.png"),
		("powertimer_edit","menu_timermenu_powertimers.png"),
		##menu_setup##
		("video_menu","service_info.png"),
		("audio_menu","menu_setup_audio.png"),
		("rec_setup","menu_extended_recording_setup.png"),
		("system_selection","menu_setup_setup.png"),
		("epg_menu","menu_epg_epg_setup.png"),
		("service_searching_selection","menu_setup_tuner.png"),
		("cam_setup","menu_setup_ci.png"),
		("parental_setup","menu_setup_parental.png"),
		("software_manager","menu_setup_software_manager.png"),
		("vmc_init_setup","menu_setup_vmc_setup.png"),
		("extended_selection","menu_system_extended_selection.png"),
		##menu_video_menu##
		("video_setup","service_info.png"),
		("videoenhancement_setup","menu_system_videoenhancement_setup.png"),
		("video_finetune","menu_system_videofinetune_setup.png"),
		("video_clipping","service_info.png"),
		##menu_audio_menu##
		("audio_setup","menu_setup_audio.png"),
		("Volume_Adjust","menu_system_AutomaticVolumeAdjustment.png"),
		("subtitle_setup","menu_extended_subtitle_setup.png"),
		("autolanguage_setup","menu_system_autolanguage_setup.png"),
		##menu_rec##
		("timshift_setup","menu_extended_timshift_setup.png"),
		("recording_setup","menu_extended_recording_setup.png"),
		##menu_cam##
		("ci_setup","menu_setup_ci.png"),
		##menu_system##
		("user_interface","menu_osd_menu_user_interface.png"),
		("remote_setup","menu_system_remote_setup.png"),
		("channelselection_setup","menu_system_channelselection_setup.png"),
		("usage_setup","menu_system_usage_setup.png"),
		("specialfeatures_menu","menu_extended_specialfeatures_menu.png"),
		("skin_setup","menu_osd_menu_skin_setup.png"),
		("display_selection","menu_extended_display_selection.png"),
		("buttonsetup_setup","menu_osd_menu_buttonsetup.png"),
		("RCU Select","remotecontrol.png"),
		("osd_setup","menu_extended_osd_setup.png"),
		("LED_Giga","menu_display_LED_Giga.png"),
		("numzapext_setup","menu_numzapext_setup.png"),
		("vfd_ew","menu_system_VFD_INI.png"),
		("language_setup","menu_system_language_setup.png"),
		("dvdplayer_setup","menu_extended_dvdplayer_setup.png"),
		("av_setup","menu_system_av_setup.png"),
		("autores_setup","menu_system_autores_setup.png"),
		("pluginhider_setup","menu_mainmenu_pluginhider.png"),
		("vps","menu_scan_streamconvert.png"),
		("remotecontrolcode","remotecontrol.png"),
		("ledManager","led.png"),
		("tempfancontrol","fan.png"),
		##menu_extended##
		("hardisk_selection","menu_extended_hardisk_selection.png"),
		("network_menu","menu_system_network_menu.png"),
		("hdmicec","menu_extended_hdmicec.png"),
		("time_setup","menu_extended_time_setup.png"),
		("logs_setup","menu_extended_logs_setup.png"),
		("fansetup_config","fan.png"),
		("factory_reset","menu_setup_reset.png"),
		("tempfancontrol","fan.png"),
		("rfmod_setup","menu_extended_rfmod_setup.png"),
		("remotecode","menu_extended_remotecode.png"),
		##menu_display##
		("display_setup","menu_display_display_setup.png"),
		("lcd_skin_setup","menu_display_lcd_skin_setup.png"),
		("lcd4linux","menu_display_lcd_skin_setup.png"),
		("VFD_INI","menu_system_VFD_INI.png"),
		##menu_osd_menu##
		("osdsetup","menu_osd_menu_osdsetup.png"),
		("input_device_setup","menu_extended_input_device_setup.png"),
		("keyboard","menu_extended_keyboard.png"),
		("osd3dsetup","menu_osd_menu_osd3dsetup.png"),
		("animation_setup","usage_setup.png"),
		##menu_harddisk##
		("harddisk_setup","menu_harddisk_harddisk_setup.png"),
		("harddisk_init","menu_harddisk_harddisk_init.png"),
		("harddisk_check","menu_harddisk_harddisk_check.png"),
		("harddisk_convert","menu_harddisk_harddisk_convert.png"),
		##menu_epg##
		("epgrefresh","menu_epg_refresh.png"),
		("epg_setup","menu_epg_epg_setup.png"),
		("epgloadsave_menu","menu_epg_epgloadsave_menu.png"),
		("setup_epgmulti","menu_epg_setup_epgmulti.png"),
		("setup_epgenhanced","menu_epg_setup_epgenhanced.png"),
		("setup_epginfobar","menu_epg_setup_epginfobar.png"),
		("setup_epginfobargraphical","menu_epg_setup_epginfobargraphical.png"),
		("setup_epggraphical","menu_epg_setup_epggraphical.png"),
		##menu_epgloadsave_menu##
		("saveepgcache","menu_epgloadsave_menu_saveepgcache.png"),
		("loadepgcache","menu_epgloadsave_menu_loadepgcache.png"),
		##menu_network##
		("device_setup","menu_network_device_setup.png"),
		("netmounts_setup","menu_network_netmounts_setup.png"),
		("netafp_setup","menu_network_netafp_setup.png"),
		("netftp_setup","menu_network_netftp_setup.png"),
		("Inadyn_setup","menu_network_Inadyn_setup.png"),
		("minidlna_setup","menu_network_minidlna_setup.png"),
		("netnfs_setup","menu_network_netnfs_setup.png"),
		("openwebif","menu_network_webif.png"),
		("netvpn_setup","menu_network_netvpn_setup.png"),
		("netsabnzbd_setup","menu_network_netsabnzbd_setup.png"),
		("netsmba_setup","menu_network_netsmba_setup.png"),
		("nettelnet_setup","menu_network_nettelnet_setup.png"),
		("netushare_setup","menu_network_netushare_setup.png"),
		("netrts_setup","menu_network_netnfs_setup.png"),
		##menu_scan##
		("tuner_setup","menu_scan_tuner_setup.png"),
		("auto_scan","menu_scan_auto_scan.png"),
		("manual_scan","menu_scan_manual_scan.png"),
		("satfinder","menu_scan_satfinder.png"),
		("positioner_setup","menu_scan_positioner_setup.png"),
		("autobouquetsmakermaker","menu_scan_autobouquetsmakermaker.png"),
		("blindscan","menu_scan_blindscan.png"),
		("sat_ip_client","menu_scan_satip.png"),
		("streamconvert","menu_scan_streamconvert.png"),
		("fastscan","menu_scan_fast_scan.png"),
		("sundtek_control_enter","pluginmanager.png"),
		("cablescan","search.png"),
		("cablescan","scan-c.png"),
		("ipbox_client_Start","menu_scan_streamconvert.png"),
		##menu_shutdown##
		("deep_standby","shutdown.png"),
		("restart","restart.png"),
		("restart_enigma","restart_enigma.png"),
		("Hardreset","restart.png"),
		("standby","power.png"),
		("sleep","shutdowntimer.png"),
		("powertimer_edit","menu_timermenu_powertimers.png")
		]
	
	@cached
	def getText(self):
		try: # is it a menu? then we handle it according to current selection
			cur = self.source.current
			if cur and len(cur) > 2:
				selection = cur[2]
				if selection in ("skin_selector","atilehd_setup"):
					return self.logo
				name = self.userpath+selection.lower()+".png"
				if fileExists(name):
					return name
				name = self.path+selection.lower()+".png"
				if fileExists(name):
					return name
				name=""
				for pair in self.names:
					if pair[0] == selection:
						break
				name=self.userpath+pair[1]
				if name != "" and fileExists(name):
					return name
				name=self.path+pair[1]
				if name != "" and fileExists(name):
					return name
		except:
			try: # is it a screen? then we handle it according to title
				text=self.source.text
				if text in ("zapHistory","Senderhistorie"):
					return self.logo
			except:
				pass
		name=self.userpath+"menu_mainmenu_pluginmanager.png"
		if fileExists(name):
			return name
		name=self.path+"menu_mainmenu_pluginmanager.png"
		if fileExists(name):
			return name
		return self.logo
	
	text = property(getText)
