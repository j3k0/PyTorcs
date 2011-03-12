# Track.cs created with MonoDevelop
# User: jeko at 5:06 PM 7/19/2008
#
# Provide a C# interface to the structures found in C++ Torcs' "track.h"
#
# Summary of changes between C# and C++ interfaces:
#
# - Track segments are stored in an array (TrackSegList). Segment.id == index in the array.
# - TTrackSeg.type becomes TrackSeg.gtype (for Geometrical Type)
# - TTrackSeg.type2 becomes TrackSeg.ptype (for Position Type)
from System import *
from System.Collections.Generic import *
from System.Text import *
from System.Runtime.InteropServices import *

class SegGType(object):
	def __init__(self):

class SegPType(object):
	def __init__(self):
 # Main track segment (ie road part) # Left side segment (outer segment) # Right side segment (outer segment) # Left border segment (inner segment) # Right border segment (inner segment)
class SegStyle(object):
	def __init__(self):
 # Flat (border only) # Curb (border only) # Wall (barrier only) # Fence (no width) (barrier only) # Pit building wall (barrier only)
# <summary>Track Surface Definition</summary>
class TrackSurface(object): # Type of material used  # Coefficient of friction  # Coefficient of energy restitution  # Rolling resistance  # Roughtness in m of the surface (wave height)  # Wave length in m of the surface  # Dammages in case of collision 
	# Unsafe constructor for interface with C++
	def __init__(self, surf):
		self._kFriction = surf.kFriction
		self._kRebound = surf.kRebound
		self._kRollRes = surf.kRollRes
		self._kRoughness = surf.kRoughness
		self._kRoughWaveLen = surf.kRoughWaveLen
		self._kDammage = surf.kDammage

# <summary>Track Segment</summary>
#
# The segments can be straights (type TR_STR): (the track goes from the right to the left)
# Or can be turn segments (type TR_RGT or TR_LFT): (the track goes from the left to the right)
# The reference angle is the orientation of the first segment of the track.
class TrackSeg(object): # Segment name # Segment number  # Geometrical type # Position type # Border and barrier segments style: # Length meters (of middle of the track)  # Width of the segment  # Width of the beginning of the segment # Width of the end of the segment  # Length of begining of segment from starting line  # Radius in meters of the middle of the track (>0)  # Radius in meters of the right side of the track (>0) # Radius in meters of the left side of the track (>0) # Arc in rad of the curve (>0)  # Center of the curve  # Coord of the start left corner of the segment. # Coord of the start right corner of the segment. # Coord of the end left corner of the segment. # Coord of the end right corner of the segment.
	# rotation angles of the track in rad anti-clockwise: # Z Start rotation angle # Z End rotation angle # Y Left rotation angle # Y Right rotation angle # X Start rotation angle # X End rotation angle # Center start rotation angle
	# constants used to find the height of a point  # long constant  # width constant 
	# constant used to find the width of a segment  # find y along x  # normal to the right side in case of straight segment 
	# public readonly int envIndex;        // Environment mapping image index # Max height for curbs  # Type of segment regarding the race: # the factor to use in calculating DoV for this Seg 
	# pointers 
	# optional extensions 
	#public TSegExt* ext;        // Extended track segment
	#public TTrackBarrier* barrierR; // Segment barriers right
	#public TTrackBarrier* barrierL; // Segment barriers left
	#public TRoadCam *cam;       // current camera  # Where are the segment stored # Next segment # Previous segment # Segment at right side # Segment at left side
	# Next segment
	def get_next(self):
		return self._list[self.__next]

	next = property(fget=get_next)

	# Previous segment
	def get_prev(self):
		return self._list[self.__prev]

	prev = property(fget=get_prev)

	# True iff there a right side
	def get_hasRSide(self):
		return self.__rSide != -1

	hasRSide = property(fget=get_hasRSide)

	# Right side segment
	def get_rSide(self):
		return self._list[self.__rSide]

	rSide = property(fget=get_rSide)

	# True iff there a left side
	def get_hasLSide(self):
		return self.__lSide != -1

	hasLSide = property(fget=get_hasLSide)

	# Left side segment
	def get_lSide(self):
		return self._list[self.__lSide]

	lSide = property(fget=get_lSide)

	# Unsafe constructor for interface with C++
	def __init__(self, list, seg):
		self._list = list
		self._id = seg.id
		if seg.type == 1:
			self._gtype = SegGType.RIGHT
		elif seg.type == 2:
			self._gtype = SegGType.LEFT
		elif seg.type == 3:
			self._gtype = SegGType.STRAIGHT
		if seg.type2 == 1:
			self._ptype = SegPType.MAIN
		elif seg.type2 == 2:
			self._ptype = SegPType.LSIDE
		elif seg.type2 == 3:
			self._ptype = SegPType.RSIDE
		elif seg.type2 == 4:
			self._ptype = SegPType.LBORDER
		elif seg.type2 == 5:
			self._ptype = SegPType.RBORDER
		if seg.style == 0:
			self._style = SegStyle.PLAN
		elif seg.style == 1:
			self._style = SegStyle.CURB
		elif seg.style == 2:
			self._style = SegStyle.WALL
		elif seg.style == 3:
			self._style = SegStyle.FENCE
		elif seg.style == 4:
			self._style = SegStyle.PITBUILDING
		self._length = seg.length
		self._width = seg.width
		self._startWidth = seg.startWidth
		self._endWidth = seg.endWidth
		self._lgfromstart = seg.lgfromstart
		self._radius = seg.radius
		self._radiusr = seg.radiusr
		self._radiusl = seg.radiusl
		self._arc = seg.arc
		self._center = seg.center
		self._vertexSL = seg.vertexSL
		self._vertexSR = seg.vertexSR
		self._vertexEL = seg.vertexEL
		self._vertexER = seg.vertexER
		self._angleZS = seg.angleZS
		self._angleZE = seg.angleZE
		self._angleYL = seg.angleYL
		self._angleYR = seg.angleYR
		self._angleXS = seg.angleXS
		self._angleXE = seg.angleXE
		self._angleCS = seg.angleCS
		self._Kzl = seg.Kzl
		self._Kzw = seg.Kzw
		self._Kyl = seg.Kyl
		self._rgtSideNormal = seg.rgtSideNormal
		self._height = seg.height
		self._raceInfo = seg.raceInfo
		self._DoVfactor = seg.DoVfactor
		self._surface = TrackSurface()

# <summary>The set of track segments ordered by id.</summary>
class TrackSegList(List):
	# Create the list of segments.
	def __init__(self, seg):
		# Find segment id = 0
		while  != 0:
			seg = 
		# Add segments
		while  != 0:
			self.Add(TrackSeg(self, ))
			seg = 

# <summary>Track</summary>
class Track(object): # Main track
	#public IntPtr parameters;       // Parameters handle */
	#public TTrackPitInfo pits;      // Pits information
	#public TTrackSurface *surfaces; // Segment surface list
	#public TVector3D min;
	#public TVector3D max;
	#public TTrackGraphicInfo  graphic;
	# Unsafe constructor for interface with C++
	def __init__(self, track):
		self._nseg = track.nseg
		self._version = track.version
		self._length = track.length
		self._width = track.width
