# OContext.cs
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
from System.Drawing import *
from System.Collections.Generic import *
# Graphical context for the OgreDotNet renderer.
class OContext(object):
	def get_Root(self):
		return self._mRoot

	Root = property(fget=get_Root)

	def get_Win(self):
		return self._rWin

	Win = property(fget=get_Win)

	def __init__(self):
		self._mRoot = None
		self._rSys = None
		self._rWin = None
		self._mViewport = None
		self._mSceneMgr = None
		self._mLoadedResources = None
		self._mLoadedResourceGroups = None

	def Init(self):
		if self._mRoot == None:
			self._mRoot = Root()
		self._mLoadedResources = Dictionary[str, int]()
		self._mLoadedResourceGroups = Dictionary[str, str]()
		if not self.InitOgreRenderSystem():
			return 
		if not self.InitOgreRenderWindow():
			return 

	# InitSceneManager();
	def Shutdown(self):
		self.ShutdownAllResources()
		if self._rWin != None:
			self._mRoot.DetachRenderTarget(self._rWin)
		if self._mSceneMgr != None:
			self._mRoot.DestroySceneManager(self._mSceneMgr)
		self._mViewport = None
		self._mSceneMgr = None
		self._rWin = None
		self._rSys = None
		self._mLoadedResources = None
		self._mLoadedResourceGroups = None
		self._mRoot.Shutdown()
		self._mRoot.Dispose()
		self._mRoot = None

	# mRoot = new Root();
	def CreateSceneManager(self):
		if self._mSceneMgr == None:
			sceneMgr = self._mRoot.CreateSceneManager(SceneType.Generic)
			# sceneMgr.SetShadowTechnique(ShadowTechnique.ShadowTypeTextureModulative);
			# sceneMgr.SetShadowFarDistance(200);
			# sceneMgr.setShadowTextureSize(4096);
			# sceneMgr.SetShadowTextureSelfShadow(true);
			self._mSceneMgr = sceneMgr
		return self._mSceneMgr

	def SetCamera(self, camera):
		if self._mViewport == None:
			self._mViewport = self._rWin.AddViewport(camera)
			self._mViewport.BackgroundColor = Color.Black
		else:
			self._rWin.GetViewport(0).SetCamera(camera)
		camera.AspectRatio = self._mViewport.GetActualWidth() / self._mViewport.GetActualHeight()

	def LoadResources(self):
		TextureManager.Instance.SetDefaultNumMipmaps(5)
		ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

	def InitOgreRenderWindow(self):
		if self._rWin == None:
			self._rWin = self._mRoot.Initialise(True)
		return True

	def InitOgreRenderSystem(self):
		if self._rSys != None:
			return True
		if not self._mRoot.RestoreConfig():
			self._mRoot.ShowConfigDialog()
		# LogManager mLogManager = LogManager.GetSingleton();
		rList = self._mRoot.GetAvailableRenderers()
		it = rList.GetEnumerator()
		while it.MoveNext():
			self._rSys = it.Current
			# if(mRenderSystemName.CompareTo("Direct3D9 Rendering Subsystem") == 0)
			if self._rSys.GetName().CompareTo("OpenGL Rendering Subsystem") == 0:
				break
		if self._rSys != None: # Set the RenderSystem
			self._mRoot.SetRenderSystem(self._rSys)
		return (self._rSys != None)

	def RegisterResource(self, path, group, type):
		if self._mLoadedResources.ContainsKey(path):
			self._mLoadedResources[path] = self._mLoadedResources[path] + 1
		else:
			self._mLoadedResources.Add(path, 1)
		if self._rWin != None:
			ResourceGroupManager.Singleton.addResourceLocation(path, type, group)
			ResourceGroupManager.Singleton.initialiseResourceGroup(group)
		else:
			ResourceGroupManager.Singleton.addResourceLocation(path, type, "General")
		self._mLoadedResourceGroups[path] = group
		Console.Out.WriteLine(">>> Registered {0}({1}) to {2}", path, self._mLoadedResources[path], path if self._rWin != None else "General")

	def RegisterResourceZip(self, path):
		self.RegisterResource(path, path, "Zip")

	def RegisterResourcePath(self, path, group):
		self.RegisterResource(path, group, "FileSystem")

	def RegisterResourcePath(self, path):
		self.RegisterResource(path, path, "FileSystem")

	def UnregisterResource(self, path):
		if self._mLoadedResources.ContainsKey(path):
			self._mLoadedResources[path] = self._mLoadedResources[path] - 1
		else:
			return 
		Console.Out.WriteLine(">>> Unregistered {0}({1})", path, self._mLoadedResources[path])
		if self._mLoadedResources[path] == 0:
			group = self._mLoadedResourceGroups[path]
			ResourceGroupManager.Singleton.removeResourceLocation(path, group)
			#if (group != "General")
			ResourceGroupManager.Singleton.destroyResourceGroup(group)
			self._mLoadedResources.Remove(path)
			self._mLoadedResourceGroups.Remove(path)

	def ShutdownAllResources(self):
		enumerator = self._mLoadedResourceGroups.Values.GetEnumerator()
		while enumerator.MoveNext():
			group = enumerator.Current
			#if (group != "General")
			ResourceGroupManager.Singleton.destroyResourceGroup(group)
