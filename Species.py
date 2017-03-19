'''
Created on Feb 5, 2017

@author: Jake
'''
import Population
import  numpy as  np
from Individual import *
class Species(object):
	indList 		= []
	fitnessList 	= []
	representative 	= None
	loseStreak     	= 0
	totalFit 		= 0.0
	bestFitness		= 0.0
	averageFitness 	= 0.0

	def __init__(self,founder):
		self.indList 			= []
		self.fitnessList 		= []
		self.bestFitness		= 0.0
		self.loseStreak     	= 0
		self.totalFit 			= 0.0
		self.averageFitness 	= 0.0
		self.representative 	= founder
		self.indList.append(founder)

	def calcAvgFitness(self):
		self.averageFitness = self.totalFit / float(len(self.indList))

	def findRep(self):
		sort = sorted(self.fitnessList, key=lambda x:x[1])[-1]
		self.representative = sort[0]
		self.bestFitness =  sort[1]

	#InputData and TargerData --> include all data points 
	def runSim(self,inputData,targetData):
		for i in self.indList:
			for dataP in range(len(inputData)):
				index = 0
				for inNeuron in i.inputNodes:
					inNeuron.value = inputData[dataP][index]
					index+=1
				output = i.calcOut()
				fitness = self.calcFitness(i,output,targetData[dataP])
				i.fitness += fitness
			i.fitness = i.fitness/float(len(targetData))
			self.fitnessList.append((i,i.fitness))
			self.totalFit += i.fitness
		self.calcAvgFitness()
		self.findRep()

	def calcFitness(self, i, output, targetData):
		if targetData ==  None:
			newInput, targetData = doAction(output)
			if targetData == None:
				runSim(i,newInput,targetData)
		return self.fitFunc(output,targetData)

	def fitFunc(self,output, targetData, func = "MSE"):
		if func == "MSE":
			total = 0
			for o in range(len(output)):
				total+= ((targetData[o]-output[o])**2)/targetData[o]
		return total

	def getNextGen(self, maximize= False):
		nextGen =  []
		#Reversed order for MSE --> first value is largest
		self.fitnessList = sorted(self.fitnessList, key=lambda x:x[1])
		if maximize: 
			self.fitnessList = self.fitnessList[::-1]
		self.representative = self.fitnessList[0][0]
		survivors = self.fitnessList[:int(len(self.fitnessList)*(1-Population.CULL_PERCENT))]
		casualties = self.fitnessList[int(len(self.fitnessList)*(1-Population.CULL_PERCENT)):]
		survivorTotal = sum([fit[1] for fit in survivors])
		#Used to divide fitness among the surviving individuals for probabilistic breeding
		probabilities = [x[1]/survivorTotal for x in survivors]

		#Range value computes what number of indivisuals to breed, using a variable Culling Percent
		for x in range(int(len(casualties))):
			"""SHITTY BREEDING PROTOCOL TEMPORARY
			--MAYBE 
			-- Pretty sure this is okaybut past luke and jake werent so sure
			--WE ARE NOW PRETTY SURE THAT PAST LUKE AND JAKE WERE REALLY ON TO SOMETHING HERE
			"""
			pair = np.random.choice(len(survivors),2,p=probabilities, replace = True)
			nextGen.append(breed(survivors[pair[0]][0], survivors[pair[1]][0]))
		
		for survivor in survivors:
			nextGen.append(survivor[0])

		self.resetSpecies()
		return nextGen

	def addInd(self,individual):
		self.indList.append(individual)


	def doAction(self): 
		pass

	def resetSpecies(self):
		self.indList 		= []
		self.fitnessList 	= []
		self.totalFit 		= 0.0

def breed(i1,i2):
	assert(type(i1)==Individual and type(i2)==Individual)
	#i1 has the higer fitness, justc double checking
	if i1.fitness > i2.fitness: stronger = i1; weaker = i2
	else: stronger = i2; weaker = i1
	a = set(stronger.genome.keys())
	b = set(weaker.genome.keys())
	union = a&b
	total = a|b
	child = Individual()
	"""Diff is a scaled value quantifying how much stronger the stronger species is (0-.5). 
	Value added to .5 to get probability of corssing over disjoint genes"""
	diff=float(stronger.fitness-weaker.fitness)/(2.0*stronger.fitness)
	#Crossing over protocol
	for gene in total:
		#if gene present in both 50% crossing over
		if gene in union:
			if random.getrandbits(1): child.addStruct(stronger.genome[gene])
			else: child.addStruct(weaker.genome[gene])
		#If gene only in one parent cross over with the fitness scaled probability
		else:
			if gene in b:
				if np.random.choice(2, 1, p=[.75,.25]):
					child.addStruct(weaker.genome[gene])
			else:
				if not np.random.choice(2, 1, p=[.25,.75]):
					child.addStruct(stronger.genome[gene])

	#Randomly add mutations to neurons and connections
	if random.randint(0,99)<=Population.MUTATION_NEURON_RATE:
		child.mutateAddNeuron()
	if random.randint(0,99)<=Population.MUTATION_CONNECTION_RATE:
		child.mutateConnection()
	return child



