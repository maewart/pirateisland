#!/usr/bin/env python3
from nose.tools import assert_equals, assert_raises
import pirate as pp

class TestHTML:
	def test_noElement(self):
		""" Test HTML element creation with no inner element value """
		elementName = 'xyz'
		paramNames = ['A','B','C']
		paramValues = ['a','b','c']
		text = pp.genHTMLElement(elementName,paramNames,paramValues)
		expectedResult = '<xyz A="a" B="b" C="c"/>\n'
		assert_equals(text,expectedResult)
		
	def test_withElement(self):
		""" Test HTML element creation with element value """
		elementName = 'xyz'
		paramNames = ['A','B','C']
		paramValues = ['a','b','c']
		elementValue = 'Easy as ABC'
		text = pp.genHTMLElement(elementName,paramNames,paramValues,elementValue)
		expectedResult = '<xyz A="a" B="b" C="c">\nEasy as ABC</xyz>\n'
		assert_equals(text,expectedResult)
	
	def test_failsDiffLengths(self):
		""" Test different length exception gets thrown """
		elementName = 'xyz'
		paramNames = ['A','B','C']
		paramValues = ['a','b']
		elementValue = 'Easy as ABC'
		assert_raises(AssertionError,pp.genHTMLElement,elementName,paramNames,paramValues,elementValue)

	def test_embed(self):
		""" Test embedding element within element works """
		elementName = 'xyz'
		paramNames = ['A','B','C']
		paramValues = ['a','b','c']
		elementValue = pp.genHTMLElement(elementName,paramNames,paramValues)
		text = pp.genHTMLElement(elementName,paramNames,paramValues,elementValue)
		expectedResult = '<xyz A="a" B="b" C="c">\n<xyz A="a" B="b" C="c"/>\n</xyz>\n'
		assert_equals(text,expectedResult)
		
		
class TestDatabase:
	def test_dbOpen(self):
		""" Test can connect to db """
		db = pp.Database()
		db.openConnection()
		
	def test_dbCloseWhenOpen(self):
		""" Test can close an open connection """
		db = pp.Database()
		db.openConnection()
		db.closeConnection()
		
	def test_dbCloseWhenNotOpen(self):
		""" Test throws error if connection not open """
		db = pp.Database()
		assert_raises(AssertionError,db.closeConnection)


class TestValidate:
	def test_boundMaxX(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(1,7.5,7.5,11.5,7.5)
		expected = [2.5,'crash',-2]
		db.closeConnection()
		assert_equals(output,expected)
		
	def test_boundMaxY(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,7.2,11.3,7.2,25.1)
		expected = [3.7,'crash',-2]
		db.closeConnection()
		assert_equals(output,expected)		
		
	def test_boundZeroX(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,3.5,2.5,-0.05,2.5)
		expected = [3.5,'crash',-2]
		db.closeConnection()
		assert_equals(output,expected)
		
	def test_boundZeroY(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,3.5,2.5,3.5,-37)
		expected = [2.5,'crash',-2]
		db.closeConnection()
		assert_equals(output,expected)

	def test_End(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(1,8.5,5.5,8.5,9.5)
		expected = [2.5,'end',5]
		db.closeConnection()
		assert_equals(output,expected)	
		
	def test_EndBeyondBound(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(1,8.5,5.5,8.5,11.5)
		expected = [2.5,'end',5]
		db.closeConnection()
		assert_equals(output,expected)

				
	def test_Icon(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,2.5,0.5,2.5,14)
		expected = [3.5,'crash',6]
		db.closeConnection()
		assert_equals(output,expected)
	
	def test_Island(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,2.5,3.5,46,3.5)
		expected = [9.4,'crash',9]
		db.closeConnection()
		assert_equals(output,expected)	
	
	def test_Island2(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,14.5,5.5,0.5,5.5)
		expected = [1.4,'crash',9]
		db.closeConnection()
		assert_equals(output,expected)
		
	def test_Island3(self):
		db = pp.Database()
		db.openConnection()
		output = db.validatePath(2,14.5,6.5,0.5,6.5)
		expected = [4.5,'crash',8]
		db.closeConnection()
		assert_equals(output,expected)		
		
