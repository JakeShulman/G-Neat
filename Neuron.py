'''
Created on Feb 4, 2017

@author: Jake
'''
import math
from Connection import Connection
from Gene import Gene
class Neuron(object):
	inCons     	= []
	outCons    	= []
	neuronID   	= None
	neuronType 	= None
	value      	= None

	def __init__(self,ID):
		self.neuronID = ID

	# Recurse through the network in reverse and calculate the final output value
	# If an input node is reached return sigmoid of value (base-case)
	# Otherwise sum the weight of connections * their input values for the whole network
	# return the final output value
	def neuralNet(self):
		if self.neuronType == 'input':
			return sigmoid(self.value)
		value = 0
		for connection in self.inCons:
			value += connection.weight * connection.inNeuron.neuralNet()
		return sigmoid(value)

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
def sigmoid(x):
	return (2 / (1+math.exp(-4.9*(x))))-1