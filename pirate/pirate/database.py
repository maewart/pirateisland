#!/usr/bin/env python3
import cx_Oracle
import math
from .gameObjects import Level, ScoreBoard

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
		
	def getMaxLevelId(self):
		"""Get Max Level Id
		"""

		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		sql = "select max(LEVEL_ID) from S1138056.PIRATE_LEVELS"
		cursor.execute(sql)
		for row in cursor:
			maxLevel = row[0]
				
		return maxLevel



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
			
	def validatePath(self,level_id,start_x,start_y,end_x,end_y):
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
	
		objId = -1
		objType = ''
		objDist = 1000
	
		iconIntersects = self._intersectIcons(level_id,start_x,start_y,end_x,end_y)
		if len(iconIntersects) > 0:
			objId = iconIntersects[0][0]
			objType = iconIntersects[0][1]
			objDist = iconIntersects[0][2]

		islandIntersects = self._intersectIslands(level_id,start_x,start_y,end_x,end_y)
		if len(islandIntersects) > 0:		
			if islandIntersects[2] < objDist:
				objId = islandIntersects[0]
				objType = islandIntersects[1]
				objDist = islandIntersects[2]
				
		#Boundary code here
		if objId == -1:
			boundaryIntersects = self._intersectBoundary(level_id,start_x,start_y,end_x,end_y)	
			if len(boundaryIntersects) > 0:		
				objId = boundaryIntersects[0]
				objType = boundaryIntersects[1]
				objDist = boundaryIntersects[2]		
		
		# hardcoded at the moment
		if (objType=='end'):
			return [round(objDist,1), 'end', objId]
		elif (objType!=''):
			return [round(objDist,1), 'crash', objId]
		else:
			objDist = math.sqrt((end_y-start_y)**2+(end_x-start_x)**2)
			return [round(objDist,1), 'not_crash', -1]
			
	def _intersectIcons(self,level_id,start_x,start_y,end_x,end_y):
		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		
		#Icons
		sql = "	select \
				OBJECT_ID,TYPE_NAME,Dist from \
					(select \
					OBJECT_ID,TYPE_NAME,Dist,MIN(Dist) over () as MinDist from \
						(select \
						a.OBJECT_ID, \
						c.TYPE_NAME, \
						SDO_GEOM.SDO_DISTANCE(a.OBJECT, MDSYS.SDO_GEOMETRY(2001,NULL,MDSYS.SDO_POINT_TYPE(&startX, &startY, NULL),NULL,NULL), 0.005) as Dist \
						from S1138056.PIRATE_OBJECTS a \
						join S1138056.PIRATE_MAPPING b on a.OBJECT_ID = b.OBJECT_ID \
						join S1138056.PIRATE_TYPES c on a.TYPE_ID = c.TYPE_ID \
						where a.TYPE_ID!=1 and b.LEVEL_ID=:levelId and SDO_GEOM.RELATE(a.OBJECT,'ANYINTERACT',MDSYS.SDO_GEOMETRY(2002,NULL,NULL,MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),MDSYS.SDO_ORDINATE_ARRAY(:startX,:startY,:endX,:endY)),0.05)='TRUE') \
					) \
				where Dist=MinDist"
		cursor.execute(sql,levelId=level_id,startX=start_x,startY=start_y,endX=end_x,endY=end_y)
		return cursor.fetchall()
	
	def _intersectIslands(self,level_id,start_x,start_y,end_x,end_y):
		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		
		#Islands
		sql = "	select \
				a.OBJECT_ID \
				from S1138056.PIRATE_OBJECTS a \
				join S1138056.PIRATE_MAPPING b on a.OBJECT_ID = b.OBJECT_ID \
				join S1138056.PIRATE_TYPES c on a.TYPE_ID = c.TYPE_ID \
				where a.TYPE_ID=1 and b.LEVEL_ID=:levelId and SDO_GEOM.RELATE(a.OBJECT,'ANYINTERACT',MDSYS.SDO_GEOMETRY(2002,NULL,NULL,MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),MDSYS.SDO_ORDINATE_ARRAY(:startX,:startY,:endX,:endY)),0.05)='TRUE'"

		cursor.execute(sql,levelId=level_id,startX=start_x,startY=start_y,endX=end_x,endY=end_y)
		islands = []
		for row in cursor:
			islands.append(row[0])
			
		if len(islands) > 0:
			sql = "	select \
				a.OBJECT_ID \
				from S1138056.PIRATE_OBJECTS a \
				join S1138056.PIRATE_MAPPING b on a.OBJECT_ID = b.OBJECT_ID \
				join S1138056.PIRATE_TYPES c on a.TYPE_ID = c.TYPE_ID \
				where a.TYPE_ID=1 and a.OBJECT_ID=:objId and b.LEVEL_ID=:levelId and SDO_GEOM.RELATE(a.OBJECT,'ANYINTERACT',MDSYS.SDO_GEOMETRY(2002,NULL,NULL,MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),MDSYS.SDO_ORDINATE_ARRAY(:startX,:startY,:endX,:endY)),0.05)='TRUE'"
		
			closestId = 0
			closestDist = 1000
			stepAmount = 0.1
			for id in islands:
				if abs(start_y - end_y) <= 0.01:
					if end_x > start_x:
						direction = 1
					else:
						direction = -1
					step = direction * stepAmount
					inter_x = start_x + step
					tempDist = abs(step)
					while direction*inter_x <= direction*(end_x + 0.05):
						cursor.execute(sql,levelId=level_id,objId=id,startX=start_x,startY=start_y,endX=inter_x,endY=end_y)
						temp = cursor.fetchall()
						if len(temp) > 0:
							if tempDist <= closestDist:
								closestDist = tempDist
								closestId = id
								break
						inter_x = inter_x + step
						tempDist = tempDist + abs(step)
				if abs(start_x - end_x) <= 0.01:
					if end_y > start_y:
						direction = 1
					else:
						direction = -1
					step = direction * stepAmount
					inter_y = start_y + step
					tempDist = abs(step)
					while direction*inter_y <= direction*(end_y + 0.05):
						cursor.execute(sql,levelId=level_id,objId=id,startX=start_x,startY=start_y,endX=end_x,endY=inter_y)
						temp = cursor.fetchall()
						if len(temp) > 0:
							if tempDist <= closestDist:
								closestDist = tempDist
								closestId = id
								break				
						inter_y = inter_y + step
						tempDist = tempDist + abs(step)
			return [closestId,'island',closestDist]
		return []
		
	def _intersectBoundary(self,level_id,start_x,start_y,end_x,end_y):
		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		
		if end_x <=0:
			return [-2,'boundary',abs(start_x)]
		elif end_y <=0:
			return [-2,'boundary',abs(start_y)]	
		
		level = self.getLevel(level_id)
		
		if end_x >= level.maxX:
			return [-2,'boundary',abs(level.maxX - start_x)]
		elif end_y >= level.maxY:
			return [-2,'boundary',abs(level.maxY - start_y)]

		return []
		
	def getScoreBoard(self):
		"""Get the score list stored in the database 
		"""

		assert self._conn != None #Check connection open
		cursor = self._conn.cursor()
		sql = " select * from s1138056.pirate_top_ten"
		cursor.execute(sql)
		scoreName = []
		scorePoint = []
		for row in cursor:
			scoreName.append(row[0])
			scorePoint.append(row[1])	
		sb = ScoreBoard(scoreName,scorePoint)
		
		return sb

		
