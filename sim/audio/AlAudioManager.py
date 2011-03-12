from Tao.OpenAl import *
from OpenRacing.Core import *
from System.Collections.Generic import *

class Engine(object):
	def __init__(self, engineName):
		self._mBuffer = Array.CreateInstance(int, 1)
		self._mSource = Array.CreateInstance(int, 1)
		self._mRpm = 0.5f
		self._mBuffer[0] = Alut.alutCreateBufferFromFile("sounds/" + engineName + ".wav")
		Al.alGenSources(1, )
		Al.alSourcei(self._mSource[0], Al.AL_BUFFER, self._mBuffer[0]) # attach the buffer to a source
		Al.alSourcePlay(self._mSource[0]) # start playback
		Al.alSourcei(self._mSource[0], Al.AL_LOOPING, 1)
 # source loops infinitely
	def Delete(self):
		Al.alSourceStop(self._mSource[0]) # halt playback
		Al.alDeleteSources(self._mSource.Length, self._mSource) # free Handles
		Al.alDeleteBuffers(self._mBuffer.Length, self._mBuffer)

	def Update(self, delta_t, x, y, z, rpm):
		self._mRpm = (1.0f - 5.0f * delta_t) * self._mRpm + 5.0f * delta_t * rpm
		f = 0.2f + self._mRpm * 1.20f # Picked some number here... TODO: find value from car parameters
		# System.Console.Out.WriteLine("Rpm={0}, f={1}", e.mRpm, f);
		volume = f
		if volume > 1.0f:
			volume = 1.0f
		Al.alSourcef(self._mSource[0], Al.AL_GAIN, volume) # source loops infinitely
		Al.alSourcef(self._mSource[0], Al.AL_PITCH, f)
 # source loops infinitely
class AlAudioManager(AudioManager):
	def __init__(self):
		self._mEngineList = List[Engine]()
		self._mEngineListLength = 0
		self._alutInitDone = False

	def Init(self):
		if not self._alutInitDone:
			Alut.alutInit()
			self._alutInitDone = True

	def Shutdown(self):
		enumerator = mEngineList.GetEnumerator()
		while enumerator.MoveNext():
			e = enumerator.Current
			if e != None:
				e.Delete()
		self._mEngineList.Clear()
		self._mEngineListLength = 0

	# Alut.alutExit();
	def UpdateListener(self, delta_t, x, y, z):
		pass

	def InitCarEngine(self, engineName):
		e = Engine(engineName)
		self._mEngineList.Add(e)
		return self._mEngineListLength += 1

	def UpdateCarEngine(self, id, delta_t, x, y, z, rpm):
		e = self._mEngineList[id]
		e.Update(delta_t, x, y, z, rpm)

	def DeleteCarEngine(self, id):
		self._mEngineList[id].Delete()
		self._mEngineList[id] = None
