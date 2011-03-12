#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# RobotTools.cs
# Utilities for robots
#--------------------------------------------------------------------------*
#
# file         : Quadratic.cs
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
# Robot tools
class RT(object):
	def __init__(self):
		pass
	def DoubleNormPiPi(angle):
		while angle > C.PI:
			angle -= 2 * C.PI
		while angle < -C.PI:
			angle += 2 * C.PI

	DoubleNormPiPi = staticmethod(DoubleNormPiPi)

	def FloatNormPiPi(angle):
		ZPI = Convert.ToSingle(2 * C.PI)
		while angle > C.PI:
			angle -= ZPI
		while angle < -C.PI:
			angle += ZPI

	FloatNormPiPi = staticmethod(FloatNormPiPi)

	def GetDistFromStart(car):
		seg = car.pub.trkPos.seg
		lg = 
		if  == C.trStr:
			lg += car.pub.trkPos.toStart
		else:
			lg += car.pub.trkPos.toStart * 
		return lg

	GetDistFromStart = staticmethod(GetDistFromStart)

	def GetDistFromStart2(p):
		seg = p.seg
		lg = 
		if  == C.trStr:
			lg += p.toStart
		else:
			lg += p.toStart * 
		return lg

	GetDistFromStart2 = staticmethod(GetDistFromStart2)

	def TrackGetWidth(seg, toStart):
		return Math.Abs( + toStart * )

	TrackGetWidth = staticmethod(TrackGetWidth)

	def TrackGlobal2Local(segment, X, Y, p, type):
		segnotfound = True
		seg = segment
		depl = 0
		p.type = type
		while segnotfound:
			if  == C.trStr:
				# rotation
				sine = Convert.ToSingle(Math.Sin())
				cosine = Convert.ToSingle(Math.Cos())
				x = X - .x
				y = Y - .y
				ts = x * cosine + y * sine
				p.seg = seg
				p.toStart = ts
				p.toRight = y * cosine - x * sine
				if (ts < 0) and (depl < 1):
					# get back
					seg = 
					depl = -1
				elif (ts > ) and (depl > -1):
					seg = 
					depl = 1
				else:
					segnotfound = False
			elif  == C.trLft:
				# rectangular to polar
				x = X - .x
				y = Y - .y
				a2 = Convert.ToSingle( / 2.0)
				theta = Convert.ToSingle(Math.Atan2(y, x) - ( + a2))
				RT.FloatNormPiPi()
				p.seg = seg
				p.toStart = theta + a2
				p.toRight = Convert.ToSingle( - Math.Sqrt(x * x + y * y))
				if (theta < -a2) and (depl < 1):
					seg = 
					depl = -1
				elif (theta > a2) and (depl > -1):
					seg = 
					depl = 1
				else:
					segnotfound = False
			elif  == C.trRgt:
				# rectangular to polar
				x = X - .x
				y = Y - .y
				a2 = Convert.ToSingle( / 2.0)
				theta = Convert.ToSingle( - a2 - Math.Atan2(y, x))
				RT.FloatNormPiPi()
				p.seg = seg
				p.toStart = theta + a2
				p.toRight = Convert.ToSingle(Math.Sqrt(x * x + y * y) - )
				if (theta < -a2) and (depl < 1):
					seg = 
					depl = -1
				elif (theta > a2) and (depl > -1):
					seg = 
					depl = 1
				else:
					segnotfound = False
		# The track is of constant width
		# This is subject to change
		p.toMiddle = Convert.ToSingle(p.toRight -  / 2.0)
		p.toLeft =  - p.toRight
		# Consider all the track with the sides
		# Stay on main segment
		if type == C.trLPosTrack:
			if  != None:
				sseg = 
				p.toRight += 
				sseg = 
				if sseg != None:
					p.toRight += 
			if  != None:
				sseg = 
				p.toLeft += 
				sseg = 
				if sseg != None:
					p.toLeft += 
		# Relative to a segment, change to the side segment if necessary
		if type == C.trLPosSegment:
			if (p.toRight < 0) and ( != None):
				sseg = 
				p.seg = sseg
				curWidth = RT.TrackGetWidth(sseg, p.toStart)
				p.toRight += self.curWidth
				p.toLeft -= 
				p.toMiddle += 
				if (p.toRight < 0) and ( != None):
					p.toLeft -= self.curWidth
					p.toMiddle += 
					seg = sseg
					sseg = 
					curWidth = RT.TrackGetWidth(sseg, p.toStart)
					p.seg = sseg
					p.toRight += self.curWidth
					p.toMiddle += 
			elif (p.toLeft < 0) and ( != None):
				sseg = 
				p.seg = sseg
				curWidth = RT.TrackGetWidth(sseg, p.toStart)
				p.toRight += 
				p.toMiddle -= 
				p.toLeft += self.curWidth
				if (p.toLeft < 0) and ( != None):
					p.toRight -= self.curWidth
					p.toMiddle -= 
					seg = sseg
					sseg = 
					curWidth = RT.TrackGetWidth(sseg, p.toStart)
					p.seg = sseg
					p.toMiddle -= 
					p.toLeft += self.curWidth

	TrackGlobal2Local = staticmethod(TrackGlobal2Local)
