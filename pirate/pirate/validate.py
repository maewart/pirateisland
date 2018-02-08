#!/usr/bin/env python3

import sys
import json
import cgi
import cgitb

import pirate as pLib
#from .moveValidation import MoveValidation

cgitb.enable(format='text')

""" Entry to the move validation
This instance creates a MoveValidation to evaluate the users moves and send back an instruction for
"""


inp = cgi.FieldStorage()

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

validation = pLib.MoveValidation(inp)
validation.validate()
sys.stdout.write(str(validation))


sys.stdout.write("\n")

sys.stdout.close()
