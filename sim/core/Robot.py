# Robot.cs
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
from System import *
from SwigTorcs import *
from OpenRacing.Core.Track import *

class IRobot(object):
	# <value>Robot index</value>
	def get_Index(self):

	Index = property(fget=get_Index)

	def SetCar(self, car):
		""" <summary>Car driven by the robot</summary>"""
		pass

	# <value>Robot parameters file</value>
	def get_RobParm(self):

	RobParm = property(fget=get_RobParm)

	# <value>Car parameters file</value>
	def get_CarParm(self):

	CarParm = property(fget=get_CarParm)

	def NewTrack(self, track, situ):
		""" <summary>Prepare for new track</summary>"""
		pass

	def NewRace(self, situ):
		""" <summary>Prepare for new race</summary>"""
		pass

	def Drive(self, situ):
		""" <summary>Update own car's controllers</summary>"""
		pass

	def Shutdown(self):
		""" <summary>Clear initialized stuffs</summary>"""
		pass

	# <value>Name of the driver</value>
	def get_Name(self):

	Name = property(fget=get_Name)

	# <value>Name of the team</value>
	def get_Team(self):

	Team = property(fget=get_Team)

	# <value>Name of the driven car</value>
	def get_CarName(self):

	CarName = property(fget=get_CarName)

	# <value>Number of the race (XXX: used to be initialized in torcs' racemanager, but what is it?)</value>
	def get_RaceNumber(self):

	RaceNumber = property(fget=get_RaceNumber)

	# <value>Either "robot" or "human"</value>
	def get_Type(self):

	Type = property(fget=get_Type)
