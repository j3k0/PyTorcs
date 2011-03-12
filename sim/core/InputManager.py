from System.Collections.Generic import *

class KeyCode(object):
	def __init__(self):
		self._KC_UNASSIGNED = 0x00
		self._KC_ESCAPE = 0x01
		self._KC_1 = 0x02
		self._KC_2 = 0x03
		self._KC_3 = 0x04
		self._KC_4 = 0x05
		self._KC_5 = 0x06
		self._KC_6 = 0x07
		self._KC_7 = 0x08
		self._KC_8 = 0x09
		self._KC_9 = 0x0A
		self._KC_0 = 0x0B
		self._KC_MINUS = 0x0C
		self._KC_EQUALS = 0x0D
		self._KC_BACK = 0x0E
		self._KC_TAB = 0x0F
		self._KC_Q = 0x10
		self._KC_W = 0x11
		self._KC_E = 0x12
		self._KC_R = 0x13
		self._KC_T = 0x14
		self._KC_Y = 0x15
		self._KC_U = 0x16
		self._KC_I = 0x17
		self._KC_O = 0x18
		self._KC_P = 0x19
		self._KC_LBRACKET = 0x1A
		self._KC_RBRACKET = 0x1B
		self._KC_RETURN = 0x1C
		self._KC_LCONTROL = 0x1D
		self._KC_A = 0x1E
		self._KC_S = 0x1F
		self._KC_D = 0x20
		self._KC_F = 0x21
		self._KC_G = 0x22
		self._KC_H = 0x23
		self._KC_J = 0x24
		self._KC_K = 0x25
		self._KC_L = 0x26
		self._KC_SEMICOLON = 0x27
		self._KC_APOSTROPHE = 0x28
		self._KC_GRAVE = 0x29
		self._KC_LSHIFT = 0x2A
		self._KC_BACKSLASH = 0x2B
		self._KC_Z = 0x2C
		self._KC_X = 0x2D
		self._KC_C = 0x2E
		self._KC_V = 0x2F
		self._KC_B = 0x30
		self._KC_N = 0x31
		self._KC_M = 0x32
		self._KC_COMMA = 0x33
		self._KC_PERIOD = 0x34
		self._KC_SLASH = 0x35
		self._KC_RSHIFT = 0x36
		self._KC_MULTIPLY = 0x37
		self._KC_LMENU = 0x38
		self._KC_SPACE = 0x39
		self._KC_CAPITAL = 0x3A
		self._KC_F1 = 0x3B
		self._KC_F2 = 0x3C
		self._KC_F3 = 0x3D
		self._KC_F4 = 0x3E
		self._KC_F5 = 0x3F
		self._KC_F6 = 0x40
		self._KC_F7 = 0x41
		self._KC_F8 = 0x42
		self._KC_F9 = 0x43
		self._KC_F10 = 0x44
		self._KC_NUMLOCK = 0x45
		self._KC_SCROLL = 0x46
		self._KC_NUMPAD7 = 0x47
		self._KC_NUMPAD8 = 0x48
		self._KC_NUMPAD9 = 0x49
		self._KC_SUBTRACT = 0x4A
		self._KC_NUMPAD4 = 0x4B
		self._KC_NUMPAD5 = 0x4C
		self._KC_NUMPAD6 = 0x4D
		self._KC_ADD = 0x4E
		self._KC_NUMPAD1 = 0x4F
		self._KC_NUMPAD2 = 0x50
		self._KC_NUMPAD3 = 0x51
		self._KC_NUMPAD0 = 0x52
		self._KC_DECIMAL = 0x53
		self._KC_OEM_102 = 0x56
		self._KC_F11 = 0x57
		self._KC_F12 = 0x58
		self._KC_F13 = 0x64
		self._KC_F14 = 0x65
		self._KC_F15 = 0x66
		self._KC_KANA = 0x70
		self._KC_ABNT_C1 = 0x73
		self._KC_CONVERT = 0x79
		self._KC_NOCONVERT = 0x7B
		self._KC_YEN = 0x7D
		self._KC_ABNT_C2 = 0x7E
		self._KC_NUMPADEQUALS = 0x8D
		self._KC_PREVTRACK = 0x90
		self._KC_AT = 0x91
		self._KC_COLON = 0x92
		self._KC_UNDERLINE = 0x93
		self._KC_KANJI = 0x94
		self._KC_STOP = 0x95
		self._KC_AX = 0x96
		self._KC_UNLABELED = 0x97
		self._KC_NEXTTRACK = 0x99
		self._KC_NUMPADENTER = 0x9C
		self._KC_RCONTROL = 0x9D
		self._KC_MUTE = 0xA0
		self._KC_CALCULATOR = 0xA1
		self._KC_PLAYPAUSE = 0xA2
		self._KC_MEDIASTOP = 0xA4
		self._KC_VOLUMEDOWN = 0xAE
		self._KC_VOLUMEUP = 0xB0
		self._KC_WEBHOME = 0xB2
		self._KC_NUMPADCOMMA = 0xB3
		self._KC_DIVIDE = 0xB5
		self._KC_SYSRQ = 0xB7
		self._KC_RMENU = 0xB8
		self._KC_PAUSE = 0xC5
		self._KC_HOME = 0xC7
		self._KC_UP = 0xC8
		self._KC_PGUP = 0xC9
		self._KC_LEFT = 0xCB
		self._KC_RIGHT = 0xCD
		self._KC_END = 0xCF
		self._KC_DOWN = 0xD0
		self._KC_PGDOWN = 0xD1
		self._KC_INSERT = 0xD2
		self._KC_DELETE = 0xD3
		self._KC_LWIN = 0xDB
		self._KC_RWIN = 0xDC
		self._KC_APPS = 0xDD
		self._KC_POWER = 0xDE
		self._KC_SLEEP = 0xDF
		self._KC_WAKE = 0xE3
		self._KC_WEBSEARCH = 0xE5
		self._KC_WEBFAVORITES = 0xE6
		self._KC_WEBREFRESH = 0xE7
		self._KC_WEBSTOP = 0xE8
		self._KC_WEBFORWARD = 0xE9
		self._KC_WEBBACK = 0xEA
		self._KC_MYCOMPUTER = 0xEB
		self._KC_MAIL = 0xEC
		self._KC_MEDIASELECT = 0xED

class InputListener(object):
	def OnKeyPressed(self, key):
		pass

	def OnKeyReleased(self, key):
		pass

	def OnButtonPressed(self, button):
		pass

	def OnButtonReleased(self, button):
		pass

	def OnAxisMoved(self, axisID, val):
		pass

class InputManager(object):

	class KeyboardListener(MyGUI.KeyboardListener):
		def __init__(self, im):
			self._mIM = im

		def OnKeyReleased(self, kc):
			k = kc
			enumerator = self._mIM.mInputListeners.GetEnumerator()
			while enumerator.MoveNext():
				i = enumerator.Current
				i.OnKeyReleased(k)

		def OnKeyPressed(self, kc):
			k = kc
			enumerator = self._mIM.mInputListeners.GetEnumerator()
			while enumerator.MoveNext():
				i = enumerator.Current
				i.OnKeyPressed(k)

	class JoystickListener(MyGUI.JoystickListener):
		def __init__(self, im):
			self._mIM = im

		def OnButtonPressed(self, button):
			enumerator = self._mIM.mInputListeners.GetEnumerator()
			while enumerator.MoveNext():
				i = enumerator.Current
				i.OnButtonPressed(button)

		def OnButtonReleased(self, button):
			enumerator = self._mIM.mInputListeners.GetEnumerator()
			while enumerator.MoveNext():
				i = enumerator.Current
				i.OnButtonReleased(button)

		def OnAxisMoved(self, axisID, val):
			enumerator = self._mIM.mInputListeners.GetEnumerator()
			while enumerator.MoveNext():
				i = enumerator.Current
				i.OnAxisMoved(axisID, val)

	# The input manager is here to hide the current usage of MyGUI's GuiManager.
	#
	#  - One or more InputListener as associated with the manager.
	#  - The manager is itself a listener of MyGUI's GuiManager, it notifies
	#    the InputListener when event occurs.
	def __init__(self, im):
		self._mIM = im

	def SetGuiManager(self, gui):
		mGuiManager = gui
		mGuiManager.SetKeyboardListener(mKeyboardListener)
		mGuiManager.SetJoystickListener(mJoystickListener)

	def AddListener(self, listener):
		mInputListeners.Add(listener)

	def RemoveListener(self, listener):
		mInputListeners.Remove(listener)
