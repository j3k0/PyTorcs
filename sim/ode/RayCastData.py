from System import *
# using Tao.Ode;
class RayCastData(object):
	def __init__(self):
		self._SurfaceId = -1
		self._Height = 0.0f
		self._Normal = Tao.Ode.Ode.dVector3()
		self._RollingResistance = 0.001f
		self._Friction = 0.95f
