import rospy
import tf
import threading
import time
from numpy import *

class ViconTracker(object):

	Xx = 0
	Yy = 0
	Oo = 0 

	def __init__(self, hexBugNumber):

		#init_node()		
		self.target = 'vicon/HexBug' + str(hexBugNumber) + '/HexBug' + str(hexBugNumber)

		self.x = 0
		self.y = 0
		self.o = 0

		self.t = tf.TransformListener()

		self.thread = threading.Thread(target=self.updatePose)
		self.thread.daemon = True
		self.thread.start()


	def updatePose(self):
		rospy
		#while True:
		#a = self.t.lookupTransform('world',self.target, rospy.Time(0))
		self.t.waitForTransform('world',self.target, rospy.Time(0), rospy.Duration(4.0))
#			while not rospy.is_shutdown():
#				try:
#					now = rospy.Time.now()
#					self.t.waitForTransform('world',self.target, now, rospy.Duration(4.0))
		a = self.t.lookupTransform('world',self.target, rospy.Time(0))			
		self.x = a[0][0]
		self.y = a[0][1]
		euler = tf.transformations.euler_from_quaternion(a[1])
		self.o = euler[2]
		Xx = self.x
		Yy = self.y
		Oo = self.o

	def _stop(self):
		print( "Vicon pose handler quitting..." )
		self.thread.join()
		print( "Terminated." )

	def getPose(self, cached=False):
		#print "({t},{x},{y},{o})".format(t=t,x=x,y=y,o=o)
		self.updatePose()
		return array([self.x, self.y, self.o])

if __name__ == "__main__": 

	rospy.init_node('Hexbug_listener')
	a = ViconTracker(7)
	print(a.getPose())
	time.sleep(2)

	while True: 
		time.sleep(0.5)
		b = a.getPose() 
		print( b )

