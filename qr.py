#!/usr/bin/python2
import qrencode
import pygame

class QRImage:
	def __init__(self,stringValue):
		self.image = qrencode.encode(stringValue)[2]
		self.image.save('qr.png')
	def prepare(self):
		self.image_surface = pygame.image.load('qr.png')
		self.image_surface = pygame.transform.scale(self.image_surface,(100,100))
	def draw (self,screen):
		border = pygame.Surface((110,110))
		border.fill([255,255,255])
		screen.blit(border,(screen.get_width()-100-10,screen.get_height()-100-10))
		screen.blit(self.image_surface,(screen.get_width()-100-5,screen.get_height()-100-5))
		

