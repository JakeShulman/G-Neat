'''
Created on Feb 5, 2017

@author: Jake
'''
from Neuron import Neuron
from Gene import Gene
from Connection import Connection
import numpy as np
import Draw_Test

class Individual(object):
	IDGeneDict  = {}
	inputsNodes = []
	hiddenNodes = [[]]
	outputNodes = []
	neuronSet   = set()
	fitness     = None
	
	def addGene(g): 
		self.IDGeneDict[g.uniqueID] = g

	def mutateAddConnect():
		pass

	def mutateAddNeuron():
		pass

	def calcOut():
		pass

	def breedGene(g1,g2):
		pass

	def drawNet(self):
		vertical_distance_between_layers = 6
		horizontal_distance_between_neurons = 2
		neuron_radius = 0.5
		number_of_neurons_in_widest_layer = 4
		network = Draw_Test.NeuralNetwork()
		# weights to convert from 10 outputs to 4 (decimal digits to their binary representation)
		inputWeights = np.array([[self.inputsNodes[i].outCons[i].weight for i in range(len(self.inputsNodes))] for j in range(len(self.hiddenNodes[0]))])
		network.add_layer(len(self.inputsNodes),inputWeights,'input')

		for x in range(len(self.hiddenNodes)-1):
			hiddenWeights = np.array([[self.hiddenNodes[x][i].outCons[i].weight for i in range(len(self.hiddenNodes[x]))] for j in range(len(self.hiddenNodes[x+1]))])
			network.add_layer(len(self.hiddenNodes[x]),hiddenWeights,'hidden')

		finalHiddenWeights = np.array([[self.hiddenNodes[-1][i].outCons[i].weight for i in range(len(self.hiddenNodes[-1]))] for j in range(len(self.outputNodes))])
		network.add_layer(len(self.hiddenNodes[-1]),finalHiddenWeights,'hidden')
		network.add_layer(len(self.outputNodes),'output')
		network.draw()

	def traverseConstruct(self, nodes):
		for node in nodes:
			self.neuronSet.add(node)
			if node.neuronType =='input':	self.inputsNodes.append(node)
			if node.neuronType =='output': 	self.outputNodes.append(node)
		print self.inputsNodes
		for n in self.outputNodes:
			layer = 0
			for c in n.inCons:
				n = c.outNeuron
				while n.neuronType == 'hidden':
					self.hiddenNodes.append([])
					for c in n.inCons:
						n = c.outNeuron
						self.hiddenNodes[layer].append(c.outNeuron)
					layer += 1

		print self.hiddenNodes

if __name__ == '__main__':

	n0=Neuron(0)
	n1=Neuron(1)
	n2=Neuron(2)
	n3=Neuron(3)
	n4=Neuron(4)

	n0.neuronType="input"
	n1.neuronType="input"
	n2.neuronType="hidden"
	n3.neuronType="hidden"
	n4.neuronType="output"


	c0=Connection(n0,n2,.9,True)
	c1=Connection(n0,n3,.3,True)
	c2=Connection(n1,n2,-.5,True)
	c3=Connection(n1,n3,.7,True)
	c4=Connection(n2,n4,-.1,True)
	c5=Connection(n3,n4,.8,True)

	n0.outCons.append(c0)
	n0.outCons.append(c1)
	n1.outCons.append(c2)
	n1.outCons.append(c3)
	n2.outCons.append(c4)
	n3.outCons.append(c4)

	n2.inCons.append(c0)
	n2.inCons.append(c1)
	n3.inCons.append(c0)
	n3.inCons.append(c1)
	n4.inCons.append(c2)
	n4.inCons.append(c3)

	n0.value=.0007
	n1.value=.0003

	i = Individual()
	# i.traverseConstruct([n0,n1,n2,n3,n4])
	i.drawNet()

	print n4.neuralNet()


