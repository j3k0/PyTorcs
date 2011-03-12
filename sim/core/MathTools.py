# MathTools.cs
#
#  Copyright (C) 2009 Jean-Christophe Hoelt <jeko@ios-software.com>
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

class MathTools(object):
	def __init__(self):
		# <summary>PI</summary>
		self._PI = 3.14159265358979323846
		# <summary>Gravity in m/s/s</summary> 
		self._G = 9.80665f

	# conversions
	def RadsToRpm(x):
		""" <summary>Radian/s to RPM conversion</summary>"""
		return x * 9.549296585

	RadsToRpm = staticmethod(RadsToRpm)

	def RpmToRads(x):
		""" <summary>RPM to Radian/s conversion</summary>        """
		return x * 0.104719755

	RpmToRads = staticmethod(RpmToRads)

	def RadToDeg(x):
		""" <summary>Radian to degree conversion</summary>"""
		return x * (180.0 / self._PI)

	RadToDeg = staticmethod(RadToDeg)

	def DegToRad(x):
		""" <summary>Degree to radian conversion</summary> """
		return x * (self._PI / 180.0)

	DegToRad = staticmethod(DegToRad)

	def FeetToM(x):
		""" <summary>Feet to meter conversion</summary>"""
		return x * 0.304801

	FeetToM = staticmethod(FeetToM)

	def Sign(x):
		""" <summary>Sign of the expression</summary>"""
		return (-1.0 if x < 0 else 1.0)

	Sign = staticmethod(Sign)

	def Normalize_0_2PI(x):
		""" <summary>Angle normalization between 0 and 2 * PI</summary>"""
		while x > 2 * self._PI:
			x -= 2 * self._PI
		while x < 0:
			x += 2 * self._PI
		return x

	Normalize_0_2PI = staticmethod(Normalize_0_2PI)

	def Normalize_PI_PI(x):
		""" <summary>Angle normalization between -PI and PI</summary>"""
		while (x) > self._PI:
			(x) -= 2 * self._PI
		while (x) < -self._PI:
			(x) += 2 * self._PI
		return x

	Normalize_PI_PI = staticmethod(Normalize_PI_PI)
