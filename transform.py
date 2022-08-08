from math import radians, cos, sin
import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

class Transform():
	
	def __init__(self, *args):
		super(Transform, self).__init__(*args)
		self.transformations = {
			'T': self.translate,
			'O': self.rotate,
			'C': self.scale,
			'S': self.shear,
			'R': self.reflect
		}
		self.N_2 = np.eye(3)
		self.N_3 = np.eye(4)
		#self.transform()
		

	# Function to translate an object
	def translate(self, *args):
		try:
			if args[0] == '2D': #For 2D
				T = self.N_2
				T[2][0] = float(args[1])
				T[2][1] = float(args[2])

			else: #For 3D
				T = self.N_3
				T[3][0] = float(args[1])
				T[3][1] = float(args[2])
				T[3][2] = float(args[3])
				
			return T.astype(np.float32)

		except:
			return '\nAn error occurred, try again. \n'

	# Function to rotate an object about an origin or a point
	def rotate(self, *args):
		tita = float(args[1])
		if args[2]=='Clockwise':
			tita=-tita
		try:
			costita = cos(radians(tita))
			sintita = sin(radians(tita))

			if args[0] == '2D': #For 2D
				O = self.N_2
				O[0][0] = costita
				O[1][1] = costita
				O[0][1] = sintita
				O[1][0] = -sintita

				#if args[3] == 'Point':
				#	cord = args[4].split(',')
				#	for i in self.cord:
				#		i = int(i)

			else: #For 3D
				O = self.N_3
				axis = args[3]
				if axis == 'X':
					O[1][1] = costita
					O[2][2] = costita
					O[1][2] = sintita
					O[2][1] = -sintita
				elif axis == 'Y':
					O[0][0] = costita
					O[2][2] = costita
					O[2][0] = sintita
					O[0][2] = -sintita
				elif axis == 'Z':
					O[0][0] = costita
					O[1][1] = costita
					O[0][1] = sintita
					O[1][0] = -sintita

			return O.astype(np.float32)

		except:
			return 'An error occurred, try again.'


	# Function to scale an object's size
	def scale(self, *args):
		try:
			if args[0] == '2D' : #For 2D
				C = self.N_2
				C[0][0] = float(args[1])
				C[1][1] = float(args[2])

			else: #For 3D
				C = self.N_3
				C[0][0] = float(args[1])
				C[1][1] = float(args[2])
				C[2][2] = float(args[3])

			return C.astype(np.float32)

		except:
			return 'An error occurred, try again.'

	# Function to shear an object
	def shear(self, *args):

		try:
			if args[0] == '2D': #For 2D
				S = self.N_2
				sh = args[2]
				axis = args[1]
				rel = args[3]
				sh = float(sh)

				if rel == 'Yes':
					rel_para = float(args[4])
					if axis == 'Y':
						S[2][1] = -sh*rel_para
					elif axis == 'X':
						S[2][0] = -sh*rel_para

				if axis == 'Y':
					S[0][1] = sh

				elif axis == 'X':
					S[1][0] = sh

			else: #For 3D
				S = self.N_3
				if args[1] == 'X':
					S[0][1] = float(args[2])
					S[0][2] = float(args[3])
				elif args[1] == 'Y':
					S[1][0] = float(args[2])
					S[1][2] = float(args[3])
				elif args[1] == 'Z':
					S[2][0] = float(args[2])
					S[2][1] = float(args[3])
					
			return S.astype(np.float32)

		except:
			return 'An error occured, try again!'

	# Function to reflect an object
	def reflect(self, *args):

		try:
			if args[0] == '2D':
				R = self.N_2
				axis = args[1]
				if axis == 'X':
					R[1][1] = -1
				elif axis == 'Y':
					R[0][0] = -1
				elif axis == 'Origin':
					R[1][1] = -1
					R[0][0] = -1
				elif axis == 'Line':
					ref = args[2]
					if ref == 'X':
						R[0][0] = 0
						R[1][1] = 0
						R[0][1] = 1
						R[1][0] = 1
					elif ref == 'Y':
						R[0][0] = 0
						R[1][1] = 0
						R[0][1] = -1
						R[1][0] = -1

			else:
				R = self.N_3
				plane = args[1]
				if plane == 'XY':
					R[2][2] = -1
				elif plane == 'XZ':
					R[1][1] = -1
				elif plane == 'YZ':
					R[0][0] = -1
					
			return R.astype(np.float32)

		except:
			return 'An exception occurred'
