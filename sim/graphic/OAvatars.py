# OAvatars.cs
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
from OgreDotNet import *
from Math3D import *
from System.IO import *
from SwigTorcs import *

class OAvatars(object):
	""" <summary>
	 Load and display avatars.
	 </summary>
	"""
	def __init__(self, ctx, scene, situ):
		""" <summary>
		 Initialize the list of avatar according to current situation.
		 </summary>
		 <param name="sceneMgr">
		 The <see cref="SceneManager"/>
		 </param>
		 <param name="situ">
		 A <see cref="Situation"/>
		 </param>
		"""
		self._mSpeeds = None
		self._mEngineRPMs = None
		self._mCtx = ctx
		self._mScene = scene
		self._mNode = Array.CreateInstance(SceneNode, situ.RaceInfo.CarsCount)
		self._mEntity = Array.CreateInstance(Entity, situ.RaceInfo.CarsCount)
		self._mSituation = situ

	def Init(self):
		i = 0
		while i < self._mEntity.Length:
			name = self._mSituation.Cars[i].Info.CarName
			dname = "cars/" + name + "/"
			zipname = dname + "ogre-model.zip"
			fname = name + ".mesh"
			self._mCtx.RegisterResourceZip(zipname)
			self._mEntity[i] = self._mScene.SceneMgr.CreateEntity(fname + i, fname)
			self._mNode[i] = self._mScene.SceneMgr.RootSceneNode.CreateChildSceneNode()
			self._mNode[i].AttachObject(self._mEntity[i])
			i += 1

	def Shutdown(self):
		i = 0
		while i < self._mEntity.Length:
			self._mScene.SceneMgr.DestroyEntity(self._mEntity[i])
			self._mEntity[i] = None
			i += 1
		i = 0
		while i < self._mEntity.Length:
			name = self._mSituation.Cars[i].Info.CarName
			dname = "cars/" + name + "/"
			self._mCtx.UnregisterResource(dname)
			i += 1

	def Update(self, situ):
		""" <summary>
		 Update position of avatars according to the current situation.
		 </summary>
		 <param name="situ">
		 A <see cref="Situation"/>
		 </param>
		"""
		if (self._mSpeeds == None) or (self._mSpeeds.Length != situ.RaceInfo.CarsCount):
			self._mSpeeds = Array.CreateInstance(Single, situ.RaceInfo.CarsCount)
		if (self._mEngineRPMs == None) or (self._mEngineRPMs.Length != situ.RaceInfo.CarsCount):
			self._mEngineRPMs = Array.CreateInstance(Single, situ.RaceInfo.CarsCount)
		i = 0
		while i < situ.RaceInfo.CarsCount:
			p = situ.Cars[i].Position
			if p.Z > -10000.0f:
				self._mNode[i].SetPosition(p.X, p.Z + 0.5f, -p.Y) # XXX (this 0.5f must be in the XML)
				heading = p.AZ
				attitude = -p.AY
				bank = p.AX
				c1 = Math.Cos(heading / 2.0f)
				c2 = Math.Cos(attitude / 2.0f)
				c3 = Math.Cos(bank / 2.0f)
				s1 = Math.Sin(heading / 2.0f)
				s2 = Math.Sin(attitude / 2.0f)
				s3 = Math.Sin(bank / 2.0f)
				c1c2 = c1 * c2
				s1s2 = s1 * s2
				qw = c1c2 * c3 - s1s2 * s3
				qx = c1c2 * s3 + s1s2 * c3
				qy = s1 * c2 * c3 + c1 * s2 * s3
				qz = c1 * s2 * c3 - s1 * c2 * s3
				self._mNode[i].SetOrientation(Quaternion(qw, qx, qy, qz))
			else:
				raise Exception("Invalid car position")
			self._mEngineRPMs[i] = situ.Cars[i].Priv.EngineRpm / situ.Cars[i].Priv.EngineRpmRedLine # XXX
			px = situ.Cars[i].Pub.DynGC.Velocity.X
			py = situ.Cars[i].Pub.DynGC.Velocity.Y
			pz = situ.Cars[i].Pub.DynGC.Velocity.Z
			self._mSpeeds[i] = Math.Sqrt(px * px + py * py + pz * pz) * 3.6f
			i += 1
 # m/s => kmph
	def GetPosition(self, i):
		""" <summary>
		 Returns the position of avatar i.
		 </summary>
		 <param name="i">
		 ID of the avatar.
		 </param>
		 <returns>
		 The position,.
		 </returns>
		"""
		return self._mNode[i].GetPosition()

	def GetOrientation(self, i):
		return self._mNode[i].GetOrientation()

	def GetSpeed(self, i):
		if (self._mSpeeds != None) and (self._mSpeeds.Length > i):
			return self._mSpeeds[i]
		else:
			return 0.0f

	def GetEngineRPM(self, i):
		if (self._mEngineRPMs != None) and (self._mEngineRPMs.Length > i):
			return self._mEngineRPMs[i]
		else:
			return 0.0f
