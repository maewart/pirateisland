#!/usr/bin/env python3

#Import field and find library objects
from .database import Database
import json
import ast

#Class list in file
__all__ = ['MoveValidation']

class MoveValidation(object):
	"""The Pirate Validation Class

	The validation class contains all information needed to:
    1) Connect to the database
	2) Submit moves for validation to the database and receive results
	3) Query if user reaches the end or not
	4) Generate an output JSON

	"""

	def __init__(self, inp):
		"""Initialise object

		Keyword arguments:
		inp -- a set of user defined moves as cgiFieldStorage params
        levelNo -- the current levelNumber
		"""

		#Setup DB Connection
		self._db = Database()

		#Input cgiFieldStorage Parameters
		#self._inp = inp

		self._coords = None

		self._levelNo=1
		if "level" in inp:
		    self._levelNo = inp['level']

		##TO-DO: better error handling
		self._directions = []
		if "direction" in inp:
			#converting the input into an array
			self._directions = ast.literal_eval(inp['direction'].value)

		##TO-DO: better error handling
		self._steps = []
		if "steps" in inp:
			#converting the input into an array
			self._steps = ast.literal_eval(inp['steps'].value)

		#validated Moves, will be filled with DB info
		self._validatedMoves = None




	def toLineCoords(self, dire, steps, start):
		"""Recursive function to convert a direction array and a step array into line coordinates"""
		assert len(dire) == len(steps)
		col=len(self._coords)-len(dire)
		self._coords[col][0]=start[0]
		self._coords[col][1]=start[1]
		if dire[0]=='x':
		    self._coords[col][2]=start[0]+steps[0]
		    self._coords[col][3]=start[1]
		elif dire[0]=='y':
			self._coords[col][3]=start[1]+steps[0]
			self._coords[col][2]=start[0]
		start=(self._coords[col][2], self._coords[col][3])
		dire.pop(0)
		steps.pop(0)
		if(len(dire)>0):
		    self.toLineCoords(dire, steps, start)



	def validate(self):
		"""Opens database Connection and run all validations"""
		self._db.openConnection()
		#connect to datebase here
		startPoint= (0,0) ##hardcoded, will be retrieved from database
		self._coords = [[None for x in range(4)] for y in range(len(self._directions))]
		if len(self._coords)>0:
			self.toLineCoords(self._directions+[], self._steps+[], startPoint)

		self._db.closeConnection()



	def __str__(self):
		"""returns JSON output as string"""
		result = {}
		result['success'] = True
		result['message'] = "The command Completed Successfully"
		#result['keys'] = ",".join(self._inp.keys())
		result['coords']= str(self._coords) + str(self._directions) + str(self._steps) #test to send back objects

		#will be filled with the returning data (moves, win?)
		d = {}
		#for k in self._inp.keys():
		    #d[k] = str(self._inp.getvalue(k)) + ' is cool'
		result['data'] = d

		return json.dumps(result,indent=1)



	def playerReachesEnd():
		"""Returns true when player hits the end obstacle"""
		return TRUE;
