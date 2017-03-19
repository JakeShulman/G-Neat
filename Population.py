'''
Created on Feb 5, 2017

@author: Jake
'''
from Species import *
from Individual import *
from Neuron import *
from Connection import *
from Data_Extract import *
from time import time
from collections  import defaultdict
import numpy as np

POPULATION_SIZE				= 100
MUTATION_VALUE 				= 5
MUTATION_WEIGHT_RATE 		= 5
MUTATION_NEURON_RATE 		= 5
MUTATION_CONNECTION_RATE	= -1
START_WEIGHT				= 1
START_WEIGHT 				= 10
CONNECTION_ID				= 0
CULL_PERCENT 				= 0.50
MAX_LOSE_STREAK 			= 10
NUM_GENERATIONS				= 100
INPUT_NUM					= 3
OUTPUT_NUM					= 1
COMPATIBILITY_THRESH		= 1.5
CURR_IND_ID					= 0


speciesList			= []
individualList 		= []
conList 			= []
bestSpecies			= None

def instantiate(inputList):
	global individualList
	global speciesList
	for x in range(POPULATION_SIZE):
		i = Individual()
		#inputList from data extract
		i.setInputs(inputList)
		individualList.append(i)
	# for i in individualList:
	# 	for c in i.genome:
	# 		contained = False
	# 		for con in conList:
	# 			if  i.genome[c] == con[0]:
	# 				contained = True
	# 				i.genome[c].ID = con[1]
	# 				i.genome[con[1]] = i.genome[c]
	# 				i.genome.pop(c, None)
	# 				break
	# 		if not contained:
	# 			conList.append((i.genome[c],c))
	# print len(conList), "SET"
	# print CONNECTION_ID, "MAX"


#################### Do Not Cross this line if you are a shmuck-a-roo ########################################


def isCompatible(i1,i2):
	score = 0.0
	#Difference of number of genes
	score+= float(abs(len(i1.genome)-len(i2.genome)))/float(max(len(i1.genome), len(i2.genome)))
	#Number of incompatible genes
	score+= float(len(set(i1.genome.keys())^set(i2.genome.keys())))/float(max(len(i1.genome), len(i2.genome)))
	#Difference of weights of same genes
	total = 0.0
	for con in set(i1.genome.keys())&set(i2.genome.keys()):
		total+= float(abs(i1.genome[con].weight - i2.genome[con].weight))/float(max(i1.genome[con].weight, i2.genome[con].weight))
	score += total/float(len(set(i1.genome.keys())&set(i2.genome.keys()))) if len(set(i1.genome.keys())&set(i2.genome.keys())) > 0 else 0.0
	return score


def speciation():
	global individualList
	global speciesList
	#For first generation
	if len(speciesList) == 0:
		for i in individualList:
			speciesList.append((i, Species(i)))
		return
	else:
		for s in speciesList:
			s = (s[1].representative, s[1])
	#For all other gens
	speciesList[:] = []
	for i in individualList:
		inSpecies = False
		for s in speciesList:
			if isCompatible(i, s[0]) > COMPATIBILITY_THRESH:
				s[1].addInd(i)
				inSpecies = True
				break
		if not inSpecies: speciesList.append((i, Species(i)))


def runGen(inputData,targetData):
	global individualList
	global speciesList
	newIndividualList=[]
	for s in speciesList:
		s[1].runSim(inputData,targetData)
	for s in speciesList:
		if len(s[1].indList) > 1:
			newIndividualList+=s[1].getNextGen()
		else:
			b=individualList[random.randint(0,len(individualList)-1)]
			newIndividualList.append(breed(s[0],b))
	individualList[:]=newIndividualList
	speciesFitness()


	# BadInds = []
	# for s in speciesList:
	# 	if s[1].loseStreak>MAX_LOSE_STREAK:
	# 		for i in s[1].indList:
	# 			BadInds.append(i.ID)

	# print len(individualList), "BEFORE"
	# print BadInds, "BAAAAAAAAAAAADs"
	speciesList[:] =  [s for s in  speciesList if not s[1].loseStreak>MAX_LOSE_STREAK]
	# newnewIs = []
	# for i in individualList:
	# 	if i.ID not in BadInds: 
	# 		newnewIs.append(i)
	# print len(newnewIs)-len(individualList), "NEEEEEEW"
	# individualList[:] = newnewIs
	# print len(individualList), "AFTER"

	# for s in speciesList:
	# 	if s[1].loseStreak>MAX_LOSE_STREAK:
	# 		for ind in s[1].indList:
	# 			individualList.remove(ind)
	# 		print len(speciesList), "BEFORE"
	# 		speciesList.remove(s)
	# 		remove=True
	# 		speciesList[:] = speciesList
	# 		print len(speciesList), "AFTER"


	while len(individualList)<POPULATION_SIZE:
		individualList.append(breed(individualList[random.randint(0,len(individualList))],individualList[random.randint(0,len(individualList))]))


def speciesFitness():
	global individualList
	global speciesList
	global bestSpecies
	minVal=10000000000000000000
	bestSpecies=None
	for s in speciesList:
		s[1].loseStreak+=1
		if s[1].bestFitness < minVal:
			minVal=s[1].bestFitness
			bestSpecies=s[1]
	bestSpecies.loseStreak=0

def totalAverageFitness():
	global individualList
	global speciesList
	total = 0.0
	for s in speciesList:
		total+= s[1].averageFitness
	return total/len(speciesList)

def results(gen):
	print  ""
	print "--------------GEN %d--------------"%gen
	print "AVG FITNESS: ", totalAverageFitness()
	print "NUM SPECIES: ", len(speciesList)
	print "INDIVIDUALS: ", len(individualList)
	print "BEST:        ", bestSpecies.bestFitness , bestSpecies.representative


def main():
	global individualList
	global speciesList
	instantiate(sqrtData()[0])
	speciation()
	for gen in range(NUM_GENERATIONS):
		runGen(sqrtData()[0],sqrtData()[1])
		results(gen)
		speciation()


if __name__ == "__main__":
	t = time()
	main()
	print time()-t, "SECONDS"