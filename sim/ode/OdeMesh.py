from System import *
from System.IO import *
# using Tao.Ode;
from System.Xml import *
from System.Collections import *

class OdeMesh(object):
	def get_Vertices(self):
		return self._vertices

	Vertices = property(fget=get_Vertices)

	def get_VertexCount(self):
		return self._vertexCount

	VertexCount = property(fget=get_VertexCount)

	def get_Indices(self):
		return self._indices

	Indices = property(fget=get_Indices)

	def get_IndexCount(self):
		return self._indexCount

	IndexCount = property(fget=get_IndexCount)

	def FromOBJ(filename):
		mesh = OdeMesh()
		mesh.LoadFromOBJ(filename)
		return mesh

	FromOBJ = staticmethod(FromOBJ)

	def __init__(self):
		# First pass to count number of vertex and faces # No normals. No texture. # Triangles only!
		# Allocate buffers
		# Second pass to load the vertices and faces.
		self._SceneObjects = None
		#    		mCtx.RegisterResourcePath("/home/mulder/projects/openracing/cleaned/data/tracks/road/icy");
		#TODO: make it parametric # not yet used # not yet used
		#    				Console.Out.WriteLine("TAGNAME: "+reader.Name);
		# 
		# float x = Convert.ToSingle(reader.GetAttribute("x"));
		# float y = Convert.ToSingle(reader.GetAttribute("y"));
		# float z = Convert.ToSingle(reader.GetAttribute("z"));
		#  # TODO
		self._mLastRaytrace = Array.CreateInstance(Single, 4)
		self._mLastFace = Array.CreateInstance(int, 4)
		self._cpt = -4

	def LoadFromOBJ(self, filename):
		Console.Out.WriteLine("OdeSimulator: Loading mesh {0}", filename)
		Console.Out.WriteLine("OdeSimulator: v{0} f{1}", self._vertexCount, self._indexCount)
		self._vertices = Array.CreateInstance(Tao.Ode.Ode.dVector3, self._vertexCount)
		self._indices = Array.CreateInstance(int, self._indexCount)
		Console.Out.WriteLine("OdeSimulator: Done loading mesh")

	def FromMeshXML(filename):
		mesh = OdeMesh()
		mesh.LoadFromMeshXML(filename)
		return mesh

	FromMeshXML = staticmethod(FromMeshXML)

	def LoadFromMeshXML(self, filename):
		self._SceneObjects = ArrayList()
		target = "data/tracks/road/icy/" + filename + ".xml"
		Console.Out.WriteLine(" 	<--- loading from mesh XML: " + target)
		reader = XmlTextReader(target)
		material = ""
		useSharedVertices = ""
		fcount = 0
		vcount = 0
		sobject = None
		while reader.Read():
			if reader.NodeType == XmlNodeType.Element:
				if reader.Name == "submesh":
					reader.MoveToContent()
					material = reader.GetAttribute("material")
					useSharedVertices = reader.GetAttribute("usesharedvertices")
					sobject = SceneObject()
					self._SceneObjects.Add(sobject)
					fcount = 0
					vcount = 0
				elif reader.Name == "faces":
					sobject.setFacesCount(Convert.ToInt32(reader.GetAttribute("count")))
					Console.Out.WriteLine("	# of allocated faces: " + sobject.faceCount)
				elif reader.Name == "face":
					sobject.Faces[fcount] = Convert.ToInt32(reader.GetAttribute("v1"))
					fcount += 1
					sobject.Faces[fcount] = Convert.ToInt32(reader.GetAttribute("v2"))
					fcount += 1
					sobject.Faces[fcount] = Convert.ToInt32(reader.GetAttribute("v3"))
					fcount += 1
				elif reader.Name == "geometry":
					sobject.setVerticesCount(Convert.ToInt32(reader.GetAttribute("vertexcount")))
					Console.Out.WriteLine("	# of allocated vertices: " + sobject.vertexCount)
				elif reader.Name == "vertexbuffer":
				elif reader.Name == "vertex":
				elif reader.Name == "position":
					if True:
						sobject.Vertices[vcount].X = Convert.ToSingle(reader.GetAttribute("x")) / 33.0f
						sobject.Vertices[vcount].Y = Convert.ToSingle(reader.GetAttribute("y")) / 33.0f
						sobject.Vertices[vcount].Z = Convert.ToSingle(reader.GetAttribute("z")) / 33.0f
					else:
						sobject.Vertices[vcount].X = Convert.ToSingle(reader.GetAttribute("x"))
						sobject.Vertices[vcount].Y = Convert.ToSingle(reader.GetAttribute("z"))
						sobject.Vertices[vcount].Z = -Convert.ToSingle(reader.GetAttribute("y"))
					vcount += 1
				elif reader.Name == "normal":
				elif reader.Name == "colour_diffuse":
				elif reader.Name == "texcooord":

	def CrossProduct(self, x1, z1, x2, z2):
		return x1 * z2 - z1 * x2

	def Sign(self, x):
		if x > 0.0f:
			return 1
		elif x < 0.0f:
			return -1
		else:
			return 0

	def SameSide(self, x, z, v0, v1, v2):
		x0 = x - v0.X
		z0 = z - v0.Z
		x1 = v1.X - v0.X
		z1 = v1.Z - v0.Z
		x2 = v2.X - v0.X
		z2 = v2.Z - v0.Z
		return self.Sign(self.CrossProduct(x1, z1, x0, z0)) == self.Sign(self.CrossProduct(x1, z1, x2, z2))

	def IsInside(self, x, z, v0, v1, v2):
		return self.SameSide(x, z, v0, v1, v2) and self.SameSide(x, z, v1, v2, v0) and self.SameSide(x, z, v2, v0, v1)

	def InterpolateY(self, x, z, v0, v1, v2):
		return (v0.Y + v1.Y + v2.Y) / 3.0f

	def RaytraceDown(self, x, y, z):
		# Check if ray still collide into same triangle (little optimization)
		if self._cpt >= 0:
			vl0 = self._vertices[self._indices[self._mLastFace[self._cpt] + 0]]
			vl1 = self._vertices[self._indices[self._mLastFace[self._cpt] + 1]]
			vl2 = self._vertices[self._indices[self._mLastFace[self._cpt] + 2]]
			if self.IsInside(x, z, vl0, vl1, vl2):
				self._mLastRaytrace[self._cpt] = self.InterpolateY(x, y, vl0, vl1, vl2)
				return self._mLastRaytrace[self._cpt]
		lcpt = self._cpt
		if lcpt < 0:
			lcpt += 4
		if self._cpt += 1 == 4:
			self._cpt = 0
		# for each triangle
		f = 0
		while f < self._indexCount:
			v0 = self._vertices[self._indices[f + 0]]
			v1 = self._vertices[self._indices[f + 1]]
			v2 = self._vertices[self._indices[f + 2]]
			# check if vec2(x,z) is within 2d triangle (3d seen from above)
			if self.IsInside(x, z, v0, v1, v2):
				self._mLastRaytrace[lcpt] = self.InterpolateY(x, y, v0, v1, v2)
				self._mLastFace[lcpt] = f
				return self._mLastRaytrace[lcpt]
			f += 3
		# if it is, intepolate between the 3 vertices of the triangle to get contact point
		# return the nearest contact point which is bellow y.
		# nothing found. return last contact;
		return self._mLastRaytrace[lcpt]
