'''
Created on Feb 4, 2017

@author: Jake
'''
from Connection import Connection
class Gene(object):
	inN        = None
	outN       = None
	connection = None
	uniqueID   = None

	def __init__(self,inNode,outNode,connect,ID):
		self.inN        = inNode
		self.outN       = outNode
		self.connection = connect
		self.uniqueID   = ID

