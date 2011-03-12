#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# CarParam.cs
# Contains informations about the cars parameters
#--------------------------------------------------------------------------*
#
# file         : CarParam.cs
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

class TCarParam(object):
	# Tuning parameters # Scaling of usable MU # Scaling of Min MU for sides # Scaling of decelleration # Bump sensitivity # Bump sensitivity at outer side # Bump sensitivity at left side # Bump sensitivity at right side
	# Fix # Pointer to TORCS data of car # Buffer to inner # Buffer to outer # Aerodynamic downforce constant # Aerodynamic downforce constant front wing # Aerodynamic downforce ground effect # Aerodynamic downforce constant rear wing # Aerodynamic drag constant car body # Aerodynamic drag constant wings # Mass of car without fuel # Length of car (m) # Mu of tyres # Mu of front tyres # Mu of rear tyres # Width of car (m)
	# Changed while racing # Damage of this car # Mass of fuel in car # Mass of car with fuel # SC-Scaling
	# Default constructor
	def __init__(self):
		self._oScaleMu = 1.0
		self._oScaleMinMu = 0.8
		self._oScaleBrake = 1.0
		self._oScaleBump = 0
		self._oScaleBumpOuter = 0
		self._oScaleBumpLeft = 0
		self._oScaleBumpRight = 0
		self._oCar = None
		self._oBorderInner = 0.0
		self._oBorderOuter = 1.0
		self._oCa = 0
		self._oCaFrontWing = 0
		self._oCaGroundEffect = 0
		self._oCaRearWing = 0
		self._oCdBody = 0
		self._oCdWing = 0
		self._oEmptyMass = 0
		self._oLength = 4.5
		self._oTyreMu = 0
		self._oTyreMuFront = 0
		self._oTyreMuRear = 0
		self._oWidth = 2.0
		self._oDamage = 0
		self._oEmptyMass = 1000.0
		self._oFuel = 0
		self._oMass = 1000.0
		self._oSkill = 1.0

	# Initialize
	def Initialize(self, Car):
		self._oCar = Car

	# Calculate acceleration
	def CalcAcceleration(self, Crv0, Crvz0, Crv1, Crvz1, Speed, Dist, Friction, TrackRollAngle):
		MU = Friction * self._oTyreMu
		CD = self._oCdBody * (1.0 + self._oDamage / 10000.0) + self._oCdWing
		Crv = (Crv0 + Crv1) * 0.5
		Crvz = (Crvz0 + Crvz1) * 0.5
		if Crvz > 0:
			Crvz = 0
		Gdown = C.G * Math.Cos(TrackRollAngle)
		Glat = C.G * Math.Sin(TrackRollAngle)
		Gtan = 0 # TODO: track pitch angle.
		U = Speed
		V = U
		PAR_A = 0.001 # Parameters of a quadratic
		PAR_B = -0.25 # of X = speed in [m/s]
		PAR_C = 15.0 # Acc = (A*X+B)*X+C
		AccFromSpd = Quadratic(PAR_A, PAR_B, PAR_C)
		OldV = 0.0
		Count = 0
		while Count < 10:
			AvgV = (U + V) * 0.5
			AvgV2 = AvgV * AvgV
			Fdown = self._oMass * Gdown + (self._oMass * Crvz + self._oCa) * AvgV2
			Froad = Fdown * MU
			Flat = self._oMass * Glat
			Ftan = self._oMass * Gtan - CD * AvgV2
			Flatroad = Math.Abs(self._oMass * AvgV2 * Crv - Flat)
			if Flatroad > Froad:
				Flatroad = Froad
			Ftanroad = Math.Sqrt(Froad * Froad - Flatroad * Flatroad) + Ftan
			Acc = Ftanroad / self._oMass
			MaxAcc = Math.Min(11.5, AccFromSpd.CalcY(AvgV))
			if Acc > MaxAcc:
				Acc = MaxAcc
			Inner = Math.Max(0, U * U + 2 * Acc * Dist)
			V = Math.Sqrt(Inner)
			if Math.Abs(V - OldV) < 0.001:
				break
			OldV = V
			Count += 1
		return V

	# Calculate decceleration
	def CalcBraking(self, CarParam, Crv0, Crvz0, Crv1, Crvz1, Speed, Dist, Friction, TrackRollAngle):
		Friction *= 0.95
		Mu = Friction * self._oTyreMu
		# From TORCS:
		Cd = self._oCdBody * (1.0 + self._oDamage / 10000.0) + self._oCdWing
		Crv = (Crv0 + Crv1) * 0.5
		Crvz = (Crvz0 + Crvz1) * 0.5
		if Crvz > 0:
			Crvz = 0
		Gdown = C.G * Math.Cos(TrackRollAngle)
		Glat = C.G * Math.Sin(TrackRollAngle)
		Gtan = 0
		V = Speed
		U = V
		I = 0
		while I < 10:
			AvgV = (U + V) * 0.5
			AvgV2 = AvgV * AvgV
			Fdown = self._oMass * Gdown + (self._oMass * Crvz + self._oCa) * AvgV2
			Froad = Fdown * Mu
			Flat = self._oMass * Glat
			Ftan = self._oMass * Gtan - Cd * AvgV2
			Flatroad = Math.Abs(self._oMass * AvgV2 * Crv - Flat)
			if Flatroad > Froad:
				Flatroad = Froad
			Ftanroad = -Math.Sqrt(Froad * Froad - Flatroad * Flatroad) + Ftan
			Acc = CarParam.oScaleBrake * Ftanroad / (self._oMass * self._oSkill)
			Inner = Math.Max(0, V * V - 2 * Acc * Dist)
			OldU = U
			U = Math.Sqrt(Inner)
			if Math.Abs(U - OldU) < 0.001:
				break
			I += 1
		return U

	# Calculate maximum of speed
	def CalcMaxSpeed(self, CarParam, Crv, CrvZ, Friction, TrackRollAngle):
		# Here we calculate the theoretical maximum speed at a point on the
		# path. This takes into account the curvature of the path (crv), the
		# grip on the road (mu), the downforce from the wings and the ground
		# effect (CA), the tilt of the road (left to right slope) (sin)
		# and the curvature of the road in z (crvz).
		#
		# There are still a few silly fudge factors to make the theory match
		# with the reality (the car goes too slowly otherwise, aarrgh!).
		Cos = Math.Cos(TrackRollAngle)
		Sin = Math.Sin(TrackRollAngle)
		Cos *= Cos
		Sin *= Sin
		AbsCrv = Math.Max(0.001, Math.Abs(Crv))
		if Crv > 0:
			ScaleBump = CarParam.oScaleBumpLeft
		else:
			ScaleBump = CarParam.oScaleBumpRight
		Mu = Friction * self._oTyreMu * CarParam.oScaleMu / self._oSkill
		Den = (AbsCrv - ScaleBump * CrvZ) - self._oCa * Mu / self._oMass
		if Den < 0.00001:
			Den = 0.00001
		Speed = Math.Sqrt((Cos * C.G * Mu + Sin * C.G * Math.Sign(Crv)) / Den)
		if Speed > 150: # (100 m/s = 360 km/h)
			Speed = 150 # (150 m/s = 540 km/h)
		return Speed

	# Calculate maximum of speed
	def CalcMaxLateralF(self, Speed, Friction, Crvz):
		Fdown = self._oMass * C.G + (self._oMass * Crvz + self._oCa) * Speed * Speed
		return Fdown * Friction * self._oTyreMu

	# Calculate maximum of speed
	def CalcMaxSpeedCrv(self):
		#  const double MAX_SPD = 100; // 360 km/h
		MAX_SPD = 150 # 540 km/h
		return C.G * self._oTyreMu / (MAX_SPD * MAX_SPD)

	# Recalculation needed?
	def Needed(self, CarFuel, CarDamage):
		if (Math.Abs(self._oFuel - CarFuel) > 5) or (Math.Abs(self._oDamage - CarDamage) > 250):
			return True
		else:
			return False

	# Update
	def Update(self, CarFuel, CarDamage):
		self._oFuel = 5 * Math.Floor(CarFuel / 5)
		self._oMass = self._oEmptyMass + self._oFuel
		self._oDamage = CarDamage
