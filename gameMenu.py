#!/usr/bin/python2
import joystick
import pygame
import csv
import menuEntry
import time
import os
import pyinotify
import menuChanged
import netutils
import qr
import fonts
from pygame.locals import *

class GameMenu():
	def __init__(self):
		print "Starting Menu"
		self.fail=False
		self.joy=joystick.Joystick()
		if (self.joy.errors!=[]):
			for error in self.joy.errors:
				print error
				self.use_joystick=False
		else:
			self.use_joystick=True
			
		self.get_settings()
		self.menuEntries = menuEntry.MenuEntry(self.num_entries_x,self.num_entries_y)
		self.menuEntries.settings(self.borders,self.gap_x,self.gap_y,self.menu_size_x,self.menu_size_y)
		self.readMenuFile()
		self.menuOutOfDate=False
		self.menuEntries.defined()
		if (self.use_sound):
			self.setupSounds()
		#TODO make more robust - not uploading a backgorund
		if (os.path.exists(self.image_dir+"/background.jpg")):
			self.background = pygame.image.load("resources/images/background.jpg")
			self.background = pygame.transform.scale(self.background,(self.screen_size_x,self.screen_size_y))
			self.use_background=True
		else:
			self.use_background = False
		self.init_filewatcher()
		iptool = netutils.ip_tool()
		self.ip = iptool.get_ip()
		print "Detected IP as", self.ip
		self.qrip = qr.QRImage('http://'+self.ip)
		self.qrip.prepare()
		pygame.init()
		font = pygame.font.Font(None, 20)
		self.iptext = fonts.textOutline(font,"To configure games go to "+self.ip+" or use the QR code.",[10,10,10],[255,255,255])

		
		# Set the height and width of the screen
		size=[self.screen_size_x,self.screen_size_y]
		#self.screen=pygame.display.set_mode(size,pygame.NOFRAME)
		self.screen=pygame.display.set_mode(size,pygame.FULLSCREEN|pygame.NOFRAME)
		pygame.display.set_caption("GameMenu")
		# Used to manage how fast the screen updates
		self.clock=pygame.time.Clock()
		
	def get_settings(self):
		#Replace with reading settings file
		print "Using Default Settings"
		self.use_sound = True
		self.sound_dir = "resources/sounds"
		self.image_dir = "resources/images"
		self.screen_size_x = 1024
		self.screen_size_y = 600
		#self.screen_size_x = 640
		#self.screen_size_y = 480
		#self.screen_size_x = 1920
		#self.screen_size_y = 1080
		
		self.frames_per_second = 5
		self.tick = 1.0 / self.frames_per_second
		
		self.num_entries_x = 4
		self.num_entries_y = 3
		self.num_pages = 2
		self.menuFile = '/srv/gameEditor/gameMenu.csv'
		
		#Gap between menu entries
		self.gap_x = 20
		self.gap_y = 20
		
		self.borders = 100
		#self.border_top = 50
		#self.border_bottom = 50
		#self.border_left = 50
		#self.border_right = 50
		
		#Calculate the size of each menu item
		self.menu_size_x = ( self.screen_size_x - self.gap_x * (self.num_entries_x - 1) - 2*self.borders ) / self.num_entries_x
		self.menu_size_y = ( self.screen_size_y - self.gap_y * (self.num_entries_y - 1) - 2*self.borders ) / self.num_entries_y
		
		self.terminate=False
		
		
	def start(self):
		if (self.fail==True):
			print "Failed to start"
			return
		loop=True
		while (loop):
			if (self.menuOutOfDate==True):
				self.rereadMenuFile()
			self.draw()
			time.sleep(self.tick)
			if (self.use_joystick == True):
				joy_input = self.joy.get_input()
			else:
				#Want to use Keyboard instead.
				self.keyboard_loop()
				continue
			if (joy_input[1]==1):
				if (self.use_sound):
					self.sounds["exit"].play()
					time.sleep(0.5)
				loop=False
			if (joy_input[0]==1):
				if (self.use_sound):
					self.sounds["select"].play()
				self.launch()
			if (joy_input[5]<-0.5):
				self.menuEntries.move_left()
				if (self.use_sound):
					self.sounds["move"].play()
			if (joy_input[5]>0.5):
				self.menuEntries.move_right()
				if (self.use_sound):
					self.sounds["move"].play()
			if (joy_input[6]<-0.5):
				self.menuEntries.move_up()
				if (self.use_sound):
					self.sounds["move"].play()
			if (joy_input[6]>0.5):
				self.menuEntries.move_down()
				if (self.use_sound):
					self.sounds["move"].play()
			if (joy_input[2]==1):
				self.menuEntries.prev_page()
				if (self.use_sound):
					self.sounds["move"].play()
			if (joy_input[3]==1):
				self.menuEntries.next_page()
				if (self.use_sound):
					self.sounds["move"].play()
		self.quit()
			

	def quit(self):
		self.watcher.kill()
		exit()
			
				
	def launch(self):
		self.menuEntries.launch()
		if (self.terminate==False):
			self.menuEntries.wait()
		else:
			loop=True
			while (loop):
				x=pygame.key.get_pressed()
				print(type(x))
				if ( self.joy.get_input()[4]):
					self.menuEntries.stop()
					loop=False
				time.sleep(self.tick)
		if (self.use_sound):
			self.sounds["exit"].play()
		pygame.event.clear()
		time.sleep(1)
		
	def __run__(self):
		self.menuEntries.launch()
		
	def readMenuFile(self):
		menuFile=open(self.menuFile)
		csvreader = csv.reader(menuFile)
		for line in csvreader:
			self.menuEntries.add(line[0],line[1],line[2])

	def draw(self):
		#Draw Background
		if (self.use_background==True):
			self.screen.blit(self.background,(0,0))
		self.menuEntries.draw(self.screen)
		self.qrip.draw(self.screen)
		self.screen.blit(self.iptext,(((self.screen.get_width()-self.iptext.get_width())*.5),self.screen.get_height()-self.iptext.get_height()))
		pygame.display.flip()
		
	def setupSounds(self):
		self.sounds = dict()
		
		if (os.path.exists(self.sound_dir+"/move.ogg") and os.path.exists(self.sound_dir+"/select.ogg") and os.path.exists(self.sound_dir+"/exit.ogg")):
			pygame.mixer.init(frequency=22050, size=8, channels=2, buffer=65000)
			self.sounds["move"] = pygame.mixer.Sound("resources/sounds/move.ogg")
			self.sounds["select"] = pygame.mixer.Sound("resources/sounds/select.ogg")
			self.sounds["exit"] = pygame.mixer.Sound("resources/sounds/exit.ogg")
			self.sounds["select"].play()
		else:
			print "Could not find sound files: move.ogg select.ogg exit.ogg"
			print "To enable sound, add them to resources/sounds/"
			self.use_sound = False

		
	def keyboard_loop(self):
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				if (self.use_sound):
					self.sounds["exit"].play()
					time.sleep(0.5)
				self.quit()
			if event.type == KEYDOWN and event.key == K_RETURN:
				if (self.use_sound):
					self.sounds["select"].play()
				self.launch()
			if event.type == KEYDOWN and event.key == K_LEFT:
				self.menuEntries.move_left()
				if (self.use_sound):
					self.sounds["move"].play()
			if event.type == KEYDOWN and event.key == K_RIGHT:
				self.menuEntries.move_right()
				if (self.use_sound):
					self.sounds["move"].play()
			if event.type == KEYDOWN and event.key == K_UP:
				self.menuEntries.move_up()
				if (self.use_sound):
					self.sounds["move"].play()
			if event.type == KEYDOWN and event.key == K_DOWN:
				self.menuEntries.move_down()
				if (self.use_sound):
					self.sounds["move"].play()
			if event.type == KEYDOWN and event.key == K_PAGEDOWN:
				self.menuEntries.prev_page()
				if (self.use_sound):
					self.sounds["move"].play()
			if event.type == KEYDOWN and event.key == K_PAGEUP:
				self.menuEntries.next_page()
				if (self.use_sound):
					self.sounds["move"].play()
	def rereadMenuFile(self):
		self.menuEntries = menuEntry.MenuEntry(self.num_entries_x,self.num_entries_y)
		self.menuEntries.settings(self.borders,self.gap_x,self.gap_y,self.menu_size_x,self.menu_size_y)
		self.readMenuFile()
		self.menuOutOfDate=False
		#self.menuEntries.clear()
		#self.readMenuFile()

	def rereadNextDraw(self):
		self.menuOutOfDate=True
		
	def init_filewatcher(self):
		self.watcher=menuChanged.EventManager(self.menuFile,self.rereadNextDraw)

if __name__=="__main__":
	gm = GameMenu()
	gm.start()

