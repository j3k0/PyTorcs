from System import *
from System.IO import *
from OgreDotNet import *
from System.Collections import *

class SceneObject(object):
	def __init__(self):
		# global position # should be vector # should be quaternion # should be vector # name of the object # name of the mesh file
		# faces and vertices
		self._vertex = ArrayList()
		self._faces = ArrayList()

	def setFacesCount(self, cnt):
		self._Faces = Array.CreateInstance(int, cnt * 3)
		self._faceCount = cnt * 3
		i = 0
		while i < self._faceCount:
			self._Faces[i] = System.Int32()
			i += 1

	def setVerticesCount(self, cnt):
		self._Vertices = Array.CreateInstance(Tao.Ode.Ode.dVector3, cnt)
		self._vertexCount = cnt
		i = 0
		while i < self._vertexCount:
			self._Vertices[i] = Tao.Ode.Ode.dVector3()
			i += 1

	# linkeage between Ogre and Ode
