'''
Created on Feb 5, 2017

@author: Jake
'''

from Neuron import *
from Connection import *
import numpy as np
import Draw_Test
import Population

class Individual(object):
	genome  	= {}
	inputNodes = []
	hiddenNodes = []
	outputNodes = []
	neuronList  = []
	fitness     = 0.0
	ID 			= 0	

	def __init__(self):
		self.genome  	= {}
		self.inputNodes = []
		self.inputIDS	= []
		self.outputIDS	= []
		self.hiddenNodes = []
		self.outputNodes = []
		self.neuronList  = []
		self.fitness     = 0
		self.ID 		= Population.CURR_IND_ID
		Population.CURR_IND_ID+=1
		self.initialize()

	def initialize(self):	
		hiddenNum = np.random.randint(1,Population.INPUT_NUM*2)
		#Think about neuronList at some point
		for x in range(Population.INPUT_NUM):
			n0=Neuron()
			n0.neuronType ="input"
			n0.neuronID=x
			self.inputNodes.append(n0)
			self.inputIDS.append(x)
		for x  in range(Population.OUTPUT_NUM):
			n1 = Neuron()
			n1.neuronType ='output'
			n1.neuronID=x
			self.outputNodes.append(n1)
			self.outputIDS.append(x)
		for x in range(hiddenNum):
			n2 = Neuron()
			n2.neuronType = 'hidden'
			self.hiddenNodes.append(n2)


		for i in self.inputNodes:
			for h in self.hiddenNodes:
				c = Connection(Population.CONNECTION_ID, i, h, np.random.uniform(Population.START_WEIGHT*2)-1)
				self.genome[Population.CONNECTION_ID] = c
				Population.CONNECTION_ID+=1
				i.outCons.append(c)
				h.inCons.append(c)
				if i.neuronID not in self.inputIDS:
					self.inputNodes.append(i)
					self.neuronList.append(i)
					self.inputIDS.append(i.neuronID)

		for h in self.hiddenNodes:
			for o in self.outputNodes:
				c = Connection(Population.CONNECTION_ID, h, o, np.random.uniform())
				self.genome[Population.CONNECTION_ID] = c
				Population.CONNECTION_ID+=1
				h.outCons.append(c)
				o.inCons.append(c)
				if o.neuronID not in self.outputIDS:
					self.outputNodes.append(o)
					self.neuronList.append(o)
					self.outputIDS.append(o.neuronID)


	def mutateConnection(self,sNeuron = None,eNeuron = None):
		if  sNeuron == None:
			iLayer = [self.inputNodes, self.hiddenNodes][random.getrandbits(1)]
			oLayer = [self.hiddenNodes, self.outputNodes][random.getrandbits(1)]
			sNeuron = iLayer[np.random.randint(0,len(iLayer))]
			eNeuron = oLayer[np.random.randint(0,len(oLayer))]
		w = random.uniform(-Population.START_WEIGHT, Population.START_WEIGHT)
		newC = Connection(Population.CONNECTION_ID, sNeuron, eNeuron, w)
		self.genome[Population.CONNECTION_ID] = newC
		Population.CONNECTION_ID+=1
		sNeuron.outCons.append(newC)
		eNeuron.inCons.append(newC)
		
	def addStruct(self,connection):
		inp=connection.inNeuron
		out=connection.outNeuron
		if inp.neuronType=="input" and  inp.neuronID not in self.inputIDS:
			self.inputNodes.append(inp)
			self.neuronList.append(inp)
			self.inputIDS.append(inp.neuronID)
		if inp.neuronType=="hidden" and  inp.neuronID not in self.genome:
			self.hiddenNodes.append(inp)
			self.neuronList.append(inp)
		if out.neuronType=="hidden" and  out.neuronID not in self.genome:
			self.hiddenNodes.append(out)
			self.neuronList.append(out)
		if out.neuronType=="output" and  out.neuronID not in self.outputIDS:
			self.outputNodes.append(out)
			self.neuronList.append(out)
			self.outputIDS.append(out.neuronID)

		copy=connection.copy()
		if random.randint(0,99) <= Population.MUTATION_WEIGHT_RATE:
			copy.mutateWeight()
		self.genome[connection.ID]=copy



	def mutateAddNeuron(self):
		iLayer = [self.inputNodes, self.hiddenNodes][random.getrandbits(1)]
		oLayer = [self.hiddenNodes, self.outputNodes][random.getrandbits(1)]
		startNeuron = iLayer[np.random.randint(0,len(iLayer))]
		endNeuron = oLayer[np.random.randint(0,len(oLayer))]
		newNeuron =  Neuron()
		self.mutateConnection(startNeuron,newNeuron)
		self.mutateConnection(newNeuron,endNeuron)
		self.hiddenNodes.append(newNeuron)
		self.neuronList.append(newNeuron)

	def setInputs(self, inputList):
		for i in range(len(self.inputNodes)):
			node = self.inputNodes[i]
			node.value = inputList[i]

	def calcOut(self,sigmoid=True):
		assert(self.inputNodes[0].value!=None)
		outList=[]
		index=0
		for output in self.outputNodes:
			outList.append(output.neuralNet(sigmoid))
			index+=1
		return outList

	def __contains__(self, l):
		for i in l:
			if self.equals(i): return True
		return False

	def equals(self, other):
		if cmp(self.genome, other.genome)!=0		: return False
		# if set(self.inputNodes)  != set(other.inputNodes)	: return False
		# if set(self.hiddenNodes) != set(other.hiddenNodes)	: return False
		# if set(self.outputNodes) != set(other.outputNodes)	: return False
		# if set(self.neuronList)  != set(other.neuronList)	: return False
		# if set(self.fitness)     != set(other.fitness)		: return False
		print "EQUAL"
		return True

	def __str__(self):
		return """
		Inputs: %d
		Hidden: %d
		Output: %d
		Number Connections: %d 
		"""% (len(self.inputNodes), len(self.hiddenNodes), len(self.outputNodes), len(self.genome))

	def drawNet(self):
		vertical_distance_between_layers = 6
		horizontal_distance_between_neurons = 2
		neuron_radius = 0.5
		number_of_neurons_in_widest_layer = 4
		network = Draw_Test.NeuralNetwork()
		# weights to convert from 10 outputs to 4 (decimal digits to their binary representation)
		inputWeights = np.array([[self.inputNodes[i].outCons[i].weight for i in range(len(self.inputNodes))] for j in range(len(self.hiddenNodes[0]))])
		network.add_layer(len(self.inputNodes),inputWeights,'input')

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
			if node.neuronType =='input':	self.inputNodes.append(node)
			if node.neuronType =='output': 	self.outputNodes.append(node)
		print self.inputNodes
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

	i1= Individual()
	i2= Individual()
	i3= Individual()

	print i1, i2, i3



	# n0=Neuron()
	# n1=Neuron()
	# n2=Neuron()
	# n3=Neuron()
	# n4=Neuron()

	# n0.neuronType="input"
	# n1.neuronType="input"
	# n2.neuronType="hidden"
	# n3.neuronType="hidden"
	# n4.neuronType="output"


	# c0=Connection(0,n0,n2,.1,True)
	# c1=Connection(1,n0,n3,.05,True)
	# c2=Connection(2,n1,n2,5,True)
	# c3=Connection(3,n1,n3,.7,True)
	# c4=Connection(4,n2,n4,.9,True)
	# c5=Connection(5,n3,n4,.8,True)

	# n0.outCons.append(c0)
	# n0.outCons.append(c1)
	# n1.outCons.append(c2)
	# n1.outCons.append(c3)
	# n2.outCons.append(c4)
	# n3.outCons.append(c4)

	# n2.inCons.append(c0)
	# n2.inCons.append(c1)
	# n3.inCons.append(c0)
	# n3.inCons.append(c1)
	# n4.inCons.append(c2)
	# n4.inCons.append(c3)

	# n0.value= .001
	# n1.value= .0000000005

	# # i = Individual()
	# # # i.traverseConstruct([n0,n1,n2,n3,n4])
	# # i.drawNet()

	# print n4.neuralNet(sigmoid=True)


