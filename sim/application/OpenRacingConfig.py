import elementtree.ElementTree as ET

class GraphicRenderingQuality:
	High = 2
	Medium = 1
	Low = 0

#import clr
#from System import *
#from System.IO import *
#from System.Xml import *
#from System.Xml.Serialization import *
#from OpenRacing.Core import *
#from OpenRacing.Graphic import *

#Put in a custom namespace to not conflict with OR types.
#class OpenRacing(object):
#	def __init__(self):
#		pass
#
#	# Used http://www.bonesoft.com/XmlModeler/Demo.aspx to generate this code
#	# Note, needed to crank up kate and do block-select mode to delete the line number junk
#	# That is put into the HTMl file
#	def get_RaceManager(self):
#		# <summary>RaceManager xml element.</summary>
#		return self._element_racemanager
#
#	def set_RaceManager(self, value):
#		self._element_racemanager = value
#
#	RaceManager = property(fget=get_RaceManager, fset=set_RaceManager)
#
#	def get_Graphic(self):
#		# <summary>Graphic xml element.</summary>
#		return self._element_graphic
#
#	def set_Graphic(self, value):
#		self._element_graphic = value
#
#	Graphic = property(fget=get_Graphic, fset=set_Graphic)
#
#	def get_Drivers(self):
#		# <summary>Driver[] Drivers xml array element.</summary>
#		return self._element_drivers
#
#	def set_Drivers(self, value):
#		self._element_drivers = value
#
#	Drivers = property(fget=get_Drivers, fset=set_Drivers)

#class RaceManager(object):
#	""" <summary>Represents a OpenRacing.RaceManager node.</summary>"""
#	def __init__(self):
#		""" <summary>Represents a OpenRacing.RaceManager node.</summary>"""
#
#	def get_RaceFile(self):
#		# <summary>String RaceFile element.</summary>
#		return self._element_racefile
#
#	def set_RaceFile(self, value):
#		self._element_racefile = value
#
#	RaceFile = property(fget=get_RaceFile, fset=set_RaceFile)

#class Graphic(object):
#	""" <summary>Represents a OpenRacing.Graphic node.</summary>"""
#	def __init__(self):
#		""" <summary>Represents a OpenRacing.Graphic node.</summary>"""
#		self._element_quality = "High"
#
#	def get_Quality(self):
#		# <summary>String Quality element.</summary>
#		return self._element_quality
#
#	def set_Quality(self, value):
#		self._element_quality = value
#
#	Quality = property(fget=get_Quality, fset=set_Quality)

#class Driver(object):
#	""" <summary>Represents a Drivers.Driver node.</summary>"""
#	def __init__(self):
#		""" <summary>Represents a Drivers.Driver node.</summary>"""
#
#	def get_Module(self):
#		# <summary>String Module element.</summary>
#		return self._element_module
#
#	def set_Module(self, value):
#		self._element_module = value
#
#	Module = property(fget=get_Module, fset=set_Module)

# OpenRacing XML configuration file
class OpenRacingConfig(object):
	# Build and load configuration from file found at given path
	def __init__(self, path):
		# self._s = XmlSerializer(clr.GetClrType(OpenRacing.Application.Conf.OpenRacing))
		self._mPath = path
		self.Load()

	# Load file into the XmlDocument
	def Load(self):
		self._tree = ET.parse(self._mPath)
		# r = StreamReader(self._mPath)
		# self._or = self._s.Deserialize(r)
		# r.Close()

	def Save(self):
		self._tree.write(self._mPath)
		# w = StreamWriter(self._mPath)
		# self._s.Serialize(w, self._or)
		# w.Close()

	def get_RaceFile(self):
		return self._tree.findtext("RaceManager/RaceFile")
		# return self._tree.self._or.RaceManager.RaceFile

	def set_RaceFile(self, value):
		elt = self._tree.find("RaceManager/RaceFile")
		elt.text = value

	RaceFile = property(fget=get_RaceFile, fset=set_RaceFile)

	def get_GraphicRenderingQuality(self):
		q = self._tree.findtext("Graphic/Quality")
		if q == "Medium":
			return GraphicRenderingQuality.Medium
		if q == "Low":
			return GraphicRenderingQuality.Low
		return GraphicRenderingQuality.High

	def set_GraphicRenderingQuality(self, value):
		elt = self._tree.find("Graphic/Quality")
		if value == GraphicRenderingQuality.High:
			elt.text = "High"
		if value == GraphicRenderingQuality.Medium:
			elt.text = "Medium"
		if value == GraphicRenderingQuality.Low:
			elt.text = "Low"

	GraphicRenderingQuality = property(fget=get_GraphicRenderingQuality, fset=set_GraphicRenderingQuality)
