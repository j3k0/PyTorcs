#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# LanePoint.cs
# Contains informations about a point in a lane
#--------------------------------------------------------------------------*
#
# file         : LanePoint.cs
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

class TLanePoint(object): # Parametric distance to next seg [0..1] # Offset from middle for the lane # Global angle # Curvature at point # Speed # Accelleration speed # Index of seg.
	# Default constructor
	def __init__(self):
