# SimuModule.cs
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

class SimuModule(object):
	def Config(self, car):
		""" <summary>Adds and configure a car for the simulation</summary>"""
		TorcsItf.SimConfig(car)

	def Init(self, nbcars):
		""" <summary>Initialize the simulation</summary>"""
		# Try to load module information for information purpose.
		modInfo = tModInfo()
		TorcsItf.simuv2(modInfo)
		# Load simuv2 interface
		self._mcSimItf = tSimItf()
		TorcsItf.simuv2Init(self._mcSimItf)
		# Initialize simulation module
		TorcsItf.SimInit(nbcars)

	def Update(self, situ):
		""" <summary>Update car locations</summary>"""
		TorcsItf.SimUpdate(situ, situ.DeltaTime, -1)

	def Shutdown(self):
		TorcsItf.SimShutdown()

	def __init__(self):
