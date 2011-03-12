from System import *
from OgreDotNet import *
from OpenRacing.Core import *

class ConfigMenu(object):
	def __init__(self, gui):
		self._mGui = None
		self._mBack = None
		self._mGraphic = None
		self._mSystem = None
		self._mExit = None
		self._mHighQuality = None
		self._mMediumQuality = None
		self._mLowQuality = None
		self._mConfigMenu = False
		self._mGui = gui

	class ExitEvent(MyGUI.GuiDelegate):
		def __init__(self, gui):
			self._mGuiController = gui

		def OnMouseButtonClick(self, w):
			self._mGuiController.OnExit()

	class QualityEvent(MyGUI.GuiDelegate):
		def __init__(self, configMenu, quality):
			self._mConfigMenu = configMenu
			self._mQuality = quality

		def OnMouseButtonClick(self, w):
			self._mConfigMenu.Init(None)
			self._mConfigMenu.mGuiController.OnGraphicQuality(self._mQuality)

	class GraphicEvent(MyGUI.GuiDelegate):
		def __init__(self, configMenu):
			self._mConfigMenu = configMenu

		def OnMouseButtonClick(self, w):
			self._mConfigMenu.Init(None)
			self._mConfigMenu.mHighQuality.show()
			self._mConfigMenu.mMediumQuality.show()
			self._mConfigMenu.mLowQuality.show()

	def Init(self, guiController):
		if not self._mConfigMenu:
			mGuiController = guiController
			w = mGui.getViewWidth()
			h = mGui.getViewHeight()
			mBack = mGui.CreateStaticImage("StaticImage", 0, 0, w, h, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Back")
			mBack.setImageTexture("openracing-background.jpg") # TODO: share with main menu
			bw = w / 4
			bh = w / 20
			mGraphic = mGui.CreateButton("Button", 1 * (w - bw) / 4, 5 * h / 7 + bh * 0 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mSystem = mGui.CreateButton("Button", 1 * (w - bw) / 4, 5 * h / 7 + bh * 4 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mExit = mGui.CreateButton("Button", 1 * (w - bw) / 4, 5 * h / 7 + bh * 8 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mHighQuality = mGui.CreateButton("Button", 3 * (w - bw) / 4, 5 * h / 7 + bh * 0 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mMediumQuality = mGui.CreateButton("Button", 3 * (w - bw) / 4, 5 * h / 7 + bh * 4 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mLowQuality = mGui.CreateButton("Button", 3 * (w - bw) / 4, 5 * h / 7 + bh * 8 / 3, bw, bh, MyGUI.ALIGN_INFO.ALIGN_DEFAULT, "Main")
			mGraphic.setCaption("Graphic")
			mGraphicEvent = GraphicEvent(self)
			mGraphic.SetGuiDelegate(mGraphicEvent)
			mSystem.setCaption("System")
			# mSystemEvent = new SystemEvent(guiController);
			# mSystem.SetGuiDelegate(mSystemEvent);
			mExit.setCaption("Back")
			mExitEvent = ExitEvent(guiController)
			mExit.SetGuiDelegate(mExitEvent)
			mHighQuality.setCaption("High Quality")
			mHighQualityEvent = QualityEvent(self, GraphicRenderingQuality.High)
			mHighQuality.SetGuiDelegate(mHighQualityEvent)
			mMediumQuality.setCaption("Medium Quality")
			mMediumQualityEvent = QualityEvent(self, GraphicRenderingQuality.Medium)
			mMediumQuality.SetGuiDelegate(mMediumQualityEvent)
			mLowQuality.setCaption("Low Quality")
			mLowQualityEvent = QualityEvent(self, GraphicRenderingQuality.Low)
			mLowQuality.SetGuiDelegate(mLowQualityEvent)
			mGraphic.show()
			mSystem.show()
			mExit.show()
			self._mConfigMenu = True
		mGraphic.show()
		mSystem.show()
		mExit.show()
		mHighQuality.hide()
		mMediumQuality.hide()
		mLowQuality.hide()

	def Shutdown(self):
		mBack.hide()
		mGraphic.hide()
		mSystem.hide()
		mExit.hide()
		mHighQuality.hide()
		mMediumQuality.hide()
		mLowQuality.hide()
