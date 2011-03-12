from System import *
from SwigTorcs import *
from OpenRacing.Core import *

class HumanModule(IRobotModule):
	def __init__(self, inputManager):
		# Initialize whatever data is shared by all driving robots
		self._mInputManager = inputManager

	def get_RobotsCount(self):
		# For now, Human only provides 1 robot
		return 1

	RobotsCount = property(fget=get_RobotsCount)

	def InitRobot(self, index):
		return HumanRobot(self._mInputManager)
