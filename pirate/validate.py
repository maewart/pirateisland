#!/usr/bin/env python3

import sys
import json
import cgi

import pirate as pLib

""" Entry to the move validation
This instance creates a MoveValidation to evaluate the users moves and send back an instruction for the animation
"""

#Get parameters submitted
inp = cgi.FieldStorage()

#Write JSON header
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

#Perform validation
validation = pLib.MoveValidation(inp)
validation.validate()

#Write out results
sys.stdout.write(str(validation))
sys.stdout.write("\n")

#Close write connection
sys.stdout.close()
