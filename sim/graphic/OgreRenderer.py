# OgreRenderer.cs
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
from Math3D import *
from System import *
from SwigTorcs import *
from OpenRacing.Core import *
from OpenRacing.Core.Track import *

class OgreRenderer(OpenRacing.Graphic.GraphicModule):
	""" <summary>
	 Manage the rendering of the scene using OgreDotNet.
	 </summary>
	""" # Visual context # Static scene # List of dynamic entities # List of cameras # The active camera
	def __init__(self):
		self._mCtx = None
		self._mGui = None
		self._mFollowingID = -1
		self._mAudioManager = None
		self._mEngine = None # XXX: Configurable from outside # Debug
		# InitScene(quality);
		self._fps = 0.0 # Interpolated fps counter.
		self._before = -1.0
		self._mFollowingID = 0

	def InitTrack(self, track):
		Console.Out.WriteLine(">>> InitTrack")
		self._mScene.Init(track)

	def InitAvatars(self, situ):
		Console.Out.WriteLine(">>> InitAvatars")
		self._mAvatars = OAvatars(self._mCtx, self._mScene, situ)
		self._mAvatars.Init()
		if self._mFollowingID >= 0:
			self._mCamera.SetFollowing(self._mAvatars, self._mFollowingID)
			self._mCamera.SetMode(OCamera.Mode.Behind)
			if self._mGui != None:
				self._mGui.ShowHUD(self._mAvatars, self._mFollowingID)
		self._mEngine = Array.CreateInstance(int, situ.RaceInfo.CarsCount)
		i = 0
		while i < situ.RaceInfo.CarsCount:
			self._mEngine[i] = self._mAudioManager.InitCarEngine("clkdtmb2")
			pos = self._mAvatars.GetPosition(i)
			rpm = self._mAvatars.GetEngineRPM(i)
			self._mAudioManager.UpdateCarEngine(self._mEngine[i], 0.0, pos.x, pos.y, pos.z, rpm)
			i += 1

	def InitView(self, enableGui, quality):
		Console.Out.WriteLine(">>> InitView")
		self._mCtx = OContext()
		self._mCtx.Init()
		self.InitScene(quality)
		if enableGui:
			self._mGui = OGui()
			self._mGui.Init(self._mCtx)
		self._mCtx.LoadResources()

	def InitScene(self, quality):
		self._mScene = OScene(self._mCtx, quality)
		self._mCameras = OCameras(self._mScene)
		self._mCamera = TestCameras.CreateBlenderTestCamera2(self._mCtx, self._mCameras)
		self._mCamera.Apply(self._mCtx)

	def ChangeQuality(self, quality):
		self._mScene.ChangeQuality(quality)

	def ShutdownView(self):
		Console.Out.WriteLine(">>> ShutdownView")
		self.ShutdownAvatars()
		self.ShutdownTrack()
		if self._mGui != None:
			self._mGui.Shutdown()
		self._mCameras.Shutdown()
		if self._mScene != None:
			self._mScene.Shutdown()
		self._mCtx.Shutdown()
		self._mCamera = None
		self._mCameras = None
		self._mGui = None
		self._mScene = None
		self._mCtx = None

	def ShutdownTrack(self):
		if self._mScene != None:
			quality = self._mScene.Quality
			self._mScene.Shutdown()
			self._mScene = None

	def ShutdownAvatars(self):
		if self._mAvatars != None:
			self._mAvatars.Shutdown()
			self._mAvatars = None
			self._mCamera.ClearFollowing()
 # Time of last rendered image.
	def Refresh(self, situ):
		""" <summary>
		 Refresh screen content and user cameras pictures if necessary.
		 </summary>
		 <param name="situ">
		 A <see cref="Situation"/>
		 </param>
		"""
		if self._mCtx == None:
			return 
		try:
			# Compute the framerate.
			now = DateTime.Now.Ticks / TimeSpan.TicksPerSecond
			if self._before < 0.0:
				self._before = now - 0.001
			delta_t = now - self._before
			self._before = now # ref track,
			self._mScene.Update(now, delta_t)
			if self._mAvatars != None:
				self._mAvatars.Update(situ)
			self._mCameras.Update(now, delta_t)
			self._fps = self._fps * 0.95 + 0.05 / delta_t
			# Console.Out.WriteLine("Refresh {0}fps", (int)fps);
			if self._mAudioManager != None:
				if self._mCamera != None:
					cpos = self._mCamera.GetPosition()
					self._mAudioManager.UpdateListener(delta_t, cpos.x, cpos.y, cpos.z)
				if self._mAvatars != None:
					i = 0
					while i < situ.RaceInfo.CarsCount:
						pos = self._mAvatars.GetPosition(i)
						rpm = self._mAvatars.GetEngineRPM(i)
						self._mAudioManager.UpdateCarEngine(self._mEngine[i], delta_t, pos.x, pos.y, pos.z, rpm)
						i += 1
			# Update non active cameras.
			enumerator = self._mCameras.All.GetEnumerator()
			while enumerator.MoveNext():
				cam = enumerator.Current
				if cam != self._mCamera:
					cam.Apply(self._mCtx)
					self._mCtx.Root.RenderOneFrame()
					self._mCtx.Win.WriteContentsToFile(cam.Name + ".png")
			# Perform on screen rendering.
			self._mCamera.Apply(self._mCtx)
			if self._mGui != None:
				self._mGui.Render(now, delta_t)
			if self._mCtx != None:
				if self._mCtx.Root != None:
					self._mCtx.Root.RenderOneFrame()
				if self._mCtx.Win != None:
					self._mCtx.Win.Update(True)
		except Exception, e:
			Console.Out.WriteLine("EXCEPTION: {0}\n{1}", e.Message, e.StackTrace)
			raise GraphicException("OgreRenderer failed miserably", e)
		finally:

	def AddCamera(self, name, fovy, freq):
		cam = self._mCameras.Create(name)
		cam.SetFOVy(fovy)
		cam.SetFrequency(freq)

	def MoveCamera(self, name, pos, lookat):
		cam = self._mCameras.Get(name)
		cam.SetPosition(pos)
		cam.LookAt(lookat)

	def get_Gui(self):
		return self._mGui

	Gui = property(fget=get_Gui)

	def get_AudioManager(self):
		return self._mAudioManager

	def set_AudioManager(self, value):
		self._mAudioManager = value

	AudioManager = property(fget=get_AudioManager, fset=set_AudioManager)
