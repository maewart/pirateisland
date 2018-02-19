#!/usr/bin/env python3

import sys
import json
import cgi
import cgitb

import pirate as pLib

cgitb.enable(format='text')

""" Entry to the high score code
This instance creates a HighScore instance to add the score to the database
"""

#Get parameters submitted
inp = cgi.FieldStorage()

#Write JSON header
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

#Add high score
leaderboard = pLib.HighScore(inp)
leaderboard.addHighScore()

#Return leaderboard position
sys.stdout.write(str(leaderboard))
sys.stdout.write("\n")

#Close connection
sys.stdout.close()
