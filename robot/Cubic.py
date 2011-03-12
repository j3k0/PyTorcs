#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# Cubic.cs
#--------------------------------------------------------------------------*
#
# file         : Cubic.cs
# created      : 26 Jul 2008
# last changed : 26 Jul 2008
# Copyright    : ###COPYRIGHTHOLDER###
# eMail        : ###CONTACT###
# Version      : 0.00.009 
#  
#--------------------------------------------------------------------------*
# ###COPYRIGHT###
#--------------------------------------------------------------------------*
# Class Cubic
class Cubic(object): # Coefficients
	# Default constructor
	def __init__(self, X0, Y0, S0, X1, Y1, S1):
		self._Coeffs = Array.CreateInstance(Double, 4)
		# Parametric constructor
		# Two point constructor
		self.Set(X0, Y0, S0, X1, Y1, S1)

	def __init__(self, X0, Y0, S0, X1, Y1, S1):
		self._Coeffs = Array.CreateInstance(Double, 4)
		self.Set(X0, Y0, S0, X1, Y1, S1)

	def __init__(self, X0, Y0, S0, X1, Y1, S1):
		self._Coeffs = Array.CreateInstance(Double, 4)
		self.Set(X0, Y0, S0, X1, Y1, S1)

	# Set coefficients
	def Set(self, C0, C1, C2, C3):
		self._Coeffs[0] = C0
		self._Coeffs[1] = C1
		self._Coeffs[2] = C2
		self._Coeffs[3] = C3

	# Set coefficients from two points
	def Set(self, X0, Y0, S0, X1, Y1, S1):
		# uses Ferguson's Parametric Cubic Curve, which requires 2
		#	endpoints and 2 slopes.  here we define the endpoints to
		#	to be (x0,y0) & (x1,y1), and the slopes are given by s0 & s1.
		#
		# see: http://graphics.cs.ucdavis.edu/CAGDNotes/
		#			Catmull-Rom-Spline/Catmull-Rom-Spline.html
		#	for the equations used.
		# step 1. convert to parametric form (x in [0..1])
		#	(this basically only effects the slopes).
		Dx = X1 - X0
		Dy = Y1 - Y0
		S0 *= Dx
		S1 *= Dx
		# step 2. use Ferguson's method.
		C3 = Y0
		C2 = S0
		C1 = 3 * Dy - 2 * S0 - S1
		C0 = -2 * Dy + S0 + S1
		# step 3. convert back to real-world form (x in [x0..x1]).
		X02 = X0 * X0
		X03 = X02 * X0
		Dx2 = Dx * Dx
		Dx3 = Dx2 * Dx
		self._Coeffs[0] = C0 / Dx3
		self._Coeffs[1] = -3 * C0 * X0 / Dx3 + C1 / Dx2
		self._Coeffs[2] = 3 * C0 * X02 / Dx3 - 2 * C1 * X0 / Dx2 + C2 / Dx
		self._Coeffs[3] = -C0 * X03 / Dx3 + C1 * X02 / Dx2 - C2 * X0 / Dx + C3

	# Get offset
	def CalcOffset(self, X):
		return ((self._Coeffs[0] * X + self._Coeffs[1]) * X + self._Coeffs[2]) * X + self._Coeffs[3]

	# Get gradient of offset
	def CalcGradient(self, X):
		return (3 * self._Coeffs[0] * X + 2 * self._Coeffs[1]) * X + self._Coeffs[2]

	# Get 2nd derivative
	def Calc2ndDerivative(self, X):
		return 6 * self._Coeffs[0] * X + 2 * self._Coeffs[1]
