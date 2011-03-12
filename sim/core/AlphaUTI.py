from System import *
from System.IO import *
from OpenRacing.Core import *

class AlphaLogicalScene(LogicalScene):
	def NumStartingPositions(self):
		return 1

	def GetStartingPosition(self, i):
		s = StartingPosition()
		s.Position = Math3D.Vector3(0.0f, 0.0f, 1.5f)
		s.Orientation = Math3D.Quaternion.FromAngleAxis(0.0f, Math3D.Vector3(0, 1, 0))
		return s

class AlphaUTI(UTI):
	def get_LogicalScene(self):
		return self._mLogicalScene

	LogicalScene = property(fget=get_LogicalScene)

	def get_VisualScene(self):
		return None

	VisualScene = property(fget=get_VisualScene)

	def get_PhysicalScene(self):
		return None

	PhysicalScene = property(fget=get_PhysicalScene)

	def __init__(self):
		self._mLogicalScene = AlphaLogicalScene()

	def GetDirectoryName(self):
		return "tracks/road/street-1"

	def GetFullPath(self, fileName):
		return self.GetDirectoryName() + Path.DirectorySeparatorChar + fileName

	def Init(self):
		pass

	def Shutdown(self):
		pass
