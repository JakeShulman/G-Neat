'''
Created on Feb 5, 2017

@author: Jake
'''
from Population import CULL_PERCENT
from Population import FECUNDITY_RATE
from Population import MUTATION_VALUE
from Population import MUTATION_WEIGHT_RATE 
from Population import MUTATION_NEURON_RATE 
from Population import MUTATION_CONNECTION_RATE
from Individual import Individual


class Species(object):
	individualList 	= []
	fitnessList 	= []
	representative 	= None
	loseStreak     	= 0
	totalFit 		= 0.0
	averageFitness 	= 0.0

	def __init__(self,founder):
		representative = founder
		individualList.append(founder)

	def calcAvgFitness(self):
		return self.totalFit/len(self.fitnessList)

	def runSim(self,i,inputData,targetData):
		index = 0
		for inNeuron in i.inputNodes:
			inNeuron.value = inputData[index]
			index+=1
		output = i.calcOut()
		fitness = calcFitness(i,output,targetData)
		i.fitness = fitness
		self.totalFit+=fitness
		self.fitnessList.append(fitness)

	def calcFitness(self, i, output, targetData):
		if targetData ==  None:
			newInput, targetData = doAction(output)
			if targetData == None:
				runSim(i,newInput,targetData)
		return fitFunc(output,targetData)

	def fitFunc(self,output, targetData, func = "MSE"):
		if func == "MSE":
			total = 0
			for o in range(len(output)):
				total+= ((targetData[o]-output[o])**2)/targetData[o]
		return total

	def getNextGen(self, minimize= True):
		nextGen =  []
		#Reversed order for MSE --> first value is largest
		self.fitnessList = sorted(self.fitnessList, key=lambda x:x[1])
		if  minimize: 
			self.fitnessList = self.fitnessList[::-1]
		self.representative = self.fitnessList[0][0]
		survivors = self.fitnessList[:len(self.fitnessList)*(1-CULL_PERCENT)]
		casualties = self.fitnessList[len(self.fitnessList)*(1-CULL_PERCENT):]
		survivorTotal = sum([fit[1] for fit in survivors])
		probabilities = [x[1]/survivorTotal for x in survivors]

		for x in range((2/(1-CULL_PERCENT))-2):
			#SHITTY BREEDING PROTOCOL TEMPORARY
			for parent in survivors:
				pair = np.random.choice(len(survivors),2,p=probabilities, replace = False)
				nextGen.append(breed(pair[0], pair[1]))
		
		for survivor in survivors:
			nextGen.append(survivor[0])

		self.averageFitness =  calcAvgFitness()
		resetSpecies()
		return nextGen


	def breed(i1,i2):
		#i1 has the higer fitness
		if i1.fitness > i2.fitness: stronger = i1; weaker = i2
		else: stronger = i2; weaker = i1
		a = set(stronger.genome.keys())
		b = set(weaker.genome.keys())
		union = a&b
		total = a|b
		child = Individual()
		diff=1/((float(stronger.fitness-weaker.fitness)/stronger.fitness)+1)
		#CROSSING OVER
		for gene in total:
			if gene in union:
				if random.randbits(1): child.addStruct(stronger[gene])
				else: child.addStruct(weaker[gene])
			else:
				if gene in b:
					if np.random.choice(1, 1, p=[.5+diff,.5-diff]):
						child.addStruct(weaker[gene])
				else:
					if not np.random.choice(1, 1, p=[.5+diff,.5-diff]):
						child.addStruct(stronger[gene])

		if random.randint(0,99)<=MUTATION_NEURON_RATE:
			child.mutateAddNeuron()
		if random.randint(0,99)<=MUTATION_CONNECTION_RATE:
			child.mutateConnection()
		return child


	def doAction(self): 
		pass

	def resetSpecies(self):
		self.individualList = []
		self.fitnessList 	= []
		self.totalFit 		= 0.0


