import numpy as np
import scipy as sp
import math


class sysParams(object):
	
	def __init__(self,n):
		self.n = n
		self.inputLim = np.ones(n)*0.1 #0.1
		self.kp = 10 #1.0 #5.0
		self.Ds = 0.2
		self.DsWall = 0.25 #0.38
		self.gamma = 8 #0.1#8 #0.1
		self.closeEnoughPose = 0.05 # 0.32 #0.2
		
		# deadlock
		self.deadlockThreInput = 0.08
		self.kDelta = 2.0
		self.controlTurnAng = 3.0*math.pi/4
		
		
		
		
	# get initial poses
	def initPose(self):
		self.theta0 = 0
		self.radius = 1.5
		self.initPose = np.zeros([2,self.n])
		
		# self.initPose = pose
	
	# get goal poses
	def goalPose(self):
		self.goalPose = np.zeros([2,self.n])
		
		# self.goalPose = pose
		
	# get neighborhood radius
	def neighborRadius(self):
		self.Dneighbor = np.zeros(self.n)
		for i in range(self.n):
			betaMax = max(self.inputLim)
			self.Dneighbor[i] = self.Ds+((self.inputLim[i]+betaMax)/self.gamma)**(1.0/3)
			
		#return self
		
	# get current positions
	def getCurrentPose(self,pose):
		self.currentPose = pose
		#return self
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
