# OScene.cs
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
from System.Drawing import *
from System.IO import *
from Math3D import *
from OgreDotNet import *
from SwigTorcs import *
from OpenRacing.Core import *
from OpenRacing.Core.Track import *
# Manage all the graphical entities of the scene 
class OScene(object):
	def get_SceneMgr(self):
		return self._mSceneMgr

	SceneMgr = property(fget=get_SceneMgr)

	def get_Quality(self):
		return self._mQuality

	Quality = property(fget=get_Quality)

	# Load and display the ogre scene
	#
	# @param sceneMgr The SceneManager
	# @param track Torcs' Track
	def __init__(self, ctx, quality):
		self._mCtx = ctx
		self._mTrack = None
		self._mSceneMgr = self._mCtx.CreateSceneManager()
		self.ChangeQuality(quality)

	def ChangeQuality(self, quality):
		self._mQuality = quality

	def Init(self, track):
		if self._mQuality == GraphicRenderingQuality.High:
			self._mSceneMgr.SetShadowTechnique(ShadowTechnique.ShadowTypeStencilModulative)
		else:
			self._mSceneMgr.SetShadowTechnique(ShadowTechnique.ShadowTypeNone)
		self._mTrack = track
		self.CreateBlenderTestLight(self._mSceneMgr)
		mZipName = self._mTrack.GetFullPath("ogre-model.zip")
		self._mCtx.RegisterResourceZip(self._mZipName)
		self.LoadSceneMeshes(self._mZipName)
		self._mSceneMgr.SetSkyBox(True, "skybox/Sky", 50)

	def Shutdown(self):
		if self._mTrack != None:
			if self._mCtx != None:
				self._mCtx.UnregisterResource(self._mZipName)
			self._mTrack = None
		if self._mEntity != None:
			i = 0
			while i < self._mEntity.Length:
				self._mSceneMgr.DestroyEntity(self._mEntity[i])
				self._mEntity[i] = None
				i += 1
			self._mEntity = None
		if self._mLight != None:
			self._mSceneMgr.DestroyLight(self._mLight)
			self._mLight = None
		if self._mSceneMgr != None:
			self._mSceneMgr.ClearScene()
			self._mSceneMgr = None
		self._mCtx = None

	def LoadSceneMeshes(self, zipname):
		# Count meshes
		count = 0
		while True:
			fname = "scene-" + count + ".mesh"
			if ResourceGroupManager.Singleton.resourceExists(zipname, fname):
				count += 1
			else:
				break
		# Allocate and load meshes
		self._mEntity = Array.CreateInstance(Entity, count)
		i = 0
		while i < count:
			fname = "scene-" + i + ".mesh"
			self._mEntity[i] = self._mSceneMgr.CreateEntity(fname, fname)
			j = 0
			while j < self._mEntity[i].NumSubEntities:
				se = self._mEntity[i].GetSubEntity(j)
				if se.getMaterialName().Contains("ALPHA"): # XXX alpha-blended objects not supported by stencil-shadows
					se.setVisible(False)
				j += 1
			if self._mEntity[i].Name.Contains("CAST"):
				self._mEntity[i].SetCastShadows(True)
			self._mSceneMgr.RootSceneNode.AttachObject(self._mEntity[i])
			i += 1

	# Create same light as in blender
	#I tweaked this to make it a little less dystopian. Feel free to make better.
	#Let's have a nice sunny day at 11am. My video card is screwed up so I can't really tell how this looks,
	#but it looks better to me!
	def CreateBlenderTestLight(self, sceneMgr):
		sceneMgr.AmbientLightColor = Color.White
		self._mLight = sceneMgr.CreateLight("MainLight")
		self._mLight.Type = Light.LightTypes.Directional
		self._mLight.DiffuseColor = Color.White
		self._mLight.SpecularColour = Color.Black
		dir = Math3D.Vector3(-0.7f, -1.0f, -1.0f)
		dir.Normalize()
		self._mLight.Direction = dir

	# Animate the scene
	#
	# @param track A Track
	# @param t Current time for the simulation
	# @param delta_t Time elapsed since the last simulation step
	def Update(self, t, delta_t):
		pass
