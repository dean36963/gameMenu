#!/usr/bin/python2
import os
import pyinotify
import time

class EventManager():
	def __init__(self,watchfile,callback_function):
		self.wm = pyinotify.WatchManager()
		self.mask = pyinotify.IN_MODIFY
		self.handler = EventHandler(callback_function)
		self.notifier = pyinotify.ThreadedNotifier(self.wm,self.handler)
		self.notifier.start()
		self.wdd = self.wm.add_watch(watchfile, self.mask, rec=True)
		print "Setup Watcher"
	
	def kill(self):
		self.wm.rm_watch(self.wdd.values())
		self.notifier.stop()
		print "Stopped watcher"

class EventHandler(pyinotify.ProcessEvent):
	def __init__(self,callback_function):
		self.callback_function = callback_function
	def process_IN_MODIFY(self,event):
		print "Modified", event.pathname
		self.callback_function()

def testfn():
	print "tested changed file"

#Test Procedure
if __name__=='__main__':
	em = EventManager('file.txt',testfn)
	time.sleep(1)
	print "Waited 10"
	outfile = open('file.txt','w')
	for x in range(1,5):
		outfile.write("pppoooop\n")
	outfile.close()
	time.sleep(1)
	em.kill()
