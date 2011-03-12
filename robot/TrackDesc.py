#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# TrackDesc.cs
# Contains informations about the track
#--------------------------------------------------------------------------*
#
# file         : TrackDesc.cs
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

class TPitSideMod(object):
	def __init__(self, side):
		self._Side = side
		self._Start = 0
		self._End = 0
 # side of pitlane # start of pitlane # end of pitlane
class TTrackDescription(object): # Number of sections in track # Mean length of sections # Array of sections # TORCS data of track # sampling rate (per m) # Pit entry # Pit exit # Pit side # Pit side mode
	# Constructor
	def __init__(self):
		self._oSections = None
		self._oTrack = None
		self._oTrackRes = 2.5 # sampling rate
		self._oMeanSectionLen = self._oTrackRes
 # First estimation
	# Destructor
	def Dispose(self):
		self._oSections = None
 # Free sections
	# Calc position from offset
	def CalcPos(self, TrkPos, Offset):
		Pos = RT.GetDistFromStart2() + Offset
		return self.NormalizePos(Pos)
 # Normalize to >= 0.0
	# Calc cars position from offset
	def CalcPos(self, Car, Offset):
		Pos = RT.GetDistFromStart() + Offset
		return self.NormalizePos(Pos)
 # Normalize to >= 0.0
	# Calc position from coordinates
	def CalcPos(self, X, Y, Sides):
		Seg = self._oSections[0].Seg
		Pos = TTrkLocPos()
		if Sides:
			RT.TrackGlobal2Local(Seg, X, Y, , 1)
		else:
			RT.TrackGlobal2Local(Seg, X, Y, , 0)
		return RT.GetDistFromStart2()

	# Calc position from coordinates
	def CalcPos(self, X, Y, Hint, Sides):
		Seg = Hint.Seg
		Pos = TTrkLocPos()
		if Sides:
			RT.TrackGlobal2Local(Seg, X, Y, , 1)
		else:
			RT.TrackGlobal2Local(Seg, X, Y, , 0)
		return RT.GetDistFromStart2()

	# Number of sections in track
	def Count(self):
		return self._oCount

	# Create track description
	# using different track resolutions along pits
	# and setting sections according to segment limmits
	def Execute(self): # Looping index of sections
		ID = 0 # ID of section
		#C++ TO C# CONVERTER TODO TASK: Pointer arithmetic is detected on this variable, so pointers on this variable are left unchanged. # First Segment;
		#C++ TO C# CONVERTER TODO TASK: Pointer arithmetic is detected on this variable, so pointers on this variable are left unchanged. # Current Segment; # Position along track # Section # Number of sections # Length of current step
		PitSection = False # Start in pit section
		self._oPitEntry = -1 # Undefined pit entry
		self._oPitExit = -1 # and pit exit
		self._oPitSide = C.trSideLft if .side == C.trLft else C.trSideRgt
		First =  # First TORCS segment
		# But find segment with smallest destination to startline ...
		while  >  / 2:
			First = 
		# ... First is new start segment for our track description!
		# Find oder of pit entry/exit ...
		Segm = First # Start near startline # loop all segments # if pit entry first # startline is out # if pit exit is first # startline is in # pit section! Start # with pit mode! # Next segment
		while Segm != First:
			if ( & C.trPitEntry) > 0:
				break
			elif ( & C.trPitExit) > 0:
				PitSection = True
				break
			Segm =  # Loop till restart
		# ... find number of sections needed ...
		Segm = First # Start near startline # loop all segments # first time # save ID of section # and change mode of # calculating steplength # If pit exit is found # we leave pit sections # save ID of section # reset steplength mode # to use for this segment # Next torcs segment
		while Segm != First:
			if (self._oPitEntry < 0) and ( & C.trPitEntry) > 0:
				self._oPitEntry = ID
				PitSection = True
			elif ( & C.trPitExit) > 0:
				self._oPitExit = ID
				PitSection = False
			ID += self.NbrOfSections(, PitSection)
			Segm =  # Loop till restart
		self._oCount = ID # Number of sections in track
		# ... estimate length of sections ...
		self._oMeanSectionLen =  / self._oCount # Mean length of sections
		# .. create track description ...
		self._oSections = Array.CreateInstance(TSection, self._oCount) # Create all sections of track
		ID = 0 # Start with ID 0
		self._oPitEntry = -1 # Reset Markers
		self._oPitExit = -1
		Segm = First # Start near startline
		segDist =  # Distance from start # Loop all segments # Local position # we enter the pit sections # If found pit exit # we leave pit sections # use for this segment
		while 		# Segment is straight ... # Steplength # Loop sections # next undefined section # Save local position # Save global distance # Derived from segment # Save initial width to # left and right side # calculate dist from start # and local position # Increment ID
		# Segment is curve ... # Step length # Loop all sections # Next undefined section # Save local position # Save global distance # Derived from segment # Save initial width to # left and right side # calculate dist from start # and local position # Increment ID # Next segment # Distance from Start
Segm != First:
			Station = 0
			if (self._oPitEntry < 0) and ( & C.trPitEntry) > 0:
				self._oPitEntry = ID
				PitSection = True
			elif ( & C.trPitExit) > 0:
				self._oPitExit = ID
				PitSection = False
			NSec = self.NbrOfSections(, PitSection)
			if  == C.trStr:
				StepLen =  / NSec
				I = 0
				while I < NSec:
					Section = self._oSections[ID]
					Section.Station = Station
					Section.DistFromStart = segDist
					Section.Seg = Segm
					Section.WidthToLeft =  / 2
					Section.WidthToRight =  / 2
					segDist += StepLen
					Station = Station + StepLen
					ID += 1
					I += 1
			else:
				StepLen =  / NSec
				I = 0
				while I < NSec:
					Section = self._oSections[ID]
					Section.Station = Station
					Section.DistFromStart = segDist
					Section.Seg = Segm
					Section.WidthToLeft =  / 2
					Section.WidthToRight =  / 2
					segDist += StepLen
					Station = Station + StepLen
					ID += 1
					I += 1
			Segm = 
			segDist =  # Loop all segments
		self.BuildPos2SecIndex()
 # Build reverse index
	# Friction of section[Index]
	def Friction(self, Index):
		Seg = self._oSections[Index].Seg
		return 

	# Angle
	def ForwardAngle(self, TrackPos):
		Index = self.IndexFromPos(TrackPos)
		Seg = self._oSections[Index].Seg
		X = 0.0
		CenterPoint = TVector3D()
		Normale = TVector3D()
		self.NormalizeDir(Seg, TrackPos - , , , )
		return TUtils.VecAngXY(Normale) + C.PI / 2

	# Find index of section to position
	def IndexFromPos(self, TrackPos):
		TrackPos = self.NormalizePos(TrackPos) # Normalize to >= 0.0
		Index = (Math.Floor(TrackPos / self._oMeanSectionLen)) % self._oCount # distance to startline
		Index = self._oSections[Index].PosIndex # Use lookup table
		# Interpolate back from estimation
		while TrackPos < self._oSections[Index].DistFromStart:
			if Index > 0:
				Index -= 1
			else:
				return 0
		# Interpolate from estimation
		while TrackPos > self._oSections[Index + 1].DistFromStart:
			if Index < self._oCount - 2:
				Index += 1
			else:
				return self._oCount - 1
		return Index

	# Build position to section index to estimate search start index
	def BuildPos2SecIndex(self):
		I = 0
		while I < self._oCount:
			TrackPos = I * self._oMeanSectionLen + 0.1
			Index = (Math.Floor(TrackPos / self._oMeanSectionLen)) % self._oCount
			while TrackPos < self._oSections[Index].DistFromStart:
				if Index > 0:
					Index -= 1
				else:
					break
			while TrackPos > self._oSections[Index + 1].DistFromStart:
				if Index < self._oCount - 1:
					Index += 1
				else:
					break
			self._oSections[I].PosIndex = Index
			I += 1

	# Build new track description
	def InitTrack(self, Track, CarParam, PitSideMod):
		#    	  if (oTrack != Track) // if used # free old ones
		if self._oSections != None:
			self._oSections = None
		self._oSections = None
		self._oCount = 0
		self._oTrack = Track # Save pointer to TORCS data
		self._oPitSideMod = PitSideMod # Set Pit side mode
		self.Execute() # Make description
		LastSeg =  # Save last segment
		LastSegType = C.trStr # Assume straight
		Seg = LastSeg # Start at last segment
		# Find usable additional width at sides of the track ...
		N = 0 # Count sections since # last curve
		I = 0
		while I < self._oCount:
			LastSeg = Seg # Save last segment
			if  != C.trStr: # if it was a curve # save last type and
				LastSegType =  # reset counter
				N = 0
			else: # increase counter
				N += 1 # on straights
			if N > 10: # After 10 sections
				LastSegType =  # reset
			Seg = self._oSections[I].Seg # Get torcs segment
			DistFromStart = self._oSections[I].DistFromStart # of section
			T = (DistFromStart - ) / 
			InPit = ((self._oPitEntry < self._oPitExit) and (self._oPitEntry <= I) and (I <= self._oPitExit) or (self._oPitEntry > self._oPitExit) and ((I <= self._oPitExit) or (I >= self._oPitEntry)))
			# Selections ...
			MIN_MU =  * CarParam.oScaleMinMu
			MAX_ROUGH = Math.Max(0.005,  * 1.2)
			MAX_RESIST = Math.Max(0.02,  * 1.2)
			SLOPE =  # Slope of segment
			S = 0
			while S < 2: # Look at both sides
				#C++ TO C# CONVERTER TODO TASK: Pointer arithmetic is detected on this variable, so pointers on this variable are left unchanged. # Side-segment
				if S == 0:
					PSide = 
				else:
					PSide = 
				if PSide == None: # If NULL no side
					continue # go to next segment
				ExtraW = 0 # Initialize add. width
				ExtraWpit = 0 # Initialize add. width
				Done = False # Reset flag
				#	  while(!Done && PSide)                      // Loop all side-segments
				while PSide != None: # Loop all side-segments
					Wpit = 0.0 # Save it for pitlane
					W =  + ( - ) * T
					if  == C.trCurb: # On curbs
						W = 0.8 * W # Use 80%
						if not ((S == self._oPitSideMod.Side) and (I >= self._oPitSideMod.Start) and (I <= self._oPitSideMod.End)):
							W = Math.Min(W, 1.5) # Keep a wheel on track
							Done = True
							if (((S == C.trSideLft) and ( == C.trRgt)) or ((S == C.trSideRgt) and ( == C.trLft))) and ( < ):
								W = 0
							# Don't go too far up raised curbs (max 2cm).
							if  > 0.02: # If more than 2 cm
								W = 0 # keep off
							elif  > 0.01: # Use 15 cm up to
								W = Math.Min(W, 0.15) # 2 cm height
							elif  > 0.0: # Use 30 cm up to
								W = Math.Min(W, 0.3) # 1 cm height
					elif  == C.trPlan: # On plan
						if (InPit and (self._oPitSide == S)) or ( & (C.trSpeedLimit | C.trPitLane)) > 0:
							Wpit = W # Save it for pitlane
							W = 0
							Done = True
						elif (S == self._oPitSideMod.Side) and (I >= self._oPitSideMod.Start) and (I <= self._oPitSideMod.End):
							Wpit = W # Save it for pitlane
							if W > 0.5: # Only 50 cm
								W = 0.5
								Done = True
						elif 						# Selections ...
( < MIN_MU) or ( > MAX_ROUGH) or ( > MAX_RESIST) or (Math.Abs( - SLOPE) > 0.005):
							W = 0
							Done = True
						else:
							W = 0.8 * W # Use 80%
						if ((S == C.trSideLft) and ( == C.trRgt) or (S == C.trSideRgt) and ( == C.trLft)) and ( < ):
							W = -2.0
						if ((S == C.trSideLft) and (LastSegType == C.trRgt) or (S == C.trSideRgt) and (LastSegType == C.trLft)) and ( < ):
							W = -2.0 + N * 0.05
					else:
						# Wall of some sort
						W = -1.0 if ( == C.trWall) else 0
						Done = True
					ExtraWpit += Wpit
					if not Done:
						ExtraW += W
					if S == 0:
						PSide = 
					else:
						PSide = 
				if S == C.trSideLft:
					self._oSections[I].PitWidthToLeft = self._oSections[I].WidthToLeft + Math.Max(ExtraW, ExtraWpit)
					self._oSections[I].WidthToLeft += self.ExtraW
				else:
					self._oSections[I].PitWidthToRight = self._oSections[I].WidthToRight + Math.Max(ExtraW, ExtraWpit)
					self._oSections[I].WidthToRight += self.ExtraW
				S += 1
			self.NormalizeDir(Seg, DistFromStart - , , , )
			I += 1

	# Mean length of sections
	def MeanSectionLen(self):
		return self._oMeanSectionLen

	# To right
	def Normale(self, TrackPos):
		#int LastPos = 0;
		Index = self.IndexFromPos(TrackPos)
		Seg = self._oSections[Index].Seg
		Tmp = 0.0
		CenterPoint = TVector3D()
		Normale = TVector3D()
		self.NormalizeDir(Seg, TrackPos - , , , )
		return TVector2D(Normale)

	# Keep pos in 0..Tracklength
	def NormalizePos(self, TrackPos):
		while TrackPos < 0:
			TrackPos += 
		while TrackPos >= :
			TrackPos -= 
		return TrackPos

	# Length of track
	def Length(self):
		return 

	# Section of index
	def Section(self, Index):
		return self._oSections[Index]

	# Get TORCS track data
	def Track(self):
		return self._oTrack

	# Const track width
	def Width(self):
		return 

	# Nbr of sections in segment
	def NbrOfSections(self, Len, PitSection):
		Den = self._oTrackRes
		if PitSection:
			Den = 1.0
		Result = (Len / Den)
		if Result > Len / Den:
			Result -= 1
		if Result < 1:
			Result = 1
		return Result

	# Calculate Center and ToRight
	def NormalizeDir(self, Seg, ToStart, T, Point, Normale):
		T = ToStart / 
		Zl = Convert.ToSingle(.z + (.z - .z) * T)
		Zr = Convert.ToSingle(.z + (.z - .z) * T)
		if  == C.trStr:
			Start = ( + ) / 2
			End = ( + ) / 2
			Point = Start + (End - Start) * T
			Normale = -
			Normale.z = (Zr - Zl) / 
		else:
			VZ = 1 if  == C.trLft else -1
			DeltaAngle = VZ * ToStart / 
			Ang =  - C.PI / 2 + DeltaAngle
			Cos = Convert.ToSingle(Math.Cos(Ang))
			CosRad = Convert.ToSingle(VZ * Math.Cos())
			Sin = Convert.ToSingle(Math.Sin(Ang))
			SinRad = Convert.ToSingle(VZ * Math.Sin())
			Point = TVector3D(.x + CosRad, .y + SinRad, (Zl + Zr) / 2)
			Normale = TVector3D(Cos, Sin, (Zr - Zl) / )
