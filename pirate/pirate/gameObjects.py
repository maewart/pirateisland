#!/usr/bin/env python3
import numpy as np
from .htmlHelper import genHTMLElement
from datetime import datetime
__all__ = ['Level']


class Level(object):
	"""The full map area
	
	The Level class contains all information needed to render the Level
	
	"""

	def __init__(self,levelId,maxX,maxY):
		"""Initialise object
		
		Keyword arguments:
		levelId,maxX,maxY
		"""
		
		self._levelId = str(levelId)
		self._maxX = int(maxX)
		self._maxY = int(maxY)
		self._htmlId = 'LevelSVG'
		
		#Define view boxes
		self._viewBoxMapOuter = '0 0 ' + str(self._maxX + 2) + ' ' + str(self._maxY + 2)
		self._viewBoxMapInner = '0 0 ' + str(self._maxX) + ' ' + str(self._maxY) #NOT USED
	
	
	def addObstacle(self,obstacleList,cssClass): #NEED to DEFINE
		"""Attach finds to area
		
		Keyword arguments:
		obstacleList -- list of obstacles
		cssClass -- css Class
		"""
		
		self._obstacleList = obstacleList
		self._cssClass = cssClass
	
	def render(self,width,height):
		"""Renders the svg map and returns the svg element for display
		
		Keyword arguments:
		width -- the svg width - can be percent or absolute
		height -- the svg height - can be percent or absolute
		"""
		
		#Render all and combine - EXAMPLE BOX
		viewBox = self._viewBoxMapOuter
		rectElement = genHTMLElement('rect',
							['class','id','x','y','width','height','fill','fill-opacity','stroke','stroke-width'],
							['',1,0,0,10,10,'lightgreen',0.5,'black',0.02])
		svgRoot = genHTMLElement('svg',
								['width','height','viewBox'],
								[width,height,viewBox],rectElement)
		
		#Return the root svg element for display
		return svgRoot
	

	@property
	def levelId(self):
		return self._levelId
		
	@property
	def maxX(self):
		return self._maxX
		
	@property
	def maxY(self):
		return self._maxY
		
