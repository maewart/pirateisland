#!/usr/bin/env python3

import sys
import json
import cgi
import cgitb

import pirate as pLib

cgitb.enable(format='text')

""" Entry to the move validation
This instance creates a MoveValidation to evaluate the users moves and send back an instruction for
"""


inp = cgi.FieldStorage()

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

leaderboard = pLib.HighScore(inp)
leaderboard.addHighScore()
sys.stdout.write(str(leaderboard))


sys.stdout.write("\n")

sys.stdout.close()
