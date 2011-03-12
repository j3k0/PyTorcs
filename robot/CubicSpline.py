#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# CubicSpline.cs
#--------------------------------------------------------------------------*
#
# file         : CubicSpline.cs
# created      : 26 Jul 2008
# last changed : 26 Jul 2008
# Copyright    : ###COPYRIGHTHOLDER###
# eMail        : ###CONTACT###
# Version      : 0.00.009 
#  
#--------------------------------------------------------------------------*
# ###COPYRIGHT###
#--------------------------------------------------------------------------*
class CubicSpline(object): # Nbr of segments # Segments # Cubics
	# Constructor
	def __init__(self, count, X, Y, S):
		self._Count = count
		self._Segs = Array.CreateInstance(Double, self._Count)
		self._Cubics = Array.CreateInstance(Cubic, self._Count - 1)
		I = 0
		while I < self._Count:
			self._Segs[I] = X[I]
			if I + 1 < self._Count:
				self._Cubics[I].Set(X[I], Y[I], S[I], X[I + 1], Y[I + 1], S[I + 1])
			I += 1

	# Destructor
	def Dispose(self):
		self._Segs = None
		self._Cubics = None

	# Get offset
	def CalcOffset(self, X):
		I = self.FindSeg(X)
		return self._Cubics[I].CalcOffset(X)

	# Get gradient
	def CalcGradient(self, X):
		I = self.FindSeg(X)
		return self._Cubics[I].CalcGradient(X)

	# Is X valid in spline
	def IsValidX(self, X):
		return X >= self._Segs[0] and X <= self._Segs[self._Count - 1]

	# Find segment to X
	def FindSeg(self, X):
		# binary chop search for interval.
		Lo = 0
		Hi = self._Count
		while Lo + 1 < Hi:
			Mid = (Lo + Hi) / 2
			if X >= self._Segs[Mid]:
				Lo = Mid
			else:
				Hi = Mid
		return Lo
