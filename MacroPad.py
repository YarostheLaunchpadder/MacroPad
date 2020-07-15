# Version 1
import sys
import contextlib
import ctypes
import time
import os
from PIL import ImageTk, Image
from tkinter import *
#from tkinter.ttk import Button, Frame, Style
import webbrowser
from PIL import ImageTk, Image

with contextlib.redirect_stdout(None): # Makes no pygame prompt appear
    import launchpad_py as launchpad

# THEME MANUAL SELECTION ----------------- white, #2d2d2d
backgound = '#2d2d2d'
foreground = 'white'

menuwindow = Tk() # create a Window
menuwindow.iconbitmap("ui/logo/logo_small.ico")
menuwindow.title("MacroPad")
menuwindow.resizable(width=False, height=False)
menuwindow.configure(bg=backgound)


window_height = 400
window_width = 500

screen_width = menuwindow.winfo_screenwidth()
screen_height = menuwindow.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

menuwindow.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# C struct redefinitions
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#Keyboard functions for in-game drivers

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def setup():
	global lp
	# create launchpad instance
	lp = launchpad.Launchpad()
	global mode
	# Launchpad model set to none before scanning, to recognize the launchpad
	mode = None

	# try the first Mk2
	if lp.Check( 0, "mk2" ):
		lp = launchpad.LaunchpadMk2()
		if lp.Open( 0, "mk2" ):
			mode = "Mk2"

			
		else:
			pass

	# try the first Pro
	elif lp.Check( 0, "Pro" ):
		lp = launchpad.LaunchpadPro()
		if lp.Open( 0, "Pro" ):
			mode = "Pro"
			
		else:
			pass

	# try the pro with cfw
	elif lp.Check( 1, "Open" ):
		lp = launchpad.LaunchpadPro()
		if lp.Open(1,"Open"):
			mode = "Pro"

	# experimental LPX implementation
	elif lp.Check( 1, "lpx" ):
		lp = launchpad.LaunchpadLPX()
		if lp.Open( 1, "lpx" ):
			mode = "X"

	else:
		pass



def clear():
	lp.Reset()
	sys.exit()

def gamelights(): # Launchpad Lights

	lp.Reset() # Clears stuck lights on Launchpad
	# LEDS Assign
	lp.LedCtrlXYByCode(3, 4, 13) # S
	lp.LedCtrlXYByCode(3, 3, 13) # W
	lp.LedCtrlXYByCode(2, 4, 13) # A
	lp.LedCtrlXYByCode(4, 4, 13) # D
	lp.LedCtrlXYByCode(1, 5, 57) # Ctrl
	lp.LedCtrlXYByCode(1, 4, 58) # Shift
	lp.LedCtrlXYByCode(2, 6, 37) # Spacebar
	lp.LedCtrlXYByCode(3, 6, 37) # Spacebar
	lp.LedCtrlXYByCode(4, 6, 37) # Spacebar
	lp.LedCtrlXYByCode(5, 6, 37) # Spacebar
	lp.LedCtrlXYByCode(2, 3, 9) # Q
	lp.LedCtrlXYByCode(1, 3, 45) # Tab
	lp.LedCtrlXYByCode(4, 3, 22) # E
	lp.LedCtrlXYByCode(5, 3, 19) # R
	lp.LedCtrlXYByCode(5, 4, 22)# F
	lp.LedCtrlXYByCode(7, 3, 41)# I
	lp.LedCtrlXYByCode(5, 8, 49) # Left Arrow
	lp.LedCtrlXYByCode(6, 8, 49) # Down Arrow
	lp.LedCtrlXYByCode(7, 8, 49) # Right Arrow
	lp.LedCtrlXYByCode(6, 7, 49) # Up Arrow
	lp.LedCtrlXYByCode(0, 1, 5) # Esc
	lp.LedCtrlXYByCode(0, 4, 1) # Alt + Tab

def obslights():
	lp.Reset() # Clears stuck lights on Launchpad
	# LEDS Assign
	lp.LedCtrlXYByCode(0, 1, 17) # Shift + 1
	lp.LedCtrlXYByCode(0, 2, 37) # Shift + 2
	lp.LedCtrlXYByCode(0, 3, 45) # Shift + 3
	lp.LedCtrlXYByCode(0, 4, 49) # Shift + 4
	lp.LedCtrlXYByCode(0, 5, 53) # Shift + 5
	lp.LedCtrlXYByCode(0, 6, 13) # Shift + 6
	lp.LedCtrlXYByCode(0, 7, 5) # Shift + 7
	lp.LedCtrlXYByCode(0, 8, 9) # Shift + 8
	lp.LedCtrlXYByCode(7, 7, 1) # Ctrl + Shift + F8
	lp.LedCtrlXYByCode(7, 8, 3) # Ctrl + Shift + F9
	lp.LedCtrlXYByCode(7, 1, 21) # Alt + Tab

	#time.sleep(1)
	#lp.Reset()



def gamescontroller(): # Launchpad games input
	
	if mode == 'Mk2':
		mk2_game = ImageTk.PhotoImage(Image.open("launchpads/layouts/mk2_game.png"))
		Label(menuwindow, image=mk2_game, bg=backgound).place(x=10, y=45)

	elif mode == 'Pro':
		pro_game = ImageTk.PhotoImage(Image.open("launchpads/layouts/pro_game.png"))
		Label(menuwindow, image=pro_game, bg=backgound).place(x=10, y=45)

	elif mode == 'X':
		x_game = ImageTk.PhotoImage(Image.open("launchpads/layouts/x_game.png"))
		Label(menuwindow, image=x_game, bg=backgound).place(x=10, y=45)

	def ButtonGet(): # scan the buttons
		return lp.ButtonStateXY() 
		return []

	while True: # Main loop
		buts=ButtonGet() # see what buttons are pressed
		if buts != []: # if any button is pressed
		# Button triggers
			if buts == [3, 3, 127]: # W Pressed
				PressKey(0x11)


			elif buts == [3, 3, 0]: # W Released
				ReleaseKey(0x11)
			
			
			elif buts == [3, 4, 127]: # S Pressed
				PressKey(0x1F)

			elif buts == [3, 4, 0]: # S Released
				ReleaseKey(0x1F)

			elif buts == [2, 4, 127]: # A Pressed
				PressKey(0x1E)

			elif buts == [2, 4, 0]: # A Released
				ReleaseKey(0x1E)

			elif buts == [4, 4, 127]: # D Pressed
				PressKey(0x20)

			elif buts == [4, 4, 0]: # D Released
				ReleaseKey(0x20)

			elif buts == [1, 5, 127]: # Ctrl Pressed
				PressKey(0x1D)

			elif buts == [1, 5, 0]: # Ctrl Released
				ReleaseKey(0x1D)

			elif buts == [1, 4, 127]: # Shift Pressed
				PressKey(0x2A)

			elif buts == [1, 4, 0]: # Shift Released
				ReleaseKey(0x2A)

			elif buts == [2, 6, 127]: # Spacebar 1 pressed
				PressKey(0x39)

			elif buts == [2, 6, 0]: # Spacebar 1 Released
				ReleaseKey(0x39)

			elif buts == [3, 6, 127]: # Spacebar 2 pressed
				PressKey(0x39)

			elif buts == [3, 6, 0]: # Spacebar 2 Released
				ReleaseKey(0x39)

			elif buts == [4, 6, 127]: # Spacebar 3 pressed
				PressKey(0x39)

			elif buts == [4, 6, 0]: # Spacebar 3 Released
				ReleaseKey(0x39)

			elif buts == [5, 6, 127]: # Spacebar 4 pressed
				PressKey(0x39)

			elif buts == [5, 6, 0]: # Spacebar 4 Released
				ReleaseKey(0x39)

			elif buts == [2, 3, 127]: # Q Pressed
				PressKey(0x10)

			elif buts == [2, 3, 0]: # Q Released
				ReleaseKey(0x10)

			elif buts == [2, 3, 127]: # Tab Pressed
				PressKey(0x0F)

			elif buts == [2, 3, 0]: # Tab Released
				ReleaseKey(0x0F)

			elif buts == [4, 3, 127]: # E Pressed
				PressKey(0x12)

			elif buts == [4, 3, 0]: # E Released
				ReleaseKey(0x12)

			elif buts == [5, 3, 127]: # R Pressed
				PressKey(0x13)

			elif buts == [5, 3, 0]: # R Released
				ReleaseKey(0x13)

			elif buts == [5, 4, 127]: # F Pressed
				PressKey(0x21)

			elif buts == [5, 4, 0]: # F Released
				ReleaseKey(0x21)

			elif buts == [7, 3, 127]: # I Pressed
				PressKey(0x17)

			elif buts == [7, 3, 0]: # I Released
				ReleaseKey(0x17)

			elif buts == [5, 8, 127]: # Left Arrow Pressed
				PressKey(0xCB)

			elif buts == [5, 8, 0]: # Left Arrow Released
				ReleaseKey(0xCB)

			elif buts == [6, 8, 127]: # Down Arrow Pressed
				PressKey(0xD0)

			elif buts == [6, 8, 0]: # Down Arrow Released
				ReleaseKey(0xD0)

			elif buts == [7, 8, 127]: # Right Arrow Pressed
				PressKey(0xCD)

			elif buts == [7, 8, 0]: # Right Arrow Released
				ReleaseKey(0xCD)

			elif buts == [6, 7, 127]: # Up Arrow Pressed
				PressKey(0xC8)

			elif buts == [6, 7, 0]: # Up Arrow Released
				ReleaseKey(0xC8)

			elif buts == [0, 1, 127]: # Esc Arrow Pressed
				PressKey(0x01)

			elif buts == [0, 1, 0]: # Esc Arrow Released
				ReleaseKey(0x01)

			elif buts == [0, 4, 127]: # Single Alt + Tab click
				os.startfile("alt+tab.exe")

			elif buts == [8, 2, 127]: # OBS Controller Page Pressed
				obslights()
				obscontroller()

			elif buts == [0, 0, 127]:
				clear()
		menuwindow.update()
		time.sleep(0.07) # wait 70 milliseconds every time it scans to reduce cpu usage over 60%


def obscontroller(): # Launchpad games input
	
	if mode == 'Mk2':
		mk2_obs = ImageTk.PhotoImage(Image.open("launchpads/layouts/mk2_obs.png"))
		Label(menuwindow, image=mk2_obs, bg=backgound).place(x=10, y=45)

	elif mode == 'Pro':
		pro_obs = ImageTk.PhotoImage(Image.open("launchpads/layouts/pro_obs.png"))
		Label(menuwindow, image=pro_obs, bg=backgound).place(x=10, y=45)

	elif mode == 'X':
		x_obs = ImageTk.PhotoImage(Image.open("launchpads/layouts/x_obs.png"))
		Label(menuwindow, image=x_obs, bg=backgound).place(x=10, y=45)

	def ButtonGet(): # scan the buttons
		return lp.ButtonStateXY() 
		return []

	while True: # Main loop
		buts=ButtonGet() # see what buttons are pressed
		if buts != []: # if any button is pressed
		# Button triggers
			if buts == [0, 1, 127]: # Press and release Shift + 1
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x02)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x02)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 2, 127]: # Press and release Ctrl + Shift + 2
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x03)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x03)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 3, 127]: # Press and release Ctrl + Shift + 3
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x04)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x04)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 4, 127]: # Press and release Ctrl + Shift + 4
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x05)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				time.sleep(0.09)
				ReleaseKey(0x05)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 5, 127]: # Press and release Ctrl + Shift + 5
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x06)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x06)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 6, 127]: # Press and release Ctrl + Shift + 6
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x07)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x07)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 7, 127]: # Press and release Ctrl + Shift + 7
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x08)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x08)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [7, 7, 127]: # Press and release Ctrl + Shift + 8
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x09)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x09)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [7, 8, 127]: # Press and release Ctrl + Shift + F8
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x42)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x42)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [0, 8, 127]: # Press and release Ctrl + Shift + F9
				PressKey(0x1D)
				time.sleep(0.09)
				PressKey(0x2A)
				time.sleep(0.09)
				PressKey(0x43)
				time.sleep(0.09)
				ReleaseKey(0x2A)
				time.sleep(0.09)
				ReleaseKey(0x43)
				time.sleep(0.09)
				ReleaseKey(0x1D)

			elif buts == [7, 1, 127]: # Single Alt + Tab click
				os.startfile("alt+tab.exe")

			elif buts == [8, 1, 127]: # Games Controller Page Pressed
				gamelights()
				gamescontroller()

			elif buts == [0, 0, 127]:
					clear()
		menuwindow.update()
		time.sleep(0.07) # wait 70 milliseconds every time it scans to reduce cpu usage over 60%

# Updates the gui and waits for a launchpad page to be selected
def menu():
	def ButtonGet(): # scan the buttons
		return lp.ButtonStateXY() 
		return []

	while True: # Main loop
		buts=ButtonGet() # see what buttons are pressed
		if buts != []: # if any button is pressed
			# Button triggers
			if buts == [8, 1, 127]: # Games Controller Page Pressed
				gamelights()
				gamescontroller()

			elif buts == [8, 2, 127]: # OBS Controller Page Pressed
				obslights()
				obscontroller()

			elif buts == [0, 0, 127]:
				clear()

		menuwindow.update()
		time.sleep(0.07)

# Opens the window and renders stuff
def mainwindow():
	if mode == "Mk2":
		Label(menuwindow, text="Launchpad Mk2 Connected", bg=backgound, foreground=foreground, font=("Calibri", 16)).place(x=10, y=5)
		lp_mk2 = ImageTk.PhotoImage(Image.open("launchpads/lp_mk2.png"))
		mk2label = Label(menuwindow, image=lp_mk2, bg=backgound).place(x=10, y=45)
		menu()

	elif mode == "Pro":
		Label(menuwindow, text="Launchpad Pro Connected", bg=backgound, foreground=foreground, font=("Calibri", 16)).place(x=10, y=5)
		lp_pro = ImageTk.PhotoImage(Image.open("launchpads/lp_pro.png"))
		prolabel = Label(menuwindow, image=lp_pro, bg=backgound).place(x=10, y=45)
		logo = ImageTk.PhotoImage(Image.open("ui/logo/logo_small.png"))
		logolabel = Label(menuwindow, image=logo, bg=backgound).place(x=460, y=5)
		menu()

	elif mode == "X":
		Label(menuwindow, text="Launchpad X Connected", bg=backgound, foreground=foreground, font=("Calibri", 16)).place(x=10, y=5)
		lp_pro = ImageTk.PhotoImage(Image.open("launchpads/lp_x.png"))
		nolplabel = Label(menuwindow, image=lp_x, bg=backgound).place(x=10, y=45)
		logo = ImageTk.PhotoImage(Image.open("ui/logo/logo_small.png"))
		logolabel = Label(menuwindow, image=logo, bg=backgound).place(x=460, y=5)
		menu()

	else:
		Label(menuwindow, text="No Compatible Launchpad Connected", fg=foreground, bg=backgound, font=("Segoe UI", 16), borderwidth=0).place(x=10, y=5)
		Label(menuwindow, text="Please connect your launchpad then restart the app", fg=foreground, bg=backgound, font=("Segoe UI", 10), borderwidth=0).place(x=10, y=35)
		no_lp = ImageTk.PhotoImage(Image.open("launchpads/no_lp.png"))
		prolabel = Label(menuwindow, image=no_lp, bg=backgound).place(x=10, y=60)
		logo = ImageTk.PhotoImage(Image.open("ui/logo/logo_small.png"))
		logolabel = Label(menuwindow, image=logo, bg=backgound).place(x=460, y=5)
		menuwindow.mainloop()


# list of functions that run the program
setup() # Recognizes your launchpad and changes the mode to corresponding model
mainwindow()
