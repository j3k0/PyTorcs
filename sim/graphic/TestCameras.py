# TestCamera1.cs
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

class TestCameras(object):
	def CreateBlenderTestCamera1(ctx, cameras):
		cam = cameras.Create("BlenderTest1")
		cam.SetFOVy(1.35f)
		cam.SetFrequency(1.0f)
		cam.SetPosition(Math3D.Vector3(-11, 46, -347))
		cam.LookAt(Math3D.Vector3(44, -1, -342))
		return cam

	CreateBlenderTestCamera1 = staticmethod(CreateBlenderTestCamera1)

	def CreateBlenderTestCamera2(ctx, cameras):
		cam = cameras.Create("BlenderTest2")
		cam.SetPosition(Math3D.Vector3(539.7f, 6.92f, -367.48f))
		cam.LookAt(Math3D.Vector3(522.26f, -1.74f, -374.67f))
		cam.SetFOVy(1.05f)
		return cam

	CreateBlenderTestCamera2 = staticmethod(CreateBlenderTestCamera2)
