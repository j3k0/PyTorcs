#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
# Quadratic.cs
#--------------------------------------------------------------------------*
#
# file         : Quadratic.cs
# created      : 02 Aug 2008
# last changed : 02 Aug 2008
# Copyright    : ###COPYRIGHTHOLDER###
# eMail        : ###CONTACT###
# Version      : 0.00.010 
#  
#--------------------------------------------------------------------------*
# ###COPYRIGHT###
#--------------------------------------------------------------------------*
from System import *
from Torcs import *

class Quadratic(object):
	# Default Constructor
	def __init__(self, X, Y, VelY, AccY):
		# Parametric constructor
		# Constructor
		self.Set(X, Y, VelY, AccY)

	def __init__(self, X, Y, VelY, AccY):
		self.Set(X, Y, VelY, AccY)

	def __init__(self, X, Y, VelY, AccY):
		self.Set(X, Y, VelY, AccY)

	# Set parameters
	def Set(self, a, b, c):
		self._A = a
		self._B = b
		self._C = c

	# Set parameters
	def Set(self, X, Y, VelY, AccY):
		self._A = AccY / 2
		self._B = VelY - 2 * self._A * X
		self._C = Y - (self._A * X + self._B) * X

	# Find minimum
	def CalcMin(self):
		# minimum is where slope == 0
		X = -self._B / (2 * self._A)
		return X

	# Horner schema
	def CalcY(self, X):
		return (self._A * X + self._B) * X + self._C

	# Solve 
	def Solve(self, Y, X0, X1):
		if self._A == 0:
			if self._B == 0:
				return False
			# y == bx + c
			#
			# x = (y - c) / b
			X0 = X1 = (Y - self._C) / self._B
			return True
		# y == a * x * x + b * x + c
		#
		# a * x * x + b * x + (c - y) == 0
		#
		# x = (-b +/- sqrt(b * b - 4 * a * (c - y))] / (2 * a)
		Inner = self._B * self._B - 4 * self._A * (self._C - Y)
		if Inner < 0:
			return False
		Inner = Math.Sqrt(Inner)
		X0 = (-self._B - Inner) / (2 * self._A)
		X1 = (-self._B + Inner) / (2 * self._A)
		return True

	# SmallestNonNegativeRoot
	def SmallestNonNegativeRoot(self, T):
		X0 = 0.0
		X1 = 0.0
		if not self.Solve(0, , ):
			return False
		T = X0
		if X1 >= 0 and X1 < X0:
			T = X1
		return T >= 0

	# Add two Quadratics
	# Substract two Quadratics
