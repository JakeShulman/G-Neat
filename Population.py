'''
Created on Feb 5, 2017

@author: Jake
'''
from Species import Species
from Individual import Individual
from Neuron import Neuron
from Connection import Connection

POPULATION_SIZE				= 0
MUTATION_VALUE 				= 0
MUTATION_WEIGHT_RATE 		= 0
MUTATION_NEURON_RATE 		= 0
MUTATION_CONNECTION_RATE	= 0
START_WEIGHT 				= 10
CONNECTION_ID				= 0
CULL_PERCENT 				= .50
MAX_LOSE_STREAK 			= 10
NUM_GENERATIONS				= 10
INPUT_NUM					= 3
OUTPUT_NUM					= 1

speciesList 	= []
individualList 	= []

def instantiate():
	for x in range(POPULATION_SIZE):
		i = Individual()

	pass

################## Do Not Cross this line if you are a shmuck-a-roo ########################################


def dataExtract():
	pass

def isCompatable(i1,i2):
	pass

def speciation():
	isCompatable()
	pass

def runGen():
	speciesFitness()
	pass

def speciesFitness():
	pass

def totalAverageFitness():
	pass

def results():
	pass

def main():
	instantiate()
	dataExtract()
	speciation()
	for gen in NUM_GENERATIONS:
		runGen()
		speciation()
		print totalAverageFitness()
	results()
	pass