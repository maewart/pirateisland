#!/usr/bin/env python3
import numpy as np
import copy as cp
from .htmlHelper import genHTMLElement
from datetime import datetime
__all__ = ['Level']


class Level(object):
	"""The full map area

	The Level class contains all information needed to render the Level

	"""




	def __init__(self,levelId,levelName,maxX,maxY,startX,startY):
		"""Initialize object

		Keyword arguments:
		levelId,levelName,maxX,maxY,startX,startY
		where:
		levelId: Id of the level (e.g. 1,2,3,..)
		levelName: Specific name of the level
		maxX: MaxX of the full map area
		maxY: MaxY of the full map area
		startX: Starting X point of the boat
		startY: Starting X point of the boat
		"""

		#Initialize the variables with the KeyWords arguments
		self._levelId = levelId
		self._maxX = int(maxX)
		self._maxY = int(maxY)
		self._levelName = levelName
		self._startX = float(startX)
		self._startY = float(startY)
		#Create 3 additional variables:
		#1. A string containing the name of the level
		self._htmlId = 'Level_' + str(self._levelId)
		#2. An empty list whereto store the svg objects
		self._objectList = []
		#Define view box size according to the maxX and MaxY KeyWords arguments
		self._viewBoxMapInner = '0 0 ' + str(self._maxX) + ' ' + str(self._maxY)

	@property
	def levelId(self):
		return self._levelId

	@property
	def maxX(self):
		return self._maxX

	@property
	def maxY(self):
		return self._maxY

	@property
	def levelName(self):
		return self._levelName

	@property
	def startX(self):
		return self._startX

	@property
	def startY(self):
		return self._startY

	@property
	def startPoint(self):
			return (self._startX, self._startY)

	def addIsland(self,objectId,fill,polygon): ##Comments waiting the wiring up!!
		"""Attach finds to area

		Keyword arguments:
		obstacleList -- list of obstacles
		type --

		"""
		obj = Island(objectId,fill,polygon)
		self._objectList.append(obj)

	def addIcon(self,objectId,fill,lowX,lowY,highX,highY): ##Comments waiting the wiring up!!
		"""Attach finds to area

		Keyword arguments:
		obstacleList -- list of obstacles
		type --

		"""
		obj = Icon(objectId,fill,lowX,lowY,highX,highY)
		self._objectList.append(obj)


	def _renderObjects(self):
		""" Renders the svg elements listed in the objectList wrapping together the appropriate html code
		"""

		output = ''
		for i in self._objectList:
			output = output + i.render()
		return output

	def render(self,width,height):
		"""Renders the svg map with the svg element representing the obstacles for display

		Keyword arguments:
		width -- the svg width - can be percent or absolute
		height -- the svg height - can be percent or absolute

		"""

		# Creation of new variable "viewBox" with the dimension of the viewbox determined by the Level KeyWords
		viewBox = self._viewBoxMapInner

		# Creation of the level background. Sea pattern plus blue background.
		# The sea pattern (#wavepattern) is stored in the pirate Template.html
		seaWaves = genHTMLElement('rect',
							['x','y','width','height','fill','fill-opacity'],
							[0,0,self._maxX,self._maxY,'url(#wavepattern)',1])
		seaBlue = genHTMLElement('rect',
							['x','y','width','height','fill','fill-opacity'],
							[0,0,self._maxX,self._maxY,'#cceeff',0.5])
		sea = seaWaves + seaBlue

		#Call the function renderObjects which renders the svg elements listed
		#in the objectList creating the appropriate html code.
		#The variable object will result with the proper html code to render the svgs
		objects = self._renderObjects()

		# Render starting pirate ship generating the appropriate html code calling the:
		# Object: ICON and method: RENDER
		# The initial ship will use the startX and startY coordinates. They need to be adjusted of 0.5
		# since the coordinates will refer to a line laying in the middle of a grid square, meanwhile
		# the svg is rendered according to his left upper corner
		shipIcon = Icon(0,'ship',self._startX-0.5,self._startY-0.5,self._startX+0.5,self._startY+0.5)
		ship = shipIcon.render()


		# Render the grid using two loops that reiterate according to MaxX and MaxY
		lines = ''
		for i in range(1,self._maxX):
			lineDef =  str(i) + ',0,' + str(i) + ','+ str(self._maxY)
			lineNew = genHTMLElement('polyline',
							['points','stroke','stroke-width'],
							[lineDef,'lightgrey',0.02])
			lines = lines + lineNew
		for i in range(1,self._maxY):
			lineDef =  '0,' + str(i) + ',' + str(self._maxX) + ',' + str(i)
			lineNew = genHTMLElement('polyline',
							['points','stroke','stroke-width'],
							[lineDef,'lightgrey',0.02])
			lines = lines + lineNew

		# Render the boundary box as a rectangle which size varies according to MaxX and MaxY
		boundary = genHTMLElement('rect',
					['x','y','width','height','fill','fill-opacity','stroke','stroke-width'],
					[0,0,self._maxX,self._maxY,'none',1,'black',0.02])

		# Combination of all the SVGs code generated so far in the variable "combined"
		combined = sea + lines + objects + ship + boundary

		# Creation of the final HTML code that wraps all the SVGs elements previously created
		svgRoot = genHTMLElement('svg',
								['width','height','viewBox'],
								[width,height,viewBox],combined)

		# Return the svgRoot element for display
		return svgRoot



class Icon(object):
	"""Create Icon

	The Icon class contains all information needed to render the obstacles

	"""

	def __init__(self,id,fill,lowX,lowY,highX,highY):
		"""Initialize object

		Keyword arguments:
		id,fill,x,y,width,height
		where:
		id: Id of the obstacle (e.g. 1,2,3,..)
		fill: type of filling. It can be "island, icon, end"
		x: X position of the left upper corner
		y: Y position of the left upper corner
		width: size of the svg
		height:  size of the svg
		"""

		self._id = int(id)
		self._fill = str(fill)
		self._htmlId = 'obj_' + str(self._id)
		self._x = float(lowX)
		self._y = float(lowY)
		self._width = float(highX) - self._x
		self._height = float(highY) - self._y

	def render(self):
		"""Renders the svg obstacles wrapping together the appropriate html code

		Type of svg obstacles: ship, seagull, octopus, diamond, iceberg, pirate, island, maelstrom, treasure

		"""

		#Structure of if-elif that calls the specific svg creation method according to the content of the KeyWord "Fill"
		icon = ''
		if self._fill == 'ship':
			icon = self._pirateShip()
			self._htmlId = 'OurShip'
		elif self._fill == 'seagull':
			icon = self._seagull()
		elif self._fill == 'octopus':
			icon = self._octopus()
		elif self._fill == 'diamond':
			icon = self._diamond()
		elif self._fill == 'iceberg':
			icon = self._iceberg()
		elif self._fill == 'pirate':
			icon = self._pirate()
		elif self._fill == 'island':
			icon = self._island()
		elif self._fill == 'maelstrom':
			icon = self._maelstrom()
		elif self._fill == 'treasure':
			icon = self._treasure()

		# Get the SVGs code for an obstacle, generated with the specific method, wrapped in an outer general <SVG>
		# which has the htmlId value and controls the X,Y position together with the width and height
		outerSVG = genHTMLElement('svg',
					['id','x','y','height','width'],
					[self._htmlId,self._x,self._y,self._width,self._height],
					icon)

		return outerSVG

	def _pirateShip(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: ship

		"""

		#Creation of the variable(s) with the svg path
		Pirateshippath1 = 'M-699.7,1090.8c0,6.8-5.5,14-12.4,14h-15v-58h-3v57.7c-5.7-1.1-10.1-6.1-10.1-12.2v-4.8h-19.7v5.8h5.3v22.4c0,9.4,7.6,17,17,17h36.7c9.4,0,17-7.6,17-17v-22h13.8v-3.1L-699.7,1090.8L-699.7,1090.8z M-734.4,1123.6c-2.9,0-5.3-2.4-5.3-5.3c0-2.9,2.4-5.3,5.3-5.3s5.3,2.4,5.3,5.3C-729.1,1121.2-731.5,1123.6-734.4,1123.6z M-718.5,1123.6c-2.9,0-5.3-2.4-5.3-5.3c0-2.9,2.4-5.3,5.3-5.3c2.9,0,5.3,2.4,5.3,5.3C-713.1,1121.2-715.5,1123.6-718.5,1123.6z M-702.5,1123.6c-2.9,0-5.3-2.4-5.3-5.3c0-2.9,2.4-5.3,5.3-5.3c3-0.1,5.3,2.3,5.3,5.3C-697.2,1121.2-699.6,1123.6-702.5,1123.6z'
		Pirateshippath2 = 'M-691.3,1049.2h-35.6c6.3,11.7,6.3,25.6,0,37.3h35.6C-684,1075.1-684,1060.7-691.3,1049.2z M-699.9,1075.8c-0.4,1.3-1.5,2.3-3,2.3h-3.1c-1.4,0-2.6-1-3-2.3c-4.5-0.5-8.1-4.3-8.1-9c0-5,4.1-9.1,9.1-9.1h7.1c5,0,9.1,4.1,9.1,9.1C-691.8,1071.5-695.4,1075.3-699.9,1075.8z'

		#Generation of the html code for the different elements that make up the svg
		pathPirateship1 = genHTMLElement('path',
							['class','d'],
							['st1_pirateship',Pirateshippath1])
		pathPirateship2 = genHTMLElement('path',
							['class','d'],
							['st3_pirateship',Pirateshippath2])
		circlePirateship1 = genHTMLElement('circle',
							['class','id','cx','cy','r'],
							['st0_pirateship','','-702.5','1118.3','2.1'])
		circlePirateship2 = genHTMLElement('circle',
							['class','id','cx','cy','r'],
							['st0_pirateship','','-734.4','1118.3','2.1'])
		circlePirateship3 = genHTMLElement('circle',
							['class','id','cx','cy','r'],
							['st0_pirateship','','-718.5','1118.3','2.1'])
		circlePirateship4 = genHTMLElement('circle',
							['class','id','cx','cy','r'],
							['st3_pirateship','','-699.3','1067.2','3.6'])
		circlePirateship5 = genHTMLElement('circle',
							['class','id','cx','cy','r'],
							['st3_pirateship','','-709.6','1067.2','3.6'])

		#Union of all the elements of the svg within the variable "combine"
		combine = pathPirateship1 + pathPirateship2 + circlePirateship1 + circlePirateship2 + circlePirateship3 + circlePirateship4 + circlePirateship5

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgPirateship = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-771 1033.5 107 112','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgPirateship

	def _seagull(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: seagull

		"""

		#Creation of the variable(s) with the svg path
		Seagullpath = 'm-220.1 378.5c0 0.6-0.5 1.1-1.1 1.1s-1.1-0.5-1.1-1.1 0.5-1.1 1.1-1.1 1.1 0.5 1.1 1.1zm67.1 44.4c-3 1.8-8.4 0.6-11.8 0.3-4.4-0.3-8.7-0.9-13.1-1.4-3.5-0.4-7-0.9-10.5-1.3-1.7-0.1-3.3-0.3-4-1.4-0.3-0.5-0.4-1.1-0.5-1.7-0.1-0.5-0.2-1.1-0.4-1.6-0.5-1.4-1.7-2.4-2.9-3.3l-0.5-0.4c-4.3-3.2-8.8-6.6-10.5-11.5-0.5-1.3 0.3-3.2-0.2-4.3-0.5-1.3-1.5-0.6-1.8 0.5-0.3 1.3 0.3 3.1 0.8 4.3 1.9 5.3 6.5 8.8 11 12.1l0.5 0.4c1.1 0.8 2.1 1.6 2.5 2.7 0.2 0.4 0.2 0.8 0.3 1.3 0.1 0.7 0.3 1.5 0.7 2.2 0.5 0.8 1.3 1.3 2.2 1.6-1.6 0.5-3.2 1-4.8 1.4-1.2 0.3-2.5 0.6-3.7 0.8 0 0.1-0.1 0.2-0.1 0.3-0.5 1.4-0.2 2.9-0.5 4.4-0.3 1.4-0.7 2.6-0.7 4 0 1.6-0.1 3.1-0.1 4.7 0 1.1 0 2.3 0.1 3.4 0.3 2.5 1.2 5 2.7 7.1-1.6 0.9-2.6-0.5-4.3-0.5-1.3 0-2.1 1-3.2 1.2s-0.8-0.8-1.6-0.9c-1.1-0.2-2.2 0.7-3.4 0.4-0.2-0.1-0.3-0.1-0.5-0.2-1 0.4-2 0.8-2.9 0.3-0.1-0.1-0.2-0.1-0.2-0.2-0.1-0.2 0-0.4-0.1-0.5-0.1-0.2-0.3-0.4-0.6-0.4h-0.1-0.7c-1.8-0.1-0.5-0.9 0.3-1.2 1-0.3 2-0.5 3-0.9 1.3-0.6 2.8-1.2 3.5-2.5 1-1.8 1-4.6 1.2-6.5 0.2-2.4 0.1-4.5-0.6-6.8-0.4-1.3-0.1-2.7-0.3-4 0-0.3-0.1-0.6-0.2-0.9-3.3-0.4-6.4-1.5-9.4-3.5-3.8-2.6-6.7-5.9-8.5-9.6-2-2.8-3.3-6.4-3.3-10.5 0-2.1 0.3-4.2 1-6.2s2.8-4.2 2.1-6.4c-0.5-1.7-1.8-2.7-3.6-2.6-1.7 0.1-2.9 0.9-4.6 1.4-1.6 0.4-3.2 0.6-4.8 0.7s-2.1-0.8-1.5-2.2c0.3-0.6 0.7-1.2 1.2-1.7 1.1-1.3 3.1-1.7 4.7-2.2 1.5-0.4 3-1.1 4.5-1.7 2.9-1.2 3.1-2.9 4.3-5.2 1.3-2.3 4.1-3.9 6.6-4.6 4-1.1 8.7 0.1 11 3.5 2.2 3.2 2.5 7.6 2.7 11.3 0.1 0.9 0.2 1.7 0.6 2.5 2.7 0.3 5.3 0.9 7.8 1.7 3.9 1.3 7.3 3.1 9.8 5.2 4.4 3.8 9.3 6.2 14.1 9.4 3 2 6 4 9.3 5.5 2.8 1.3 5.7 2.4 8.7 3.2 0.6 0.2 1.2 0.4 1.3 1 0 0.7-0.8 1-1.5 1.1-3.4 0.5-6.8 0.8-10.1 1.5-1.7 0.4-3.4 0.4-5.1 0.6 3 0.8 6 1.5 9 2.1 0.8 0.5 14.4 1.9 9.7 4.7zm-67.9-46.3c-0.9 0-3.2 1.9-2.1 2.8 0.7 0.7 1.5 1.4 2.5 1 0.8-0.3 1.4-0.9 1.8-1.6 0.1-0.1 0.1-0.2 0.1-0.3 0.5-0.9-1.5-1.9-2.3-1.9zm14.2 65.6c0.1 0.7 0.3 1.3 0.7 1.9 0.1 0.2 0.2 0.3 0.2 0.5 0.3-0.2 0.6-0.3 0.8-0.6 1.6-1.6 1.1-4.3 1.3-6.3 0.2-1.8 0.2-3.6 0.1-5.5v-2.3c-0.1-1.4-0.3-2.5-0.1-3.9 0.1-0.6 0.1-1.3 0-1.9-0.8 0.1-1.5 0.1-2.3 0.1 0.1 1.2 0.5 2.4 0.4 3.7 0 1.4-0.4 2.8-0.6 4.2-0.3 2.7-0.5 5.4-0.7 8.1 0.1 0.6 0.1 1.3 0.2 2z'

		#Generation of the html code for the different elements that make up the svg

		pathSeagull = genHTMLElement('path',
							['class','d'],
							['st0_seagull',Seagullpath])

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgSeagull = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-247 358.9 100 105.4','preserve','http://www.w3.org/2000/svg'],
							pathSeagull)
		#Return of the html code that represent the svg
		return svgSeagull

	def _octopus(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: octopus

		"""

		#Creation of the variable(s) with the svg path
		Octopuspath1 = 'M-483.7,693.4c-2.2,2.9-5.9,5-10.9,6.4c-3.6-1.9-6.2-4.8-9.1-7.9c-0.8-0.9-1.6-1.7-2.4-2.7 c2.5-1.3,3.7-3.3,4.3-5c1.3-3.7,0.4-8.8-2.3-12.2c-3.3-4.2-8-7.1-12.5-9.6c-10.9-6.1-13-14.5-13.7-21.2c-0.6-5.8,2.6-13.5,13.4-16 c5.7-1.3,10.3,1.8,12.7,5.2c2.2,3.2,2.8,6.8,1.3,9.1c-1.1,1.7-2.3,2.7-3.7,3c0.8-1.1,1.2-2.5,1.1-4.1c-0.2-4-3.8-8.1-10-7.9 c-3.7,0.2-7.4,3.3-8.6,7.3c-1.3,4.3,0.3,8.5,4.4,11.5c3.4,2.5,7.4,3.7,11.7,5.1c6.5,2,13.2,4.1,18,10.8c-3.9,3.8-5.5,9-5.6,13.4 c-0.2,6.3,2.6,11.7,7.1,13.6C-486.8,692.9-485.2,693.3-483.7,693.4z'
		Octopuspath2 = 'M-539.2,641.1c-0.7,6.7-2.9,15.1-13.7,21.2c-4.5,2.6-9.2,5.5-12.4,9.6c-2.8,3.5-3.7,8.5-2.4,12.2 c0.6,1.7,1.8,3.8,4.3,5.1c-0.8,0.9-1.6,1.8-2.4,2.6c-2.9,3.2-5.5,6-9.1,8c-4.9-1.4-8.6-3.6-10.9-6.4c1.5-0.1,3.1-0.5,4.7-1.2 c4.5-1.9,7.3-7.2,7.1-13.6c-0.2-4.4-1.7-9.5-5.6-13.4c4.9-6.8,11.6-8.8,18.1-10.9c4.2-1.3,8.3-2.6,11.7-5.1 c4.1-3.1,5.7-7.2,4.4-11.5c-1.2-4-4.9-7.1-8.6-7.3c-6.2-0.3-9.8,3.9-10,7.9c-0.1,1.6,0.4,3,1.1,4.1c-1.3-0.3-2.6-1.3-3.7-3 c-1.4-2.2-0.9-5.9,1.3-9.1c2.3-3.4,6.9-6.5,12.7-5.2C-541.8,627.7-538.6,635.3-539.2,641.1z'
		Octopuspath3 = 'M-504.3,708.7c-0.7,0.7-0.8,1.8-0.2,2.6c0,0.1,3.8,4.8,7,25.1c2.1,13.4,6.9,19.2,10.6,21.7c3,2,6.4,2.7,9.6,1.9 c5.1-1.2,8.7-4.1,10-8.1s-0.1-8.6-3.8-13c-1.7-1.9-3.1-3.4-4.4-4.8c-4.1-4.3-5.8-6.1-6.1-11.5c-0.2-3.8,1.1-5.8,4.5-6.6 c2-0.5,3.6,0.7,4.4,1.8c0.3,0.4,0.5,0.9,0.6,1.3c-0.5-0.6-1.1-1-1.9-1.2c-1.6-0.4-3.2,0.2-4.2,1.6c-1.3,1.8-1.1,4.4,0.4,6.6 c1.7,2.4,4.4,4.3,7.3,6.3c4.4,3,9.5,6.4,11.7,13c1.6,4.8,1.5,9.4-0.6,13.3c-2.6,5-8.3,8.8-16.2,11.1c-6.3,1.8-13.3,0.5-19.5-3.7 c-9.1-6.2-15.1-17.3-16.4-30.5c-0.1-0.8-0.7-1.4-1.4-1.6c-0.8-0.2-1.5,0.2-1.9,0.9c-0.3,0.4-5.7,9.7-0.6,21.5 c3.4,8,8.8,13.6,14.1,19.1c5.4,5.6,10.4,10.9,12.9,18.1c2.3,6.9,1.2,14.2-3,19c-3.5,4-8.5,5.6-14,4.4c-3.1-0.6-10.2-3.2-9.3-13.8 c0.7-8.7,8.6-11.4,10.6-11.9c0.8,0.8,1.5,1.6,2.1,2.4c0.3,0.4,0.6,0.7,0.9,1.1c-2.7,0.4-6.2,1.7-7.8,5.4c-1,2.4-0.6,5.2,1,7.3 c1.3,1.6,3.1,2.4,4.9,2.4c0.3,0,0.6,0,0.9-0.1c2.4-0.4,4.7-2.6,5.8-5.5c1-2.7,0.9-5.6-0.2-8.4c0-0.1,0-0.2-0.1-0.3 c-0.7-1.4-1.5-2.9-2.7-4.2c-4.3-5.1-9.4-9.4-14.4-13.5c-2.8-2.2-5.3-4.3-7.8-6.6c-4.9-4.5-9.6-8.9-11.6-18.3c1-4.5,1.3-9.7,0.8-15.8 c-0.1-1-1-1.7-1.9-1.6c-0.9,0.1-1.7,1-1.7,2c1.7,18.1-5.3,27.2-12.4,33.8c-2.4,2.2-5.1,4.4-7.8,6.6c-5,4.1-10.2,8.4-14.4,13.5 c-1.1,1.4-2,2.8-2.6,4.2c0,0.1-0.1,0.2-0.1,0.2c-1.1,2.9-1.2,5.8-0.2,8.5c1.1,2.9,3.4,5.2,5.8,5.5c0.3,0.1,0.6,0.1,0.9,0.1 c1.9,0,3.6-0.9,4.8-2.4c1.6-2.1,2-4.8,1-7.3c-1.5-3.7-5.1-4.9-7.7-5.4c0.3-0.4,0.5-0.7,0.9-1.1c0.7-0.8,1.4-1.6,2.1-2.4 c2,0.6,9.8,3.2,10.6,11.9c0.9,10.6-6.2,13.2-9.3,13.8c-5.5,1.1-10.5-0.5-14-4.4c-4.1-4.7-5.3-12-3-19c2.4-7.2,7.5-12.5,12.9-18.1 c5.3-5.5,10.7-11.1,14.1-19.1c5.1-11.8-0.4-21.1-0.6-21.5c-0.4-0.7-1.2-1-1.9-0.9c-0.8,0.2-1.3,0.8-1.4,1.6 c-1.3,13.2-7.4,24.3-16.5,30.5c-6.2,4.2-13.1,5.5-19.4,3.7c-8-2.3-13.6-6.1-16.2-11.1c-2-3.9-2.2-8.5-0.6-13.3 c2.2-6.6,7.3-10,11.7-13c2.9-2,5.6-3.8,7.3-6.3c1.5-2.1,1.7-4.7,0.4-6.6c-1-1.4-2.6-2-4.2-1.6c-0.8,0.2-1.4,0.6-1.9,1.2 c0.1-0.4,0.3-0.9,0.6-1.3c0.8-1.2,2.4-2.2,4.4-1.8c3.4,0.8,4.7,2.8,4.5,6.6c-0.3,5.3-2,7.1-6.1,11.5c-1.3,1.4-2.7,2.9-4.4,4.8 c-3.8,4.4-5.2,9-3.8,13c1.2,3.9,4.9,6.9,10,8.1c3.2,0.8,6.6,0.1,9.6-1.9c3.7-2.5,8.5-8.3,10.6-21.7c3.1-20,6.8-24.9,7-25 c0.7-0.7,0.6-1.9-0.2-2.6c-0.8-0.7-1.9-0.6-2.6,0.2c-0.3,0.3-1.7,2-3.5,7.4c-3.9,3.2-10.3,3.5-13.2,3.4c-0.8-4.7-4.2-6.5-7.1-7.2 c-3.4-0.8-6.1,0.8-7.8,2.7c-9.5-4-15.6-9.8-18.2-17.4c-2.6-7.6-0.8-17.1,4.1-25c4.4-7.1,13.8-13,26.8-8.3c6.7,2.5,9.3,8.8,9.4,13.9 c0.1,4.8-1.8,8.9-4.9,10.2c-2.4,1.1-4.5,1.2-6.1,0.5l-0.6-0.3c1.7-0.4,3.3-1.6,4.4-3.4c2.4-4.1,1.1-8.5-1.7-11.5 c-0.1-0.2-0.3-0.3-0.4-0.5c-0.8-0.7-1.6-1.4-2.5-1.9c-3.6-2.2-9.6-1.1-13.6,2.4c-2.3,2-7.1,7.8-2.8,17.8 c4.3,9.7,15.7,15.7,25.9,13.5c8-1.7,12.4-6.5,16.7-11.1c5.9-6.4,12-13,28.4-13c16.4,0,22.5,6.6,28.4,13c4.3,4.6,8.7,9.4,16.7,11.1 c10.2,2.1,21.5-3.8,25.8-13.5c4.4-9.9-0.5-15.8-2.8-17.8c-4-3.6-9.9-4.6-13.6-2.4c-0.9,0.6-1.7,1.2-2.5,1.9 c-0.2,0.2-0.3,0.3-0.4,0.5c-2.9,3.1-4.2,7.4-1.7,11.5c1.1,1.8,2.7,3,4.4,3.4l-0.6,0.3c-1.6,0.8-3.6,0.6-6.1-0.5 c-3.1-1.3-5-5.4-4.9-10.2c0.1-5.1,2.7-11.4,9.4-13.8c13-4.8,22.3,1.1,26.8,8.2c4.9,7.9,6.4,17.1,3.9,24.8 c-2.6,7.6-8.6,13.4-18.2,17.4c-1.6-1.9-4.4-3.5-7.8-2.7c-3,0.7-6.4,2.5-7.1,7.2c-2.9,0.1-9.3-0.2-13.3-3.4c-1.8-5.4-3.2-7.1-3.5-7.4 C-502.5,708.2-503.5,708.1-504.3,708.7z'
		Octopuspath4 = 'M-542.4,710.2c0,3.4-2.8,6.2-6.2,6.2c-3.4,0-6.2-2.8-6.2-6.2c0-3.6,2.8-6.2,6.2-6.2 C-545.2,704-542.4,706.6-542.4,710.2z'
		Octopuspath5 = 'M-514.7,710.2c0,3.4-2.8,6.2-6.2,6.2c-3.4,0-6.2-2.8-6.2-6.2c0-3.6,2.8-6.2,6.2-6.2 C-517.5,704-514.7,706.6-514.7,710.2z'

		#Generation of the html code for the different elements that make up the svg
		pathOctopus1 = genHTMLElement('path',
							['class','d'],
							['st0_octopus',Octopuspath1])
		pathOctopus2 = genHTMLElement('path',
							['class','d'],
							['st0_octopus',Octopuspath2])
		pathOctopus3 = genHTMLElement('path',
							['class','d'],
							['st0_octopus',Octopuspath3])
		pathOctopus4 = genHTMLElement('path',
							['class','d'],
							['st1_octopus',Octopuspath4])
		pathOctopus5 = genHTMLElement('path',
							['class','d'],
							['st1_octopus',Octopuspath5])

		#Union of all the elements of the svg within the variable "combine"
		combine = pathOctopus1 + pathOctopus2 + pathOctopus3 + pathOctopus4 + pathOctopus5

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgOctopus = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-629.9 613.3 193.9 212.9','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgOctopus

	def _diamond(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: diamond

		"""

		#Creation of the variable(s) with the svg path
		Diamondpath1 = 'M-74.8,349.3c3.7,6.9,12.2,9.4,19.1,5.8c6.9-3.7,9.4-12.2,5.8-19.1l-22.5-39.4c-3.7-6.9-12.2-9.4-19.1-5.8c-6.9,3.6-9.4,12.2-5.8,19.1L-74.8,349.3z'
		Diamondpath2 = 'M353.1,474.6l-42.3-89.9c-2.3-4.9-7.3-8.1-12.8-8.1H-97c-5.5,0-10.4,3.2-12.8,8.1l-42.3,89.9 c-2.4,5.1-1.5,11.1,2.2,15.3L90,762.6c6.5,6.7,15.8,6.2,21.2,0l239.9-272.7C354.7,485.8,355.5,479.8,353.1,474.6z M43.1,404.8 h114.7l10.2,61.7H32.9L43.1,404.8z M-88.1,404.8H14.5L4.3,466.5h-121.4L-88.1,404.8z M-108.2,494.8H5.9l61.7,199.8L-108.2,494.8z M100.5,705.5L35.4,494.8h130.1L100.5,705.5z M133.4,694.5l61.7-199.8h114.1L133.4,694.5z M196.7,466.5l-10.2-61.7h102.6l29.1,61.7 H196.7z'
		Diamondpath3 = 'M100.5,328.6c7.8,0,14.1-6.3,14.1-14.1v-40.9c0-7.8-6.3-14.1-14.1-14.1s-14.1,6.3-14.1,14.1v40.9 C86.4,322.3,92.7,328.6,100.5,328.6z'
		Diamondpath4 = 'M256.5,355.3c6.9,3.7,15.4,1.1,19.1-5.8L298,310c3.7-6.9,1.1-15.4-5.8-19.1c-6.9-3.7-15.4-1.1-19.1,5.8 l-22.4,39.4C247.1,342.9,249.6,351.5,256.5,355.3z'

		#Generation of the html code for the different elements that make up the svg
		pathDiamond1 = genHTMLElement('path',
							['class','d'],
							['st0_diamond',Diamondpath1])
		pathDiamond2 = genHTMLElement('path',
							['class','d'],
							['st0_diamond',Diamondpath2])
		pathDiamond3 = genHTMLElement('path',
							['class','d'],
							['st0_diamond',Diamondpath3])
		pathDiamond4 = genHTMLElement('path',
							['class','d'],
							['st0_diamond',Diamondpath4])

		#Union of all the elements of the svg within the variable "combine"
		combine = pathDiamond1 + pathDiamond2 + pathDiamond3 + pathDiamond4

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgDiamond = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-153.4 259.5 507.9 507.9','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgDiamond

	def _iceberg(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: iceberg

		"""

		#Creation of the variable(s) with the svg path
		Icebergpath = 'M-950,1411.6h-23.5l6.6,11.7c0,0.1,0.1,0.2,0.1,0.3l1.3,12.1c0,0.4-0.2,0.7-0.5,0.8l-5.8,2.3l-1.9,14.8 c0,0.1-0.1,0.2-0.1,0.3l-14.4,25.4c-0.1,0.2-0.3,0.4-0.6,0.4c-0.2,0-0.5-0.2-0.6-0.4l-11.1-19.2l-11.9-11.3 c-0.1-0.1-0.2-0.4-0.2-0.6l2.5-23.1l-4.1-3.4c-0.3-0.2-0.3-0.6-0.2-0.9l4.3-9.3h-19.9v-1.5h20.6l5.4-11.7c0.1-0.2,0.3-0.4,0.5-0.4 c0.3-0.1,0.5,0,0.7,0.2l1.4,1.4l6.6-11c0.2-0.3,0.4-0.4,0.7-0.4c0.2,0,0.5,0.1,0.6,0.4l3.4,6.6l2.1-0.5c0.3-0.1,0.6,0.1,0.8,0.3 l6.3,9.1l2.4-0.3c0.4,0,0.6,0.1,0.8,0.4l3.4,6h24.3V1411.6z'

		#Generation of the html code for the different elements that make up the svg
		pathIceberg = genHTMLElement('path',
							['class','d'],
							['st0_iceberg',Icebergpath])

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgIceberg = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-1030 1388.1 80 91.6','preserve','http://www.w3.org/2000/svg'],
							pathIceberg)

		#Return of the html code that represent the svg
		return svgIceberg

	def _pirate(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: pirate

		"""

		#Creation of the variable(s) with the svg path
		Piratepath1 = 'M-799.8,2049.2c-9.1,3.4-17.2,9.2-23.3,17.1l-6.8,8.9c-6.6,8.6-15.3,15.4-25.2,19.8l-14.2,6.3l3.3,19.5h43.9v-13 c25.7-9.6,56.6-9.4,81.4,0v13h43.9l3.3-17.9l-15.9-8c-8.8-4.4-16.5-10.7-22.5-18.5l-7.8-10.1c-6.1-7.9-14.2-13.7-23.3-17.1 c-2.7,11.7-10.1,19.5-18.4,19.6C-789.7,2068.8-797,2060.9-799.8,2049.2L-799.8,2049.2z M-789.6,2078.5c0.6,0,1.2,0.2,1.8,0.5 l6.4,3.9l6.4-3.9c0.6-0.3,1.2-0.5,1.9-0.5c1.8,0.1,3.2,1.6,3.1,3.4c-0.1,1.1-0.7,2.1-1.6,2.7l-3.4,2.1l3.4,2.1 c1.5,0.9,2,2.9,1.1,4.5c-0.9,1.5-2.9,2-4.5,1.1l-6.4-3.9l-6.4,3.9c-1.5,0.9-3.5,0.4-4.5-1.1c-0.9-1.5-0.4-3.5,1.1-4.5l3.4-2.1 l-3.4-2.1c-1.6-0.9-2.1-2.9-1.2-4.5C-791.8,2079.2-790.7,2078.5-789.6,2078.5L-789.6,2078.5z'
		Piratepath2 = 'M-781.4,2105.7c-12.1,0-24.3,2.3-35.7,7h-0.1v29.6l10.7-10.7c-0.6-1.3-1-2.7-1-4.2c0-5.4,4.4-9.7,9.8-9.8 c1.5,0,2.9,0.3,4.2,1l12.8-12.8C-780.9,2105.7-781.1,2105.7-781.4,2105.7L-781.4,2105.7z M-771.9,2106.2l-17,17c0.6,1.3,1,2.7,1,4.2 c0,5.4-4.4,9.8-9.8,9.8c-1.5,0-2.9-0.3-4.2-1l-15.3,15.3v11.7l10.7,9.7c1.6-4.2,2.4-8.7,2.4-13.3v-2.7c0-5.3,4.2-9.6,9.2-10 c0.7-0.1,1.5,0,2.2,0.1l11.4,2l11.4-2c6-1,11.4,3.8,11.4,9.9v3.2c0,4.4,0.8,8.7,2.3,12.8l10.8-9.8v-50.5h-0.1 C-754.1,2109.2-763,2107.1-771.9,2106.2L-771.9,2106.2z M-758.7,2117.6c1.8-0.1,3.3,1.4,3.4,3.2c0,1.3-0.7,2.6-2,3.1l-14.6,6.5 c-1.6,0.8-3.6,0.2-4.4-1.4c-0.8-1.6-0.2-3.6,1.4-4.4c0.1-0.1,0.2-0.1,0.3-0.2l14.6-6.5C-759.5,2117.7-759.1,2117.6-758.7,2117.6 L-758.7,2117.6z M-761.9,2130.6c1.8-0.1,3.3,1.3,3.4,3.1c0.1,1.5-0.9,2.8-2.3,3.2l-4.9,1.6c-1.7,0.7-3.6-0.2-4.2-1.8 c-0.7-1.7,0.2-3.6,1.8-4.2c0.1,0,0.2-0.1,0.3-0.1l4.9-1.6C-762.6,2130.7-762.3,2130.6-761.9,2130.6L-761.9,2130.6z M-793.9,2153.4 c-2-0.3-3.8,1.2-3.8,3.4v2.7c0,6.2-1.3,12.3-3.8,17.9l20,18.2l19.9-18.1c-2.3-5.5-3.6-11.5-3.6-17.5v-3.2c0-2.3-1.8-3.8-3.8-3.4 l-11.9,2.1c-0.4,0.1-0.7,0.1-1.1,0L-793.9,2153.4L-793.9,2153.4z M-788.1,2159.9h0.2h13c1.8,0,3.3,1.4,3.3,3.2 c0,1.8-1.4,3.3-3.2,3.3h-0.1h-13c-1.8,0.1-3.3-1.3-3.4-3.1C-791.3,2161.5-789.9,2160-788.1,2159.9z'

		#Generation of the html code for the different elements that make up the svg
		pathPirate1 = genHTMLElement('path',
							['class','d'],
							['st0_pirate',Piratepath1])
		pathPirate2 = genHTMLElement('path',
							['class','d'],
							['st0_pirate',Piratepath2])

		#Union of all the elements of the svg within the variable "combine"
		combine = pathPirate1 + pathPirate2
		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgPirate = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-869.3 2049.2 175.8 146.4','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgPirate

	def _island(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: Island

		"""

		#Creation of the variable(s) with the svg path
		Islandpath1 = 'M-474.1,715.3c0.2-0.1,0.4-0.1,0.6-0.2c0.4-0.1,0.7-0.3,1.1-0.5s0.8-0.3,1.2-0.5c0.4-0.2,0.8-0.3,1.2-0.5 c0.4-0.1,0.8-0.3,1.2-0.4c0.4-0.1,0.8-0.3,1.2-0.4c0.2,0,0.4-0.1,0.6-0.2c0.2,0,0.4-0.1,0.6-0.1c0.4-0.1,0.8-0.2,1.2-0.2 c0.2,0,0.4-0.1,0.6-0.1s0.4,0,0.6-0.1c0.4,0,0.7-0.1,1.1-0.1c0.3,0,0.6-0.1,0.9-0.1c0.5-0.1,0.8-0.1,0.8-0.1s-0.2-0.3-0.5-0.7 c-0.2-0.2-0.4-0.5-0.7-0.7c-0.3-0.3-0.6-0.5-1-0.7c-0.2-0.1-0.4-0.2-0.6-0.4c-0.2-0.1-0.5-0.2-0.7-0.3c-0.3-0.1-0.5-0.2-0.8-0.2 c-0.3-0.1-0.6-0.1-0.9-0.1s-0.6,0-0.9-0.1c-0.3,0-0.6,0-0.9,0.1c-0.6,0-1.2,0.2-1.8,0.4c-0.6,0.2-1.2,0.5-1.7,0.8 c0.2-0.3,0.5-0.7,0.7-1c0.3-0.4,0.6-0.8,0.8-1.2c0.1-0.2,0.3-0.4,0.4-0.6c0.1-0.2,0.3-0.3,0.4-0.5c0.6-0.7,1.1-1.3,1.7-1.8 c0.3-0.3,0.6-0.5,0.8-0.7c0.3-0.2,0.5-0.4,0.8-0.5c0.5-0.3,0.7-0.5,0.7-0.5s-0.3-0.2-0.8-0.4c-0.3-0.1-0.6-0.2-1-0.2 c-0.4-0.1-0.9-0.1-1.4,0c-1,0.1-2.2,0.5-3.3,1.2c-0.5,0.4-1.1,0.8-1.5,1.2c-0.5,0.5-0.9,1-1.2,1.5c-0.4,0.5-0.7,1.1-0.9,1.7 c-0.1,0.2-0.2,0.5-0.3,0.8v-0.5c0-0.4-0.1-0.9-0.1-1.3c0-0.4-0.1-0.8-0.1-1.2s-0.1-0.8-0.1-1.2s-0.1-0.8,0-1.1v-1v-0.8V701 c0,0-0.3,0.1-0.7,0.4c-0.2,0.1-0.5,0.3-0.8,0.5l-0.8,0.8c-0.3,0.3-0.5,0.7-0.8,1.2c-0.3,0.4-0.4,0.9-0.6,1.4s-0.3,1-0.3,1.6 c-0.1,0.6-0.1,1.1-0.1,1.7c0,0.5,0.1,1.1,0.2,1.6c-0.2-0.1-0.4-0.3-0.6-0.4c-0.5-0.3-1.1-0.6-1.7-0.8c-0.6-0.2-1.2-0.4-1.8-0.4 c-0.3,0-0.6-0.1-0.9-0.1s-0.6,0-0.9,0.1c-0.6,0-1.2,0.2-1.7,0.4c-0.3,0.1-0.5,0.2-0.7,0.3c-0.2,0.1-0.5,0.2-0.7,0.4 c-0.4,0.3-0.8,0.5-1,0.7s-0.5,0.5-0.6,0.7c-0.3,0.4-0.5,0.7-0.5,0.7s0.3,0.1,0.8,0.1h0.9c0.4,0,0.7,0.1,1.1,0.1c0.2,0,0.4,0,0.5,0.1 c0.2,0,0.4,0.1,0.6,0.1s0.4,0.1,0.6,0.1s0.4,0.1,0.6,0.1c0.2,0.1,0.4,0.1,0.6,0.1c0.2,0.1,0.4,0.1,0.6,0.2c0.4,0.1,0.8,0.2,1.2,0.4 c0.4,0.1,0.8,0.3,1.2,0.4c0.4,0.2,0.8,0.3,1.2,0.5c0.1,0.1,0.3,0.1,0.4,0.2h-1.2c-0.6,0-1.2,0.1-1.8,0.3c-0.6,0.1-1.2,0.4-1.7,0.6 c-0.6,0.2-1.1,0.6-1.6,0.9c-0.5,0.3-0.9,0.7-1.4,1.1c-0.4,0.4-0.8,0.8-1.1,1.2c-0.3,0.4-0.6,0.9-0.8,1.2c-0.2,0.4-0.4,0.8-0.5,1.1 c-0.1,0.4-0.2,0.7-0.3,0.9c-0.1,0.5-0.1,0.8-0.1,0.8s0.3-0.1,0.8-0.3c0.2-0.1,0.5-0.2,0.8-0.4c0.3-0.2,0.7-0.3,1-0.5 c0.4-0.2,0.7-0.4,1.1-0.6l1.2-0.6l1.2-0.6c0.4-0.2,0.8-0.4,1.3-0.6c0.4-0.2,0.8-0.3,1.1-0.5c-0.1,0.1-0.2,0.2-0.3,0.2 c-0.4,0.4-0.8,0.8-1.1,1.3c-0.3,0.5-0.7,1-0.9,1.5c-0.3,0.5-0.5,1-0.6,1.6c-0.1,0.3-0.1,0.5-0.2,0.8c0,0.3-0.1,0.5-0.1,0.8v0.7 c0,0.2,0,0.5,0.1,0.7c0.1,0.4,0.1,0.8,0.2,1.2c0.1,0.3,0.2,0.6,0.4,0.9c0.2,0.5,0.4,0.7,0.4,0.7s0.2-0.3,0.5-0.7 c0.1-0.2,0.3-0.5,0.4-0.7l0.6-0.9c0.2-0.3,0.4-0.6,0.6-1c0.1-0.2,0.2-0.3,0.3-0.5s0.2-0.3,0.4-0.5c0.1-0.2,0.2-0.4,0.3-0.5 c0.1-0.2,0.3-0.3,0.4-0.5c0.2-0.4,0.5-0.7,0.8-1.1c0.2-0.4,0.5-0.7,0.8-1.1c0.3-0.3,0.5-0.7,0.8-1.1c0.5-0.7,1-1.4,1.4-2.1 c0.1-0.1,0.1-0.2,0.2-0.3c1.6,2.7,6.2,10.9,7.4,19.8c1.7,0,2.7,0,4.2-0.7C-467.1,726.8-472.7,717.5-474.1,715.3L-474.1,715.3z'
		Islandpath2 = 'M-454.5,737.7c0.8-19.7,6.7-30.8,7.9-32.9c0.3,0.3,0.7,0.7,1.1,1l1.2,1.2c0.4,0.4,0.8,0.9,1.3,1.3 c0.4,0.5,0.8,0.9,1.3,1.4c0.4,0.5,0.9,0.9,1.2,1.5l0.6,0.7c0.2,0.3,0.4,0.5,0.5,0.8c0.2,0.3,0.4,0.5,0.5,0.8 c0.2,0.3,0.3,0.5,0.5,0.8c0.4,0.5,0.6,1,0.9,1.5c0.1,0.2,0.3,0.5,0.4,0.7s0.2,0.5,0.3,0.7c0.2,0.5,0.5,0.9,0.6,1.3 c0.2,0.4,0.3,0.8,0.5,1.1l0.5,1c0,0,0.2-0.4,0.4-1c0.1-0.3,0.2-0.7,0.3-1.2s0.1-1,0.1-1.6v-0.9c0-0.3-0.1-0.6-0.1-1 c-0.1-0.7-0.2-1.4-0.5-2.1c-0.2-0.7-0.5-1.5-0.9-2.1c-0.2-0.3-0.4-0.7-0.6-1l-0.7-1c-0.5-0.6-1.1-1.2-1.6-1.7 c-0.3-0.3-0.6-0.5-0.9-0.7c-0.3-0.2-0.6-0.5-0.9-0.7c-0.6-0.4-1.2-0.7-1.9-1c-0.6-0.3-1.1-0.5-1.6-0.6c0.3,0,0.6,0.1,0.9,0.1 c0.5,0,1.1,0.2,1.6,0.2c0.5,0.1,1.1,0.1,1.7,0.3c0.6,0.1,1.1,0.2,1.7,0.3c0.6,0.1,1.1,0.3,1.7,0.4s1.1,0.3,1.6,0.4 c0.6,0.1,1,0.3,1.5,0.5c0.5,0.1,1,0.3,1.4,0.5c0.4,0.2,0.9,0.3,1.3,0.4c0.4,0.2,0.7,0.3,1,0.4c0.6,0.2,1,0.3,1,0.3s-0.1-0.4-0.4-0.9 c-0.1-0.3-0.3-0.6-0.5-1c-0.2-0.4-0.5-0.7-0.9-1.2c-0.4-0.4-0.7-0.9-1.2-1.2c-0.5-0.4-1-0.8-1.6-1.2c-0.3-0.2-0.6-0.3-0.9-0.5 s-0.6-0.3-1-0.4c-0.7-0.3-1.4-0.5-2.1-0.6c-0.4-0.1-0.7-0.1-1.1-0.2c-0.4,0-0.7-0.1-1.1-0.1h-1.1c-0.3,0-0.7,0-1,0.1 c0.3-0.2,0.7-0.3,1-0.5l1.2-0.6l0.6-0.3l0.6-0.3c0.4-0.2,0.8-0.4,1.2-0.5c0.4-0.1,0.8-0.3,1.1-0.4c0.4-0.1,0.7-0.3,1-0.4 c0.3-0.1,0.6-0.2,0.8-0.3c0.5-0.2,0.8-0.3,0.8-0.3s-0.2-0.2-0.6-0.5c-0.2-0.2-0.5-0.4-0.8-0.6c-0.3-0.2-0.7-0.3-1.2-0.5 s-0.9-0.2-1.5-0.3c-0.5-0.1-1.1-0.1-1.7,0c-0.6,0-1.2,0.2-1.8,0.3s-1.1,0.4-1.7,0.7c-0.5,0.3-1.1,0.6-1.6,0.9 c-0.1,0.1-0.3,0.2-0.4,0.3c0-0.2,0.1-0.4,0.1-0.7c0.1-0.6,0.2-1.2,0.2-1.8v-0.9c0-0.3-0.1-0.6-0.1-0.9c-0.1-0.6-0.2-1.2-0.4-1.7 c-0.1-0.6-0.4-1.1-0.6-1.6c-0.1-0.2-0.2-0.5-0.3-0.7c-0.1-0.2-0.3-0.4-0.4-0.6c-0.3-0.4-0.5-0.7-0.8-1l-0.7-0.7 c-0.4-0.4-0.7-0.5-0.7-0.5s-0.1,0.3-0.1,0.9c0,0.5-0.1,1.2-0.1,2.1v1.3v1.4v1.4v1.5v1.5c-0.2-0.5-0.5-1.1-0.9-1.6 c-0.4-0.6-0.9-1.1-1.4-1.6s-1.1-0.9-1.7-1.3c-0.6-0.3-1.2-0.7-1.8-0.9s-1.2-0.4-1.8-0.5c-0.6-0.1-1.1-0.2-1.7-0.2h-1.4 c-0.4,0.1-0.8,0.1-1.1,0.2c-0.6,0.1-0.9,0.2-0.9,0.2s0.3,0.3,0.7,0.6c0.2,0.2,0.5,0.4,0.8,0.6s0.7,0.5,1,0.7 c0.4,0.3,0.8,0.5,1.2,0.8l1.2,0.9c0.4,0.3,0.8,0.7,1.2,1c0.4,0.4,0.8,0.7,1.2,1c0.4,0.4,0.8,0.7,1.1,1.1c0.2,0.2,0.3,0.4,0.5,0.6 c0.2,0.2,0.3,0.4,0.5,0.6c0.3,0.4,0.6,0.8,0.9,1.2s0.5,0.7,0.8,1.1c-0.1-0.2-0.3-0.3-0.4-0.5c-0.4-0.4-0.9-0.8-1.4-1.2 s-1.1-0.8-1.8-1.1s-1.3-0.7-2.1-0.9c-0.4-0.1-0.7-0.3-1.1-0.4l-1.2-0.3c-0.8-0.2-1.6-0.2-2.3-0.3h-1.2c-0.4,0-0.8,0-1.1,0.1 c-0.7,0.1-1.4,0.3-2.1,0.4s-1.2,0.4-1.8,0.6c-0.5,0.2-1,0.4-1.4,0.7c-0.4,0.3-0.7,0.5-1,0.7c-0.5,0.4-0.8,0.7-0.8,0.7 s0.4,0.1,1.1,0.1c0.3,0,0.7,0.1,1.2,0.1c0.4,0,0.9,0.1,1.5,0.1c0.5,0.1,1.1,0,1.7,0.1c0.6,0.1,1.2,0.1,1.8,0.2 c0.6,0.1,1.2,0.1,1.9,0.3c0.6,0.1,1.3,0.2,1.9,0.3l1,0.2c0.3,0.1,0.6,0.2,0.9,0.2c0.6,0.1,1.2,0.3,1.8,0.5c1.2,0.3,2.3,0.7,3.3,1 c0.5,0.2,1,0.3,1.4,0.4c-1.5,2.5-7.7,14.1-8.5,34.8'
		Islandpath3 = 'M-458.8,737.4h-1.2c-2,0-3.9,0.1-5.7,0.3v-0.3c-1.5,0.7-2.5,0.7-4.2,0.7v0.2c-11.5,2.3-18.6,8.4-21.2,11 c-0.7,0.7-0.4,1.3,0.6,1.3h61.1c1,0,1.2-0.6,0.5-1.2c-3-2.9-11.5-9.9-25.6-11.6'
		Islandpath4 = 'M-479.6,761.1c1.9,1.6,5.8,4.3,9.8,4.3s7.9-2.8,9.8-4.3c1.9,1.6,5.8,4.3,9.8,4.3s7.9-2.8,9.8-4.3 c1.9,1.6,5.8,4.3,9.8,4.3c5.5,0,10.7-5.2,10.9-5.4l-2.3-2.3c0,0-4.5,4.4-8.6,4.4c-4.2,0-8.6-4.4-8.6-4.4l-1.1-1.1l-1.2,1.1 c0,0-4.5,4.4-8.6,4.4c-4.1,0-8.6-4.4-8.6-4.4l-1.2-1.1l-1.2,1.1c0,0-4.5,4.4-8.6,4.4c-4.2,0-8.6-4.4-8.6-4.4l-1.2-1.1l-1.1,1.1 	c0,0-4.5,4.4-8.6,4.4c-4.2,0-8.6-4.4-8.6-4.4l-2.3,2.3c0.2,0.2,5.4,5.4,10.9,5.4C-485.3,765.4-481.5,762.6-479.6,761.1L-479.6,761.1 z'
		Islandpath5 = 'M-430.6,772.7c-4.2,0-8.6-4.4-8.6-4.4l-1.1-1.1l-1.2,1.1c0,0-4.5,4.4-8.6,4.4c-4.1,0-8.6-4.4-8.6-4.4l-1.2-1.1 l-1.2,1.1c0,0-4.5,4.4-8.6,4.4c-4.2,0-8.6-4.4-8.6-4.4l-1.2-1.1l-1.1,1.1c0,0-4.5,4.4-8.6,4.4c-4.2,0-8.6-4.4-8.6-4.4l-2.3,2.3 c0.2,0.2,5.4,5.4,10.9,5.4c4,0,7.9-2.8,9.8-4.3c1.9,1.6,5.8,4.3,9.8,4.3s7.9-2.8,9.8-4.3c1.9,1.6,5.8,4.3,9.8,4.3s7.9-2.8,9.8-4.3 c1.9,1.6,5.8,4.3,9.8,4.3c5.5,0,10.7-5.2,10.9-5.4l-2.3-2.3C-422,768.4-426.5,772.7-430.6,772.7L-430.6,772.7z'

		#Generation of the html code for the different elements that make up the svg
		pathIsland1 = genHTMLElement('path',
							['class','d'],
							['st0_island',Islandpath1])
		pathIsland2 = genHTMLElement('path',
							['class','d'],
							['st0_island',Islandpath2])
		pathIsland3 = genHTMLElement('path',
							['class','d'],
							['st1_island',Islandpath3])
		pathIsland4 = genHTMLElement('path',
							['class','d'],
							['st2_island',Islandpath4])
		pathIsland5 = genHTMLElement('path',
							['class','d'],
							['st2_island',Islandpath5])
		#Union of all the elements of the svg within the variable "combine"
		combine = pathIsland1 + pathIsland2 + pathIsland3 + pathIsland4 + pathIsland5

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgIsland = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-505 684 91 95.5','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgIsland

	def _maelstrom(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg obstacles: maelstrom

		"""

		#Creation of the variable(s) with the svg path
		Maelstrompath1 = 'M-192.5,401.5c0.6,0.7,1.1,1.5,1.7,2.3c1.3,1.5,1.4,3.2,0.2,4.7c-1.2,1.6-2.7,3-4.2,4.4c-0.5,0.4-1.4,0.6-2.1,0.6 c-5.5-0.1-10-3.2-10.8-8.9c-0.2-1.6,0.2-3.5,1.1-4.9c1.5-2.6,3.6-4.7,6.8-5.5c1.9-0.5,3.7-1.1,5.7-1.1c5.2-0.2,10,2.9,11.8,7.7 c1.3,3.5,1.6,7.2,0.5,10.8c-0.6,2-1.8,4.1-3.2,5.6c-1.2,1.3-3.2,1.8-4.8,2.8c-0.7,0.4-1.6,0.9-2.1,1.6c-1.4,1.9-3.4,2.3-5.6,2.3 c-1.1,0-2.3-0.1-3.4-0.1c-7.8-0.3-14.4-3.3-18.5-9.9c-3.8-6.2-5-13.1-1.2-19.9c1.7-2.9,4.2-5.3,6.4-7.9c0.5-0.6,1.3-0.9,2.1-1.2 c4.4-1.6,8.9-2.6,13.5-2.9c3.6-0.2,7.1-0.3,10.7,0.4c4.4,0.8,8.1,2.6,11.2,5.9c3.5,3.7,6.3,7.8,8.1,12.6c2.2,6.2,1.5,12.2-1.8,17.8 c-2.7,4.5-5.9,8.7-9.6,12.5c-2.1,2.1-4.7,3.7-7.1,5.5c-0.6,0.5-1.5,0.8-2,1.3c-3.1,3.1-6.9,3.3-10.9,2.9c-3-0.4-6-1-9.1-1.5 c-1.5-0.3-3-0.6-4.2-1.8c-0.6-0.6-1.5-0.9-2.4-1.2c-5.6-2.4-10-6.5-14.7-10.2c-0.1-0.1-0.2-0.2-0.3-0.4c-2.7-3.5-5.5-7.1-7-11.3 c-1.5-4.2-2-8.5-1.2-12.9c1.1-5.8,3.2-11.3,5.9-16.4c1.5-2.8,3.8-5.3,6.1-7.5c2.7-2.5,5.8-4.8,9-6.6c2.3-1.3,5.1-1.9,7.8-2.6 c8-2.3,16.1-2.6,24.2-2c2.1,0.2,4.3,0.8,6.3,1.7c3.3,1.4,6.4,3.1,9.5,4.8c1.2,0.7,2,1.9,3,2.9c5.1,5.2,9.3,11,11.9,17.9 c1,2.7,2.3,5.4,2.9,8.3c0.8,4,0.2,8.1-1.3,11.9c-1.1,2.9-1.9,5.8-3.1,8.7c-0.6,1.5-1.6,3-2.5,4.4c-0.7,1.2-1.7,2.2-2.4,3.3 c-2,3-3.7,6.1-5.8,8.9c-3.8,5-8.5,8.9-14.9,10.2c-3.4,0.7-6.8,1.5-10.2,1.8c-4.1,0.4-8.1-0.3-12-1.3c-2.1-0.5-4.3-1-6.4-1.6 c-1.2-0.3-2.3-0.8-3.4-1.2c-0.7-0.2-1.4-0.5-2.1-0.6c-5.9-1.3-11.5-3.4-16.4-7c-2.6-1.9-5.5-3.5-7.5-6.1c-2-2.5-2-4.1,0.3-6.9 c0.4,0.6,0.9,1.1,1.2,1.7c1.5,2.7,3.5,4.8,6.3,6.3c0.6,0.3,1.2,0.8,1.8,1.2c3.1,2.4,6.5,4.3,10,5.9c0.5,0.2,1,0.5,1.6,0.6 c4.7,1,9.3,2.1,14,3c2.5,0.5,5,0.6,7.5,1.1s5,0.3,7.5-0.2c4.4-0.9,8.8-1.7,12.9-3.5c4.1-1.8,7.6-4.4,10.2-8.1 c2.7-3.8,5.5-7.6,8-11.6c0.7-1.1,1-2.6,1.4-3.9c0.5-1.5,0.8-3.1,1.5-4.6c1.1-2.6,1.7-5.2,1.3-8c0-0.2,0-0.3-0.1-0.5 c-2.3-4.9-2.7-10.6-6.1-15c-2.1-2.7-4.2-5.3-6.3-8c-0.5-0.6-0.9-1.2-1.3-1.8c-1-1.4-2.2-2.5-3.9-3.3c-3-1.4-6-2.9-8.9-4.4 c-2.3-1.2-4.7-1.5-7.3-1.7c-5-0.4-9.9-0.3-14.8,0.6c-4,0.7-8,1.5-11.8,3c-2.9,1.2-5.4,3.5-8.1,5.3c-2.8,1.8-4.6,4.2-6.6,6.4 c-0.8,0.9-1.3,2-1.9,3.1c-2,3.5-3.8,7-4.5,11c-0.2,1.6-0.1,3.2,0.1,4.8c0.8,5.3,3.8,9.6,6.9,13.8c3.8,5.1,8.8,8.5,14.5,11.1 c6.6,3,13.5,4.1,20.6,4.3c2,0.1,3.6-0.6,5.1-1.8c1.8-1.4,3.7-2.7,5.5-4c5.2-3.7,8.9-8.7,12.2-14c2-3.2,2.5-6.8,1.2-10.5 c-2-5.4-5.3-9.9-9.1-14c-1.6-1.7-3.7-2.3-5.9-2.8c-8.5-1.9-17-1.1-25.2,1.6c-2.4,0.8-4.5,2.5-6.6,4c-1.5,1.1-1.8,2.9-1.9,4.6 c-0.4,3.9,0.7,7.6,1.8,11.2c0.2,0.7,0.9,1.4,1.4,2c1.1,1.4,2.1,2.9,3.3,4.2c0.6,0.7,1.3,1.3,2.1,1.6c3.2,1.3,6.4,2.9,10,2.6 c1.1-0.1,2.3,0.1,3.4-0.1c1.3-0.2,2.7-0.5,3.9-1.2c2.2-1.3,4.5-2.7,6.5-4.3c2.4-1.9,4.7-6.9,2.7-10.8c-1.6-3.2-4.4-4.9-7.5-6.2 c-1-0.4-2-0.7-3-1c-0.5-0.1-1-0.3-1.4-0.3c-3,0.3-5.7,1.2-7.9,3.3c-1.6,1.5-1.7,4.4,0.7,7c1.3,1.4,3,2.9,5.2,3c0.9,0,1.9,0,2.8-0.4 c1.6-0.6,1.8-1.3,1.2-2.8c-0.2-0.5-0.5-1-0.8-1.5C-195.5,402.6-195,401.8-192.5,401.5z'

		#Generation of the html code for the different elements that make up the svg
		pathMaelstrom1 = genHTMLElement('path',
							['class','d'],
							['st0_maelstrom',Maelstrompath1])

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgMaelstrom = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-247 358.9 100 97.6','preserve','http://www.w3.org/2000/svg'],
							pathMaelstrom1)

		#Return of the html code that represent the svg
		return svgMaelstrom

	def _treasure(self):
		"""Renders the specific SVG obstacle wrapping the html code for all the icon elements

		Type of svg end point: treasure

		"""

		#Creation of the variable(s) with the svg path
		Treasurepath1 = '-469.3,822.7 -514.9,822.7 -523.1,810.6 -523.2,782.6 -527.1,780.4 -527,766.9 -522.8,764.7 -476.8,764.7 -476.9,776.3 -473.3,782.6 -475,785.9 -469.2,794.7'
		Treasurepath2 = '-495,782.6 -492,776.9 -476.4,776.9 -473.3,782.6 -482,794.3 -486.1,794.3'
		Treasurepath3 = 'M-515.2,794.3h16.2v-21.8c-5.4-3.4-10.8-3.4-16.2,0'
		Treasurepath4 = 'M-468.1,794.4L-468.1,794.4c-0.1-0.1-0.1-0.2-0.1-0.2l-5.8-8.6l1.7-2.2c0.2-0.3,0.3-0.7,0.1-1.1l-3-6 c-0.2-0.3-0.5-0.6-0.9-0.6v-11c0-0.6-0.4-1-1-1h-46l0,0c-0.1,0-0.2,0-0.3,0.1c0,0,0,0-0.1,0l0,0l-4,2c-0.3,0.2-0.6,0.5-0.6,0.9v14 c0,0.4,0.2,0.7,0.6,0.9l3.4,1.7v27.4c0,0.2,0.1,0.4,0.2,0.6l8,12l0.1,0.1l0,0c0.1,0.1,0.2,0.1,0.3,0.2c0,0,0,0,0.1,0 c0.1,0,0.2,0.1,0.3,0.1h6h8h18h8h6c0.6,0,1-0.4,1-1v-28l0,0C-468,794.7-468,794.5-468.1,794.4z M-475,793.8h-5.4l5.1-6.5l4.4,6.5 H-475z M-514,793.8v-3.4c1.7,0.9,4.4,1.4,7,1.4s5.3-0.5,7-1.4v3.4h-1h-8H-514z M-495.5,783.8l7.9,10h-0.4h-8h-2v-6v-1v-3H-495.5z M-477.9,777.8l-2.1,3.2l-2.1-3.2H-477.9z M-475.9,784.9L-475.9,784.9l-0.5,0.6l-5.2,6.6l2.4-8.4h4.2L-475.9,784.9z M-486.1,781.8 l2.1-3.2l2.1,3.2H-486.1z M-481.3,783.8l-2.7,9.4l-2.7-9.4H-481.3z M-486.4,792.2l-6.6-8.4h1.9h2.2L-486.4,792.2z M-488,781 l-2.1-3.2h4.3L-488,781z M-491.9,778.8l2,3h-1.1h-2.4L-491.9,778.8z M-495,795.8h2v3h2v-3h2v4.5l-3,2.3l-3-2.3V795.8z M-514,786.8 v-1.4c1.7,0.9,4.4,1.4,7,1.4s5.3-0.5,7-1.4v1.4v1c0,0.6-2.5,2-7,2s-7-1.4-7-2V786.8z M-514,781.8v-1.4c1.7,0.9,4.4,1.4,7,1.4 s5.3-0.5,7-1.4v1.4v1c0,0.6-2.5,2-7,2s-7-1.4-7-2V781.8z M-514,775.4c1.7,0.9,4.4,1.4,7,1.4s5.3-0.5,7-1.4v1.4v1c0,0.6-2.5,2-7,2 s-7-1.4-7-2v-1V775.4z M-514,772.8c0-0.6,2.5-2,7-2s7,1.4,7,2c0,0.6-2.5,2-7,2S-514,773.4-514,772.8z M-516,786.8v1v3.7l-5.1-7.7 h5.1V786.8z M-497,795.8v5c0,0.3,0.1,0.6,0.4,0.8l4,3c0.2,0.1,0.4,0.2,0.6,0.2s0.4-0.1,0.6-0.2l4-3c0.3-0.2,0.4-0.5,0.4-0.8v-5h1.4 h1h0.6v26h-16v-26H-497z M-474.6,781.8h-3.5l2-3L-474.6,781.8z M-478,775.8h-14c-0.4,0-0.7,0.2-0.9,0.6l-2.7,5.4h-2.4v-4v-1v-4 c0-2.6-4.5-4-9-4s-9,1.4-9,4v4v1v4h-6v-16h44V775.8z M-526,767.4l2-1v14.8l-2-1V767.4z M-522,786.1l2,3v11.7h2v-8.7l2,3v24.4l-6-9 V786.1z M-514,795.8h4v26h-4V795.8z M-508,821.8v-26h6v26H-508z M-482,821.8v-26h6v26H-482z M-470,821.8h-4v-26h4V821.8z'

		#Generation of the html code for the different elements that make up the svg
		pathTreasure1 = genHTMLElement('polygon',
							['class','points'],
							['st0_treasure',Treasurepath1])
		pathTreasure2 = genHTMLElement('polygon',
							['class','points'],
							['st1_treasure',Treasurepath2])
		pathTreasure3 = genHTMLElement('path',
							['class','d'],
							['st2_treasure',Treasurepath3])
		pathTreasure4 = genHTMLElement('path',
							['class','d'],
							['st4_treasure',Treasurepath4])

		#Union of all the elements of the svg within the variable "combine"
		combine = pathTreasure1 + pathTreasure2 + pathTreasure3 + pathTreasure4

		#Generation of the html code for the svg, all svg element are wrapped into the variable combine
		svgTreasure = genHTMLElement('svg',
							['version','viewBox','xml:space','xmlns',],
							[1.1,'-532.5 760.3 74 68','preserve','http://www.w3.org/2000/svg'],
							combine)

		#Return of the html code that represent the svg
		return svgTreasure



class Island(object):
	"""Create an Island

	The Icon class contains all information needed to render the obstacles

	"""

	def __init__(self,id,fill,path):
		"""Keyword arguments:

		id,fill,path
		where:
		id: Id of the island (e.g. 1,2,3,..)
		fill: type of filling. It can be "#sandpattern"
		path: polygon path

		"""
		self._id = int(id)
		self._fill = 'url(#' + str(fill) +')'
		self._htmlId = 'obj_' + str(self._id)

		#pathTemp = str(path).replace(',',' ')
		#pathTemp = pathTemp.replace(';',' L ')
		#pathTemp = 'M ' + pathTemp + ' Z'
		self._path = path

	def render(self):
		"""Renders the Island obstacle wrapping the html code

		"""
		#Generation of the html code for the path that represent the island
		island = genHTMLElement('path',
						['class','id','d','fill'],
						['island',self._htmlId, self._path,self._fill])

		#Return of the html code that represent the island
		return island

class ScoreBoard (object):

	def __init__(self,scoreName,scorePoint):
		
		#cp.deepcopy to create a copy of the list and not pass only the pointer
		#self._scoreName = cp.deepcopy(scoreName)
		#self._scorePoint = cp.deepcopy(scorePoint)

		self._scoreName = scoreName
		self._scorePoint = scorePoint
		
		#self._scoreName = ['A','B','C','D','E']
		#self._scorePoint = [1,2,3,4,5]

	def __str__(self):
		#10 reiteration are hard coded
		scoreHtml = ''
		tableRow = ''
		tableHtml = ''	
		for i in range(2):
			
			scoreHtml = genHTMLElement('td',[],[],str(self._scoreName[i])) + genHTMLElement('td',[],[],str(self._scorePoint[i]))
	#		scorePoiHtml.append(genHTMLElement('td',[],[],self._scorePoint[i]))
			
			tableRow = tableRow + genHTMLElement('tr',[],[],scoreHtml)
		
		tableHtml = genHTMLElement('tbody',[],[],tableRow)
		
		return tableHtml