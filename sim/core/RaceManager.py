# RaceEngine.cs
#
#  Copyright (C) 2008 Jean-Christophe Hoelt <jeko@ios-software.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#
#

#from System import *
from swigtorcs.TorcsItf import *
#from System.Collections.Generic import *
#from OpenRacing.Ode import *
#from OpenRacing.Core.Track import *

class RaceManager(object): # Prevents objects from being freed
	@staticmethod
	def Reset():
		# self._Pool.Clear()
		pass

	# All loaded modules: references are kept to prevent garbage collection # Universal Track Interface
	def get_Track(self):
		return self._mUTrack

	Track = property(fget=get_Track)

	def __init__(self):
		# self._Pool = List[Object]()
		self._mGfParm = None
		self._mSituation = tSituation()
		self._mRobots = None
		self._mCars = None
		self._mSimulator = None
		self._mRobotModule = None
		self._mUTrack = None

	def Init(self, raceFile, numBots, inputManager):
		self._mNumBots = numBots
		self._mGfParm = tGfParm()
                self._mGfParm.ReadFile(raceFile, tGfParm.RMode_STD)
		self._mSituation.RaceInfo.State = TorcsItf.RM_RACE_PRESTART
		self._mRaceName = self._mGfParm.GetStr("Header", "name", None)
		self._mSituation.RaceInfo.CarsCount = 0
		self._mSituation.DeltaTime = 0.1
		self._mSituation.CurrentTime = 0.0
		self._mSituation.PlayersCount = 0
		self.InitTrack()
		self.InitSimu()
		self.InitRobots(inputManager)
		self.LinkAll()

	def InitSimu(self):
		# SimuModule simuModule = new SimuModule();
		# simuModule.Init(mNumBots, mTrackModule.Track);
		simuModule = OdeSimulator()
		simuModule.Init(self._mNumBots, self.Track)
		self._mSimulator = simuModule

	def InitTrack(self):
		self._mUTrack = Track.AlphaUTI()
		self._mUTrack.Init()

	def InitRobots(self, inputManager):
		#mRobotModule = new LegacyRobotModule();
		self._mRobotModule = Sharpy.SharpyModule()
		#mRobotModule = new Human.HumanModule(inputManager);
		self._mRobots = Array.CreateInstance(IRobot, self._mNumBots)
		i = 0
		while i < self._mRobots.Length:
			self._mRobots[i] = self._mRobotModule.InitRobot(i)
			i += 1
		self._mCars = Array.CreateInstance(tCarElt, self._mRobots.Length)

	def GetTrackFile(self):
		# int curTrkIdx = 1;
		buf = "Tracks/1"
		trackName = self._mGfParm.GetStr(buf, "name", None)
		if trackName == None:
			return None
		catName = self._mGfParm.GetStr(buf, "category", None)
		if catName == None:
			return None
		return "tracks/" + catName + "/" + trackName + "/" + trackName + ".xml"

	def get_Situation(self):
		return self._mSituation

	Situation = property(fget=get_Situation)

	def LinkAll(self):
		Console.Out.WriteLine(" >-----------------<")
		Console.Out.WriteLine(" > Initialize Cars <")
		Console.Out.WriteLine(" >-----------------<")
		self.LinkRobotCars()
		Console.Out.WriteLine(" >--------------------------<")
		Console.Out.WriteLine(" > Initialize the Situation <")
		Console.Out.WriteLine(" >--------------------------<")
		i = 0
		while i < self._mCars.Length:
			car = self._mCars[i]
			self._mSituation.AddCar(car)
			car.Race.RemainingLaps = 1
			i += 1
		Console.Out.WriteLine(" >--------------------<")
		Console.Out.WriteLine(" > Init Starting Grid <")
		Console.Out.WriteLine(" >--------------------<")
		self.InitStartingGrid()
		Console.Out.WriteLine(" >----------------------------<")
		Console.Out.WriteLine(" > Register Cars To Simulator <")
		Console.Out.WriteLine(" >----------------------------<")
		i = 0
		while i < self._mCars.Length:
			self._mSimulator.Config(self._mCars[i])
			i += 1

	def LinkRobotCars(self):
		i = 0
		while i < self._mRobots.Length:
			car = tCarElt()
			# Initialize Car
			car.Index = self._mRobots[i].Index
			car.Priv.ParamsHandle = self._mRobots[i].RobParm.Handle
			car.Priv.DriverIndex = self._mRobots[i].Index
			car.Info.Name = self._mRobots[i].Name
			car.Info.TeamName = self._mRobots[i].Team
			car.Info.CarName = self._mRobots[i].CarName
			car.Info.RaceNumber = self._mRobots[i].RaceNumber
			if self._mRobots[i].Type == "robot":
				car.Info.DriverType = TorcsItf.RM_DRV_ROBOT
			else:
				car.Info.DriverType = TorcsItf.RM_DRV_HUMAN
			car.Info.SkillLevel = 0
			car.Info.StartRank = car.Index
			car.Race.Position = car.Index + 1
			car.Race.RemainingLaps = 0
			self._mCars[i] = car
			self._mRobots[i].SetCar(car)
			i += 1
		i = 0
		while i < self._mRobots.Length:
			self._mRobots[i].NewTrack(self.Track, self._mSituation)
			carHandle = CarManager.ReadSpecification(self._mCars[i])
			if self._mRobots[i].CarParm.Handle != None:
				self._mRobots[i].CarParm.Handle = tGfParm.MergeHandles(carHandle.Handle, self._mRobots[i].CarParm.Handle, TorcsItf.GFPARM_MMODE_SRC | TorcsItf.GFPARM_MMODE_DST | TorcsItf.GFPARM_MMODE_RELSRC | TorcsItf.GFPARM_MMODE_RELDST)
				self._mCars[i].Priv.CarHandle = self._mRobots[i].CarParm.Handle
			else:
				# Pool.Add(mRobots[i].CarParm.Handle);
				raise InvalidConfigurationException("Bad Car parameters for driver " + self._mCars[i].Info.Name)
			i += 1

	def InitStartingGrid(self):
		""" <summary>
		 Place the cars on the starting grid.
		 </summary>
		 <remarks>Requires Track, Cars and Simulator registered</remarks>
		"""
		i = 0
		while i < self._mSituation.RaceInfo.CarsCount:
			car = self._mSituation.Cars[i]
			car.Speed.X = 0
			sPos = self._mUTrack.LogicalScene.GetStartingPosition(0)
			car.Position.Yaw = 0 # TODO: get this from sPos.Orientation
			car.Position.X = sPos.Position.x
			car.Position.Y = sPos.Position.y
			car.Position.Z = sPos.Position.z
			car.Position.Yaw = MathTools.Normalize_0_2PI(car.Position.Yaw)
			i += 1

	def Update(self, now, delta):
		self._mSituation.CurrentTime = now
		self._mSituation.DeltaTime = delta
		if self._mSituation.RaceInfo.State == TorcsItf.RM_RACE_PRESTART:
			i = 0
			while i < self._mRobots.Length:
				self._mRobots[i].NewRace(self._mSituation)
				i += 1
		elif self._mSituation.RaceInfo.State == TorcsItf.RM_RACE_RUNNING:
			i = 0
			while i < self._mRobots.Length:
				self._mRobots[i].Drive(self._mSituation)
				i += 1
		self._mSimulator.Update(self._mSituation)
		if self._mSituation.RaceInfo.State == TorcsItf.RM_RACE_PRESTART:
			self._mSituation.RaceInfo.State = TorcsItf.RM_RACE_STARTING
		elif self._mSituation.RaceInfo.State == TorcsItf.RM_RACE_STARTING:
			self._mSituation.RaceInfo.State = TorcsItf.RM_RACE_RUNNING

	def Shutdown(self):
		i = 0
		while i < self._mRobots.Length:
			self._mRobots[i].Shutdown()
			i += 1
		self._mSimulator.Shutdown()
		self._mSimulator = None
		self._mUTrack.Shutdown()
		self._mUTrack = None
		self._mCars = None
