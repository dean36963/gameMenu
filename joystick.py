#!/usr/bin/python2

import pygame.joystick

class Joystick:
	def __init__(self):
		print "Creating Joystick"
		self.errors = []
		self.init()
		self.set_buttons(0, 1, 2, 3,8)
		
	
	def init(self):
		print "Initialising joysticks"
		if(pygame.joystick.get_init()):
			print "Joystick module active - restarting"
			pygame.joystick.quit()
		pygame.joystick.init()
		
		if(pygame.joystick.get_count()==0):
			print "No Joysticks found."
			self.errors.append("No Joystick Found")
			return
		
		self.active_joystick = pygame.joystick.Joystick(0)
		print "Found joystick: " + self.active_joystick.get_name()
		self.active_joystick.init()
		self.get_joy_stats()
		
	def set_buttons(self,select_button,back_button,left_button,right_button,quit_button):
		self.select_button=select_button
		self.back_button=back_button
		self.left_button=left_button
		self.right_button=right_button
		self.quit_button=quit_button
		
	def get_input(self):
		pygame.event.pump()
		return(
				self.active_joystick.get_button(self.select_button),
				self.active_joystick.get_button(self.back_button),
				self.active_joystick.get_button(self.left_button),
				self.active_joystick.get_button(self.right_button),
				self.active_joystick.get_button(self.quit_button),
				self.active_joystick.get_axis(0),
				self.active_joystick.get_axis(1))
	
	def get_joy_stats(self):
		if (self.active_joystick.get_numaxes>=2):
			self.use_axes=True
		else:
			self.use_axes=False
		if (self.active_joystick.get_numbuttons()>=4):
			self.use_buttons=True
		else:
			self.use_buttons=False
		if (self.active_joystick.get_numhats()>=1):
			self.use_hat=True
		else:
			self.use_hat=False
		if not self.use_axes and not self.use_hat or not self.use_buttons:
			print "Unable to use this joystick"
			self.errors.append("Unable to use joystick, not enough buttons/axes")
			return 2;
		else:
			return 0
	

