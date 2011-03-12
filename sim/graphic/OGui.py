from System import *
from OgreDotNet import *
from MyGUI import *
from OpenRacing.Core import *

class OGui(IGui):
	def __init__(self):
		self._mGuiManager = None
		self._mGui = None
		self._mMainMenu = None
		self._mConfigMenu = None
		self._mHud = None

	def SetController(self, igc):
		self._mController = igc

	def SetInputManager(self, im):
		im.SetGuiManager(self._mGuiManager)

	def Init(self, ctx):
		Console.Out.WriteLine(">>> OGui.Init")
		self._mCtx = ctx
		self._mCtx.RegisterResourcePath("mygui", "General")
		self._mGuiManager = GuiManager()
		self._mGui = self._mGuiManager.InitGUI(self._mCtx.Root, self._mCtx.Win)
		self._mHud = Gui.HUD(self._mCtx)

	def Shutdown(self):
		Console.Out.WriteLine(">>> OGui.Shutdown")
		self.ShutdownConfigMenu()
		self.ShutdownMainMenu()
		self._mHud.Destroy()
		self._mCtx.UnregisterResource("mygui")
		self._mGuiManager.ShutdownGUI()
		self._mGui = None
		self._mHud = None
		self._mCtx = None
		self._mGuiManager = None

	# Main menu
	def InitMainMenu(self):
		Console.Out.WriteLine(">>> OGui.InitMainMenu")
		self._mMainMenu = Gui.MainMenu(self._mGui)
		self._mMainMenu.Init(self._mController)

	def ShutdownMainMenu(self):
		if self._mMainMenu != None:
			Console.Out.WriteLine(">>> OGui.ShutdownMainMenu")
			self._mMainMenu.Shutdown()
			self._mMainMenu = None

	# Config menu
	def InitConfigMenu(self):
		self._mConfigMenu = Gui.ConfigMenu(self._mGui)
		self._mConfigMenu.Init(self._mController)

	def ShutdownConfigMenu(self):
		if self._mConfigMenu != None:
			self._mConfigMenu.Shutdown()
			self._mConfigMenu = None

	def Render(self, t, delta_t):
		# Prepare MyGUI frame
		self._mGui.InjectFrameEntered(delta_t)
		self._mHud.Update()
		# Process MyGUI events
		ev = self._mGuiManager.PollEvents()
		while ev != None:
			if ev.Type == MyGUI.GuiManager.EventType.EXIT:
				self._mController.OnExit()
			ev = self._mGuiManager.PollEvents()

	def ShowHUD(self, avatars, avatarID):
		self._mHud.Create(avatars, avatarID)

	def HideHUD(self):
		self._mHud.Destroy()
