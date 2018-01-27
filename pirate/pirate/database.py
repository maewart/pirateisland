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
		#cursor = self._conn.cursor()
		#sql = "Select * from s1783947.FF_AREA where AREA_NAME=:Area"
		#cursor.execute(sql,Area=areaName)
		#for row in cursor:
			#area = MapArea(row[0],row[1],row[2],row[3],row[4])
			
		level = Level(levelId,10,10)
			
		return level

