#!/usr/bin/env python
#
# Quick usage of "launchpad.py", LEDs and buttons.
# Works with all Launchpads: Mk1, Mk2, S/Mini, Pro, XL and LaunchKey
# 
#
# FMMT666(ASkr) 7/2013..2/2020
# www.askrprojects.net
#

import sys

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad.py")

import random
from pygame import time


def main():

	mode = None

	# create an instance
	lp = launchpad.Launchpad()

	# check what we have here and override lp if necessary
	if lp.Check( 0, "Open" ):
		lp = launchpad.LaunchpadPro()
		if lp.Open(0,"Open"):
			print("Launchpad Pro")
			mode = "Pro"

	# experimental MK3 implementation
	# The MK3 has two MIDI instances per device; we need the 2nd one.
	# If you have two MK3s attached, its "1" for the first and "3" for the 2nd device
	elif lp.Check( 1, "mk3" ):
		lp = launchpad.LaunchpadMk3()
		if lp.Open( 1, "mk3" ):
			print("Launchpad Mk3")
			mode = "Pro"

	# experimental LPX implementation
	# Like the Mk3, the LPX also has two MIDI instances per device; we need the 2nd one.
	# If you have two LPXs attached, its "1" for the first and "3" for the 2nd device
	elif lp.Check( 1, "lpx" ):
		lp = launchpad.LaunchpadLPX()
		if lp.Open( 1, "lpx" ):
			print("Launchpad X")
			mode = "Pro"
			
	elif lp.Check( 0, "mk2" ):
		lp = launchpad.LaunchpadMk2()
		if lp.Open( 0, "mk2" ):
			print("Launchpad Mk2")
			mode = "Mk2"

	elif lp.Check( 0, "control xl" ):
		lp = launchpad.LaunchControlXL()
		if lp.Open( 0, "control xl" ):
			print("Launch Control XL")
			mode = "XL"
			
	elif lp.Check( 0, "launchkey" ):
		lp = launchpad.LaunchKeyMini()
		if lp.Open( 0, "launchkey" ):
			print("LaunchKey (Mini)")
			mode = "LKM"

	elif lp.Check( 0, "dicer" ):
		lp = launchpad.Dicer()
		if lp.Open( 0, "dicer" ):
			print("Dicer")
			mode = "Dcr"
			
	else:
		if lp.Open():
			print("Launchpad Mk1/S/Mini")
			mode = "Mk1"

	if mode is None:
		print("Did not find any Launchpads, meh...")
		return


	# scroll "HELLO" from right to left
	if mode == "Mk1":
		lp.LedCtrlString( "h ", 0, 3, -1 )
	# for all others except the XL and the LaunchKey
	elif mode != "XL" and mode != "LKM" and mode != "Dcr":
		lp.LedCtrlString( "HELLO!", 63, 63, 63, -1, 10 )

	lp.Reset() # turn all LEDs off
	lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)

	
if __name__ == '__main__':
	main()

