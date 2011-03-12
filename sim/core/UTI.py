from System import *
from Math3D import *

class PhysicalSurface(object):
	# Returns the list of vertices
	def GetVertices(self):
		pass

	# Returns the number of vertices
	def NumVertices(self):
		pass

	# Returns the list of normals
	def GetNormals(self):
		pass

	# Returns the number of normals
	def NumNormals(self):
		pass

	# Returns the list of indices, each 3 indices gives a triangle
	def GetIndices(self):
		pass

	# Returns the number of indices
	def NumIndices(self):
		pass

	# Returns the resistance to rolling of the surface
	def GetRollingResistance(self):
		pass

	# Returns the friction of the surface
	def GetFriction(self):
		pass

class PhysicalScene(object):
	# Returns the number of surfaces in the physical scene
	def NumSurfaces(self):
		pass

	# Returns the surface at index i
	def GetSurface(self, i):
		pass

class StartingPosition(object):
	def __init__(self):

class LogicalScene(object):
	def NumStartingPositions(self):
		pass

	def GetStartingPosition(self, i):
		pass

class VisualMesh(object):
	# Returns the list of vertices
	def GetVertices(self):
		pass

	# Returns the number of vertices
	def NumVertices(self):
		pass

	# Returns the list of normals
	def GetNormals(self):
		pass

	# Returns the number of normals
	def NumNormals(self):
		pass

	# Returns the list of tangents
	def GetTangents(self):
		pass

	# Returns the number of tangents
	def NumTangents(self):
		pass

	# Returns the list of texture coordinates
	def GetTexcoords(self):
		pass

	# Returns the number of texture coordinates
	def NumTexcoords(self):
		pass

	# Returns the list of indices, each 3 indices gives a triangle
	def GetIndices(self):
		pass

	# Returns the number of indices
	def NumIndices(self):
		pass

	# Material associated with this mesh
	def GetMaterialName(self):
		pass

# A material with its attributes
class VisualMaterial(object):
	def __init__(self):
 # Name of the material # Type of material: shader to apply
	# Shader's parameters
class VisualScene(object):
	# Returns the number of meshes composing the track
	def NumMeshes(self):
		pass

	# Returns mesh at index i
	def GetMesh(self, i):
		pass

	# Returns the number of materials
	def NumMaterials(self):
		pass

	# Returns material at index i
	def GetMaterial(self, i):
		pass

class UTI(object):
	def Init(self):
		pass

	def Shutdown(self):
		pass

	def get_PhysicalScene(self):

	PhysicalScene = property(fget=get_PhysicalScene)

	def get_VisualScene(self):

	VisualScene = property(fget=get_VisualScene)

	def get_LogicalScene(self):

	LogicalScene = property(fget=get_LogicalScene)

	def GetFullPath(self, fileName):
		pass
