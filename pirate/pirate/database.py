#!/usr/bin/env python3
import cx_Oracle
from .gameObjects import Level
__all__ = ['Database']

class Database(object):
	"""This object controls all interactions with the  database

	This class contains all functionality to:
	1) xxxxxx
	"""

	def __init__(self):
		"""Initialise and set connection to None"""

		self._conn = None

	def openConnection(self):
		"""Open Connection"""

		pwdPath = "../../../oracle/mainpwd"
		userPath = "../../../oracle/username"
		with open(pwdPath,'r') as pwdRaw:
			pwd = pwdRaw.read().strip()
		with open(userPath,'r') as userRaw:
			username = userRaw.read().strip()
		self._conn = cx_Oracle.connect(dsn="geosgen",user=username,password=pwd)
		pwd = None #Keep Pwd in memory for a short as possible

	def closeConnection(self):
		"""Close Connection"""

		assert self._conn != None #Check connection open
		self._conn.close
		self._conn = None

	def getLevel(self,levelId):
		"""Get Level

		Keyword arguments:
		levelId -- Level Id
		"""

		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		sql = "Select * from s1138056.PIRATE_LEVELS_VIEW where LEVEL_ID=:Id"
		cursor.execute(sql,Id=levelId)
		for row in cursor:
			level = Level(levelId,row[1],row[4],row[5],row[2],row[3])
				
		return level


  	def addObjects(self,levelObject):
    	""" Adds Object to a level

		Keyword arguments:
		levelObject

		"""
		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		sql = "Select * from s1138056.PIRATE_ISLAND_VIEW where LEVEL_ID=:Id"
		cursor.execute(sql,Id=levelObject.levelId)
		for row in cursor:
			levelObject.addIsland(row[1],row[2],row[4])
		
		sql = "Select * from s1138056.PIRATE_ICONS_VIEW where LEVEL_ID=:Id"
		cursor.execute(sql,Id=levelObject.levelId)
		for row in cursor:
			levelObject.addIcon(row[1],row[2],row[4],row[5],row[6],row[7])
			
	def getLevelStart(self, levelId):
		"""queries the database for the startpoint of a certain level

		Keyword arguments:
		levelId -- Level Id

		returns an tuple with x and y coordinate of level start point

		"""
		##hardcoded, will be retrieved from database
		return (0,0)

	def validatePath(self,levelId,start_x,start_y,end_x,end_y):
		"""validates a line within a level

		Keyword arguments:
		levelId -- Level Id
		start_x -- start x coordinate of the line
		start_y -- start y coordinate of the line
		end_x -- end x coordinate of the line
		end_y -- end y coordinate of the line

		returns an array containig two objects:
		array [1] (int) -- distance to the action
		array [0] (string) -- action at the end of the given distance; 'end', 'crash' or 'not_crash'
		"""
		# hardcoded at the moment
		if (end_y-start_y==5):
			return [3, 'end']
		elif (end_y-start_y==4):
			return [5, 'crash']
		else:
			return [2, 'not_crash']
