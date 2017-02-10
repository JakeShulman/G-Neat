'''
Created on Feb 4, 2017

@author: Jake
'''
class Connection(object):
	inNeuron  = None
	outNeuron = None
	weight    = None
	enabled   = None


	def __init__(self,inNeuron,outNeuron,weight,enabled):
		self.inNeuron  = inNeuron
		self.outNeuron = outNeuron
		self.weight    = weight
		self.enabled   = enabled

	def mutateWeight():
		pass

	def mutateEnable():
		pass