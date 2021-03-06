import pygame
import subprocess
import shlex
import os
import fonts

class MenuEntry:
	def __init__(self,max_x,max_y):
		self.init_data(max_x,max_y)

	def init_data(self,max_x,max_y):
		self.data = []
		self.positions = []
		self.count = 0
		self.x = 0
		self.y = 1
		self.max_x = max_x
		self.max_y = max_y
		self.page=1
		self.max_page=1
		self.id=0
		self.scale_factor=0.8
		self.menu_img = pygame.image.load("resources/images/menuItem.png")
		self.menu_img_selected = pygame.image.load("resources/images/menuItemSelected.png")
		
	def add(self,title,cmd,icon):
		if (self.x == self.max_x):
			self.x = 1
			if (self.y < self.max_y):
				self.y += 1
			else:
				self.page+=1
				self.y=1
				self.max_page=self.page
		else:
			self.x +=1
		if(os.path.exists(icon)):
			use_icon=True
			img = pygame.image.load(icon)
			if (img.get_width() > self.scale_factor*self.menu_size_x):
				new_height = int(img.get_height()*self.scale_factor*(float(self.menu_size_x)/float(img.get_width())))
				new_width = int(self.scale_factor*self.menu_size_x)
				img = pygame.transform.scale(img,(new_width,new_height))
			if (img.get_height() > self.scale_factor*self.menu_size_y):
				new_width = int(img.get_width()*self.scale_factor*(float(self.menu_size_y)/float(img.get_height())))
				new_height = int(self.scale_factor*self.menu_size_y)
				img = pygame.transform.scale(img,(new_width,new_height))
		else:
			img=img = pygame.Surface((1,1))
			use_icon=False
		self.data.append([self.id,title,cmd,img,use_icon])
		self.positions.append([self.x,self.y,self.page])
		if (self.count==0):
			self.active_x=1
			self.active_y=1
		self.count += 1
		self.id+=1
		#print self.data
		#print self.positions

	def clear(self):
		print "Clearing menu entries"
		if self.id == 0:
			return
		else:
			self.init_data(self.max_x,self.max_y)
			self.active_x=1
			self.active_y=1
			self.settings(self.borders,self.gap_x,self.gap_y,self.menu_size_x,self.menu_size_y)
		
		
	def defined(self):
		self.page=1
	
	def get_id(self,i):
		return self.data[i][0]
	
	def get_y(self,i):
		return self.data[i][1]
	
	def get_title(self,i):
		return self.data[i][2]
	
	def get_cmd(self,i):
		return self.data[i][3]
	
	def settings(self,borders,gap_x,gap_y,menu_size_x,menu_size_y):
		print "Menu entries have settings"
		self.borders = borders
		self.gap_x = gap_x
		self.gap_y = gap_y
		self.menu_size_x = menu_size_x
		self.menu_size_y = menu_size_y
		self.menu_img = pygame.transform.scale(self.menu_img,(self.menu_size_x,self.menu_size_y))
		self.menu_img_selected = pygame.transform.scale(self.menu_img_selected,(self.menu_size_x,self.menu_size_y))
	
	def draw(self,screen):
		#print str(self.active_x)
		for item in self.data:
			itemid = item[0]
			if self.positions[itemid][2] == self.page:
				x = self.positions[itemid][0]
				y = self.positions[itemid][1]
				start_x = self.borders + (x-1)*self.menu_size_x + (x-1)*self.gap_x
				start_y = self.borders + (y-1)*self.menu_size_y + (y-1)*self.gap_y
				screen.blit(self.menu_img,(start_x,start_y))
				if (x==self.active_x and y==self.active_y):
					screen.blit(self.menu_img_selected,(start_x,start_y))
				use_icon = item[4]
				icon = item[3]
				if (use_icon):
					ico_start_x = 0.5*(self.menu_size_x-icon.get_width())+start_x
					ico_start_y = 0.5*(self.menu_size_y-icon.get_height())+start_y
					screen.blit(icon,(ico_start_x,ico_start_y))
				title=item[1]
				font = pygame.font.Font(None, 20)
				text = fonts.textOutline(font,title,[10,10,10],[255,255,255])
				#text = font.render(title, True, [0,0,0])
				textRect = text.get_rect()
				textRect.x = start_x + 0.5*(self.menu_size_x-textRect.width)
				textRect.y = start_y + self.menu_size_y - 1.5*textRect.height
				screen.blit(text, textRect)

				
	def move_left(self):
		if (self.positions.count([self.active_x-1,self.active_y,self.page])>0):
			self.active_x-=1
	def move_right(self):
		if (self.positions.count([self.active_x+1,self.active_y,self.page])>0):
			self.active_x+=1
	def move_down(self):
		if (self.positions.count([self.active_x,self.active_y+1,self.page])>0):
			self.active_y+=1
	def move_up(self):
		if (self.positions.count([self.active_x,self.active_y-1,self.page])>0):
			self.active_y-=1
	def prev_page(self):
		if (self.page>1):
			self.page-=1
			#If there is a previous page then it is full, don't reset position
	def next_page(self):
		if (self.page < self.max_page):
			self.page+=1
			selected_item=False
			while (not selected_item):
				if (self.positions.count([self.active_x,self.active_y,self.page])==0):
					#Then currently highlightling a dead zone!!!
					if(self.active_x==1):
						self.active_x=self.max_x
						if(self.active_y==1):
							print "Blank Page?"
						else:
							self.active_y-=1
					else:
						self.active_x-=1
				else:
					selected_item=True
				
			

	def launch(self):
		pygame.display.toggle_fullscreen()
		command = str(self.data[self.positions.index([self.active_x,self.active_y,self.page])][2])
		cmds = shlex.split(command)
		self.process = subprocess.Popen(cmds,stdin=subprocess.PIPE)

	def stop(self):
		self.process.terminate()
		pygame.display.toggle_fullscreen()
		
	def wait(self):
		self.process.wait()
		pygame.display.toggle_fullscreen()

			
