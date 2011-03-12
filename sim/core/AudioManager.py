class AudioManager(object):
	def Init(self):
		pass

	def Shutdown(self):
		pass

	def UpdateListener(self, delta_t, x, y, z):
		pass

	def InitCarEngine(self, engineName):
		pass

	def UpdateCarEngine(self, id, delta_t, x, y, z, rpm):
		pass

	def DeleteCarEngine(self, id):
		pass
