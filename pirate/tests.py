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

		

#class TestGameObjects:
"""def test_mapArea(self):
		""" Check mapArea rendering works """
		ff = ffLib.DbFieldsFinds()
		ff.openConnection()
		area=ff.getMapArea('Default')
		map=area.renderMap(500,500)
		info=area.renderInfo(300,500)
		assert map[:4] == '<svg'
		assert info[:4] == '<svg'
		assert map[-6:] == '</svg>'
		assert info[-6:] == '</svg>'
		ff.closeConnection()
	
	def test_field(self):
		""" Check field rendering works """
		ff = ffLib.DbFieldsFinds()
		ff.openConnection()
		field=ff.getFields(1)[0]
		geo=field.renderGeo('xxx',20)
		info=field.renderInfo()
		assert geo[:5] == '<text'
		assert info[:4] == '<svg'
		assert geo[-7:] == '</rect>'
		assert info[-6:] == '</svg>'
		ff.closeConnection()"""
