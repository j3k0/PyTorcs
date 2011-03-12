# Situation.cs created with MonoDevelop
# User: jeko at 5:26 PM 8/22/2008
#
# To change standard headers go to Edit->Preferences->Coding->Standard Headers
#
from Math3D import *
from System import *
from System.Collections.Generic import *
from System.Runtime.InteropServices import *
from System.IO import *

class Avatar(object):
	# public readonly Vector3 position;
	def __init__(self, car):
		self._name = Marshal.PtrToStringAnsi(IntPtr())
		team = Marshal.PtrToStringAnsi(IntPtr())
		self._filename = "cars" + Path.DirectorySeparatorChar + team + Path.DirectorySeparatorChar + team + ".xml"
		# posMat = car->pub.posMat;
		# position = new Vector3(car->pub.cornerFrontR.x, car->pub.cornerFrontR.y, car->pub.cornerFrontR.z);
		# position = new Vector3(car->pub.DynGCg.pos.x, car->pub.DynGCg.pos.y, car->pub.DynGCg.pos.z);
		#Console.Out.WriteLine("POS: {0}", position);
		# TMovement t = car->pub.DynGC;
		#Console.Out.Write("DynGC pos: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.pos.x, t.pos.y, t.pos.z, t.pos.ax, t.pos.ay, t.pos.az); 
		#Console.Out.Write("      vel: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.vel.x, t.vel.y, t.vel.z, t.vel.ax, t.vel.ay, t.vel.az); 
		#Console.Out.Write("      acc: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.acc.x, t.acc.y, t.acc.z, t.acc.ax, t.acc.ay, t.acc.az); 
		# t = car->pub.DynGCg;
		#Console.Out.Write("DynGCg pos: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.pos.x, t.pos.y, t.pos.z, t.pos.ax, t.pos.ay, t.pos.az); 
		#Console.Out.Write("       vel: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.vel.x, t.vel.y, t.vel.z, t.vel.ax, t.vel.ay, t.vel.az); 
		#Console.Out.Write("       acc: {0:0.##} {1:0.##} {2:0.##} {3:0.##} {4:0.##} {5:0.##}\n", t.acc.x, t.acc.y, t.acc.z, t.acc.ax, t.acc.ay, t.acc.az); 
		m = .posMat
		self._posMat = Matrix4(m.a00, m.a01, m.a02, m.a03, m.a10, m.a11, m.a12, m.a13, m.a20, m.a21, m.a22, m.a23, m.a30, m.a31, m.a32, m.a33).Transpose()

class Situation(object):
	def __init__(self, situ):
		self._avatars = List[Avatar]()
		self._deltaTime = situ.deltaTime
		self._currentTime = situ.curTime
