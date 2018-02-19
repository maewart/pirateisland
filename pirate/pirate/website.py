#!/usr/bin/env python3

#Import field and find library objects
from .gameObjects import Level, ScoreBoard
from .database import Database

#Import Jinja2 to render website
from jinja2 import Environment, FileSystemLoader

#Class list in file
__all__ = ['Website']

class Website(object):
	"""The Pirate Website
	
	The website class contains all information needed to:
	1) Load data from database
	2) Generate the SVG
	3) Generate the webpage using a Jinja2 html template
	
	"""
	
	def __init__(self,params):
		"""Initialize object - create the different variables
		
		Keyword arguments:
		params -- a dictonary of parameters submitted from browser
		"""
		
		#Get Website Templates
		self._env = Environment(loader=FileSystemLoader('templates'))
		self._mainTemplate = self._env.get_template('pirateTemplate.html')
				
		#Setup DB Connection
		self._db = Database()
			
		#Status - default empty line
		self._status = '<br>'
		
		#Parameters
		self._params = params

		#set level 1 as default
		self._levelNo = 1
		self._level = None
		
		#if level param entered then set to that level
		if 'level' in self._params:
			self._levelNo = self._params['level'].value
		
		self._score = 0		
		#if score param entered then set to that score
		if 'score' in self._params:
			self._score = self._params['score'].value
			
		self._music = 'on'		
		#if score param entered then set to that score
		if 'music' in self._params:
			self._music = self._params['music'].value
		
		self._maxLevelId = 0
		# Create the variable fro the score board
		self._sb = None
		
	def run(self):
		"""Run all actions requested and generate the website"""
	
		self._db.openConnection()
		
		#Get the number of levels so know when have completed the game
		self._maxLevelId = self._db.getMaxLevelId()
		
		#Get the level information
		self._level = self._db.getLevel(self._levelNo)
		
		#Add objects for level
		self._db.addObjects(self._level)
		
		#Get the scoreboard
		self._sb = self._db.getScoreBoard()
		
		self._db.closeConnection()
	
	def __str__(self):
		"""return rendered website as string object"""
		
		assert self._level != None
		
		#Render the website
		return self._mainTemplate.render(
										gameDisplay = self._level.render(10,10),
										levelId = self._level.levelId,
										levelName = self._level.levelName,
										startX = self._level.startX-0.5,
										startY = self._level.startY-0.5,
										maxX = self._level.maxX,
										maxY = self._level.maxY,
										maxLevelNumber = self._maxLevelId,
										score = self._score,
										scoreBoard = str(self._sb),
										music = self._music
										)	
	