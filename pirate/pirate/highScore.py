#!/usr/bin/env python3

#Import objects
from .database import Database
import json
import ast

#Class list in file
__all__ = ['HighScore']

class HighScore(object):
	"""The HighScore Class

	The validation class contains all information needed to:
    1) Connect to the database
	2) Submit the high score
	4) Generate an output JSON

	"""

	def __init__(self, params):
		"""Initialise object

		Keyword arguments:
		params -- a set of user defined moves as cgiFieldStorage params
		"""

		#Setup DB Connection
		self._db = Database()

		self._highScore = None
		if "highScore" in params:
		    self._highScore = params['highScore'].value
		
		self._name = None
		if "name" in params:
			self._name = params['name'].value
			
		self._position = 0


	def addHighScore(self):
		"""Opens database Connection and adds the high score"""
		self._db.openConnection()
		self._position=self._db.addHighScore(self._name,self._highScore)
		self._db.closeConnection()
		
	def __str__(self):
		return str(self._position)