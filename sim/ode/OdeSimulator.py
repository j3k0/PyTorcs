from System import *
from System.IO import *
from System.Xml import *
from System.Collections.Generic import *
from System.Runtime.InteropServices import *
from SwigTorcs import *
from OpenRacing.Core import *
from OpenRacing.Core.Track import *

class OdeSimulator(Simulator): # ODE World # ODE space for the ground mesh
	# The following references are kept here but not used.
	def Config(self, car):
		""" <summary>Adds and configure a car for the simulation</summary>"""
		TorcsItf.SimConfig(car)

	def Init(self, nbcars, track):
		""" <summary>Initialize the simulation</summary>"""
		Console.Out.WriteLine("OdeSimulator: Init")
		# Try to load module information for information purpose.
		modInfo = tModInfo()
		TorcsItf.simuv2(modInfo)
		# Load simuv2 interface
		self._mcSimItf = tSimItf()
		TorcsItf.simuv2Init(self._mcSimItf)
		# Initialize simulation module
		TorcsItf.SimInit(nbcars)
		Console.Out.WriteLine("OdeSimulator: Create World")
		# Now initialize ODE
		Tao.Ode.Ode.dInitODE()
		# Create a world
		self._mWorld = Tao.Ode.Ode.dWorldCreate()
		# Add gravity to the world (pull down on the Y axis 9.81 meters/second
		Console.Out.WriteLine("OdeSimulator: Set Gravity")
		#            Ode.dWorldSetGravity(mWorld, 0, -9.81f, 0);
		Tao.Ode.Ode.dWorldSetGravity(self._mWorld, 0, 0, 0)
		# 
		# * The QuadTreeSpace was freezing ODE while being initialized
		# *
		# // Create a space for the ground geometry
		# Ode.dVector3 mGroundCenter = new Ode.dVector3(0,0,0); // center of root block
		# Ode.dVector3 mGroundExtents = new Ode.dVector3(5000, 1000, 5000); // extents of root block
		# int depth = 2; // depth of the tree
		# Console.Out.WriteLine("OdeSimulator: Create QuadTree");
		# mGroundSpace = Ode.dQuadTreeSpaceCreate(IntPtr.Zero, mGroundCenter, mGroundExtents, depth);
		# 
		self._mGroundSpace = Tao.Ode.Ode.dSimpleSpaceCreate(IntPtr.Zero)
		# TODO: Replace the following by OTI loading -- Imre did LoadOSMTrack();
		objname = track.GetFullPath("ode-model.obj")
		self._mOdeMesh = OdeMesh.FromOBJ(objname) # Reference SHOULD be kept
		Console.Out.WriteLine("OdeSimulator: Create TriMesh Geometry")
		self._mGroundTriMeshData = Tao.Ode.Ode.dGeomTriMeshDataCreate()
		Console.Out.WriteLine("OdeSimulator: Build TriMesh Geometry")
		Tao.Ode.Ode.dGeomTriMeshDataBuildSimple(self._mGroundTriMeshData, self._mOdeMesh.Vertices, self._mOdeMesh.VertexCount, self._mOdeMesh.Indices, self._mOdeMesh.IndexCount)
		Console.Out.WriteLine("OdeSimulator: Create TriMesh")
		self._mGroundGeom = Tao.Ode.Ode.dCreateTriMesh(self._mGroundSpace, self._mGroundTriMeshData, None, None, None)
		self.CreateRayTrace()
		Console.Out.WriteLine("OdeSimulator: Done")
 # Id of raycast used for measure track height
	def CreateRayTrace(self):
		# set ray length to 1000. This is the maximum height of any part of the track
		# mHeightRayId = Ode.dCreateRay(mGroundSpace, 1000);
		self._mHeightRayId = Tao.Ode.Ode.dCreateRay(IntPtr.Zero, 1024)
		Tao.Ode.Ode.dGeomRaySetParams(self._mHeightRayId, 0, 0)
		Tao.Ode.Ode.dGeomRaySetClosestHit(self._mHeightRayId, 1)
		Tao.Ode.Ode.dGeomRaySetLength(self._mHeightRayId, 1024)
		self._mContacts = Array.CreateInstance(Tao.Ode.Ode.dContactGeom, 1)
		self._mContacts[0] = Tao.Ode.Ode.dContactGeom()

	# return height of the first polygon point hit by a ray casted down from x,y,z.
	def RaytraceGroundDown(self, x, y, z):
		retdata = RayCastData()
		Tao.Ode.Ode.dGeomRaySet(self._mHeightRayId, x, y + 5, z, 0, -1, 0)
		numContacts = Tao.Ode.Ode.dCollide(self._mHeightRayId, self._mGroundSpace, self._mContacts.Length, self._mContacts, Marshal.SizeOf(self._mContacts[0]))
		if numContacts < 1:
			Console.Out.WriteLine("OUT-OF-TRACK   {0} {1} {2}", x, y, z)
		else:
			retdata.Height = self._mContacts[0].pos.Y
			retdata.Normal = self._mContacts[0].normal
			retdata.SurfaceId = self._mContacts[0].g2
		# bool found = false; Used to determine friction.
		# int i=0;
		# while (i<iceGeoms.Count && !found) {
		# if ((int)retdata.SurfaceId == (int)iceGeoms[i])
		# found = true;
		# ++i;
		# }
		# if (found) {
		# Console.Out.WriteLine("ICE");
		# retdata.Friction=0.3f;
		# }
		return retdata

	# Compute zRoad for each wheel.
	def ComputeWheelsZRoad(self, situ):
		carID = 0
		while carID < situ.RaceInfo.CarsCount:
			wheelArray = situ.Cars[carID].Priv.Wheels
			m = situ.Cars[carID].PositionMatrix
			wheelID = 0
			while wheelID < 4:
				wheel = wheelArray[wheelID]
				x = wheel.RelativePosition.X
				y = wheel.RelativePosition.Y
				z = wheel.RelativePosition.Z
				v = Math3D.Vector3(x, y, z)
				v = m * v # Get position of wheel in world coordinate
				rcd = self.RaytraceGroundDown(v.x, v.z, -v.y)
				wheel.zRoad = rcd.Height
				wheel.nnorm_x = rcd.Normal.X
				wheel.nnorm_y = rcd.Normal.Z
				wheel.nnorm_z = -rcd.Normal.Y
				wheel.friction = rcd.Friction
				wheelID += 1
			carID += 1

	def Update(self, situ):
		""" <summary>Update car locations</summary>"""
		if self._mWorld == IntPtr.Zero:
			return 
		self.ComputeWheelsZRoad(situ)
		# Update simuv2
		TorcsItf.SimUpdate(situ, situ.DeltaTime, -1)
		# Update ODE
		Tao.Ode.Ode.dWorldStep(self._mWorld, situ.DeltaTime)

	def Shutdown(self):
		Tao.Ode.Ode.dCloseODE()
		TorcsItf.SimShutdown()

	def __init__(self):
		self._mWorld = IntPtr.Zero
		self._mGroundSpace = IntPtr.Zero
		self._mContacts = Array.CreateInstance(Tao.Ode.Ode.dContactGeom, 1)
