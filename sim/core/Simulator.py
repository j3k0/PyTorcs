# Simu.cs
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

class Simulator(object):
	def Config(self, car):
		""" <summary>Adds and configure a car for the simulation</summary>"""
		pass

	def Init(self, nbcars, track):
		""" <summary>Initialize the simulation</summary>"""
		pass

	def Update(self, situ):
		""" <summary>Update car locations</summary>"""
		pass

	def Shutdown(self):
		pass
