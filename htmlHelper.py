#!/usr/bin/env python3

__all__ = ['genHTMLElement','genTextElement','genTableElements','genImageElements']

def genHTMLElement(elementName,paramNames,paramValues,elementValue=""):
	"""Function to generate a html element of the form <element params=values>text</element>
	text can be left blank
	
	Keyword arguments:
	elementName -- Element Name. e.g. font
	paramNames -- List of params
	paramValues -- List of values for params
	elementValue -- any text to go in element - can be another element
	"""
	
	#param names and values must be same length
	assert len(paramNames) == len(paramValues)
	
	#Start of element
	text='<' + elementName
	
	#Iterate through list and add params
	for i in range(0, len(paramNames)):
		text = text + ' ' + str(paramNames[i]) + '="' + str(paramValues[i]) + '"'
		
	#Add element value if not empty
	if elementValue=="":
		text = text + '/>'
	else:
		text = text + '>' + elementValue + '</' + elementName + '>'
		
	return text

def genImageElement(imageHref,preserveAspectRatio,width,height,x,y):
	"""Create an image svg element
	
	Keyword arguments:
	imageHref -- http location of image
	preserveAspectRatio -- true or false
	width -- width in percent or absolute
	height -- height in percent or absolute
	x -- x location within view box
	y -- y location within view box
	"""

	imageLink = genHTMLElement('image',['href','width','height','preserveAspectRatio'],[imageHref,'100%','100%',preserveAspectRatio])
	imageSVG = genHTMLElement('svg',['width','height','x','y'],[width,height,x,y],imageLink)
	imageElement = imageSVG
	return imageElement
	
	
	
	