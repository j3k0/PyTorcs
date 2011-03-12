from System import *
from OgreDotNet import *
from MyGUI import *
from OpenRacing.Core import *

class HUD(object):
	def __init__(self, ctx):
		self._mCtx = ctx
		self._mMaxRpm = 8500.0f
		self._mMaxSpeed = 180.0f
		self._mIsCreated = False

	def Create(self, avatars, avatarID):
		self._mAvatars = avatars
		self._mAvatarID = avatarID
		if self._mIsCreated:
			return 
		self._mIsCreated = True
		self._mCtx.RegisterResourceZip("data/hud.zip")
		om = OverlayManager.getSingleton()
		self._mOverlay = om.getByName("HUD/Panel")
		self._mOverlay.show()
		self._mSpeedoNeedle = om.getOverlayElement("HUD/SpeedoNeedle")
		self._mSpeedoNeedleMaterial = self._mSpeedoNeedle.getMaterial().Get()
		self._mSpeedoTexture = self._mSpeedoNeedleMaterial.GetTechnique(0).GetPass(0).GetTextureUnitState(0)
		self._mTachoNeedle = om.getOverlayElement("HUD/TachoNeedle")
		self._mTachoNeedleMaterial = self._mTachoNeedle.getMaterial().Get()
		self._mTachoTexture = self._mTachoNeedleMaterial.GetTechnique(0).GetPass(0).GetTextureUnitState(0)
		self.SetSpeedo(40.0f)
		self.SetTacho(4500.0f)

	def Destroy(self):
		if not self._mIsCreated:
			return 
		self._mIsCreated = False
		self._mCtx.UnregisterResource("data/hud.zip")
		self._mOverlay.hide()

	def SetSpeedo(self, speed):
		zpos = 138.0f
		mpos = -115.0f
		maxv = self._mMaxSpeed
		l = zpos - mpos
		rot = zpos - (speed / maxv) * l
		self._mSpeedoTexture.SetTextureRotate(Radian((MathTools.DegToRad(rot))))

	def SetTacho(self, tacho):
		zpos = 138.0f
		mpos = -115.0f
		maxv = self._mMaxRpm
		l = zpos - mpos
		rot = zpos - (tacho * self._mMaxRpm / maxv) * l
		self._mTachoTexture.SetTextureRotate(Radian((MathTools.DegToRad(rot))))

	def Update(self):
		if not self._mIsCreated:
			return 
		speed = self._mAvatars.GetSpeed(self._mAvatarID)
		rpm = self._mAvatars.GetEngineRPM(self._mAvatarID)
		self.SetSpeedo(speed)
		self.SetTacho(rpm)
