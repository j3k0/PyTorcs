# TorcsInterfaces.cs created with MonoDevelop
# User: jeko at 10:19 AM 7/13/2008
# Reworked to get a unique Vector2D and Vector3D struct for 
# OgreDotNet and Robot code and have same names, functions and 
# operators for TVector2D and TVector3D as long as possible
# Uses now Matrix4 and Matrix3 from OgreDotNet with (Vector3 = TVector3D)
# If tested that OgreDotNet works with this code Vector2/Vector3 
# should be replaced by TVector2D/3D renamed to Vector2/3 
# to have one Math name space for all
from System import *
from System.Runtime.InteropServices import *
from Math3D import *
# Constants and Conversions used from TORCS, SharpyCs AND wrapper ...
# tgf.h,v 1.41 2005/08/05 09:22:00
class C(object):
	# This class only contains static data and members
	# Prevent compiler from generationg a default constructor
	def __init__(self):
		# Common constants as defined by TORCS
		self._G = 9.80665f
		self._PI = 3.14159265358979323846
		# Common conversion constants as defined by TORCS
		self._rads2Rpm = 9.549296585
		self._rpm2Rads = 0.104719755
		self._rad2Deg = 180.0 / self._PI
		self._deg2Rad = self._PI / 180.0
		self._feet2M = 0.304801
		# Common conversions
		# TORCS related stuff ...
		self._simTimeStep = 0.02
		# Race state:
		# raceman.h v 1.28 2006/02/20 20:17:43
		self._rmRaceRunning = 0x00000001
		self._rmRaceFinishing = 0x00000002
		self._rmRaceEnded = 0x00000004
		self._rmRaceStarting = 0x00000008
		self._rmRacePrestart = 0x00000010
		self._rmRacePaused = 0x40000000
		# Race type:
		self._rmTypePractice = 0
		self._rmTypeQualif = 1
		self._rmTypeRace = 2
		#
		# Track segment:
		#
		# Geometrical type:
		self._trRgt = 1 # Right curve 
		self._trLft = 2 # Left curve 
		self._trStr = 3 # Straight 
		# Position type
		self._trMain = 1 # Main track segment (ie road part)
		self._trLSide = 2 # Left side segment (outer segment) 
		self._trRSide = 3 # Right side segment (outer seg.)
		self._trLBorder = 4 # Left border segment (inner seg.)
		self._trRBorder = 5 # Right border segment (inner seg.)
		# Border and barrier segments style:
		self._trPlan = 0 # Flat (border only)
		self._trCurb = 1 # Curb (border only)
		self._trWall = 2 # Wall (barrier only)
		self._trFende = 3 # Fence (no width) (ba. only)
		self._trPitBuilding = 4 # Pit building wall (ba. only)
		# Coord of the 4 corners of the segment:
		self._trSL = 0 # Start-Left corner 
		self._trSR = 1 # Start-Right corner
		self._trEL = 2 # End-Left corner 
		self._trER = 3 # End_Right corner 
		# Rotation angles of the track in rad anti-clockwise:
		self._trZS = 0 # Z Start angle 
		self._trZE = 1 # Z End angle 
		self._trYL = 2 # Y Left angle
		self._trYR = 3 # Y Right angle
		self._trXS = 4 # X Start angle
		self._trXE = 5 # X End angle 
		self._trCS = 6 # Center start angle 
		# Type of segment regarding the race:
		self._trNormal = 0x00000000 # Normal segment 
		self._trLast = 0x00000001 # S. before start line
		self._trStart = 0x00000002 # S. after start line
		self._trPitLane = 0x00000004 # Pit lane segment 
		self._trSpeedLimit = 0x00000008 # S.'s speed is limited 
		self._trPitEntry = 0x00000010 # S. pitlane cr. track
		self._trPitExit = 0x00000020 # S. pitlane cr. track 
		self._trPit = 0x00000040 # Car pit 
		self._trPitStart = 0x00000080 # Car pit Star
		self._trPitEnd = 0x00000100 # Car pit End
		self._trSideRgt = 0
		self._trSideLft = 1
		# ... Track segment
		# Location on the track in local coordinates: Description 
		# car.h,v 1.37 2006/10/12 22:19:22
		self._trLPosMain = 0 # Relative to main segment
		self._trLPosSegment = 1 # If on a side, rel. to side
		self._trLPosTrack = 2 # Local pos incl. all t.width
		# Public info on the cars: States
		# car.h,v 1.37 2006/10/12 22:19:22
		self._rmCarStateFinish = 0x00000100 # Car having passed the finish line
		self._rmCarStatePit = 0x00000001 # Car currently stopped in pits 
		self._rmCarStateDidNotFinish = 0x00000002 # Car did not finish
		self._rmCarStatePullUp = 0x00000004 # Car pulled out in the air
		self._rmCarStatePullSide = 0x00000008 # Car pulled out in the air 
		self._rmCarStatePullDown = 0x00000010 # Car pulled out in the air 
		self._rmCarStateOut = (self._rmCarStateDidNotFinish | self._rmCarStateFinish)
		self._rmCarStateNoSimu = 0x000000FF # Do not simulate the car
		self._rmCarStateBroken = 0x00000200 # Engine no more working
		self._rmCarStateOutOfGas = 0x00000400 # Out of Gas
		self._rmCarStateEliminated = 0x00000800 # Eliminated due to rules infringement
		self._rmCarStateSimuNoMove = 0x00010000 # Simu. without car move (i.e. clutch applied and no wheel move)
		# Designation 
		self._FrntRgt = 0 # front right 
		self._FrntLft = 1 # front left
		self._RearRgt = 2 # rear right
		self._RearLft = 3 # rear left 
		self._Frnt = 0 # front 
		self._Rear = 1 # rear 
		self._Right = 0 # right
		self._Left = 1 # left 
		# Wrapper commands: Info returned by driver during the race
		# Values defined by TORCS: 
		self._rmLightHead1 = 0x00000001 # head light 1 
		self._rmLightHead2 = 0x00000002 # head light 2  # head light 1 + 2 
		self._rmLightHeadL = (self._rmLightHead1 | self._rmLightHead2)
		# Pitting:
		# track.h,v 1.22 2006/02/20 20:19:04
		self._trPitMaxCarPerPit = 4 # maximum cars per pit
		# robot.h,v 1.10 2006/02/20 20:18:07
		self._robPitIm = 0 # Immediate return from pit com.
		self._robPitMenu = 1 # Call the interactive menu 
		# car.h,v 1.37 2006/10/12 22:19:22
		self._rmPitRepair = 0 # Do repair
		self._rmPitStopAndGo = 1 # Do stop and go
		# ... TORCS related stuff
		# Sharpy related stuff ...
		self._ABSdelta = 0.5f
		self._ABSscale = 0.5f
		self._BackCollDist = 70.0f
		self._CatchFactor = 1.1f
		self._ClutchMax = 0.5f
		self._ClutchDelta = 0.05f
		self._ClutchRange = 0.8f
		self._FrontCollDist = 200.0f
		self._LengthMargin = 3.0f
		self._MaxBrakePress = 0.91f
		self._SideMargin = 1.0f
		self._SpeedPassMargin = 5.0f
		self._ScaleBrake = 0.8f
		self._ScaleFriction = 0.8f
		self._TCLslip = 2.0f
		self._TCLrange = 10.0f

	def Rads2Rpm(value):
		return value * self._rads2Rpm

	Rads2Rpm = staticmethod(Rads2Rpm)

	def Rpm2Rads(value):
		return value * self._rpm2Rads

	Rpm2Rads = staticmethod(Rpm2Rads)

	def Rad2Deg(value):
		return value * self._rad2Deg

	Rad2Deg = staticmethod(Rad2Deg)

	def Deg2Rad(value):
		return value * self._deg2Rad

	Deg2Rad = staticmethod(Deg2Rad)

	def Feet2M(value):
		return value * self._feet2M

	Feet2M = staticmethod(Feet2M)

class TSituation(object):
	def __init__(self):

	# ... Sharpy related stuff
	# Current situation
	# raceman.h v 1.28 2006/02/20 20:17:43 # Number of cars # Total laps to race # Race state # Race type # Max. allowed dammage # Frames per second # HACK: GCC align doubles on 64 bit addresses. # Time since last call # Current time in sec # Number of human player
class TPoint3D(object): # List of cars
	# 3D Point (with tdble = float = Single coordinates)
	# tgf.h,v 1.41 2005/08/05 09:22:00
	# Some basics for linear algebra 
	# Rework in progress
	#[Serializable()]  # x coordinate  # y coordinate  # z coordinate  # Constructors
	# Copy constructor
	def __init__(self, x, y, z):
		# Constructor
		self._x = x
		self._y = y
		self._z = z

	def __init__(self, x, y, z):
		self._x = x
		self._y = y
		self._z = z

class TVector2D(object):
	# 2D Vector (with tdble = float = Single coordinates)
	# sg.h v 1.3 2005/02/01 15:36:04
	# Some basics for linear algebra 
	# Reworked to get a unique Vector2D struct for OgreDotNet and 
	# Robot code and have same names, functions and operators for 
	# TVector2D and TVector3D as long as possible
	#[Serializable()]  # x dimension # y dimension # Constructors
	# Copy constructor
	def __init__(self, p):
		self._zeroVector = TVector2D(0.0f, 0.0f)
		self._unitX = TVector2D(1.0f, 0.0f)
		self._unitY = TVector2D(0.0f, 1.0f)
		self._negativeUnitX = TVector2D(-1.0f, 0.0f)
		self._negativeUnitY = TVector2D(0.0f, -1.0f)
		self._unitVector = TVector2D(1.0f, 1.0f)
		# Constructor
		# Constructor from 3D vectors projection into x-y 
		# Constructor from 3D points projection into x-y 
		self._x = p.x
		self._y = p.y

	def __init__(self, p):
		self._zeroVector = TVector2D(0.0f, 0.0f)
		self._unitX = TVector2D(1.0f, 0.0f)
		self._unitY = TVector2D(0.0f, 1.0f)
		self._negativeUnitX = TVector2D(-1.0f, 0.0f)
		self._negativeUnitY = TVector2D(0.0f, -1.0f)
		self._unitVector = TVector2D(1.0f, 1.0f)
		self._x = p.x
		self._y = p.y

	def __init__(self, p):
		self._zeroVector = TVector2D(0.0f, 0.0f)
		self._unitX = TVector2D(1.0f, 0.0f)
		self._unitY = TVector2D(0.0f, 1.0f)
		self._negativeUnitX = TVector2D(-1.0f, 0.0f)
		self._negativeUnitY = TVector2D(0.0f, -1.0f)
		self._unitVector = TVector2D(1.0f, 1.0f)
		self._x = p.x
		self._y = p.y

	def __init__(self, p):
		self._zeroVector = TVector2D(0.0f, 0.0f)
		self._unitX = TVector2D(1.0f, 0.0f)
		self._unitY = TVector2D(0.0f, 1.0f)
		self._negativeUnitX = TVector2D(-1.0f, 0.0f)
		self._negativeUnitY = TVector2D(0.0f, -1.0f)
		self._unitVector = TVector2D(1.0f, 1.0f)
		self._x = p.x
		self._y = p.y
 # Add to this vector
	def Add(self, rhs):
		self._x += rhs.x
		self._y += rhs.y

	# Add two vectors
	def Add(lhs, rhs):
		return lhs + rhs

	Add = staticmethod(Add)

	# Add two vectors operator # Check this vector being equal to vector v
	def Equal(self, vector):
		return self == vector

	# Check two vectors being equal
	# Check this vector being unequal to vector v
	def Unequal(self, vector):
		return self != vector

	# Check two vectors being unequal
	# Check vector lhs being greater vector rhs in all components
	# Check vector lhs being smaller vector rhs in all components
	# Overrides the Object.ToString() method to provide a text 
	# representation of a TVector2D
	def ToString(self):
		return str.Format("TVector2D({0}, {1})", self._x, self._y)

	# Provides a unique hash code based on the member variables
	# This should be done because the equality operators (==, !=)
	# have been overriden.
	# The standard implementation is a simple XOR operation 
	# between all local member variables.
	def GetHashCode(self):
		return self._x.GetHashCode() ^ (self._y.GetHashCode())

	# Compares this Vector to another object.  
	# This should be done because the equality operators 
	# (==, !=) have been overriden.
	def Equals(self, obj):
		if :
			return (self == obj)
		else:
			return False
 # Get Length of this vector
	def get_Length(self):
		return Convert.ToSingle(Math.Sqrt(self._x * self._x + self._y * self._y))

	Length = property(fget=get_Length)

	# Get square of length of this vector
	def get_LengthSquared(self):
		return Convert.ToSingle(self._x * self._x + self._y * self._y)

	LengthSquared = property(fget=get_LengthSquared)

	# Get Length of a vector
	def LengthOf(vector):
		return vector.Length

	LengthOf = staticmethod(LengthOf)

	# Get square of length of a vector
	def LengthSquaredOf(vector):
		return vector.LengthSquared

	LengthSquaredOf = staticmethod(LengthSquaredOf)
 # Scale this vector with scalar factor
	def Multiply(self, factor):
		self._x *= factor
		self._y *= factor

	# Multiply vector with scalar 
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply scalar with vector
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply vector with scalar operator
	# Multiply scalar with vector operator
	# Multiply vector with vector
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply vector with vector operator # Divide this vector by scalar factor
	def Divide(self, factor):
		self._x /= factor
		self._y /= factor

	# Divide vector by scalar 
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide scalar by vector
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide vector by scalar operator
	# Divide scalar by vector operator
	# Divide vector by vector
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide vector by vector operator # Negate this vector
	def Negate(self):
		self._x *= -1.0f
		self._y *= -1.0f

	# Negate a vector
	def Negate(vector):
		return -vector

	Negate = staticmethod(Negate)

	# Negate a vector operator # normalize this vector
	def Normalize(self):
		d = self.Length
		if d > Single.Epsilon:
			self._x /= d
			self._y /= d

	# normalize a vector
	def Normalize(vector):
		d = vector.Length
		if d > Single.Epsilon:
			return TVector2D(vector.x / d, vector.y / d)
		else:
			return TVector2D(vector.x, vector.y)

	Normalize = staticmethod(Normalize)
 # Rotate this vector by arc around center
	def Rotate(self, center, arc):
		sinA = Math.Sin(arc)
		cosA = Math.Cos(arc)
		d.x = self._x - center.x
		d.y = self._y - center.y
		self._x = Convert.ToSingle(d.x * cosA - d.y * sinA)
		self._y = Convert.ToSingle(d.x * sinA + d.y * cosA)
		self._x += center.x
		self._y += center.y

	# Rotate a vector by arc around center
	def Rotate(vector, center, arc):
		sinA = Math.Sin(arc)
		cosA = Math.Cos(arc)
		d.x = vector.x - center.x
		d.y = vector.y - center.y
		return TVector2D(Convert.ToSingle(center.x + d.x * cosA - d.y * sinA), Convert.ToSingle(center.y + d.x * sinA + d.y * cosA))

	Rotate = staticmethod(Rotate)
 # Subtract from this vector
	def Subtract(self, rhs):
		self._x -= rhs.x
		self._y -= rhs.y

	# Subtract from two vectors
	def Subtract(lhs, rhs):
		return lhs - rhs

	Subtract = staticmethod(Subtract)

	# Substract two vectors operator # Performs a Dot Product operation on this vector and an other 
	def Dot(self, vector):
		dotProduct = 0.0f
		dotProduct += self._x * vector.x
		dotProduct += self._y * vector.y
		return dotProduct

	# Performs a Dot Product operation on two vectors 
	def Dot(self, lhs, rhs):
		dotProduct = 0.0f
		dotProduct += lhs.x * rhs.x
		dotProduct += lhs.y * rhs.y
		return dotProduct

class TVector3D(object):
	# 3D Vector (with tdble = float = Single coordinates)
	# sg.h v 1.3 2005/02/01 15:36:04
	# Some basics for linear algebra 
	# Reworked to get a unique Vector3D struct for OgreDotNet and 
	# Robot code and have same names, functions and operators for 
	# TVector2D and TVector3D as long as possible
	#[Serializable()]  # x dimension # y dimension # z dimension
	# Gets a TVector3D with all components set to 0.
	def get_Zero(self):
		return self._zeroVector

	Zero = property(fget=get_Zero)

	# Gets a TVector3D with all components set to 1.
	def get_UnitScale(self):
		return self._unitVector

	UnitScale = property(fget=get_UnitScale)

	# Gets a TVector3D with the X set to 1, and the others set to 0.
	def get_UnitX(self):
		return self._unitX

	UnitX = property(fget=get_UnitX)

	# Gets a TVector3D with the Y set to 1, and the others set to 0.
	def get_UnitY(self):
		return self._unitY

	UnitY = property(fget=get_UnitY)

	# Gets a TVector3D with the Z set to 1, and the others set to 0.
	def get_UnitZ(self):
		return self._unitZ

	UnitZ = property(fget=get_UnitZ)

	# Gets a TVector3D with the X set to -1, and the others set to 0.
	def get_NegativeUnitX(self):
		return self._negativeUnitX

	NegativeUnitX = property(fget=get_NegativeUnitX)

	# Gets a TVector3D with the Y set to -1, and the others set to 0.
	def get_NegativeUnitY(self):
		return self._negativeUnitY

	NegativeUnitY = property(fget=get_NegativeUnitY)

	# Gets a TVector3D with the Z set to -1, and the others set to 0.
	def get_NegativeUnitZ(self):
		return self._negativeUnitZ

	NegativeUnitZ = property(fget=get_NegativeUnitZ)
 # Constructors
	# Copy constructor
	def __init__(self, p):
		self._zeroVector = TVector3D(0.0f, 0.0f, 0.0f)
		self._unitX = TVector3D(1.0f, 0.0f, 0.0f)
		self._unitY = TVector3D(0.0f, 1.0f, 0.0f)
		self._unitZ = TVector3D(0.0f, 0.0f, 1.0f)
		self._negativeUnitX = TVector3D(-1.0f, 0.0f, 0.0f)
		self._negativeUnitY = TVector3D(0.0f, -1.0f, 0.0f)
		self._negativeUnitZ = TVector3D(0.0f, 0.0f, -1.0f)
		self._unitVector = TVector3D(1.0f, 1.0f, 1.0f)
		# Constructor
		# Constructor from 3D points projection into x-y 
		self._x = p.x
		self._y = p.y
		self._z = p.z

	def __init__(self, p):
		self._zeroVector = TVector3D(0.0f, 0.0f, 0.0f)
		self._unitX = TVector3D(1.0f, 0.0f, 0.0f)
		self._unitY = TVector3D(0.0f, 1.0f, 0.0f)
		self._unitZ = TVector3D(0.0f, 0.0f, 1.0f)
		self._negativeUnitX = TVector3D(-1.0f, 0.0f, 0.0f)
		self._negativeUnitY = TVector3D(0.0f, -1.0f, 0.0f)
		self._negativeUnitZ = TVector3D(0.0f, 0.0f, -1.0f)
		self._unitVector = TVector3D(1.0f, 1.0f, 1.0f)
		self._x = p.x
		self._y = p.y
		self._z = p.z

	def __init__(self, p):
		self._zeroVector = TVector3D(0.0f, 0.0f, 0.0f)
		self._unitX = TVector3D(1.0f, 0.0f, 0.0f)
		self._unitY = TVector3D(0.0f, 1.0f, 0.0f)
		self._unitZ = TVector3D(0.0f, 0.0f, 1.0f)
		self._negativeUnitX = TVector3D(-1.0f, 0.0f, 0.0f)
		self._negativeUnitY = TVector3D(0.0f, -1.0f, 0.0f)
		self._negativeUnitZ = TVector3D(0.0f, 0.0f, -1.0f)
		self._unitVector = TVector3D(1.0f, 1.0f, 1.0f)
		self._x = p.x
		self._y = p.y
		self._z = p.z
 # Add to this vector
	def Add(self, rhs):
		self._x += rhs.x
		self._y += rhs.y
		self._z += rhs.z

	# Add two vectors
	def Add(lhs, rhs):
		return lhs + rhs

	Add = staticmethod(Add)

	# Add two vectors operator # Check this vector being equal to vector v
	def Equal(self, vector):
		return self == vector

	# Check two vectors being equal
	# Check this vector being unequal to vector v
	def Unequal(self, vector):
		return self != vector

	# Check two vectors being unequal
	# Check vector lhs being greater vector rhs in all components
	# Check vector lhs being smaller vector rhs in all components
	# Overrides the Object.ToString() method to provide a text 
	# representation of a TVector3D
	def ToString(self):
		return str.Format("TVector3D({0}, {1}, {2})", self._x, self._y, self._z)

	# Provides a unique hash code based on the member variables
	# This should be done because the equality operators (==, !=)
	# have been overriden.
	# The standard implementation is a simple XOR operation 
	# between all local member variables.
	def GetHashCode(self):
		return self._x.GetHashCode() ^ (self._y.GetHashCode() ^ (~self._z.GetHashCode()))

	# Compares this Vector to another object.  
	# This should be done because the equality operators 
	# (==, !=) have been overriden.
	def Equals(self, obj):
		if :
			return (self == obj)
		else:
			return False
 # Get Length of this vector
	def get_Length(self):
		return Convert.ToSingle(Math.Sqrt(self._x * self._x + self._y * self._y + self._z * self._z))

	Length = property(fget=get_Length)

	# Get square of length of this vector
	def get_LengthSquared(self):
		return Convert.ToSingle(self._x * self._x + self._y * self._y + self._z * self._z)

	LengthSquared = property(fget=get_LengthSquared)

	# Get Length of a vector
	def LengthOf(vector):
		return vector.Length

	LengthOf = staticmethod(LengthOf)

	# Get square of length of a vector
	def LengthSquaredOf(vector):
		return vector.LengthSquared

	LengthSquaredOf = staticmethod(LengthSquaredOf)

	# Get Length of the x-y projection of a vector
	def LengthXY(vector):
		return Convert.ToSingle(Math.Sqrt(vector.x * vector.x + vector.y * vector.y))

	LengthXY = staticmethod(LengthXY)

	# Get square of length of the x-y projection of a vector
	def LengthXYSquared(vector):
		return Convert.ToSingle(vector.x * vector.x + vector.y * vector.y)

	LengthXYSquared = staticmethod(LengthXYSquared)
 # Scale this vector with scalar factor
	def Multiply(self, factor):
		self._x *= factor
		self._y *= factor
		self._z *= factor

	# Multiply vector with scalar 
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply scalar with vector
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply vector with scalar operator
	# Multiply scalar with vector operator
	# Multiply vector with scalar operator
	# Multiply scalar with vector operator
	# Multiply vector with vector
	def Multiply(lhs, rhs):
		return lhs * rhs

	Multiply = staticmethod(Multiply)

	# Multiply vector with vector operator # Divide this vector by scalar factor
	def Divide(self, factor):
		# get the inverse of the scalar up front to avoid doing multiple divides later
		inverse = 1.0f / factor
		self._x *= inverse
		self._y *= inverse
		self._z *= inverse

	# Divide vector by scalar 
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide scalar by vector
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide vector by scalar operator
	# get the inverse of the scalar up front to avoid doing multiple divides later
	# Divide scalar by vector operator
	# Divide vector by vector
	def Divide(lhs, rhs):
		return lhs / rhs

	Divide = staticmethod(Divide)

	# Divide vector by vector operator # Negate this vector
	def Negate(self):
		self._x *= -1.0f
		self._y *= -1.0f
		self._z *= -1.0f

	# Negate a vector
	def Negate(vector):
		return -vector

	Negate = staticmethod(Negate)

	# Negate a vector operator # normalize this vector
	def Normalize(self):
		d = self.Length
		if d > Single.Epsilon:
			self._x /= d
			self._y /= d
			self._z /= d

	# normalize a vector
	def Normalize(vector):
		d = vector.Length
		if d > Single.Epsilon:
			return TVector3D(vector.x / d, vector.y / d, vector.z / d)
		else:
			return TVector3D(vector.x, vector.y, vector.z)

	Normalize = staticmethod(Normalize)
 # Rotate this vector by arc around center in XY
	def RotateXY(self, center, arc):
		sinA = Math.Sin(arc)
		cosA = Math.Cos(arc)
		d.x = self._x - center.x
		d.y = self._y - center.y
		self._x = Convert.ToSingle(d.x * cosA - d.y * sinA)
		self._y = Convert.ToSingle(d.x * sinA + d.y * cosA)
		self._x += center.x
		self._y += center.y

	# Rotate a vector by arc around center in XY
	def RotateXY(vector, center, arc):
		sinA = Math.Sin(arc)
		cosA = Math.Cos(arc)
		d.x = vector.x - center.x
		d.y = vector.y - center.y
		return TVector3D(Convert.ToSingle(center.x + d.x * cosA - d.y * sinA), Convert.ToSingle(center.y + d.x * sinA + d.y * cosA), vector.z)

	RotateXY = staticmethod(RotateXY)
 # Subtract from this vector
	def Subtract(self, rhs):
		self._x -= rhs.x
		self._y -= rhs.y
		self._z -= rhs.z

	# Subtract from two vectors
	def Subtract(lhs, rhs):
		return lhs - rhs

	Subtract = staticmethod(Subtract)

	# Substract two vectors operator # 
	# // For later use with OgreDotNet
	# 
	# public static explicit operator Vector4 (TVector3D vector)
	# {
	# return new Vector4(vector.x, vector.y, vector.z, 1.0f);
	# }
	# 
	# // Used to access a Vector by index 0 = x, 1 = y, 2 = z.
	# // Uses unsafe pointer arithmetic to reduce the code required.
	# public float this[int index]
	# {
	# get
	# {
	# // using pointer arithmetic here for less code.
	# // Otherwise, we'd have a big switch statement.
	# unsafe
	# {
	# fixed(float* pX = &x)
	# return *(pX + index);
	# }
	# }
	# set
	# {
	# 
	# // using pointer arithmetic here for less code.
	# // Otherwise, we'd have a big switch statement.
	# unsafe
	# {
	# fixed(float* pX = &x)
	# *(pX + index) = value;
	# }
	# }
	# }
	#  # Performs a Dot Product operation on this vector and an other 
	def Dot(self, vector):
		dotProduct = 0.0f
		dotProduct += self._x * vector.x
		dotProduct += self._y * vector.y
		dotProduct += self._z * vector.z
		return dotProduct

	# Performs a Dot Product operation on two vectors 
	def Dot(self, lhs, rhs):
		dotProduct = 0.0f
		dotProduct += lhs.x * rhs.x
		dotProduct += lhs.y * rhs.y
		dotProduct += lhs.z * rhs.z
		return dotProduct
 # Performs a Cross Product operation on 2 vectors, which 
	# returns a vector that is perpendicular to the intersection 
	# of the 2 vectors.  Useful for finding face normals.
	def Cross(self, vector):
		cross = TVector3D()
		cross.x = (self._y * vector.z) - (self._z * vector.y)
		cross.y = (self._z * vector.x) - (self._x * vector.z)
		cross.z = (self._x * vector.y) - (self._y * vector.x)
		return cross

	# Finds a vector perpendicular to this one.
	def Perpendicular(self):
		result = self.Cross(TVector3D.UnitX)
		# check length
		if result.LengthSquared < Single.Epsilon:
			# This vector is the Y axis multiplied by a scalar, 
			# so we have to use another axis
			result = self.Cross(TVector3D.UnitY)
		return result

	# Calculates a reflection vector to the plane with the given normal.
	# Assumes this vector is pointing AWAY from the plane, invert if not.
	def Reflect(self, normal):
		return self - (2 * self.Dot(normal) * normal)

	# Finds the midpoint between the supplied Vector and this vector.
	def MidPoint(self, vector):
		return TVector3D((self._x + vector.x) * 0.5f, (self._y + vector.y) * 0.5f, (self._z + vector.z) * 0.5f)

	# Compares the supplied vector and updates it's 
	# x/y/z components of they are higher in value.
	def Ceil(self, compare):
		if compare.x > self._x:
			self._x = compare.x
		if compare.y > self._y:
			self._y = compare.y
		if compare.z > self._z:
			self._z = compare.z

	# Compares the supplied vector and updates it's 
	# x/y/z components of they are lower in value.
	def Floor(self, compare):
		if compare.x < self._x:
			self._x = compare.x
		if compare.y < self._y:
			self._y = compare.y
		if compare.z < self._z:
			self._z = compare.z

class TMatrix4x4(object):
	def __init__(self):

	# 
	# // For later use with OgreDotNet
	# // Gets the shortest arc quaternion to rotate this vector
	# // to the destination vector.
	# // Don't call this if you think the dest vector can be close
	# // to the inverse of this vector, since then ANY axis
	# // of rotation is ok.
	# public Quaternion GetRotationTo(TVector3D destination)
	# {
	# // Based on Stan Melax's article in Game Programming Gems
	# Quaternion q = new Quaternion();
	# 
	# TVector3D v0 = new TVector3D(this.x, this.y, this.z);
	# TVector3D v1 = destination;
	# 
	# // normalize both vectors
	# v0.Normalize();
	# v1.Normalize();
	# 
	# // get the cross product of the vectors
	# TVector3D c = v0.Cross(v1);
	# 
	# // If the cross product approaches zero, we get unstable because ANY axis will do
	# // when v0 == -v1
	# float d = v0.Dot(v1);
	# 
	# // If dot == 1, vectors are the same
	# if (d >= 1.0f)
	# {
	# return Quaternion.Identity;
	# }
	# 
	# float s = (float)Math.Sqrt( (1+d) * 2 );
	# float inverse = 1 / s;
	# 
	# q.x = c.x * inverse;
	# q.y = c.y * inverse;
	# q.z = c.z * inverse;
	# q.w = s * 0.5f;
	# 
	# return q;
	# }
	# 
	# 4x4 Matrix (with tdble = float = Single coordinates)
	# sg.h v 1.3 2005/02/01 15:36:04
	# Replaced by by a copy of Matrix4 using TVector3D  
class TPosition(object):
	def __init__(self):

	# Position (with tdble = float = float coordinates)
	# tgf.h,v 1.41 2005/08/05 09:22:00 # x coordinate  # y coordinate  # z coordinate  # angle along x axis  # angle along y axis 
class TMovement(object):
	def __init__(self):
 # angle along z axis 
	# Values of the cars current movement
	# tgf.h,v 1.41 2005/08/05 09:22:00 # position  # velocity 
class TCollisionState(object):
	def __init__(self):
 # acceleration
	# Collision state 
	# car.h,v 1.37 2006/10/12 22:19:22 # Collision counter # Position of collision
class TTrackSurface(object):
	def __init__(self):
 # Force of collision
	# Surface
	# track.h,v 1.22 2006/02/20 20:19:04 # Next surface in list # Type of material used  # Coefficient of friction  # Coefficient of energy restitution  # Rolling resistance  # Roughtness in m of the surface (wave height)  # Wave length in m of the surface 
class TTrackBarrier(object):
	def __init__(self):
 # Dammages in case of collision 
	# Barrier
	# track.h,v 1.22 2006/02/20 20:19:04 # Barrier style  # Barrier width  # Barrier height  # Barrier surface 
class TSegExt(object):
	def __init__(self):
 # Normal on the vertical 
	# track inside pointing 
	# towards the track middle.
	# Extended track segment
	# track.h,v 1.22 2006/02/20 20:19:04 # turn marks
class TRoadCam(object):
	def __init__(self):
 # marks array 
	# Road camera
	# track.h,v 1.22 2006/02/20 20:19:04
class TTrackOwnPit(object):
	def __init__(self):

	# Driver's pit
	# track.h,v 1.22 2006/02/20 20:19:04
	# TR_PIT_STATE_FREE   -1
	# TR_PIT_MAXCARPERPIT  4 maximum cars per pit # Center of the pit # Index of the car in
	# the car array below
	# which occupies the
	# pit. If the pit is
	# free the value is 
	# C.TR_PIT_STATE_FREE  # Pit. area len. min  # Pitting a. l. max  # Index of next free 
	# car entry (look at 
	# the next line) # Car links for pit
class TTrackSeg(object):
	def __init__(self):

	# Track segment 
	# car.h,v 1.37 2006/10/12 22:19:22
	# The segments can be straights (type TR_STR) 
	# or can be turn segments (type TR_RGT or TR_LFT): 
	# The reference angle is the orientation of the first segment 
	# of the track. # Segment name (char*) # Segment number  # Geometrical type # Position type # Border and barrier segments style: # Length meters (of middle of the track)  # Width of the segment  # Width of the beginning of the segment # Width of the end of the segment  # Length of begining of segment from starting line  # Radius in meters of the middle of the track (>0)  # Radius in meters of the right side of the track (>0) # Radius in meters of the left side of the track (>0) # Arc in rad of the curve (>0)  # Center of the curve  # Coord of the start left corner of the segment. # Coord of the start right corner of the segment. # Coord of the end left corner of the segment. # Coord of the end right corner of the segment.
	# rotation angles of the track in rad anti-clockwise: # Z Start rotation angle # Z End rotation angle # Y Left rotation angle # Y Right rotation angle # X Start rotation angle # X End rotation angle # Center start rotation angle
	# constants used to find the height of a point  # long constant  # width constant 
	# constant used to find the width of a segment  # find y along x  # normal to the right side in case of straight segment  # Environment mapping image index # Max height for curbs  # Type of segment regarding the race: # the factor to use in calculating DoV for this Seg 
	# pointers 
	# optional extensions  # Extended track segment # Segment surface # Segment barriers right # Segment barriers left # current camera  # Next segment  # Previous segment # segment at right side
class TTrkLocPos(object):
	def __init__(self):
 # segment at left side
	# Location on the track in local coordinates 
	# car.h,v 1.37 2006/10/12 22:19:22
	# Type of description: # Track segment # Type of description: # Distance to start of segment (or arc if turn)  # Distance to right side of segment (+ to inside of track - to outside)  # Distance to middle of segment (+ to left - to right) 
class TPublicCar(object):
	def __init__(self):
 # Distance to left side of segment (+ to inside of track - to outside)
	# Public info on the cars
	# car.h,v 1.37 2006/10/12 22:19:22 # GC data (car axis) # GC data (world axis)         # Position matrix  # Current track position. The segment is the track segment (not sides) # State of the car. # Position of the corners # Position of the corners # Position of the corners
class TTrackPitInfo(object):
	def __init__(self):
 # Position of the corners # Type of Pit: TR_PIT_NONE/TR_PIT_ON_TRACK_SIDE # max number of pits  # actual number of pits  # Pits side: TR_RGT/TR_LFT # Lenght of each pit stop  # Width of each pit stop # Speed limit between pitStart and pitEnd  # Pit lane segment  # Pit lane segment # Pit lane segment  # Pit lane segment  # List of pits by driver 
class TTurnMarksInfo(object):
	def __init__(self):
 # Number of drivers 
class TTrackGraphicInfo(object):
	def __init__(self):

class TTrack(object):
	def __init__(self):

	# track.h,v 1.22 2006/02/20 20:19:04 # Name of the track # Author's name # Filename of the track description # Parameters handle */ # Internal name of the track # Category of the track # Number of segments # Version of the track type # main track length # main track width # Pits information # Main track # Segment surface list
class TCarPenaltyLink(object):
	def __init__(self):
 # next penalty # previous penalty
# One penalty 
class TCarPenalty(object):
	def __init__(self):
 # penalty type # the lap before the penalty has to be cleared 
# 
class TCarPenaltyHead(object):
	def __init__(self):
 # First penalty  # Last penalty
# Public info on the race related to the cars
# car.h,v 1.37 2006/10/12 22:19:22
class TCarRaceInfo(object):
	def __init__(self):
 # tTrackOwnPit *pit;
class TWheelState(object):
	def __init__(self):
 # List of current penalties
	# Dynamic wheel information, data known only by the driver 
	# car.h,v 1.37 2006/10/12 22:19:22 # position relative to GC  # spin velocity rad/s  # brake temperature from 0 (cool) to 1.0 (hot)  # wheel state  # Track segment where the wheel is # rolling resistance, useful for sound 
class TPrivCar(object):
	def __init__(self):

	# Data known only by the driver 
	# car.h,v 1.37 2006/10/12 22:19:22 # Front right wheel's state  # Front left wheel's state  # Rear right wheel's state  # Rear left wheel's state  # Front right corner pos. # Front left corner pos. # Rear right corner pos. # Rear left corner pos. # Current gear # Remaining fuel (kg) # kg # kg/100km (>100 means infinity) # Engine's revolutions pre minute # Engine's  speed limiter: # Max. for Engine's revolutions # Revolutions at max torque # Revolutions at max power # Max torque # Max power # Reverse gear # Neutral gear # First gear #   the last gear depends on #   the car type #   get it from #   gearNb - gearOffset # # # # Incl reverse and neutral  # Offset (reverse and neutral gear) # Skid intensity front right # Skid intensity front left # Skid intensity rear right # Skid intensity rear left  # Reaction on wheel  front right  # Reaction on wheel front left # Reaction on wheel rear right # Reaction on wheel rear left # Number of collisions  # Smoke # Normal # Collision position, useful for sound # Dammage # ??
class TName(object):
	def __init__(self):
 # collision state 
	# Textbuffer
	# car.h,v 1.37 2006/10/12 22:19:22
class TWheelSpec(object):
	def __init__(self):

	# Wheels Specifications
	# car.h,v 1.37 2006/10/12 22:19:22 # Rim radius # Tire height # Tire width # Brake disk radius 
class TVisualAttributes(object):
	def __init__(self):
 # Overall wheel radius
	# Static visual attributes
	# car.h,v 1.37 2006/10/12 22:19:22 # Number of exhaust pipes (max 2) # Position of exhaust pipes  # Position of exhaust pipes 
class TInitCar(object):
	def __init__(self):
 # Power of the flames (from 1 to 3) 
	# Static Public info
	# car.h,v 1.37 2006/10/12 22:19:22
	# Values defined by TORCS: 
	#
	# stopType:
	# RM_PIT_REPAIR    Do repait
	# RM_PIT_STOPANDGO Do stop and go # Driver's name  # Team name # Car object name # Car's category # Car's race number  # Car's starting position  # Driver type  # Driver's skill level (0=rookie -> 3=pro)  # Red car color in leaders board  # Green Car color in leaders board  # Blue Car color in leaders board  # Car's mesures  # Driver's position #  Bonnet's position # Fuel tank capa  # Steer lock angle  # Static pos of GC (should be the 
	# origin of car axis)  # Wheels specifications  # Wheels specifications  # Wheels specifications  # Wheels specifications 
class TCarPitCmd(object):
	def __init__(self):
 # Visual attributes 
	# Command issued by the car during pit stop
	# robot.h,v 1.10 2006/02/20 20:18:07
	# Values defined by TORCS: 
	#
	# stopType:
	# RM_PIT_REPAIR    Do repait
	# RM_PIT_STOPANDGO Do stop and go
class TRobotItf(object):
	def __init__(self):

	# TORCS robot interface (Dummy)
	# robot.h,v 1.10 2006/02/20 20:18:07
	# Values defined by TORCS: 
	#
	# rbPitCmd Returns:
	# ROB_PIT_IM   Immediate return from pit command 
	# ROB_PIT_MENU Call the interactive menu for pit command # Called for every track change and/or new race  # Start a new race  # Drive during race  # Get the driver's pit commands # Called before the dll is unloaded 
class TCarCtrl(object):
	def __init__(self):
 # Index used if multiple interfaces 
	#
	# here will be other datatypes later
	#
	# TORCS commands: Info returned by driver during the race
	# car.h,v 1.37 2006/10/12 22:19:22 # Steer command [-1.0, 1.0]  # Accelerator command [0.0, 1.0] # Brake command [0.0, 1.0] # Clutch command [0.0, 1.0] # [-1,X] gear selection, X depends on car
class TWrapperCtrl(object):
	def __init__(self):
 # command issued by the driver
	# Wrapper commands: Info returned by driver during the race
	# Values defined by TORCS: 
class TCarData(object):
	def __init__(self):
 # Lights command 
	# here will be other commands later
	# Car structure: Parts of TCarElt
	# car.h,v 1.37 2006/10/12 22:19:22
	#        int   index;               // car index (saved in driver object)
	#        TInitCar info;             // public static data of car (") # public dynamic data of car # Alignment gap 
class TCarElt(object):
	def __init__(self):
 # public dynamic data of race
	#        TPrivCar priv;             // private dynamic data of car
	#        TCarCtrl ctrl;             // private commands
	#        TCarPitCmd pitcmd;         // private pit commands
	#        struct RobotItf *robot;    // private TORCS interface of wrapper
	#        struct CarElt *next;       // is null, so can not be used
	# Car structure: This is the main car structure, used everywhere
	# car.h,v 1.37 2006/10/12 22:19:22 # car index (saved in driver object) # public static data of car (") # public dynamic data of car # Alignment gap  # public dynamic data of race # private dynamic data of car # private commands # private pit commands # private TORCS interface of wrapper
class TScreen(object):
	def __init__(self):
 # is null, so can not be used
