#  Contributed by FromHell555
#  CC BY-NC-SA

from Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eDVBVolumecontrol, eTimer

class SevenHDVVolumeText(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.vol_timer = eTimer()
		self.vol_timer.callback.append(self.poll)
	GUI_WIDGET = eLabel

	def poll(self):
		self.changed(None)

	def onHide(self):
		self.suspended = True
		self.vol_timer.stop()
		
	def onShow(self):
		self.suspended = False
		self.vol_timer.start(200)

	def changed(self, what):
		if not self.suspended:
			self.text = str(eDVBVolumecontrol.getInstance().getVolume())
