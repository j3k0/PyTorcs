#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# Lane.cs
# Contains informations about the points along a track
#--------------------------------------------------------------------------*
#
# file         : Lane.cs
# created      : 02 Aug 2008
# last changed : 06 Aug 2008
# Copyright    : ###COPYRIGHTHOLDER###
# eMail        : ###CONTACT###
# Version      : 0.00.010 
#   
#--------------------------------------------------------------------------*
# ###COPYRIGHT###
#--------------------------------------------------------------------------*
from System import *
from Torcs import *
from RobotTools import *

class TPathPt(object):
	def __init__(self):
 # Section # Lane specific center # Curvature in xy # Curvature in z direction... e.g. bumps # Offset from centre point # Actual point (same as CalcPt()) # Max speed through this point # Speed through this point (braking only) # Speed through this point, with modelled accel # Predicted height of car above track (flying) # Buffer from left for safety # Buffer from right for safety # Cuvature comming next # Lane specfic width to left # Lane specfic width to right  # Lane specfic width to left # Lane specfic width to right 
	def Dist(self):
		return self._Sec.DistFromStart

	def WtoL(self):
		return self._WToL

	def WtoR(self):
		return self._WToR

	def Pt(self):
		return self._Center

	def Norm(self):
		return self._Sec.ToRight

	def CalcPt(self):
		return self._Center + self._Sec.ToRight * self._Offset

class TLane(object): # Copy of car params # Length of track # Nbr of PathPoints # Points in this lane
	# Default constructor
	def __init__(self, count, Track):
		self._Length = Track.length
		self._Count = count
		self._oPathPoints = Array.CreateInstance(TPathPt, self._Count)

	# Set operator (Sets lane)
	# ORIGINAL LINE: TLane& TLane::operator = (const TLane& Lane)
	# C++ TO C# CONVERTER NOTE: This 'CopyFrom' method was converted from the original C++ copy assignment operator:
	def CopyFrom(self, Lane):
		self.SetLane(Lane)
		return self

	# Set lane
	def SetLane(self, Lane):
		self._oCarParam = Lane.oCarParam
		self._Count = Lane.Count
		self._oPathPoints = Array.CreateInstance(TPathPt, self._Count)
		# The memory management function 'memcpy' has no equivalent in C#:
		# memcpy(oPathPoints, Lane.oPathPoints, Count * sizeof(*oPathPoints));
		I = 0
		while I < self._Count:
			self._oPathPoints[I] = Lane.oPathPoints[I]
			I += 1

	# Check wether position is in lane
	def ContainsPos(self, TrackPos):
		if TrackPos > 0.0: # Use parameter
			return True
		else: # Allways true because # this lane type
			return True
 # contains all points
	# Get information to the point nearest the given position
	def GetLanePoint(self, TrackPos, IndexFromTrackPos, LanePoint):
		Idx0 = IndexFromTrackPos
		Idxp = (Idx0 - 1 + self._Count) % self._Count
		Idx1 = (Idx0 + 1) % self._Count
		Idx2 = (Idx0 + 2) % self._Count
		Dist0 = self._oPathPoints[Idx0].Dist()
		Dist1 = self._oPathPoints[Idx1].Dist()
		if Idx1 == 0:
			Dist1 = self._Length
		P0 = self._oPathPoints[Idxp].CalcPt()
		P1 = self._oPathPoints[Idx0].CalcPt()
		P2 = self._oPathPoints[Idx1].CalcPt()
		P3 = self._oPathPoints[Idx2].CalcPt()
		Crv1 = TUtils.CalcCurvatureXY(P0, P1, P2)
		Crv2 = TUtils.CalcCurvatureXY(P1, P2, P3)
		Tx = (TrackPos - Dist0) / (Dist1 - Dist0)
		LanePoint.Index = Idx0
		LanePoint.Crv = (1.0 - Tx) * Crv1 + Tx * Crv2
		LanePoint.T = Tx
		LanePoint.Offset = (self._oPathPoints[Idx0].Offset) + Tx * (self._oPathPoints[Idx1].Offset - self._oPathPoints[Idx0].Offset)
		Ang0 = TUtils.VecAngXY(self._oPathPoints[Idx1].CalcPt() - self._oPathPoints[Idx0].CalcPt())
		Ang1 = TUtils.VecAngXY(self._oPathPoints[Idx2].CalcPt() - self._oPathPoints[Idx1].CalcPt())
		DeltaAng = Ang1 - Ang0
		RT.DoubleNormPiPi()
		LanePoint.Angle = Ang0 + LanePoint.T * DeltaAng
		Tang1 = TVector2D()
		Tang2 = TVector2D()
		TUtils.CalcTangent(P0, P1, P2, )
		TUtils.CalcTangent(P1, P2, P3, )
		Dir = TUtils.VecUnit(Tang1) * (1 - Tx) + TUtils.VecUnit(Tang2) * Tx
		Ang0 = TUtils.VecAngle(Tang1)
		Ang1 = TUtils.VecAngle(Tang2)
		DeltaAng = Ang1 - Ang0
		RT.DoubleNormPiPi()
		LanePoint.Speed = self._oPathPoints[LanePoint.Index].Speed + (self._oPathPoints[Idx1].Speed - self._oPathPoints[LanePoint.Index].Speed) * LanePoint.T
		LanePoint.AccSpd = self._oPathPoints[LanePoint.Index].AccSpd + (self._oPathPoints[Idx1].AccSpd - self._oPathPoints[LanePoint.Index].AccSpd) * LanePoint.T
		return True

	# Initialize lane from track limiting width to left and right
	def Initialise(self, Track, CarParam, MaxLeft, MaxRight):
		self._Length = Convert.ToSingle(Track.Length())
		self._Count = Track.Count()
		self._oPathPoints = Array.CreateInstance(TPathPt, self._Count)
		self._oCarParam = CarParam # Copy car params
		if MaxLeft < 999.0:
			W = Track.Width() / 4
			I = 0
			while I < self._Count:
				Sec = Track.Section(I)
				self._oPathPoints[I].Sec = Sec
				self._oPathPoints[I].Center = Sec.Center
				self._oPathPoints[I].Crv = 0
				self._oPathPoints[I].CrvZ = 0
				self._oPathPoints[I].Offset = 0.0f
				self._oPathPoints[I].Point = self._oPathPoints[I].CalcPt()
				self._oPathPoints[I].MaxSpeed = 10
				self._oPathPoints[I].Speed = 10
				self._oPathPoints[I].AccSpd = 10
				self._oPathPoints[I].FlyHeight = 0
				self._oPathPoints[I].BufL = 0
				self._oPathPoints[I].BufR = 0
				self._oPathPoints[I].NextCrv = 0.0
				self._oPathPoints[I].WToL = -0.5
				self._oPathPoints[I].WToR = Sec.WidthToRight
				self._oPathPoints[I].WPitToL = Sec.PitWidthToLeft
				self._oPathPoints[I].WPitToR = Sec.PitWidthToRight
				self._oPathPoints[I].Fix = False
				I += 1
		elif MaxRight < 999.0:
			W = Track.Width() / 4
			I = 0
			while I < self._Count:
				Sec = Track.Section(I)
				self._oPathPoints[I].Sec = Sec
				self._oPathPoints[I].Center = Sec.Center
				self._oPathPoints[I].Crv = 0
				self._oPathPoints[I].CrvZ = 0
				self._oPathPoints[I].Offset = 0.0f
				self._oPathPoints[I].Point = self._oPathPoints[I].CalcPt()
				self._oPathPoints[I].MaxSpeed = 10
				self._oPathPoints[I].Speed = 10
				self._oPathPoints[I].AccSpd = 10
				self._oPathPoints[I].FlyHeight = 0
				self._oPathPoints[I].BufL = 0
				self._oPathPoints[I].BufR = 0
				self._oPathPoints[I].NextCrv = 0.0
				self._oPathPoints[I].WToL = Sec.WidthToLeft
				self._oPathPoints[I].WToR = -0.5
				self._oPathPoints[I].WPitToL = Sec.PitWidthToLeft
				self._oPathPoints[I].WPitToR = Sec.PitWidthToRight
				self._oPathPoints[I].Fix = False
				I += 1
		else:
			I = 0
			while I < self._Count:
				Sec = Track.Section(I)
				self._oPathPoints[I].Sec = Sec
				self._oPathPoints[I].Center = Sec.Center
				self._oPathPoints[I].Crv = 0
				self._oPathPoints[I].CrvZ = 0
				self._oPathPoints[I].Offset = 0.0f
				self._oPathPoints[I].Point = self._oPathPoints[I].CalcPt()
				self._oPathPoints[I].MaxSpeed = 10
				self._oPathPoints[I].Speed = 10
				self._oPathPoints[I].AccSpd = 10
				self._oPathPoints[I].FlyHeight = 0
				self._oPathPoints[I].BufL = 0
				self._oPathPoints[I].BufR = 0
				self._oPathPoints[I].NextCrv = 0.0
				self._oPathPoints[I].WToL = Sec.WidthToLeft
				self._oPathPoints[I].WToR = Sec.WidthToRight
				self._oPathPoints[I].WPitToL = Sec.PitWidthToLeft
				self._oPathPoints[I].WPitToR = Sec.PitWidthToRight
				self._oPathPoints[I].Fix = False
				I += 1
		self.CalcCurvaturesXY(1)
		self.CalcCurvaturesZ(1)

	# Get path point from index
	def PathPoints(self, Index):
		return self._oPathPoints[Index]

	# Calc curvature in XY
	def CalcCurvaturesXY(self, Start, Step):
		I = 0
		while I < self._Count:
			P = (Start + I) % self._Count # Point
			Pp = (P - Step + self._Count) % self._Count # Prev Point
			Pn = (P + Step) % self._Count # Next Point
			self._oPathPoints[P].Crv = TUtils.CalcCurvatureXY(self._oPathPoints[Pp].CalcPt(), self._oPathPoints[P].CalcPt(), self._oPathPoints[Pn].CalcPt())
			I += 1

	# Calc curvature in Z
	def CalcCurvaturesZ(self, Start, Step):
		Step *= 3
		I = 0
		while I < self._Count:
			P = (Start + I) % self._Count # Point
			Pp = (P - Step + self._Count) % self._Count # Prev Point
			Pn = (P + Step) % self._Count # Next Point
			self._oPathPoints[P].CrvZ = 6 * TUtils.CalcCurvatureZ(self._oPathPoints[Pp].CalcPt(), self._oPathPoints[P].CalcPt(), self._oPathPoints[Pn].CalcPt())
			I += 1

	# Calc max possible speed depending on car modell
	def CalcMaxSpeeds(self, Start, Len, Step):
		I = 0
		while I < Len:
			P = (Start + I) % self._Count
			TrackRollAngle = Math.Atan2(self._oPathPoints[P].Norm().z, 1)
			Friction = 
			Speed = self._oCarParam.CalcMaxSpeed(, self._oPathPoints[P].Crv, self._oPathPoints[P].CrvZ, Friction, TrackRollAngle)
			self._oPathPoints[P].MaxSpeed = Speed
			self._oPathPoints[P].Speed = Speed
			self._oPathPoints[P].AccSpd = Speed
			I += Step

	# Propagate braking
	def PropagateBreaking(self, Start, Len, Step):
		I = Step * ((2 * Len - 1) / Step)
		while I >= 0:
			P = (Start + I) % self._Count
			Q = (P + Step) % self._Count
			if self._oPathPoints[P].Speed > self._oPathPoints[Q].Speed:
				# see if we need to adjust spd[i] to make it possible
				#   to slow to spd[j] by the next seg.
				Delta = self._oPathPoints[P].CalcPt() - self._oPathPoints[Q].CalcPt()
				Dist = TUtils.VecLenXY(Delta)
				K = (self._oPathPoints[P].Crv + self._oPathPoints[Q].Crv) * 0.5
				if Math.Abs(K) > 0.0001:
					Dist = 2 * Math.Asin(0.5 * Dist * K) / K
				TrackRollAngle = Math.Atan2(self._oPathPoints[P].Norm().z, 1)
				Friction = 
				U = self._oCarParam.CalcBraking(, self._oPathPoints[P].Crv, self._oPathPoints[P].CrvZ, self._oPathPoints[Q].Crv, self._oPathPoints[Q].CrvZ, self._oPathPoints[Q].Speed, Dist, Friction, TrackRollAngle)
				if self._oPathPoints[P].Speed > U:
					self._oPathPoints[P].Speed = self._oPathPoints[P].AccSpd = U
				if self._oPathPoints[P].FlyHeight > 0.1:
					self._oPathPoints[P].Speed = self._oPathPoints[Q].Speed
			I -= Step

	# Propagate acceleration
	def PropagateAcceleration(self, Start, Len, Step):
		I = 0
		while I < 2 * Len:
			Q = (Start + I + self._Count) % self._Count
			P = (Q - Step + self._Count) % self._Count
			if Q == 0:
				P = (self._Count - 3)
			if self._oPathPoints[P].AccSpd < self._oPathPoints[Q].AccSpd:
				# see if we need to adjust spd[Q] to make it possible
				#   to speed up to spd[P] from spd[Q].
				Dist = TUtils.VecLenXY(self._oPathPoints[P].CalcPt() - self._oPathPoints[Q].CalcPt())
				K = (self._oPathPoints[P].Crv + self._oPathPoints[Q].Crv) * 0.5
				if Math.Abs(K) > 0.0001:
					Dist = 2 * Math.Asin(0.5 * Dist * K) / K
				TrackRollAngle = Math.Atan2(self._oPathPoints[P].Norm().z, 1)
				Friction = 
				V = self._oCarParam.CalcAcceleration(self._oPathPoints[P].Crv, self._oPathPoints[P].CrvZ, self._oPathPoints[Q].Crv, self._oPathPoints[Q].CrvZ, self._oPathPoints[P].AccSpd, Dist, Friction, TrackRollAngle)
				#if (oPathPoints[Q].AccSpd > V)
				self._oPathPoints[Q].AccSpd = Math.Min(V, self._oPathPoints[Q].Speed)
			I += Step

	# Calculate curvature in XY
	def CalcCurvaturesXY(self, Step):
		self.CalcCurvaturesXY(0, Step)

	# Calculate curvature in Z
	def CalcCurvaturesZ(self, Step):
		self.CalcCurvaturesZ(0, Step)

	# Calculate max possible speed
	def CalcMaxSpeeds(self, Step):
		self.CalcMaxSpeeds(0, self._Count, Step)

	# Propagate breaking
	def PropagateBreaking(self, Step):
		self.PropagateBreaking(0, self._Count, Step)

	# Propagate acceleration
	def PropagateAcceleration(self, Step):
		self.PropagateAcceleration(0, self._Count, Step)

	# Calculate forward absolute curvature
	def CalcFwdAbsCrv(self, Range, Step):
		N = self._Count - 1
		count = Range / Step
		P = count * Step
		Q = P
		TotalCrv = 0
		while P > 0:
			TotalCrv += self._oPathPoints[P].Crv
			P -= Step
		self._oPathPoints[0].NextCrv = TotalCrv / count
		TotalCrv += Math.Abs(self._oPathPoints[0].Crv)
		TotalCrv -= Math.Abs(self._oPathPoints[Q].Crv)
		P = (N / Step) * Step
		Q -= Step
		if Q < 0:
			Q = (N / Step) * Step
		while P > 0:
			self._oPathPoints[P].NextCrv = TotalCrv / count
			TotalCrv += Math.Abs(self._oPathPoints[P].Crv)
			TotalCrv -= Math.Abs(self._oPathPoints[Q].Crv)
			P -= Step
			Q -= Step
			if Q < 0:
				Q = (N / Step) * Step

	# Calculate estimated time
	def CalcEstimatedTime(self, Start, Len):
		TotalTime = 0
		I = 0
		while I < Len:
			P = (Start + I) % self._Count
			Q = (P + 1) % self._Count
			Dist = TUtils.VecLenXY(self._oPathPoints[P].CalcPt() - self._oPathPoints[Q].CalcPt())
			TotalTime += Dist / ((self._oPathPoints[P].AccSpd + self._oPathPoints[Q].AccSpd) * 0.5)
			I += 1
		return TotalTime

	# Calculate estimated lap time
	def CalcEstimatedLapTime(self):
		LapTime = 0
		I = 0
		while I < self._Count:
			Q = (I + 1) % self._Count
			Dist = TUtils.VecLenXY(self._oPathPoints[I].CalcPt() - self._oPathPoints[Q].CalcPt())
			LapTime += Dist / ((self._oPathPoints[I].AccSpd + self._oPathPoints[Q].AccSpd) * 0.5)
			I += 1
		return LapTime
