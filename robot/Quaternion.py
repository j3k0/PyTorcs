from System import *

class Quaternion(object):
	#		public Quaternion()
	#		{
	#			this.w = 1.0f;
	#		}
	def __init__(self, w, x, y, z):
		""" <summary>
				Creates a new Quaternion.
		 </summary>
		"""
		self._EPSILON = 1e-03f
		self._identityQuat = Quaternion(1.0f, 0.0f, 0.0f, 0.0f)
		self._zeroQuat = Quaternion(0.0f, 0.0f, 0.0f, 0.0f)
		self._next = Array[int]((1, 2, 0))
		self._w = w
		self._x = x
		self._y = y
		self._z = z

	# public Quaternion( OgreQuaternion q )
	# {
	# this.x = q.x;
	# this.y = q.y;
	# this.z = q.z;
	# this.w = q.w;
	# }
	# 
	# public OgreQuaternion ToOgreQuaternion()
	# {
	# return new OgreQuaternion( this.w, this.x, this.y, this.z );
	# }
	def Multiply(left, right):
		""" <summary>
		 Used to multiply 2 Quaternions together.
		 </summary>
		 <remarks>
				Quaternion multiplication is not communative in most cases.
				i.e. p*q != q*p
		 </remarks>
		 <param name="left"></param>
		 <param name="right"></param>
		 <returns></returns>
		"""
		return left * right

	Multiply = staticmethod(Multiply)

	# 
	# return new Quaternion
	# (
	# left.w * right.w - left.x * right.x - left.y * right.y - left.z * right.z,
	# left.w * right.x + left.x * right.w + left.y * right.z - left.z * right.y,
	# left.w * right.y + left.y * right.w + left.z * right.x - left.x * right.z,
	# left.w * right.z + left.z * right.w + left.x * right.y - left.y * right.x
	# );
	def Multiply(quat, vector):
		""" <summary>
		 
		 </summary>
		 <param name="quat"></param>
		 <param name="vector"></param>
		 <returns></returns>
		"""
		return quat * vector

	Multiply = staticmethod(Multiply)

	# nVidia SDK implementation
	# get the rotation matrix of the Quaternion and multiply it times the vector
	#return quat.ToRotationMatrix() * vector;
	def Multiply(scalar, right):
		""" <summary>
		 Used when a float value is multiplied by a Quaternion.
		 </summary>
		 <param name="scalar"></param>
		 <param name="right"></param>
		 <returns></returns>
		"""
		return scalar * right

	Multiply = staticmethod(Multiply)

	def Multiply(left, scalar):
		""" <summary>
		 Used when a Quaternion is multiplied by a float value.
		 </summary>
		 <param name="left"></param>
		 <param name="scalar"></param>
		 <returns></returns>
		"""
		return left * scalar

	Multiply = staticmethod(Multiply)

	def Add(left, right):
		""" <summary>
		 Used when a Quaternion is added to another Quaternion.
		 </summary>
		 <param name="left"></param>
		 <param name="right"></param>
		 <returns></returns>
		"""
		return left + right

	Add = staticmethod(Add)

	# <summary>
	#    An Identity Quaternion.
	# </summary>
	def get_Identity(self):
		return self._identityQuat

	Identity = property(fget=get_Identity)

	# <summary>
	#    A Quaternion with all elements set to 0.0f;
	# </summary>
	def get_Zero(self):
		return self._zeroQuat

	Zero = property(fget=get_Zero)

	# <summary>
	#		Squared 'length' of this quaternion.
	# </summary>
	def get_Norm(self):
		return x * x + y * y + z * z + self._w * self._w

	Norm = property(fget=get_Norm)

	# <summary>
	#    Local X-axis portion of this rotation.
	# </summary>
	def get_XAxis(self):
		fTy = 2.0f * y
		fTz = 2.0f * z
		fTwy = fTy * self._w
		fTwz = fTz * self._w
		fTxy = fTy * x
		fTxz = fTz * x
		fTyy = fTy * y
		fTzz = fTz * z
		return Vector3(1.0f - (fTyy + fTzz), fTxy + fTwz, fTxz - fTwy)

	XAxis = property(fget=get_XAxis)

	# <summary>
	#    Local Y-axis portion of this rotation.
	# </summary>
	def get_YAxis(self):
		fTx = 2.0f * x
		fTy = 2.0f * y
		fTz = 2.0f * z
		fTwx = fTx * self._w
		fTwz = fTz * self._w
		fTxx = fTx * x
		fTxy = fTy * x
		fTyz = fTz * y
		fTzz = fTz * z
		return Vector3(fTxy - fTwz, 1.0f - (fTxx + fTzz), fTyz + fTwx)

	YAxis = property(fget=get_YAxis)

	# <summary>
	#    Local Z-axis portion of this rotation.
	# </summary>
	def get_ZAxis(self):
		fTx = 2.0f * x
		fTy = 2.0f * y
		fTz = 2.0f * z
		fTwx = fTx * self._w
		fTwy = fTy * self._w
		fTxx = fTx * x
		fTxz = fTz * x
		fTyy = fTy * y
		fTyz = fTz * y
		return Vector3(fTxz + fTwy, fTyz - fTwx, 1.0f - (fTxx + fTyy))

	ZAxis = property(fget=get_ZAxis)

	def Slerp(time, quatA, quatB):
		return Quaternion.Slerp(time, quatA, quatB, False)

	Slerp = staticmethod(Slerp)

	def Slerp(time, quatA, quatB, useShortestPath):
		""" <summary>
		 
		 </summary>
		 <param name="time"></param>
		 <param name="quatA"></param>
		 <param name="quatB"></param>
		 <param name="useShortestPath"></param>
		 <returns></returns>
		"""
		cos = quatA.Dot(quatB)
		angle = Math.Acos(cos)
		if Math.Abs(angle) < self._EPSILON:
			return quatA
		sin = Math.Sin(angle)
		inverseSin = 1.0f / sin
		coeff0 = Math.Sin((1.0f - time) * angle) * inverseSin
		coeff1 = Math.Sin(time * angle) * inverseSin
		if cos < 0.0f and useShortestPath:
			coeff0 = -coeff0
			# taking the complement requires renormalisation
			t = coeff0 * quatA + coeff1 * quatB
			t.Normalize()
			result = t
		else:
			result = (coeff0 * quatA + coeff1 * quatB)
		return result

	Slerp = staticmethod(Slerp)

	def FromAngleAxis(angle, axis):
		""" <summary>
		 Creates a Quaternion from a supplied angle and axis.
		 </summary>
		 <param name="angle">Value of an angle in radians.</param>
		 <param name="axis">Arbitrary axis vector.</param>
		 <returns></returns>
		"""
		quat = Quaternion()
		halfAngle = 0.5f * angle
		sin = Math.Sin(halfAngle)
		quat.w = Math.Cos(halfAngle)
		quat.x = sin * axis.x
		quat.y = sin * axis.y
		quat.z = sin * axis.z
		return quat

	FromAngleAxis = staticmethod(FromAngleAxis)

	def FromAngleDegreeAxis(angleD, axis):
		""" <summary>
		 Creates a Quaternion from a supplied angle and axis.
		 </summary>
		 <param name="angle">Value of an angle in radians.</param>
		 <param name="axis">Arbitrary axis vector.</param>
		 <returns></returns>
		"""
		quat = Quaternion()
		angle = angleD * (Math.PI / 180.0)
		halfAngle = 0.5f * angle
		sin = Math.Sin(halfAngle)
		quat.w = Math.Cos(halfAngle)
		quat.x = sin * axis.x
		quat.y = sin * axis.y
		quat.z = sin * axis.z
		return quat

	FromAngleDegreeAxis = staticmethod(FromAngleDegreeAxis)

	def Squad(t, p, a, b, q):
		return Quaternion.Squad(t, p, a, b, q, False)

	Squad = staticmethod(Squad)

	def Squad(t, p, a, b, q, useShortestPath):
		""" <summary>
				Performs spherical quadratic interpolation.
		 </summary>
		 <param name="t"></param>
		 <param name="p"></param>
		 <param name="a"></param>
		 <param name="b"></param>
		 <param name="q"></param>
		 <returns></returns>
		"""
		slerpT = 2.0f * t * (1.0f - t)
		# use spherical linear interpolation
		slerpP = Quaternion.Slerp(t, p, q, useShortestPath)
		slerpQ = Quaternion.Slerp(t, a, b)
		# run another Slerp on the results of the first 2, and return the results
		return Quaternion.Slerp(slerpT, slerpP, slerpQ)

	Squad = staticmethod(Squad)

	def Dot(self, quat):
		""" <summary>
		 Performs a Dot Product operation on 2 Quaternions.
		 </summary>
		 <param name="quat"></param>
		 <returns></returns>
		"""
		return self._w * quat.w + self._x * quat.x + self._y * quat.y + self._z * quat.z

	def Normalize(self):
		""" <summary>
				Normalizes elements of this quaterion to the range [0,1].
		 </summary>
		"""
		factor = 1.0f / Math.Sqrt(self.Norm)
		self._w = self._w * factor
		x = x * factor
		y = y * factor
		z = z * factor

	def ToAngleAxis(self, angle, axis):
		""" <summary>
		    
		 </summary>
		 <param name="angle"></param>
		 <param name="axis"></param>
		 <returns></returns>
		"""
		# The quaternion representing the rotation is
		#   q = cos(A/2)+sin(A/2)*(x*i+y*j+z*k)
		sqrLength = x * x + y * y + z * z
		if sqrLength > 0.0f:
			angle = 2.0f * Math.Acos(self._w)
			invLength = -Math.Sqrt(sqrLength)
			axis.x = x * invLength
			axis.y = y * invLength
			axis.z = z * invLength
		else:
			angle = 0.0f
			axis.x = 1.0f
			axis.y = 0.0f
			axis.z = 0.0f

	def ToRotationMatrix(self):
		""" <summary>
		 Gets a 3x3 rotation matrix from this Quaternion.
		 </summary>
		 <returns></returns>
		"""
		rotation = Matrix3()
		tx = 2.0f * self._x
		ty = 2.0f * self._y
		tz = 2.0f * self._z
		twx = tx * self._w
		twy = ty * self._w
		twz = tz * self._w
		txx = tx * self._x
		txy = ty * self._x
		txz = tz * self._x
		tyy = ty * self._y
		tyz = tz * self._y
		tzz = tz * self._z
		rotation.m00 = 1.0f - (tyy + tzz)
		rotation.m01 = txy - twz
		rotation.m02 = txz + twy
		rotation.m10 = txy + twz
		rotation.m11 = 1.0f - (txx + tzz)
		rotation.m12 = tyz - twx
		rotation.m20 = txz - twy
		rotation.m21 = tyz + twx
		rotation.m22 = 1.0f - (txx + tyy)
		return rotation

	def Inverse(self):
		""" <summary>
		 Computes the inverse of a Quaternion.
		 </summary>
		 <returns></returns>
		"""
		norm = self._w * self._w + self._x * self._x + self._y * self._y + self._z * self._z
		if norm > 0.0f:
			inverseNorm = 1.0f / norm
			return Quaternion(self._w * inverseNorm, -self._x * inverseNorm, -self._y * inverseNorm, -self._z * inverseNorm)
		else:
			# return an invalid result to flag the error
			return Quaternion.Zero

	def ToAxes(self, xAxis, yAxis, zAxis):
		""" <summary>
		 
		 </summary>
		 <param name="xAxis"></param>
		 <param name="yAxis"></param>
		 <param name="zAxis"></param>
		"""
		xAxis = Vector3()
		yAxis = Vector3()
		zAxis = Vector3()
		rotation = self.ToRotationMatrix()
		xAxis.x = rotation.m00
		xAxis.y = rotation.m10
		xAxis.z = rotation.m20
		yAxis.x = rotation.m01
		yAxis.y = rotation.m11
		yAxis.z = rotation.m21
		zAxis.x = rotation.m02
		zAxis.y = rotation.m12
		zAxis.z = rotation.m22

	def FromAxes(self, xAxis, yAxis, zAxis):
		""" <summary>
		 
		 </summary>
		 <param name="xAxis"></param>
		 <param name="yAxis"></param>
		 <param name="zAxis"></param>
		"""
		rotation = Matrix3()
		rotation.m00 = xAxis.x
		rotation.m10 = xAxis.y
		rotation.m20 = xAxis.z
		rotation.m01 = yAxis.x
		rotation.m11 = yAxis.y
		rotation.m21 = yAxis.z
		rotation.m02 = zAxis.x
		rotation.m12 = zAxis.y
		rotation.m22 = zAxis.z
		# set this quaternions values from the rotation matrix built
		self.FromRotationMatrix(rotation)

	def FromRotationMatrix(self, matrix):
		""" <summary>
		 
		 </summary>
		 <param name="matrix"></param>
		"""
		# Algorithm in Ken Shoemake's article in 1987 SIGGRAPH course notes
		# article "Quaternion Calculus and Fast Animation".
		trace = matrix.m00 + matrix.m11 + matrix.m22
		root = 0.0f
		if trace > 0.0f:
			# |this.w| > 1/2, may as well choose this.w > 1/2
			root = Math.Sqrt(trace + 1.0f) # 2w
			self._w = 0.5f * root
			root = 0.5f / root # 1/(4w)
			self._x = (matrix.m21 - matrix.m12) * root
			self._y = (matrix.m02 - matrix.m20) * root
			self._z = (matrix.m10 - matrix.m01) * root
		else:
			# |this.w| <= 1/2
			i = 0
			if matrix.m11 > matrix.m00:
				i = 1
			if matrix.m22 > matrix[i][i]:
				i = 2
			j = self._next[i]
			k = self._next[j]
			root = Math.Sqrt(matrix[i][i] - matrix[j][j] - matrix[k][k] + 1.0f)

	def Log(self):
		""" <summary>
				Calculates the logarithm of a Quaternion.
		 </summary>
		 <returns></returns>
		"""
		# BLACKBOX: Learn this
		# If q = cos(A)+sin(A)*(x*i+y*j+z*k) where (x,y,z) is unit length, then
		# log(q) = A*(x*i+y*j+z*k).  If sin(A) is near zero, use log(q) =
		# sin(A)*(x*i+y*j+z*k) since sin(A)/A has limit 1.
		# start off with a zero quat
		result = Quaternion.Zero
		if Math.Abs(self._w) < 1.0f:
			angle = Math.Acos(self._w)
			sin = Math.Sin(angle)
			if Math.Abs(sin) >= self._EPSILON:
				coeff = angle / sin
				result.x = coeff * x
				result.y = coeff * y
				result.z = coeff * z
			else:
				result.x = x
				result.y = y
				result.z = z
		return result

	def Exp(self):
		""" <summary>
				Calculates the Exponent of a Quaternion.
		 </summary>
		 <returns></returns>
		"""
		# If q = A*(x*i+y*j+z*k) where (x,y,z) is unit length, then
		# exp(q) = cos(A)+sin(A)*(x*i+y*j+z*k).  If sin(A) is near zero,
		# use exp(q) = cos(A)+A*(x*i+y*j+z*k) since A/sin(A) has limit 1.
		angle = Math.Sqrt(x * x + y * y + z * z)
		sin = Math.Sin(angle)
		# start off with a zero quat
		result = Quaternion.Zero
		result.w = Math.Cos(angle)
		if Math.Abs(sin) >= self._EPSILON:
			coeff = sin / angle
			result.x = coeff * x
			result.y = coeff * y
			result.z = coeff * z
		else:
			result.x = x
			result.y = y
			result.z = z
		return result

	def ToString(self):
		""" <summary>
				Overrides the Object.ToString() method to provide a text representation of 
				a Quaternion.
		 </summary>
		 <returns>A string representation of a Quaternion.</returns>
		"""
		return str.Format("Quaternion({0}, {1}, {2}, {3})", self._x, self._y, self._z, self._w)

	def GetHashCode(self):
		return x ^ y ^ z ^ self._w

	def Equals(self, obj):
		quat = obj
		return quat == self
