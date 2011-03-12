from System import *
from OgreDotNet import *
from MyGUI import *
from OpenRacing.Core import *

class MainMenu(object):
	def __init__(self, gui):
		self._mGui = None
		self._mBack = None
		self._mExit = None
		self._mConfig = None
		self._mStartRace = None
		self._mMainMenu = False
		self._mGui = gui

	class ExitEvent(GuiDelegate):
		def __init__(self, gui):
			self._mGuiController = gui

		def OnMouseButtonClick(self, w):
			self._mGuiController.OnExit()

	class StartRaceEvent(GuiDelegate):
		def __init__(self, gui):
			self._mGuiController = gui

		def OnMouseButtonClick(self, w):
			self._mGuiController.OnStartRace()

	class ConfigEvent(GuiDelegate):
		def __init__(self, gui):
			self._mGuiController = gui

		def OnMouseButtonClick(self, w):
			self._mGuiController.OnConfig()

	def Init(self, guiController):
		if mMainMenu == True:
			mBack.show()
			mStartRace.show()
			mExit.show()
			mConfig.show()
		else:
			w = mGui.getViewWidth()
			h = mGui.getViewHeight()
			mBack = mGui.CreateStaticImage("StaticImage", 0, 0, w, h, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Back")
			mBack.setImageTexture("openracing-background.jpg")
			bw = w / 2
			bh = w / 20
			mStartRace = mGui.CreateButton("Button", (w - bw) / 2, 5 * h / 7, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mConfig = mGui.CreateButton("Button", (w - bw) / 2, 5 * h / 7 + bh * 4 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mExit = mGui.CreateButton("Button", (w - bw) / 2, 5 * h / 7 + bh * 8 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mStartRace.setCaption("Start Race")
			mStartRaceEvent = StartRaceEvent(guiController)
			mStartRace.SetGuiDelegate(mStartRaceEvent)
			mConfig.setCaption("Config")
			mConfigEvent = ConfigEvent(guiController)
			mConfig.SetGuiDelegate(mConfigEvent)
			mExit.setCaption("Exit")
			mExitEvent = ExitEvent(guiController)
			mExit.SetGuiDelegate(mExitEvent)
			mBack.show()
			mStartRace.show()
			mExit.show()
			mConfig.show()
			mMainMenu = True

	def Shutdown(self):
		mBack.hide()
		mStartRace.hide()
		mConfig.hide()
		mExit.hide()
		mStartRaceEvent = None
		mConfigEvent = None
		mExitEvent = None
		mMainMenu = False
