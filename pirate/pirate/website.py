#!/usr/bin/env python3

#Import field and find library objects
from .gameObjects import Level
from .database import Database

#Import Jinja2 to render website
from jinja2 import Environment, FileSystemLoader

#Class list in file
__all__ = ['Website']

class Website(object):
	"""The Pirate Website
	
	The website class contains all information needed to:
	1) Load and submit data from database
	2) Perform any actions - filter or add data
	3) Generate the SVG
	4) Generate the webpage using a Jinja2 html template
	
	"""
	
	def __init__(self,params):
		"""Initialise object
		
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
		
		
	def run(self):
		"""Run all actions requested and generate the website"""
	
		self._db.openConnection()
		#print(str(self._levelNo))
		self._level = self._db.getLevel(self._levelNo)
		self._db.addObjects(self._level)
		self._db.closeConnection()
	
	def __str__(self):
		"""return rendered website as string object"""
		
		assert self._level != None
		
		#Demonstration purposes for reading params
		#something = ''
		#for i in self._params:
		#	something  =  i +' '+ self._params[i].value + '<br>' + something
		#something = 'Hello Everyone <br><br>' + something	
		
		return self._mainTemplate.render(
										paramList = self._level.render(500,500)
										)
		
	def _getParam(self,key):
		"""This checks if parameter exists and return and errors if doesn't exist"""
		
		if key not in self._params:
			raise Exception(key + ' cannot be blank')
		return self._params[key].value
			
	def _allowBlank(self,key):
		"""This checks if parameter exists and return blank if doesn't exists """
		
		val = '' #This allows the value to be blank
		if key in self._params:
			val = self._params[key].value
		return val
	

		

		
	