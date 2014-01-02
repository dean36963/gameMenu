#!/usr/bin/python2

class Settings():
	def __init__(self,file_path=None):
		self.__data__ = dict()
		if file_path is not None:
			self.read_properties_file(file_path)
	def read_properties_file(self,file_path):
		try:
			file=open(file_path)
			for line in file:
				self.__parse_line__(line)
			return True
		except Exception as e:
			print "Failed to read",file_path
			print e
			return False
			
	def __parse_line__(self,line):
		if line.strip().startswith('#'):
			pass
		elif '=' in line:
			property_name,property_value = line.split('=')
			property_name = property_name.strip()
			property_value = property_value.strip()
			if property_name in self.__data__.keys():
				print "Property \""+property_name+"\" appears more than once, taking latest value."
			self.__data__[property_name]=property_value

	def print_data(self):
		print self.__data__

	def get(self,property_name):
		try:
			prop = self.__data__[property_name]
		except:
			prop = None
		return prop

	def set(self,property_name,value):
		self.__data__[property_name] = value

if __name__ == '__main__':
	print "Running this shit"
	s = Settings('test.properties')
	s.print_data()
