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
		    self._levelNo = inp['level'].value

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
		self._validatedSteps = []
		self._validatedDirections = []
		self._endActions = []




	def _toLineCoords(self, dire, steps, start):
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
		    self._toLineCoords(dire, steps, start)

	def _validatePaths(self):
		"""Validates the lines in self._coords by connecting to the database"""
		assert len(self._coords)>0
		for line in self._coords:
			validatedPath = self._db.validatePath(self._levelNo,line[0], line[1], line[2], line[3])
			self._toJsInstructions(line, validatedPath[0]) #convert to a readable format for javascript
			self._endActions.append(validatedPath[1])
			if self._endActions[-1] != 'not_crash':
				break


	def validate(self):
		"""Opens database Connection and runs all validations"""
		self._db.openConnection()
		startPoint = self._db.getLevelStart(self._levelNo)
		self._coords = [[None for x in range(4)] for y in range(len(self._directions))]
		if len(self._coords)>0:
			self._toLineCoords(self._directions+[], self._steps+[], startPoint)
			self._validatePaths()
		self._db.closeConnection()


	def _toJsInstructions(self, line, distance):
		"""Converts distance and line coordinate information to JavaScript instructions
		The input is converted into 'x' or 'y' direction and appended to _validatedDirections
		the sign of the distance is calculated and appended to _validatedSteps

		Keyword arguments:
		line -- original not validated array with the four coordinates: start_x, start_y, end_x, end_y
        distance -- a positive number with the validated distance from the start point to where the ship arrives for a certain action. Can be smaller or equal the distance between start and endpoint of the line
		"""
		if (line[0]!=line[2]): #indicates change in x direction
			self._validatedDirections.append('x')
			sign = 1 if line[2]-line[0] >= 0 else -1 #indicates if distance must be positive or negative numbers
			self._validatedSteps.append(sign*distance)
		elif (line[1]!=line[3]):
			self._validatedDirections.append('y')
			sign = 1 if line[2]-line[0] >= 0 else -1 #indicates if steps must be positive or negative numbers (depending on the direction along axis)
			self._validatedSteps.append(sign*distance)


	def __str__(self):
		"""returns JSON output as string"""
		result = {}
		result['success'] = True
		result['message'] = "The command Completed Successfully"
		d = {}
		d['direction']=self._validatedDirections
		d['steps']=self._validatedSteps
		d['endaction']=self._endActions[-1]
		d['endactionarray']=self._endActions
		result['data'] = d

		return json.dumps(result,indent=1)
