class IGui(object):
	def SetInputManager(self, im):
		pass

	def SetController(self, igc):
		pass

	def InitMainMenu(self):
		pass

	def ShutdownMainMenu(self):
		pass

	def InitConfigMenu(self):
		pass

	def ShutdownConfigMenu(self):
		pass

class IGuiController(object):
	def OnStartRace(self):
		pass

	def OnExit(self):
		pass

	# Configuration changes
	def OnConfig(self):
		pass

	def OnGraphicQuality(self, quality):
		pass
