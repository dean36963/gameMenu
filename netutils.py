#!/usr/bin/python2
import netifaces
import re

class ip_tool:

	def __init__(self):
		self.blacklisted_interfaces=['lo']
		self.ip4_regex = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

	def get_ip(self):
		ip_addrs=[]
		for interface in netifaces.interfaces():
			if interface not in self.blacklisted_interfaces:
				for key in netifaces.ifaddresses(interface):
					ipaddr = netifaces.ifaddresses(interface)[key][0]['addr']
					if re.search(self.ip4_regex,ipaddr):
						ip_addrs.append(ipaddr)
		if len(ip_addrs)==1:
			return ip_addrs[0]
		else:
			print 'Warning multiple addresses found'
			return ip_addrs[0]




if __name__ == '__main__':
	ip = ip_tool()
	ipaddr = ip.get_ip()
	print ipaddr
