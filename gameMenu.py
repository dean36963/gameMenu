#!/usr/bin/python2


import joystick
import pygame
import csv
import menuEntry
import time

class GameMenu():
    def __init__(self):
        print "Starting Menu"
        self.fail=False
        self.joy=joystick.Joystick()
        if (self.joy.errors!=[]):
            for error in self.joy.errors:
                print error
                self.fail=True
                return
        self.get_settings()
        self.menuEntries = menuEntry.MenuEntry(self.num_entries_x,self.num_entries_y)
        self.readMenuFile()
        self.menuEntries.settings(self.borders,self.gap_x,self.gap_y,self.menu_size_x,self.menu_size_y)

        pygame.init()
        # Set the height and width of the screen
        size=[self.screen_size_x,self.screen_size_y]
        self.screen=pygame.display.set_mode(size)
        pygame.display.set_caption("GameMenu")
        # Used to manage how fast the screen updates
        self.clock=pygame.time.Clock()
        
    def get_settings(self):
        #Replace with reading settings file
        print "Using Default Settings"
        self.screen_size_x = 640
        self.screen_size_y = 480
        
        self.frames_per_second = 5
        self.tick = 1.0 / self.frames_per_second
        
        self.num_entries_x = 4
        self.num_entries_y = 3
        self.num_pages = 2
        
        #Gap between menu entries
        self.gap_x = 20
        self.gap_y = 20
        
        self.borders = 50
        #self.border_top = 50
        #self.border_bottom = 50
        #self.border_left = 50
        #self.border_right = 50
        
        #Calculate the size of each menu item
        self.menu_size_x = ( self.screen_size_x - self.gap_x * (self.num_entries_x - 1) - 2*self.borders ) / self.num_entries_x
        self.menu_size_y = ( self.screen_size_y - self.gap_y * (self.num_entries_y - 1) - 2*self.borders ) / self.num_entries_y
        
        
    def start(self):
        if (self.fail==True):
            print "Failed to start"
            return
        loop=True
        while (loop):
            self.draw()
            time.sleep(self.tick)
            joy_input = self.joy.get_input()
            if (joy_input[5]<-0.5):
                self.menuEntries.move_left()
            if (joy_input[5]>0.5):
                self.menuEntries.move_right()
            if (joy_input[6]<-0.5):
                self.menuEntries.move_up()
            if (joy_input[6]>0.5):
                self.menuEntries.move_down()
            if (joy_input[1]==1):
                loop=False
            if (joy_input[0]==1):
                self.launch()
                
    def launch(self):
        self.menuEntries.launch()
        loop=True
        print "stop"
        while (loop):
            print "looping press x to quit"
            if ( self.joy.get_input()[4]):
                self.menuEntries.stop()
                loop=False
            time.sleep(self.tick)
        
    def __run__(self):
        self.menuEntries.launch()
        
    def readMenuFile(self):
        menuFile=open("gameMenu.csv")
        csvreader = csv.reader(menuFile)
        for line in csvreader:
            self.menuEntries.add(line[0],line[1])
        #exit()

    def draw(self):
        #Draw Background
        self.menuEntries.draw(self.screen)
        pygame.display.flip()
        
if __name__=="__main__":
    gm = GameMenu()
    gm.start()

