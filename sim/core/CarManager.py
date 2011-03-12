# CarManager.cs
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
from System import *
from Math3D import *
from SwigTorcs import *
from System.IO import *
from System.Collections.Generic import *

class CarManager(object):
	def __init__(self):
		self._Pool = List[Object]()
 # Prevents objects from being freed
	def Reset():
		self._Pool.Clear()

	Reset = staticmethod(Reset)

	def ReadSpecification(car):
		carSpecif = "cars/" + car.Info.CarName + "/" + car.Info.CarName + ".xml"
		Console.Out.WriteLine("Car Specification: {0}", carSpecif)
		carHandle = tGfParm(carSpecif, tGfParm.RMode.STD | tGfParm.RMode.CREAT)
		self._Pool.Add(carHandle)
		car.Info.Category = carHandle.GetStr(TorcsItf.SECT_CAR, TorcsItf.PRM_CATEGORY, None)
		if (car.Info.Category != None) and (car.Info.Category.Length > 0):
			catSpecif = "categories/" + car.Info.Category + ".xml"
			Console.Out.WriteLine("Category Specification: {0}", catSpecif)
			catHandle = tGfParm(catSpecif, tGfParm.RMode.STD | tGfParm.RMode.CREAT)
			self._Pool.Add(carHandle)
			# if (GfParmCheckHandle(catHandle, carHandle)) {
			# GfTrace("Car %s not in Category %s (driver %s) !!!\n", elt->_carName, category, elt->_name);
			# break;
			# } TODO
			carHandle.Handle = tGfParm.MergeHandles(catHandle.Handle, carHandle.Handle, TorcsItf.GFPARM_MMODE_SRC | TorcsItf.GFPARM_MMODE_DST | TorcsItf.GFPARM_MMODE_RELSRC | TorcsItf.GFPARM_MMODE_RELDST)
			Console.Out.WriteLine("POSY PARAM: " + carHandle.GetStr(TorcsItf.SECT_REARRGTWHEEL, TorcsItf.PRM_YPOS, None))
			return carHandle
		else:
			raise InvalidConfigurationException("Bad Car category for driver " + car.Info.Name)

	ReadSpecification = staticmethod(ReadSpecification)A
