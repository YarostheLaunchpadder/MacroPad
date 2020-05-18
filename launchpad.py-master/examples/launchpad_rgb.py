#!/usr/bin/env python
#
# Launchpad tests for RGB-style variants Mk2, Mk3, Pro ...
# 
#
# FMMT666(ASkr) 7/2013..2/2020
# www.askrprojects.net
#

import sys
import launchpad_py as launchpad
import random
import pygame
from pygame import time


def main():

	# create an instance
	lp = launchpad.Launchpad();

	# try the first Mk2
	if lp.Check( 0, "mk2" ):
		lp = launchpad.LaunchpadMk2()
		if lp.Open( 0, "mk2" ):
			print( " - Launchpad Mk2: OK" )
		else:
			print( " - Launchpad Mk2: ERROR")
			return
		
	# try the first Mk3
	elif lp.Check( 1, "mk3" ):
		lp = launchpad.LaunchpadMk3()
		if lp.Open( 1, "mk3" ):
			print( " - Launchpad Mk3: OK" )
		else:
			print( " - Launchpad Mk3: ERROR")
			return

	# try the first Pro
	elif lp.Check( 0, "pro" ):
		lp = launchpad.LaunchpadPro()
		if lp.Open( 0, "pro" ):
			print( " - Launchpad Pro: OK" )
		else:
			print( " - Launchpad Pro: ERROR")
			return
		
	else:
		print( " - No Launchpad available" )
		return


	lp.ButtonFlush()

	for i in [ 5, 21, 79, 3]:
		lp.LedAllOn( i )
		time.wait(500)
	lp.LedAllOn( 0 )

	colors = [ [63,0,0],[0,63,0],[0,0,63],[63,63,0],[63,0,63],[0,63,63],[63,63,63] ]
	for i in range(4):
		for y in range( i + 1, 8 - i + 1 ):
			for x in range( i, 8 - i ):
				lp.LedCtrlXY( x, y, colors[i][0], colors[i][1], colors[i][2])
		time.wait(500)

	# turn all LEDs off
	lp.Reset()

	# close this instance
	lp.Close()

main()

