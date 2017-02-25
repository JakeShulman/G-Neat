'''
Created on Feb 5, 2017

@author: Jake
'''

from Neuron import Neuron
from Gene import Gene
from Connection import Connection
import numpy as np
import Draw_Test
from Population import START_WEIGHT
from Population import CONNECTION_ID
from Population import MUTATION_VALUE
from Population import MUTATION_WEIGHT_RATE 
from Population import MUTATION_NEURON_RATE 
from Population import INPUT_NUM
from Population import OUT_NUM

class Individual(object):
	genome  	= {}
	inputsNodes = []
	hiddenNodes = []
	outputNodes = []
	neuronList  = []
	fitness     = None	


	def intialize(self):
		#Only work on this if you are a supreme shmuck
		for x in range(INPUT_NUM):
			n0=Neuron()
			n0.neuronType="input"
			inputsNodes.append()

			c0=Connection(0,n0,n2,.1,True)

			n0.outCons.append(c0)

			n2.inCons.append(c0)


	def mutateConnection(self,sNeuron = None,eNeuron = None):
		if  sNeuron == None:
			iLayer = [self.inputsNodes, self.hiddenNodes][random.randbits(1)]
			oLayer = [self.hiddenNodes, self.outputNodes][random.randbits(1)]
			sNeuron = iLayer[np.random.randint(0,len(iLayer)-1)]
			eNeuron = oLayer[np.random.randint(0,len(oLayer)-1)]
		w = random.uniform(-START_WEIGHT, START_WEIGHT)
		newC = Connection(Population.CONNECTION_ID, sNeuron, eNeuron, w)
		self.genome[Population.CONNECTION_ID] = newC
		Population.CONNECTION_ID+=1
		sNeuron.outCons.append(newC)
		eNeuron.inCons.append(newC)
		
	def addStruct(self,connection):
		inp=connection.inNeuron
		out=connection.outNeuron


		if inp.neuronType=="input" and  inp not in self.inputsNodes:
			self.inputsNodes.append(inp)
			self.neuronList.append(inp)
		if inp.neuronType=="hidden" and  inp not in self.hiddenNodes:
			self.hiddenNodes.append(inp)
			self.neuronList.append(inp)
		if out.neuronType=="hidden" and  out not in self.hiddenNodes:
			self.hiddenNodes.append(out)
			self.neuronList.append(out)
		if out.neuronType=="output" and  out not in self.outputNodes:
			self.outputNodes.append(out)
			self.neuronList.append(out)
		copy=connection.copy()
		if random.randint(0,99) <= MUTATION_WEIGHT_RATE:
			copy.mutateWeight()
		self.genome[connection.ID]=copy


	def mutateAddNeuron(self):
		iLayer = [self.inputsNodes, self.hiddenNodes][random.randbits(1)]
		oLayer = [self.hiddenNodes, self.outputNodes][random.randbits(1)]
		startNeuron = iLayer[np.random.randint(0,len(iLayer)-1)]
		endNeuron = oLayer[np.random.randint(0,len(oLayer)-1)]
		newNeuron =  Neuron()
		mutateConnection(startNeuron,newNeuron)
		mutateConnection(newNeuron,endNeuron)
		self.hiddenNodes.append(newNeuron)
		self.neuronSet.append(newNeuron)


	def calcOut(sigmoid=True):
		assert(inputsNodes[0].value!=None)
		outList=[]
		index=0
		for output in outputNodes:
			outList[index]=output.NeuralNetwork(sigmoid)
			index+=1
		return outList

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

	n0=Neuron()
	n1=Neuron()
	n2=Neuron()
	n3=Neuron()
	n4=Neuron()

	n0.neuronType="input"
	n1.neuronType="input"
	n2.neuronType="hidden"
	n3.neuronType="hidden"
	n4.neuronType="output"


	c0=Connection(0,n0,n2,.1,True)
	c1=Connection(1,n0,n3,.05,True)
	c2=Connection(2,n1,n2,5,True)
	c3=Connection(3,n1,n3,.7,True)
	c4=Connection(4,n2,n4,.9,True)
	c5=Connection(5,n3,n4,.8,True)

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

	n0.value= .001
	n1.value= .0000000005

	# i = Individual()
	# # i.traverseConstruct([n0,n1,n2,n3,n4])
	# i.drawNet()

	print n4.neuralNet(sigmoid=True)


