#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# CommonUtils.cs             
# Common used utilities
#--------------------------------------------------------------------------*
#
# file         : CommonUtils.cs
# created      : 02 Aug 2008
# last changed : 02 Aug 2008
# Copyright    : ###COPYRIGHTHOLDER###
# eMail        : ###CONTACT###
# Version      : 0.00.010 
#  
#--------------------------------------------------------------------------*
# ###COPYRIGHT###
#--------------------------------------------------------------------------*
from System import *
from Torcs import *

class TUtils(object):
	# Default constructor
	def __init__(self):
		pass
	# 
	# 
	# // Utility to merge parameter files
	# 
	# public IntPtr MergeParamFile(PCarSettings Params, string FileName)
	# 
	# {
	# 
	# PCarSettings NewParams = GfParmReadFile(FileName, GFPARM_RMODE_STD);
	# 
	# 
	# 
	# if(NewParams == null) // Return old one,
	# 
	# return Params; // if new one is empty
	# 
	# 
	# 
	# if(Params == null) // Return new one,
	# 
	# return NewParams; // if old one is empty
	# 
	# 
	# 
	# return GfParmMergeHandles(Params, NewParams, GFPARM_MMODE_SRC | GFPARM_MMODE_DST | GFPARM_MMODE_RELSRC | GFPARM_MMODE_RELDST);
	# 
	# }
	# 
	# 
	# Utility to find the closest point on a line (Lot auf Linie)
	def ClosestPtOnLine(ptx, pty, px, py, vx, vy):
		# P from AB
		# Q is closest pt on AB
		# (P-Q).(B-A) == 0 then Q is closest pt.
		# Q = A + t.(B-A)
		# (P-(A+t.(B-A)).(B-A)
		# use AB for const B-A, and AP for P-A.
		# (AP + tAB).AB == AP.AB + tAB.AB
		# t = -AP.AB / AB.AB == PA.AB / AB.AB
		pax = px - ptx
		pay = py - pty
		den = vx * vx + vy * vy
		if den == 0:
			return 0
		num = pax * vx + pay * vy
		t = num / den
		return t

	ClosestPtOnLine = staticmethod(ClosestPtOnLine)

	# Utility to find distance of a point on a line (Lot auf Linie)
	def DistPtFromLine(ptx, pty, px, py, vx, vy):
		t = TUtils.ClosestPtOnLine(ptx, pty, px, py, vx, vy)
		qx = px + vx * t
		qy = py + vy * t
		dist = Math.Sqrt((ptx - qx) + (ptx - qx) + (pty - qy) * (pty - qy))
		return dist

	DistPtFromLine = staticmethod(DistPtFromLine)

	# Utility to find crossing point (Schnittpunkt zweier Geraden)
	def LineCrossesLine(p0x, p0y, v0x, v0y, p1x, p1y, v1x, v1y, t):
		#	double	denom = lv0 % lv1;
		denom = v0x * v1y - v0y * v1x
		if denom == 0:
			return False
		#	double	numer = lv1 % (lp0 - lp1);
		numer = v1x * (p0y - p1y) - v1y * (p0x - p1x)
		t = numer / denom
		return True

	LineCrossesLine = staticmethod(LineCrossesLine)

	# Utility to find crossing point (Schnittpunkt zweier Geraden)
	def LineCrossesLine(p0, v0, p1, v1, t):
		return TUtils.LineCrossesLine(p0.x, p0.y, v0.x, v0.y, p1.x, p1.y, v1.x, v1.y, )

	LineCrossesLine = staticmethod(LineCrossesLine)

	# Utility to find crossing point (Schnittpunkt zweier Geraden)
	def LineCrossesLineXY(p0, v0, p1, v1, t):
		return TUtils.LineCrossesLine(p0.x, p0.y, v0.x, v0.y, p1.x, p1.y, v1.x, v1.y, )

	LineCrossesLineXY = staticmethod(LineCrossesLineXY)

	# Utility to find crossing point (Schnittpunkt zweier Geraden)
	def LineCrossesLine(p0, v0, p1, v1, t0, t1):
		denom = v0.x * v1.y - v0.y * v1.x
		if denom == 0:
			return False
		numer0 = v1.x * (p0.y - p1.y) - v1.y * (p0.x - p1.x)
		numer1 = v0.x * (p1.y - p0.y) - v0.y * (p1.x - p0.x)
		t0 = numer0 / denom
		t1 = -numer1 / denom
		return True

	LineCrossesLine = staticmethod(LineCrossesLine)

	# Utility to get curvature (Inverse Radius)
	def CalcCurvature(p1x, p1y, p2x, p2y, p3x, p3y):
		px = p1x - p2x
		py = p1y - p2y
		qx = p2x - p3x
		qy = p2y - p3y
		sx = p3x - p1x
		sy = p3y - p1y
		K = (2 * (px * qy - py * qx)) / Math.Sqrt((px * px + py * py) * (qx * qx + qy * qy) * (sx * sx + sy * sy))
		return K

	CalcCurvature = staticmethod(CalcCurvature)

	# Utility to get curvature (Inverser Radius)
	def CalcCurvature(p1, p2, p3):
		return TUtils.CalcCurvature(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)

	CalcCurvature = staticmethod(CalcCurvature)

	# Utility to get curvature (Inverser Radius)
	def CalcCurvatureTan(p1, tangent, p2):
		v = TUtils.VecUnit(TUtils.VecNorm(tangent))
		u = TUtils.VecNorm(p2 - p1)
		q = (p1 + p2) * 0.5f
		radius = 1
		if not TUtils.LineCrossesLine(p1, v, q, u, ):
			return 0
		else:
			return 1.0 / radius

	CalcCurvatureTan = staticmethod(CalcCurvatureTan)

	# Utility to get curvature (Inverser Radius)
	def CalcCurvatureXY(p1, p2, p3):
		return TUtils.CalcCurvature(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)

	CalcCurvatureXY = staticmethod(CalcCurvatureXY)

	# Utility to get curvature in height profil (Inverser Radius i. Höhenprofil)
	def CalcCurvatureZ(p1, p2, p3):
		x1 = 0
		x2 = (p1 - p2).Length
		x3 = x2 + (p2 - p3).Length
		return TUtils.CalcCurvature(x1, p1.z, x2, p2.z, x3, p3.z)

	CalcCurvatureZ = staticmethod(CalcCurvatureZ)

	# Utility to get tangent (Tangente)
	def CalcTangent(p1, p2, p3, tangent):
		mid1 = (p1 + p2) * 0.5f
		norm1 = TUtils.VecNorm(p2 - p1)
		mid2 = (p2 + p3) * 0.5f
		norm2 = TUtils.VecNorm(p3 - p2)
		t = 0.0
		if not TUtils.LineCrossesLine(mid1, norm1, mid2, norm2, ):
			if p1 != p3:
				tangent = TUtils.VecUnit(p3 - p1)
				return True
			return False
		centre = mid1 + norm1 * t
		tangent = TUtils.VecUnit(TUtils.VecNorm(p2 - centre))
		f = TVector2D.Dot(norm1, (p3 - p1))
		if f < 0:
			tangent = -tangent
		return True

	CalcTangent = staticmethod(CalcTangent)

	# Utility to interpolate a curve linear 
	def InterpCurvatureLin(k0, k1, t):
		return k0 + (k1 - k0) * t

	InterpCurvatureLin = staticmethod(InterpCurvatureLin)

	# Utility to interpolate a curve radial
	def InterpCurvatureRad(k0, k1, t):
		# r = r0 + (r1 - r0) * t;
		#
		# 1/k = 1/k0 + (1/k1 - 1/k0) * t
		# 1/k = (k1 + (k0 - k1) * t) / (k0 * k1);
		# k = (k0 * k1) / (k1 + (k0 - k1) * t)
		#
		den = k1 + (k0 - k1) * t
		if Math.Abs(den) < 0.000001:
			den = 0.000001
		return k0 * k1 / den

	InterpCurvatureRad = staticmethod(InterpCurvatureRad)

	# Utility to interpolate a curve 
	def InterpCurvature(k0, k1, t):
		#	return InterpCurvatureRad(k0, k1, t);
		return TUtils.InterpCurvatureLin(k0, k1, t)

	InterpCurvature = staticmethod(InterpCurvature)

	# Utility to get direction angle
	def VecAngXY(v):
		return Math.Atan2(v.y, v.x)

	VecAngXY = staticmethod(VecAngXY)

	# Utility to get length of 3D-Vector in 2D projection
	def VecLenXY(v):
		return Math.Sqrt(v.y * v.y + v.x * v.x)

	VecLenXY = staticmethod(VecLenXY)

	# Utility to get a normal vector to a 3D vector in 2D projection
	def VecNormXY(v):
		return TVector3D(-v.y, v.x, v.z)

	VecNormXY = staticmethod(VecNormXY)

	# Utility to get direction angle
	def VecAngle(v):
		return Math.Atan2(v.y, v.x)

	VecAngle = staticmethod(VecAngle)

	# Utility to get a normal vector to a 2D vector
	def VecNorm(v):
		return TVector2D(-v.y, v.x)

	VecNorm = staticmethod(VecNorm)

	# Utility to normalize a 2D vector
	def VecUnit(v):
		h = Convert.ToSingle(Math.Sqrt(v.x * v.x + v.y * v.y))
		if h == 0:
			return TVector2D(0, 0)
		else:
			return TVector2D(v.x / h, v.y / h)

	VecUnit = staticmethod(VecUnit)
