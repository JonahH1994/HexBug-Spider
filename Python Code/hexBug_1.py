import socket
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import functions_tcp
import ViconTrackerPoseHandler as vt
import threading as td 

class hexBug(object):

	#UDP_IP = None
	#UDP_PORT = None
	#name = None
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#r0 = np.array([0,0,np.pi/2])
	#hexB = None
	#rot_const = 3 / 2/ np.pi
	#mot_const = 3.69 
	#tolerance = 0.5

	def __init__(self, IP_BUG, name, port, vic_port ):

		self.name = name
		self.UDP_IP = IP_BUG
		self.UDP_PORT = port

		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.soc.connect((IP_BUG, port))

		self.cali = False

		self.r0 = np.array([0,0,np.pi/2])
		self.prevR = self.r0 
		self.orientation = 0
		self.mot_const = 3.69 
		self.rot_const = 4.0675/ ( 2 * np.pi )
		self.tolerance = 0.05 # 0.1
		self.calib_tol = 0.025
		self.angTol = np.pi/30
		self.hexB = vt.ViconTrackerPoseHandler(None, None, "", vic_port, name )
		self.thread1 = td.Thread(target=self.updatePo, args=() )
		self.thread1.start()
		#print( self.r0 )
		while np.all( self.r0 == 0 ):
			self.mot_const = self.mot_const 
			#print( self.r0 )
		self.motionStart = 0
		time.sleep(2)
		self.__calibrate()
		time.sleep(2)
		self.orientThread = td.Thread(target=self.findOrientation, args=() )
		self.orientThread.daemon = True 
		self.orientThread.start()
		#self.r0 = hexB.getPose()

		#self.__r0 = hexB.getPose() 
	"""
	def cordToRad(self, p1, p2, the = None):

		# Vector from point 1 to 2
		r12 = p2 - p1

		# Current direction of the HexBug
		nor = [ np.cos(the), np.sin(the) ]

		# Magnitude of the distance vector
		r = np.sqrt( np.dot( r12, r12 ) )
		theN = np.arccos( np.dot( nor, r12 )/ r )


		# Check to see if angle should be positive or negative
		nor1 = [ np.cos( the + theN ), np.sin( the + theN ) ]

		#print( np.abs( np.dot( nor1, r12 )/ r - 1 ) )

		if( np.abs( np.dot( nor1, r12 )/ r - 1) > self.tolerance ):
			theN = -theN 

		return r, theN	

	"""

	def cordToRad(self, p1, p2, the):

		# Vector from point 1 to 2
		r12 = p2 - p1
		the = self.orientation

		# Current direction of the HexBug
		nor = [ np.cos(the), np.sin(the) ]

		# Magnitude of the distance vector
		r = np.sqrt( np.dot( r12, r12 ) )
		theN = np.arccos( np.dot( nor, r12 )/ r )


		# Check to see if angle should be positive or negative
		nor1 = [ np.cos( the + theN ), np.sin( the + theN ) ]

		#print( np.abs( np.dot( nor1, r12 )/ r - 1 ) )

		if( np.abs( np.dot( nor1, r12 )/ r - 1) > self.tolerance ):
			theN = -theN 

		return r, theN	

	def writeXY( self, pos ):

		"""
		the0 = self.r0[2]
		x0 = self.r0[0]
		y0 = self.r0[1]

		dm = len( pos )

		r = np.zeros(dm)
		thes = np.zeros( dm )

		for i in range(dm):

			if i is 0:

				r[i], thes[i] = self.cordToRad( [x0,y0], pos[i], the0 )

			else:

				r[i], thes[i] = self.cordToRad( pos[i-1], pos[i], the0 )

			the0 += thes[i]

		"""

		#self.thread = td.Thread(target = self.writeToTCP, args=(r, thes, pos, ) )
		self.thread = td.Thread(target = self.writeToTCP, args=( pos, ) )
		self.thread.daemon = True 
		self.thread.start()


	#def writeToTCP(self, r, the, pos ):
	def writeToTCP(self, pos ):

		self.motionStart = 1
		time.sleep(1)

		for i in range( len( pos ) ): 

			x = pos[i][0]
			y = pos[i][1]

			pT = self.r0 

			#print( pT )

			r, the = self.cordToRad( pT[0:2], pos[i], pT[2] )

			if np.abs( the == 0 ) :
		
				self.__fwd_back( r )

			else:

				self.__rig_lef( the )
				self.__fwd_back( r )


			print( "Doing things" )
			time.sleep(1)
			while ( np.abs( x - self.r0[0] ) > self.tolerance ) and ( np.abs( y - self.r0[1] ) > self.tolerance ):
			#while( np.sqrt( (x-self.r0[0])^2 + (y-self.r0[1])^2 ) > self.tolerance):

				self.findOrientation() 
				if np.abs( the - self.orientation ) > self.angTol :

					print( "Fixing Orientation" )
					r1, th1 = self.cordToRad( self.r0[0:2], pos[i], self.r0[2] )
					self.__rig_lef( th1 )
					self.__fwd_back( r1 )
					the = self.orientation

				#print( "Still moving to position " + str(i+1) )
				#print( self.orientation )
				#print( the )

			self.soc.send( b's' )


		self.motionStart = 0
		self.close()

	def __fwd_back(self, r ):

		if r < 0:

			self.soc.send( b'k' ) 

		else:

			self.soc.send( b'i')

		#time.sleep( np.abs( r/ self.mot_const ) )

	def __rig_lef( self, the ):

		if the < 0:

			self.soc.send( b'l' )
			print( "left" )

		else:

			self.soc.send( b'j' )
			print( "right" )

		#time.sleep( np.abs( the * self.rot_const ) )
		#self.s.send( b's' )
		#time.sleep(1)

		print( "Rotating")
		#while np.abs( the - self.r0[2] ) > self.angTol :
		#self.orientThread.pause()
		time.sleep( np.abs(the) * self.rot_const )
		print( "Done Rotating")
		self.orientation = the 

		self.soc.send( b's' )

	def close(self):

		self.soc.send(b's')
		self.soc.close() 

	def getPos(self):

		return self.r0

	def getDist( self, x1, y1 ):

		return( np.sqrt( ( x1 - self.r0[0] )^2 + ( y1 - self.r0[1] )^2 ) )

	def updatePo( self ):

		while True:
			time.sleep(0.1)
			self.r0 = self.hexB.getPose()


	def arccos2( self, p1, p2 ):

		nor = p2 - p1  
		mag = np.sqrt( np.dot( nor, nor ) )
		nor = nor/ mag

		axVec = [ 1, 0 ]
		offset = 0

		if np.sign(nor[0]) * np.sign(nor[1]) == 1:

			# Vector is pointing in either quadrant one or three

			if np.sign(nor[0]) == -1:
				# In third quadrant
				axVec = [ -1, 0 ]
				offset = np.pi

			# else the vector is as we assumed previously.

		else:

			# Vector is pointing in either quadrant two or four

			if np.sign(nor[0]) == 1 :
				# In fourth quadrant
				axVec = [0,-1]
				offset = 3 * np.pi/2

			else:
			 	# In the second quadrant
				axVec = [ 0, 1]
				offset = np.pi/2

		return np.arccos( np.dot( nor, axVec ) ) + offset
	 
	def findOrientation( self ):

		#time.sleep( 0.5 )

		nor = self.prevR[0:2] - self.r0[0:2]   
		mag = np.sqrt( np.dot( nor, nor ) )
		#print( nor/mag )

		if mag > self.tolerance or self.cali == True:

			self.orientation = self.arccos2( self.prevR[0:2], self.r0[0:2]  )
			self.prevR = self.r0 

	def __calibrate( self ):
		
		# Have the robot move forward to estimate normal vector
		self.cali = True 
		tol = self.calib_tol
		self.prevR = self.r0 
		self.soc.send(b'i')
		while( np.abs( self.prevR[0] - self.r0[0] ) < tol or np.abs( self.prevR[1] - self.r0[1] ) < tol ):
			# do nothing
			self.tolerance = self.tolerance
			#print( "Still here" )
			#print( self.r0 )
		self.soc.send(b's')

		self.findOrientation()
		self.cali = False 
		print( self.orientation )