#!/ usr/bin/env python
# tms.py (SERVER)
import socket
import sys
import time
import MySQLdb
from thread import *
import heapq
#from heapq import heappush, heappop, heapify
with open(".variables") as f:
   content=f.readlines()
passwd = content[0][:-1]
db = MySQLdb.connect("localhost","root",passwd,"p2p" )
cursor = db.cursor()
host = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
s.bind((host,port))
s.listen(1)
nick=""
flag=0

def Connect(conn,addr):
   global nick
   print 'client is at', addr
   ip,port=addr
   nick = conn.recv(10)
   #sql="select * from user where nick='%s' and ip='%s'" % (nick,ip)
   #cursor.execute(sql)
   #results = cursor.fetchall()

   #nick = conn.recv(10)
   while conn:
	#ip,port=addr
	sql="select * from user where nick='%s' and ip='%s'" % (nick,ip)
        cursor.execute(sql)
        results = cursor.fetchall()
	#print results
	if len(results)==0:
		opt="Nick doesn't exist.\n1. Register\n4. Quit"
		conn.send(opt)
		data2=conn.recv(1)
		if data2=="1":
			#nick=Register(conn,addr)
			#heappush(pq,(1,(conn,addr,nick)))
			#heapify(pq)
			pq.append((1,(conn,addr,nick)))
			time.sleep(2)
		elif data2=="4":
			conn.close()
	elif len(results)!=0:
		opt="2. Share files\n3. Search a file\n4. Quit"
                conn.send(opt)
		nick,ip1,port1 = results[0]
		data2=conn.recv(1)
		print "---------------"+data2
		if data2=="2" or data2=="q":
			pq.append((2,(conn,addr,nick)))
			#heappush(pq,(2,(conn,addr,nick)))
			#heapify(pq)
			time.sleep(7)
			#Share(conn,nick)
		elif data2=="3":
			#heappush(pq,(3,(conn,addr,nick)))
			#heapify(pq)
			pq.append((3,(conn,addr,nick)))
			time.sleep(5)
			#Search(conn)
		elif data2=="4":
			conn.close()
			break
			
def Register(conn,addr):
	global nick
	#opt2="Choose a Nick"
        #conn.send(opt2)
        while(True):
        	#nick=conn.recv(20)
                ip,port=addr
                #sql="select * from user where nick='%s'" % (nick)
                #cursor.execute(sql)
                #results = cursor.fetchall()
                #if len(results)==0:
                sql="INSERT INTO user VALUES ('%s','%s',%d)" % (nick,str(ip),int(port))
                if(cursor.execute(sql)):
                                        #print ip,port	
                       	print "Client "+nick+" with address "+str(ip)+":"+str(port)+" registered"
                        db.commit()
                else:
                        conn.send("Error in registering")
			sys.exit(0)
                conn.send("reg")
                break
                #else:
                #        conn.send("not")
                #        conn.send("Name already taken\nChoose another Name")
	return nick

def Share(conn,nick,addr):
	#global cursor
	ip,port=addr
	conn.send("Give filename and path separated by a space")
        while True:
		data3=""
        	data3=conn.recv(1024)
		data4=data3.split(' ')
        	if(data3 not in "quit" and len(data4)>1):
              		print data3
               		#data4=data3.split(' ')
               		sql="INSERT INTO files VALUES ('%s','%s',%d,'%s','%s')" % (nick,str(ip),int(port),data4[0],data4[1])
                	if(cursor.execute(sql)):
                	                        #print ip,port
                       		print "File indexed"
                        	db.commit()
		elif data3=="2":
			continue
               	elif data3=="quit":
                	break

def Search(conn):
	data3=conn.recv(20)
        data3="%"+data3+"%"
        sql="select * from files where name like '%s'" % (data3)
        cursor.execute(sql)
        results1 = cursor.fetchall()
        final=""
	i=0
        for res in results1:
        	i=i+1
		nick,addr,port,name,path=res
                                #print res
                final=final+str(i)+". "+str(nick)+" "+" "+str(addr)+" "+str(port)+" "+str(name)+" "+str(path)+"\n"
        
	conn.send(final)

def ReqQueue():
	while True:
		if pq:
			heapq.heapify(pq)
			priority,tupl=heapq.heappop(pq)	
			conn,addr,nick=tupl
			if priority==1:
				Register(conn,addr)
			elif priority==2:
				Share(conn,nick,addr)
			elif priority==3:
				Search(conn)

pq = []
start_new_thread(ReqQueue,())
while True:
   conn, addr = s.accept()
   #print 'client is at', addr
   #data = conn.recv(10)
   #Connect(conn,addr)
   start_new_thread(Connect,(conn,addr,))
