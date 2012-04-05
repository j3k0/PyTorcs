#from System import *
#from OpenRacing.Core import *
#from OpenRacing.Graphic import *
#from OpenRacing.Audio import *

from OpenRacingConfig import *
from core.RaceManager import *

class ApplicationState:
	RACING = 1
	EXITING = 2
	MAIN_MENU = 3
	CONFIG_MENU = 4

#
# Initialize and launch OpenRacing GUI and races
#
class ApplicationController: # Speed of the simulation relative to real time # Minimal simulation step
	# Exit requested
	# Manager of the race
	def __init__(self):
		self._SimuSpeed = 1.0
		self._SimuStep = 0.03
		self._mExit = False
		self._mExitRace = False
		self._mTimeBeforeExit = -1.0
		self._mRaceManager = None
		self._mGraphicModule = None
		self._mAudioManager = None
		self._mInputManager = None
		self._mConfig = OpenRacingConfig("openracing.xml")
		# self._mInputManager = InputManager()

	def RunRace(self):
		self._mRaceManager = RaceManager()
		self._mRaceManager.Init(self._mConfig.RaceFile, 1, self._mInputManager)
		if self._mGraphicModule != None:
			self._mGraphicModule.InitTrack(self._mRaceManager.Track)
			self._mGraphicModule.InitAvatars(self._mRaceManager.Situation)
		firstStep = True
		start = self._SimuSpeed * (DateTime.Now.Ticks / TimeSpan.TicksPerSecond) # Starting date
		before = 0.0
		Console.Out.WriteLine(" >---------------------<")
		Console.Out.WriteLine(" > Starting Simulation <")
		Console.Out.WriteLine(" >---------------------<")
		self._mExitRace = False
		while not self._mExit and not self._mExitRace: # Loop until RaceManager as been destroyed
			now = self._SimuSpeed * (DateTime.Now.Ticks / TimeSpan.TicksPerSecond) - start
			nnow = before + self._SimuStep
			while nnow < now:
				# if a frame takes more than SimuStep to complete, split the simulation into small.
				# (physics engines do like small delta_t)
				self._mRaceManager.Update(nnow, nnow - before)
				before = nnow
				nnow += self._SimuStep
			if now - before > 0.00000001: # Engine still requires a simulation step > epsilon?
				self._mRaceManager.Update(now, now - before)
			if self._mGraphicModule != None:
				try:
					self._mGraphicModule.Refresh(self._mRaceManager.Situation)
				except GraphicException, ge:
					Console.Out.WriteLine(" Error while refreshing screen: {0}\nMore details:\n{1}", ge, ge.MoreDetails)
					self._mState = ApplicationState.EXITING
					self._mExit = True
				finally:
					pass
			if firstStep:
				# First step takes long because of initializations. Fix the starting time.
				start = self._SimuSpeed * (DateTime.Now.Ticks / TimeSpan.TicksPerSecond) + before - now
				firstStep = False
			before = now
			if (self._mTimeBeforeExit > 0.0) and (now > self._mTimeBeforeExit):
				self._mExitRace = True
				self._mExit = True
				self._mState = ApplicationState.EXITING
		Console.Out.WriteLine(" >-------------------<")
		Console.Out.WriteLine(" > End of Simulation <")
		Console.Out.WriteLine(" >-------------------<")

	# The application main loop
	def Run(self):
		if self._mState == ApplicationState.RACING:
			self.RunRace()
		else:
			while not self._mExit:
				if self._mState == ApplicationState.RACING:
					# Reset all contexts
					self._mGraphicModule.Gui.ShutdownMainMenu()
					self.ShutdownAll()
					self.InitAll()
					# Run the race
					self.RunRace()
					# Reset all contexts (to make sure everything is clean)
					self.ShutdownAll()
					if self._mState != ApplicationState.EXITING:
						self.InitAll()
					if self._mState == ApplicationState.MAIN_MENU:
						self._mGraphicModule.Gui.InitMainMenu()
				elif self._mGraphicModule != None:
					# Just display the GUI
					self._mGraphicModule.Refresh(None)
		self.ShutdownAll()

	# Initialize a full featured application controller
	def Init(self):
		self.InitAll()
		self._mGraphicModule.Gui.InitMainMenu()
		self._mState = ApplicationState.MAIN_MENU
		self._mGraphicModule.Refresh(None)

	# Initialize and launch a race without GUI
	def InitQuickRace(self):
		self.InitAll()
		self._mState = ApplicationState.RACING

	# Initialize and launch a race without GUI and display
	def InitConsoleRace(self):
		self._mTimeBeforeExit = 3.0
		self._mState = ApplicationState.RACING

	# User requested to launch a new race
	def OnStartRace(self):
		self._mState = ApplicationState.RACING

	# Config menu as been requested
	def OnConfig(self):
		self._mState = ApplicationState.CONFIG_MENU
		self._mGraphicModule.Gui.ShutdownMainMenu()
		self._mGraphicModule.Gui.InitConfigMenu()

	# Graphic rendering quality as been changed.
	def OnGraphicQuality(self, quality):
		self._mConfig.GraphicRenderingQuality = quality
		self._mGraphicModule.ChangeQuality(quality)
		Console.Out.WriteLine("CONFIG: Graphic quality changed to {0}.", quality)

	def InitAll(self):
		self._mAudioManager = AlAudioManager()
		self._mAudioManager.Init()
		self._mGraphicModule = OgreRenderer()
		self._mGraphicModule.AudioManager = self._mAudioManager
		self._mGraphicModule.InitView(True, self._mConfig.GraphicRenderingQuality)
		self._mGraphicModule.Gui.SetController(self)
		self._mGraphicModule.Gui.SetInputManager(self._mInputManager)

	def ShutdownAll(self):
		if (self._mState == ApplicationState.RACING) and (self._mGraphicModule != None):
			self._mGraphicModule.ShutdownAvatars()
			self._mGraphicModule.ShutdownTrack()
		if self._mRaceManager != None:
			self._mRaceManager.Shutdown()
			self._mRaceManager = None
		if self._mGraphicModule != None:
			self._mGraphicModule.ShutdownView()
		# mGraphicModule = null;
		if self._mAudioManager != None:
			self._mAudioManager.Shutdown()
			self._mAudioManager = None
		# mState = ApplicationState.EXITING;
		GC.Collect()
		GC.WaitForPendingFinalizers()

	# Exit event as been sent
	def OnExit(self):
		if self._mState == ApplicationState.RACING:
			self._mState = ApplicationState.MAIN_MENU
			self._mExitRace = True
		elif self._mState == ApplicationState.CONFIG_MENU:
			self._mState = ApplicationState.MAIN_MENU
			self._mGraphicModule.Gui.ShutdownConfigMenu()
			self._mGraphicModule.Gui.InitMainMenu()
			self._mConfig.Save()
		else: # Save all config changes.
			self._mExit = True
			self._mState = ApplicationState.EXITING
