'''
Created on Feb 4, 2017

@author: Jake
'''
import numpy as np
import random
import Population

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
		if(self.inNeuron.neuronType=='hidden'):
			self.inNeuron.neuronID=self.ID
		if(self.outNeuron.neuronType=='hidden'):
			self.outNeuron.neuronID=self.ID

		#Hi future luke and Jake Think about  making connection .equals function for convergent evolution

	def mutateWeight(self):
		#generates a random bool efficiently bitwise
		if random.getrandbits(1): self.weight = self.weight + Population.MUTATION_VALUE
		else: self.weight = self.weight - Population.MUTATION_VALUE

	def mutateEnable(self):
		#switch the enabled status of the connection
		#WORRY ABOUT LATER CAN CAUSE BACK PROP PROBLEMS
		self.enabled = not self.enabled

	def copy(self):
		return Connection(self.ID, self.inNeuron, self.outNeuron, self.weight)

	def __eq__(self, other):
		# if self.inNeuron  	!= other.inNeuron: return False
		# if self.outNeuron 	!= other.outNeuron: return False
		# if self.enabled   	!= other.enabled: return False
		print "SAME"
		return True