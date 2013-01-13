import pygame
import subprocess
import shlex

class MenuEntry:
    def __init__(self,max_x,max_y):
        self.data = []
        self.positions = []
        self.count = 0
        self.x = 0
        self.y = 1
        self.max_x = max_x
        self.max_y = max_y
        self.page=1
        self.id=0
        
    def add(self,title,cmd):
        if (self.x == self.max_x):
            self.x = 1
            if (self.y < self.max_y):
                self.y += 1
            else:
                return
        else:
            self.x +=1
        self.data.append([self.id,title,cmd])
        self.positions.append([self.x,self.y])
        if (self.count==0):
            self.active_x=1
            self.active_y=1
        self.count += 1
        self.id+=1
        print self.data
        print self.positions
        
    def get_x(self,i):
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
    
    def draw(self,screen):
        print str(self.active_x)
        for item in self.data:
            itemid = item[0]
            x = self.positions[itemid][0]
            y = self.positions[itemid][1]
            start_x = self.borders + (x-1)*self.menu_size_x + (x-1)*self.gap_x
            start_y = self.borders + (y-1)*self.menu_size_y + (y-1)*self.gap_y
            pygame.draw.rect(screen,[255,255,255],[start_x,start_y,self.menu_size_x,self.menu_size_y])
            if (x==self.active_x and y==self.active_y):
                pygame.draw.rect(screen,[255,0,0],[start_x,start_y,self.menu_size_x,self.menu_size_y],0)
            title=item[1]
            font = pygame.font.Font(None, 20)
            text = font.render(title, True, [0,0,0], [0,155,0])
            textRect = text.get_rect()
            textRect.x = start_x
            textRect.y = start_y
            screen.blit(text, textRect)
                
    def move_left(self):
        if (self.positions.count([self.active_x-1,self.active_y])>0):
            self.active_x-=1
    def move_right(self):
        if (self.positions.count([self.active_x+1,self.active_y])>0):
            self.active_x+=1
    def move_down(self):
        if (self.positions.count([self.active_x,self.active_y+1])>0):
            self.active_y+=1
    def move_up(self):
        if (self.positions.count([self.active_x,self.active_y-1])>0):
            self.active_y-=1

    def launch(self):
        command = str(self.data[self.positions.index([self.active_x,self.active_y])][2])
        cmds = shlex.split(command)
        self.process = subprocess.Popen(cmds)

    def stop(self):
        self.process.kill()
            
            
            