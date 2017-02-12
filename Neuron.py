'''
Created on Feb 4, 2017

@author: Jake
'''
import math
from Connection import Connection

class Neuron(object):
	inCons     	= []
	outCons    	= []
	neuronID   	= None
	neuronType 	= None
	value      	= None

	def __init__(self):
		pass
	# Recurse through the network in reverse and calculate the final output value
	# If an input node is reached return sigmoid of value (base-case)
	# Otherwise sum the weight of connections * their input values for the whole network
	# return the final output value
	def neuralNet(self,sigmoid = True):
		if self.neuronType == 'input':
			if sigmoid: return sigmoidF(self.value)
			else: return self.value
		value = 0
		for connection in self.inCons:
			value += connection.weight * connection.inNeuron.neuralNet()
		if sigmoid: return sigmoidF(value)
		else: return value


	#Return an identical copy of the neuron 
	def copy(self):
		new = Neuron()
		new.neuronID 	= self.neuronID
		new.inCons 		= self.inCons
		new.outCons 	= self.outCons
		new.neuronType	= self.neuronType
		new.value		= self.value
		return new 

	#Print the properities of the neuron
	def printNeuron(self):
		print ("Neuron ID: %d \nNeuron Type: %s \n"% (self.neuronID, self.neuronType)
		+ "Neuron Value: %d \nNeuron Inputs: %s \n"% (self.value, str(self.inCons))
		+ "Neuron Outputs: %s" %(str(self.outCons)))




#Specialized sigmoid function applied  to the value at each neuron
#Subject to change in order to refine predictions
def sigmoidF(x):
	#MUST CHANGE SIGMOIDF FUNCTION WITHIN RANGE OF DESIRED OUTPUTS
	return (2 / (1+math.exp(-4.9*(x))))-1