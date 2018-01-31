#!/usr/bin/env python3

__all__ = ['genCSSElement']

def genCSSElement(className,paramNames,paramValues,):
	"""Function to generate a CSS element of the form
	.st0{fill:#C62405;}
	.st1{fill:#5B5959;}
	.logo {
		display: block;
		height: 50px;
		width: 52px;
		padding-top: 0px;
		margin-right: 20px;
	}
		
	Keyword arguments:
	ClassName -- Class Name. e.g. logo
	paramNames -- List of params e.g. fill, display,height, etc.
	paramValues -- List of values for params e.g. block, #C62405, etc.
	"""
	
	#param names and values must be same length
	assert len(paramNames) == len(paramValues)
	
	#Start of element
	text='.' + className + '{'
	
	#Iterate through list and add params
	for i in range(0, len(paramNames)):
		text = text + ' ' + str(paramNames[i]) + ':' + str(paramValues[i]) + ';'
		
	#Add element value if not empty
	text = text + '}'
		
	return text

	
	
	