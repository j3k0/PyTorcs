from System import *
from SwigTorcs import *
from OpenRacing.Core import *
from OpenRacing.Core.Track import *

class HumanRobot(IRobot, InputListener):
	# Keys/Button allocations
	#  # Driven car # Robot parameter (useles for human, but required by simulator) # Input handling system
	# Commands
	def __init__(self, inputManager):
		self._ACCELERATOR_KEY = KeyCode.KC_UP
		self._BRAKE_KEY = KeyCode.KC_DOWN
		self._STEER_LEFT_KEY = KeyCode.KC_LEFT
		self._STEER_RIGHT_KEY = KeyCode.KC_RIGHT
		self._GEAR_DOWN_KEY = KeyCode.KC_C
		self._GEAR_UP_KEY = KeyCode.KC_D
		self._ACCELERATOR_BUTTON = 0
		self._BRAKE_BUTTON = 1
		self._STEER_AXIS = 0
		self._THROTTLE_AXIS = 1
		self._GEAR_DOWN_BUTTON = 4
		self._GEAR_UP_BUTTON = 5
		self._mCar = None
		self._mRobParm = None
		self._AcceleratorCommand = 0.0f
		self._BrakeCommand = 0.0f
		self._SteerCommand = 0.0f
		self._GearCommand = 1
		# Load parameter file
		self._mRobParm = tGfParm("drivers/sharpy/default.xml", tGfParm.RMode.STD)
		self._mInputManager = inputManager
		self._mInputManager.AddListener(self)

	def OnKeyPressed(self, key):
		if key == self._ACCELERATOR_KEY:
			self._AcceleratorCommand += 1.0f
			self._BrakeCommand -= 1.0f
		if key == self._BRAKE_KEY:
			self._AcceleratorCommand -= 1.0f
			self._BrakeCommand += 1.0f
		if key == self._STEER_RIGHT_KEY:
			self._SteerCommand -= 0.2f
		if key == self._STEER_LEFT_KEY:
			self._SteerCommand += 0.2f
		if key == self._GEAR_UP_KEY:
			#TODO: Find the max gear for a car
			if self._GearCommand < 5:
				self._GearCommand += 1
		if key == self._GEAR_DOWN_KEY:
			if self._GearCommand > -1:
				self._GearCommand -= 1

	def OnKeyReleased(self, key):
		if key == self._ACCELERATOR_KEY:
			self._AcceleratorCommand -= 1.0f
			self._BrakeCommand += 1.0f
		if key == self._BRAKE_KEY:
			self._AcceleratorCommand += 1.0f
			self._BrakeCommand -= 1.0f
		if key == self._STEER_RIGHT_KEY:
			self._SteerCommand += 0.2f
		if key == self._STEER_LEFT_KEY:
			self._SteerCommand -= 0.2f

	def OnButtonPressed(self, button):
		# Console.Out.WriteLine("button {0}", button);
		if button == self._ACCELERATOR_BUTTON:
			self._AcceleratorCommand += 1.0f
			self._BrakeCommand -= 1.0f
		if button == self._BRAKE_BUTTON:
			self._AcceleratorCommand -= 1.0f
			self._BrakeCommand += 1.0f
		if button == self._GEAR_UP_BUTTON:
			#TODO: Find the max gear for a car
			if self._GearCommand < 5:
				self._GearCommand += 1
		if button == self._GEAR_DOWN_BUTTON:
			if self._GearCommand > -1:
				self._GearCommand -= 1

	def OnButtonReleased(self, button):
		if button == self._ACCELERATOR_BUTTON:
			self._AcceleratorCommand -= 1.0f
			self._BrakeCommand += 1.0f
		if button == self._BRAKE_BUTTON:
			self._AcceleratorCommand += 1.0f
			self._BrakeCommand -= 1.0f

	def OnAxisMoved(self, axisID, val):
		# Console.Out.WriteLine("axisID {0} val {1}", axisID, val);
		if axisID == self._STEER_AXIS:
			self._SteerCommand = -val
		elif axisID == self._THROTTLE_AXIS:
			#TODO should watch out if throttle, brake and clutch are on different axis!
			if val > 0: # brake	
				self._BrakeCommand = val
			elif val < 0: # accelerate
				self._AcceleratorCommand = -val

	def get_Index(self):
		return 0

	Index = property(fget=get_Index)
 # Only 1 robot so index is always 0
	def SetCar(self, car):
		self._mCar = car
 # Driven car
	def get_RobParm(self):
		return self._mRobParm

	RobParm = property(fget=get_RobParm)
 # RobParm and
	def get_CarParm(self):
		return self._mRobParm

	CarParm = property(fget=get_CarParm)
 # CarParm can be the same file.
	def NewTrack(self, track, situ):
		pass

	def NewRace(self, situ):
		pass

	def Drive(self, situ):
		# Drive !
		self._mCar.Ctrl.BrakeCommand = self._BrakeCommand
		self._mCar.Ctrl.AcceleratorCommand = self._AcceleratorCommand
		self._mCar.Ctrl.SteerCommand = self._SteerCommand
		self._mCar.Ctrl.Gear = self._GearCommand
		self._mCar.Ctrl.RaceCommand = 0
		self._mCar.Ctrl.ClutchCommand = 1.0f - self._mCar.Priv.EngineRpm / 500.0f
		if self._mCar.Ctrl.ClutchCommand < 0.0f:
			self._mCar.Ctrl.ClutchCommand = 0.0f

	def Shutdown(self):
		self._mInputManager.RemoveListener(self)

	def get_Name(self):
		return "human"

	Name = property(fget=get_Name)

	def get_Team(self):
		return "human"

	Team = property(fget=get_Team)

	def get_CarName(self):
		return "p406"

	CarName = property(fget=get_CarName)

	def get_RaceNumber(self):
		return 0

	RaceNumber = property(fget=get_RaceNumber)

	def get_Type(self):
		return "robot"

	Type = property(fget=get_Type)
