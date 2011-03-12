# Graphic.cs
#
#  Copyright (C) 2008 Jean-Christophe Hoelt <jeko@ios-software.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#
#
from Math3D import *
from SwigTorcs import *
from OpenRacing.Core import *
from OpenRacing.Core.Track import *

class GraphicRenderingQuality(object):
	def __init__(self):

# Interface to be implemented by a graphic plugin
class GraphicModule(object):
	# Open a window
	def InitView(self, enableGui, quality):
		pass

	# Close the window
	def ShutdownView(self):
		pass

	# Change graphic rendering quality
	def ChangeQuality(self, quality):
		pass

	# Load and initialize track data
	def InitTrack(self, track):
		pass

	# Load and initialize avatars data
	def InitAvatars(self, situ):
		pass

	# Refresh the situation and displayed image
	def Refresh(self, situ):
		pass

	# Deallocate track data
	def ShutdownTrack(self):
		pass

	# Deallocate avatars data
	def ShutdownAvatars(self):
		pass

	# Take a screenshot from given position/angle
	def AddCamera(self, name, fov, freq):
		pass

	# Take photos from given position/angle
	def MoveCamera(self, name, pos, lookat):
		pass

	def get_Gui(self):

	Gui = property(fget=get_Gui)

	def get_AudioManager(self):

	def set_AudioManager(self, value):

	AudioManager = property(fget=get_AudioManager, fset=set_AudioManager)
