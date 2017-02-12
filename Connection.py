'''
Created on Feb 4, 2017

@author: Jake
'''
import numpy as np
import random
from Population import MUTATION_VALUE

class Connection(object):
	inNeuron  	= None
	outNeuron 	= None
	weight 		= None
	enabled		= None
	ID			= None

	def __init__(self,ID,inNeuron,outNeuron,weight,enabled = True):
		self.inNeuron  	= inNeuron
		self.outNeuron 	= outNeuron
		self.weight    	= weight
		self.enabled   	= enabled
		self.ID			= ID

	def mutateWeight(self):
		#generates a random bool efficiently bitwise
		if random.randbits(1): self.weight = self.weight + MUTATION_VALUE
		else: self.weight = self.weight - MUTATION_VALUE

	def mutateEnable(self):
		#switch the enabled status of the connection
		#WORRY ABOUT LATER CAN CAUSE BACK PROP PROBLEMS
		self.enabled = not self.enabled

	def copy(self):
		return Connection(self.ID, self.inNeuron, self.outNeuron, self.weight)