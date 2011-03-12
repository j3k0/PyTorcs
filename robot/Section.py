#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# Section.cs
# Contains informations about a short way of the track
#--------------------------------------------------------------------------*
#
# file         : Section.cs
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

class TSection(object): # Dist. f. Start of Segment  # Dist. from Start of Track # Original Track segment. # Width to left. # Width to right. # Width to left. # Width to right. # Local station in segment # Centre # To right # Position to section index
	# Default constructor
	def __init__(self):
