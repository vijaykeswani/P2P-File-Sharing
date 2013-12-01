#/ usr/bin/env python
# filename: tmc.py (CLIENT)

import socket
import sys
import time
import os
from thread import *
from random import choice
from cStringIO import StringIO

def getJoke():
	joke = ["If at first you don't succeed; call it version 1.0","My software never has bugs. It just develops random features","Hand over the calculator, friends don't let friends derive drunk","The box said 'Requires Windows 95 or better'. So I installed LINUX","Unix, DOS and Windows...the good, the bad and the ugly","It's not bogus, it's an IBM standard","To err is human - and to blame it on a computer is even more so","To err is human...to really foul up requires the root password."]
	print ""
	print choice(joke)	
	print ""

getJoke()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host,port))
host1 = ''
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((host1,50000))
s1.listen(1)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "ENTER NICK"
user=raw_input("")
s.send(user)
i = 0

def File():
	while True:
		conn, addr = s1.accept()
		print "connection request from "+str(addr)
		fil=conn.recv(20)
		#fi=StringIO(fil)
		f=open(fil,"r")
		if(len(fil)>0):
			print fil
			conn.send(f.read())	

start_new_thread(File,())
while True:
	data = s.recv(39)
	if(len(data)>0):
		print data.upper()
		opt=raw_input()
		if opt=="1":
			print "Registering with server".upper()
			s.send("1")
			while(True):
				#opt2=s.recv(50)
				#print opt2
				#nick=raw_input()
				#s.send(nick)
				#time.sleep(2)
				res=s.recv(3)
				if(res=="reg"):
					print "Registered with server using above nick".upper()
					break
		if opt=="2":
			print "Sharing with peers (write quit to end)".upper()
			s.send("2")
			data2=s.recv(44);
			print data2.upper()
			while True:
				data2=raw_input()
				if(data2=="quit"):
					#s.send(data2)
					#while((50-len(data2))>0):
					#	data2=data2+" "
					s.send(data2)
					break
				else:
					s.send(data2)
			time.sleep(2)
			#if(data2=="not_reg"):
			#	print "Please register before sharing files"
			#break
		if opt=="3":
			s.send("3")
			print "Enter filename to be searched".upper()
			data2=raw_input()
			fname=data2
			s.send(data2)
			#time.sleep(2)
			data2=s.recv(1024)
			print data2
			data3=data2.split('\n')
			if(len(data3)>0 and data2[0]=='1'):
				print "Download file (y/n) :"
				opt2=raw_input()
				if(opt2=='n'):
					sys.exit(0)
				elif(opt2=='y'):
					print "Choose location : "
					opt3=raw_input()
					data4=data3[int(opt3)-1].split(' ')
					user=data4[1]
					ip=data4[3]
					port=data4[4]
					path=data4[6]
					print user,ip,port,path	
					try:
						s2.connect((ip,50000))
					except Exception, e:
						print "User offline"
						continue
					s2.send(path)
                                        f=open(fname,"w")
                                        data5=s2.recv(1024)
                                        f.write(data5)
                                        f.close()
					#comm="scp "+user+"@"+ip+":"+path+" ./"
					#print comm
					#os.system(comm)
					sys.exit(0)	
			else:
				sys.exit(0)
				
		if opt=="4":
			s.send("4")
			s.close()
			break
