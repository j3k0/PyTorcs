# OCameras.cs
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
from Math3D import *
from OgreDotNet import *

class OCamera(object):
	""" <summary>
	 A camera managed by <see cref="OCameras"/>
	 </summary>
	"""
	def get_Name(self):
		return self._mCamera.Name

	Name = property(fget=get_Name)

	class Mode(object):
		def __init__(self):

	def __init__(self):

	def SetMode(self, mode):
		mMode = mode
		if mMode == Mode.Fixed:
			mCamera.NearClipDistance = 5.0f
			mCamera.FarClipDistance = 5000.0f
		elif mMode == Mode.Behind:
			mCamera.NearClipDistance = 1.0f
			mCamera.FarClipDistance = 1000.0f
		elif mMode == Mode.Cockpit:
			pass
		elif mMode == Mode.SideChase:
			pass

	def SetFollowing(self, followingAvatars, followingID):
		mFollowingAvatars = followingAvatars
		mFollowingID = followingID

	def ClearFollowing(self):
		mFollowingAvatars = None
		mFollowingID = -1

	def SetPosition(self, position):
		mPosition = position
		mCamera.SetPosition(position)

	def GetPosition(self):
		return mPosition

	def LookAt(self, lookat):
		mCamera.LookAt(lookat)

	def SetFOVy(self, fovy):
		mCamera.SetFOVy(Radian(fovy))

	def Apply(self, ctx):
		ctx.SetCamera(mCamera)

	def SetFrequency(self, updateFreq):
		mFreq = updateFreq

	def Update(self, now, delta_t):
		# Return if no need to update camera position/orientation
		if mFollowingID < 0:
			return 
		# if (mFreq > 0.0f) {
		#    mTimeUntilUpdate -= delta_t;
		#    if (mTimeUntilUpdate > 0.0f)
		#        return;
		#    mTimeUntilUpdate = 1.0f / mFreq;
		# }
		# Update needed: do it!
		if mMode == Mode.Fixed:
			self.LookAt(mFollowingAvatars.GetPosition(mFollowingID))
			self.SetPosition(Vector3(50, 38000, 50))
		elif mMode == Mode.Behind:
			o = mFollowingAvatars.GetOrientation(mFollowingID)
			p = mFollowingAvatars.GetPosition(mFollowingID)
			v = (o * (Vector3(-5, 0, 0))) + p + Vector3(0, 1.5f, 0)
			self.SetPosition(v)
			self.LookAt(p)
		elif mMode == Mode.Cockpit:
			p = mFollowingAvatars.GetPosition(mFollowingID)
			self.SetPosition(p)
			r = Quaternion(Math.Sqrt(0.5f), 0, -Math.Sqrt(0.5f), 0)
			o = mFollowingAvatars.GetOrientation(mFollowingID)
			mCamera.SetOrientation(o * r)
		elif mMode == Mode.SideChase:
			self.LookAt(mFollowingAvatars.GetPosition(mFollowingID))
			self.SetPosition(Vector3(-20.0f, 3.0f, 0) + mFollowingAvatars.GetPosition(mFollowingID))

class OCameras(object):
	""" <summary>
	 Manage the list of cameras
	 </summary>
	"""
	def get_All(self):
		return self._mHash.Values

	All = property(fget=get_All)

	def __init__(self, scene):
		""" <summary>
		 Builds an empty camera list
		 </summary>
		 <param name="scene">
		 Associated scene
		 </param>
		"""
		self._mHash = System.Collections.Hashtable()
		self._mScene = scene

	def Create(self, name):
		""" <summary>
		 Create a new camera with given name
		 </summary>
		 <param name="name">
		 Name (ID) of the camera
		 </param>
		 <returns>
		 A newly creaty <see cref="OCamera"/>
		 </returns>
		"""
		camera = self._mScene.SceneMgr.CreateCamera(name)
		camera.SetFOVy(Radian(1.35f))
		ocam = OCamera(camera)
		self._mHash.Add(name, ocam)
		return ocam

	def Get(self, name):
		return self._mHash[name]

	def MoveCamera(self, name, pos, lookat):
		""" <summary>
		 Move the camera with given name to a new position
		 </summary>
		 <param name="name">
		 Name (ID) of the camera
		 </param>
		 <param name="pos">
		 New position
		 </param>
		 <param name="lookat">
		 New orientation (spot the camera is looking at)
		 </param>
		"""
		camera = self._mHash[name]
		camera.SetPosition(pos)
		camera.LookAt(lookat)

	def ApplyCamera(self, name, ctx):
		""" <summary>
		 Prepare the scene to be rendered from given camera position
		 </summary>
		 <param name="name">
		 Name (ID) of the camera
		 </param>
		 <param name="ctx">
		 The camera will become active on this context
		 </param>
		"""
		camera = self._mHash[name]
		camera.Apply(ctx)

	def Update(self, now, delta_t):
		""" <summary>
		 Update the cameras positions
		 </summary>
		 <remarks>
		 Some cameras may have automatic tracking of an avatar or inertia
		 activated, this method apply such behaviours.
		 </remarks>
		"""
		enumerator = self._mHash.Values.GetEnumerator()
		while enumerator.MoveNext():
			cam = enumerator.Current
			cam.Update(now, delta_t)

	def Shutdown(self):
		self._mHash.Clear()
