#!/usr/bin/env python3

__all__ = ['genHTMLElement']

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
		text = text + '/>\n'
	else:
		text = text + '>\n' + elementValue + '</' + elementName + '>\n'
		
	return text

	
	
	